"""PostgreSQL adapters for Guest Arrival."""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from types import TracebackType
from typing import Any
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.guest_arrival.application.dtos import (
    ActivityLogRecord,
    CustomerGroupDTO,
    OpenCustomerGroupResult,
    ServiceLocationDTO,
)
from beachos_api.packs.beachos.guest_arrival.application.ports import (
    ActivityLog,
    CommandReceiptStore,
    GuestArrivalUnitOfWork,
    OrderingProvisioner,
    ServiceLocationRepository,
)
from beachos_api.packs.beachos.guest_arrival.domain import (
    BillCreated,
    BillLineAdded,
    CustomerGroupOpened,
    FinancialObligationCreated,
    GuestArrivalEvent,
    GuestDeparted,
    Money,
    ResponsibleWaiterAssigned,
    ServiceLocation,
    ServiceLocationStatus,
    ServiceLocationType,
)
from beachos_api.packs.beachos.guest_arrival.infrastructure.errors import (
    GuestArrivalConcurrencyError,
)


def _event_to_data(event: GuestArrivalEvent) -> tuple[str, dict[str, Any], datetime]:
    if isinstance(event, ResponsibleWaiterAssigned):
        return (
            "RESPONSIBLE_WAITER_ASSIGNED",
            {
                "customer_group_id": event.customer_group_id,
                "service_location_id": event.service_location_id,
                "responsible_waiter_id": event.responsible_waiter_id,
            },
            event.occurred_at,
        )
    if isinstance(event, CustomerGroupOpened):
        return (
            "CUSTOMER_GROUP_OPENED",
            {
                "customer_group_id": event.customer_group_id,
                "venue_id": event.venue_id,
                "service_location_id": event.service_location_id,
                "responsible_waiter_id": event.responsible_waiter_id,
            },
            event.occurred_at,
        )
    if isinstance(event, FinancialObligationCreated):
        return (
            "FINANCIAL_OBLIGATION_CREATED",
            {
                "obligation_id": event.obligation_id,
                "customer_group_id": event.customer_group_id,
                "source": event.source,
                "amount": str(event.amount),
                "currency": event.currency,
            },
            event.occurred_at,
        )
    if isinstance(event, BillCreated):
        return (
            "BILL_CREATED",
            {
                "bill_id": event.bill_id,
                "customer_group_id": event.customer_group_id,
                "currency": event.currency,
            },
            event.occurred_at,
        )
    if isinstance(event, BillLineAdded):
        return (
            "BILL_LINE_ADDED",
            {
                "bill_id": event.bill_id,
                "bill_line_id": event.bill_line_id,
                "description": event.description,
                "amount": str(event.amount),
                "currency": event.currency,
                "source": event.source,
            },
            event.occurred_at,
        )
    if isinstance(event, GuestDeparted):
        return (
            "GUEST_DEPARTED",
            {
                "customer_group_id": event.customer_group_id,
                "service_location_id": event.service_location_id,
                "departed_by_id": event.departed_by_id,
            },
            event.occurred_at,
        )
    raise ValueError("unsupported Guest Arrival event")


def _event_from_data(kind: str, data: dict[str, Any], at: datetime) -> GuestArrivalEvent:
    if kind == "RESPONSIBLE_WAITER_ASSIGNED":
        return ResponsibleWaiterAssigned(
            data["customer_group_id"],
            data["service_location_id"],
            data["responsible_waiter_id"],
            at,
        )
    if kind == "CUSTOMER_GROUP_OPENED":
        return CustomerGroupOpened(
            data["customer_group_id"],
            data["venue_id"],
            data["service_location_id"],
            data["responsible_waiter_id"],
            at,
        )
    if kind == "FINANCIAL_OBLIGATION_CREATED":
        return FinancialObligationCreated(
            data["obligation_id"],
            data["customer_group_id"],
            data["source"],
            Decimal(data["amount"]),
            data["currency"],
            at,
        )
    if kind == "BILL_CREATED":
        return BillCreated(data["bill_id"], data["customer_group_id"], data["currency"], at)
    if kind == "BILL_LINE_ADDED":
        return BillLineAdded(
            data["bill_id"],
            data["bill_line_id"],
            data["description"],
            Decimal(data["amount"]),
            data["currency"],
            data["source"],
            at,
        )
    if kind == "GUEST_DEPARTED":
        return GuestDeparted(
            data["customer_group_id"],
            data["service_location_id"],
            data["departed_by_id"],
            at,
        )
    raise ValueError(f"unsupported Guest Arrival event type: {kind}")


def _restore(row: dict[str, Any], events: tuple[GuestArrivalEvent, ...]) -> ServiceLocation:
    charge = (
        Money(Decimal(row["beach_sunbed_charge"]), row["charge_currency"])
        if row["beach_sunbed_charge"] is not None
        else None
    )
    return ServiceLocation.restore(
        service_location_id=row["service_location_id"],
        venue_id=row["venue_id"],
        visible_name=row["visible_name"],
        digital_identity=row["digital_identity"],
        location_type=ServiceLocationType(row["location_type"]),
        initial_status=ServiceLocationStatus(row["initial_status"]),
        beach_sunbed_charge=charge,
        charge_description=row["charge_description"],
        events=events,
    )


class PostgresServiceLocationRepository:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._versions: dict[str, int] = {}

    def _from_row(self, row: dict[str, Any]) -> ServiceLocation:
        event_rows = self._connection.execute(
            "SELECT event_type,event_data,occurred_at FROM guest_arrival_events WHERE service_location_id=%s ORDER BY sequence",  # noqa: E501
            (row["service_location_id"],),
        ).fetchall()
        location = _restore(
            row,
            tuple(
                _event_from_data(e["event_type"], e["event_data"], e["occurred_at"])
                for e in event_rows
            ),
        )
        if location.version != row["stream_version"]:
            raise GuestArrivalConcurrencyError("Service Location event stream is inconsistent")
        self._versions[location.service_location_id] = location.version
        return location

    def list_for_venue(self, *, venue_id: str) -> tuple[ServiceLocation, ...]:
        rows = self._connection.execute(
            "SELECT * FROM guest_arrival_service_locations WHERE venue_id=%s ORDER BY visible_name",
            (venue_id,),
        ).fetchall()
        return tuple(self._from_row(row) for row in rows)

    def get(self, *, service_location_id: str) -> ServiceLocation | None:
        row = self._connection.execute(
            "SELECT * FROM guest_arrival_service_locations WHERE service_location_id=%s",
            (service_location_id,),
        ).fetchone()
        return self._from_row(row) if row else None

    def get_for_customer_group(self, *, customer_group_id: str) -> ServiceLocation | None:
        row = self._connection.execute(
            """SELECT location.* FROM guest_arrival_service_locations AS location
            JOIN guest_arrival_events AS event
              ON event.service_location_id=location.service_location_id
            WHERE event.event_type='CUSTOMER_GROUP_OPENED'
              AND event.event_data->>'customer_group_id'=%s""",
            (customer_group_id,),
        ).fetchone()
        return self._from_row(row) if row else None

    def get_by_digital_identity(
        self, *, venue_id: str, digital_identity: str
    ) -> ServiceLocation | None:
        row = self._connection.execute(
            "SELECT * FROM guest_arrival_service_locations WHERE venue_id=%s AND digital_identity=%s",  # noqa: E501
            (venue_id, digital_identity),
        ).fetchone()
        return self._from_row(row) if row else None

    def save(self, location: ServiceLocation) -> None:
        expected = self._versions.get(location.service_location_id)
        if expected is None:
            raise GuestArrivalConcurrencyError("Service Location must be loaded before saving")
        events = location.pull_events()
        updated = self._connection.execute(
            "UPDATE guest_arrival_service_locations SET stream_version=%s WHERE service_location_id=%s AND stream_version=%s",  # noqa: E501
            (location.version, location.service_location_id, expected),
        )
        if updated.rowcount != 1:
            raise GuestArrivalConcurrencyError(
                "The Service Location changed. Review its current state."
            )
        for sequence, event in enumerate(events, expected + 1):
            kind, data, at = _event_to_data(event)
            self._connection.execute(
                "INSERT INTO guest_arrival_events(service_location_id,sequence,event_type,event_data,occurred_at) VALUES(%s,%s,%s,%s,%s)",  # noqa: E501
                (location.service_location_id, sequence, kind, json.dumps(data), at),
            )
        self._versions[location.service_location_id] = location.version


def _result_data(result: OpenCustomerGroupResult) -> dict[str, Any]:
    group = result.customer_group
    location = result.service_location
    return {
        "request_id": result.request_id,
        "customer_group": {
            "customer_group_id": group.customer_group_id,
            "venue_id": group.venue_id,
            "service_location_id": group.service_location_id,
            "responsible_waiter_id": group.responsible_waiter_id,
            "opened_at": group.opened_at.isoformat(),
            "bill_id": group.bill_id,
            "opening_obligation": str(group.opening_obligation)
            if group.opening_obligation is not None
            else None,
            "currency": group.currency,
        },
        "service_location": {
            "service_location_id": location.service_location_id,
            "visible_name": location.visible_name,
            "digital_identity": location.digital_identity,
            "location_type": location.location_type,
            "status": location.status,
            "active_customer_group_id": location.active_customer_group_id,
            "opening_charge": str(location.opening_charge)
            if location.opening_charge is not None
            else None,
            "currency": location.currency,
            "charge_description": location.charge_description,
        },
    }


class PostgresReceiptStore:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> OpenCustomerGroupResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM guest_arrival_command_receipts WHERE request_id=%s",
            (request_id,),
        ).fetchone()
        if not row:
            return None
        data = row["result_data"]
        group = data["customer_group"]
        location = data["service_location"]
        return OpenCustomerGroupResult(
            data["request_id"],
            CustomerGroupDTO(
                group["customer_group_id"],
                group["venue_id"],
                group["service_location_id"],
                group["responsible_waiter_id"],
                datetime.fromisoformat(group["opened_at"]),
                group["bill_id"],
                Decimal(group["opening_obligation"]) if group["opening_obligation"] else None,
                group["currency"],
            ),
            ServiceLocationDTO(
                location["service_location_id"],
                location["visible_name"],
                location["digital_identity"],
                location["location_type"],
                location["status"],
                location["active_customer_group_id"],
                Decimal(location["opening_charge"]) if location["opening_charge"] else None,
                location["currency"],
                location["charge_description"],
            ),
        )

    def save(self, *, request_id: str, result: OpenCustomerGroupResult) -> None:
        self._connection.execute(
            "INSERT INTO guest_arrival_command_receipts(request_id,service_location_id,result_data) VALUES(%s,%s,%s)",  # noqa: E501
            (
                request_id,
                result.service_location.service_location_id,
                json.dumps(_result_data(result)),
            ),
        )


class PostgresOrderingProvisioner:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def provision(self, location: ServiceLocation) -> None:
        group = location.active_customer_group
        if group is None:
            raise GuestArrivalConcurrencyError(
                "Customer Group opening was not available for Ordering"
            )
        events = []
        if group.bill_id and group.opening_obligation:
            obligation = next(
                event for event in location.history if isinstance(event, FinancialObligationCreated)
            )
            line = next(event for event in location.history if isinstance(event, BillLineAdded))
            events = [
                (
                    "FINANCIAL_OBLIGATION_CREATED",
                    {
                        "obligation_id": obligation.obligation_id,
                        "customer_group_id": group.customer_group_id,
                        "order_item_id": None,
                        "amount": str(group.opening_obligation.amount),
                        "currency": group.opening_obligation.currency,
                    },
                ),
                (
                    "BILL_CREATED",
                    {
                        "bill_id": group.bill_id,
                        "customer_group_id": group.customer_group_id,
                        "currency": group.opening_obligation.currency,
                    },
                ),
                (
                    "BILL_LINE_ADDED",
                    {
                        "bill_id": group.bill_id,
                        "bill_line_id": line.bill_line_id,
                        "order_item_id": None,
                        "description": location.charge_description,
                        "quantity": "1",
                        "unit_price": str(group.opening_obligation.amount),
                        "amount": str(group.opening_obligation.amount),
                        "currency": group.opening_obligation.currency,
                    },
                ),
            ]
        self._connection.execute(
            "INSERT INTO ordering_customer_groups(customer_group_id,venue_id,service_location_id,responsible_waiter_id,status,stream_version) VALUES(%s,%s,%s,%s,'ACTIVE',%s)",  # noqa: E501
            (
                group.customer_group_id,
                group.venue_id,
                group.service_location_id,
                group.responsible_waiter_id,
                len(events),
            ),
        )
        for sequence, (kind, data) in enumerate(events, 1):
            self._connection.execute(
                "INSERT INTO ordering_events(customer_group_id,sequence,event_type,event_data,occurred_at) VALUES(%s,%s,%s,%s,%s)",  # noqa: E501
                (group.customer_group_id, sequence, kind, json.dumps(data), group.opened_at),
            )


class PostgresActivityLog:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def record_customer_group_opened(self, record: ActivityLogRecord) -> None:
        self._connection.execute(
            "INSERT INTO guest_arrival_activity_log(request_id,actor_id,venue_id,service_location_id,customer_group_id,action_name,occurred_at) VALUES(%s,%s,%s,%s,%s,'CUSTOMER_GROUP_OPENED',%s)",  # noqa: E501
            (
                record.request_id,
                record.actor_id,
                record.venue_id,
                record.service_location_id,
                record.customer_group_id,
                record.occurred_at,
            ),
        )


class PostgresGuestArrivalUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, Any]] | None = None
        self._committed = False
        self._locations: PostgresServiceLocationRepository | None = None
        self._receipts: PostgresReceiptStore | None = None
        self._ordering: PostgresOrderingProvisioner | None = None
        self._activity: PostgresActivityLog | None = None

    def __enter__(self) -> PostgresGuestArrivalUnitOfWork:
        connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._connection = connection
        self._locations = PostgresServiceLocationRepository(connection)
        self._receipts = PostgresReceiptStore(connection)
        self._ordering = PostgresOrderingProvisioner(connection)
        self._activity = PostgresActivityLog(connection)
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exception_type, exception, traceback
        if self._connection is not None:
            if not self._committed:
                self._connection.rollback()
            self._connection.close()

    def _conn(self) -> psycopg.Connection[dict[str, Any]]:
        if self._connection is None:
            raise RuntimeError("unit of work has not been entered")
        return self._connection

    @property
    def locations(self) -> ServiceLocationRepository:
        self._conn()
        if self._locations is None:
            raise RuntimeError("unit of work has not been entered")
        return self._locations

    @property
    def receipts(self) -> CommandReceiptStore:
        self._conn()
        if self._receipts is None:
            raise RuntimeError("unit of work has not been entered")
        return self._receipts

    @property
    def ordering(self) -> OrderingProvisioner:
        self._conn()
        if self._ordering is None:
            raise RuntimeError("unit of work has not been entered")
        return self._ordering

    @property
    def activity_log(self) -> ActivityLog:
        self._conn()
        if self._activity is None:
            raise RuntimeError("unit of work has not been entered")
        return self._activity

    def commit(self) -> None:
        self._conn().commit()
        self._committed = True


class PostgresGuestArrivalUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> GuestArrivalUnitOfWork:
        return PostgresGuestArrivalUnitOfWork(self._connection_string)


class PostgresVenueOpeningReader:
    def __init__(self, connection_string: str, business_dates: Any) -> None:
        self._connection_string = connection_string
        self._business_dates = business_dates

    def current(self, *, venue_id: str) -> tuple[str, str, bool] | None:
        business_date = self._business_dates.current_for(venue_id=venue_id)
        with psycopg.connect(self._connection_string, row_factory=dict_row) as connection:
            row = connection.execute(
                "SELECT venue_name,business_date,opening_status FROM venue_opening_venues WHERE venue_id=%s AND business_date=%s",  # noqa: E501
                (venue_id, business_date.value),
            ).fetchone()
        return (
            (row["venue_name"], row["business_date"].isoformat(), row["opening_status"] == "OPEN")
            if row
            else None
        )


class UUIDIdentityGenerator:
    def new_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid4()}"
