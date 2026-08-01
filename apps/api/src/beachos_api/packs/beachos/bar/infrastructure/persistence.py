"""PostgreSQL adapters for Bar Operations."""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from types import TracebackType
from typing import Any

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.bar.application.dtos import (
    AcknowledgeBarTicketResult,
    BarTicketDTO,
    BarTicketItemDTO,
)
from beachos_api.packs.beachos.bar.application.ports import (
    BarCommandReceiptStore,
    BarTicketRepository,
    BarUnitOfWork,
)
from beachos_api.packs.beachos.bar.domain import (
    BarEvent,
    BarTicket,
    BarTicketAcknowledged,
    BarTicketCollected,
    BarTicketDelivered,
    BarTicketItem,
    BarTicketReady,
)

from .errors import BarConcurrencyError


def _event_to_data(event: BarEvent) -> tuple[str, dict[str, Any], datetime]:
    if isinstance(event, BarTicketReady):
        return (
            "BAR_TICKET_READY",
            {"ticket_id": event.ticket_id, "confirmed_by_id": event.confirmed_by_id},
            event.confirmed_at,
        )
    if isinstance(event, BarTicketCollected):
        return (
            "BAR_TICKET_COLLECTED",
            {"ticket_id": event.ticket_id, "collected_by_id": event.collected_by_id},
            event.collected_at,
        )
    if isinstance(event, BarTicketDelivered):
        return (
            "BAR_TICKET_DELIVERED",
            {"ticket_id": event.ticket_id, "delivered_by_id": event.delivered_by_id},
            event.delivered_at,
        )
    return (
        "BAR_TICKET_ACKNOWLEDGED",
        {"ticket_id": event.ticket_id, "acknowledged_by_id": event.acknowledged_by_id},
        event.acknowledged_at,
    )


def _event_from_data(event_type: str, data: dict[str, Any], occurred_at: datetime) -> BarEvent:
    if event_type == "BAR_TICKET_READY":
        return BarTicketReady(data["ticket_id"], data["confirmed_by_id"], occurred_at)
    if event_type == "BAR_TICKET_COLLECTED":
        return BarTicketCollected(data["ticket_id"], data["collected_by_id"], occurred_at)
    if event_type == "BAR_TICKET_DELIVERED":
        return BarTicketDelivered(data["ticket_id"], data["delivered_by_id"], occurred_at)
    if event_type != "BAR_TICKET_ACKNOWLEDGED":
        raise ValueError(f"unsupported Bar event type: {event_type}")
    return BarTicketAcknowledged(data["ticket_id"], data["acknowledged_by_id"], occurred_at)


class PostgresBarTicketRepository:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._loaded_versions: dict[str, int] = {}

    def _from_row(self, row: dict[str, Any]) -> BarTicket:
        data = row["event_data"]
        ticket_id = data["ticket_id"]
        event_rows = self._connection.execute(
            """SELECT event_type,event_data,occurred_at FROM bar_events
               WHERE ticket_id=%s ORDER BY sequence""",
            (ticket_id,),
        ).fetchall()
        ticket = BarTicket.restore(
            ticket_id=ticket_id,
            order_id=data["order_id"],
            customer_group_id=row["customer_group_id"],
            venue_id=row["venue_id"],
            submission_service_location_id=data["service_location_id"],
            current_service_location_id=row["current_service_location_id"],
            responsible_service_staff_id=data["responsible_waiter_id"],
            submitted_at=datetime.fromisoformat(data["created_at"]),
            items=tuple(
                BarTicketItem(
                    item["order_item_id"], item["name"], Decimal(item["quantity"]), item["note"]
                )
                for item in data["items"]
            ),
            events=tuple(
                _event_from_data(e["event_type"], e["event_data"], e["occurred_at"])
                for e in event_rows
            ),
        )
        version = row["stream_version"] or 0
        if ticket.version != version:
            raise BarConcurrencyError("Bar event stream version is inconsistent")
        self._loaded_versions[ticket_id] = version
        return ticket

    def get(self, *, ticket_id: str) -> BarTicket | None:
        row = self._connection.execute(
            """SELECT event_data, events.customer_group_id, groups.venue_id,
                      groups.service_location_id AS current_service_location_id,
                      streams.stream_version
               FROM ordering_events AS events
               JOIN ordering_customer_groups AS groups
                 ON groups.customer_group_id=events.customer_group_id
               LEFT JOIN bar_ticket_streams AS streams
                 ON streams.ticket_id=events.event_data->>'ticket_id'
               WHERE events.event_type='BAR_TICKET_CREATED'
                 AND events.event_data->>'ticket_id'=%s""",
            (ticket_id,),
        ).fetchone()
        return self._from_row(row) if row else None

    def list_for_venue(self, *, venue_id: str) -> tuple[BarTicket, ...]:
        rows = self._connection.execute(
            """SELECT event_data, events.customer_group_id, groups.venue_id,
                      groups.service_location_id AS current_service_location_id,
                      streams.stream_version
               FROM ordering_events AS events
               JOIN ordering_customer_groups AS groups
                 ON groups.customer_group_id=events.customer_group_id
               LEFT JOIN bar_ticket_streams AS streams
                 ON streams.ticket_id=events.event_data->>'ticket_id'
               WHERE events.event_type='BAR_TICKET_CREATED' AND groups.venue_id=%s
               ORDER BY events.occurred_at, events.event_data->>'ticket_id'""",
            (venue_id,),
        ).fetchall()
        return tuple(self._from_row(row) for row in rows)

    def save(self, ticket: BarTicket) -> None:
        expected = self._loaded_versions.get(ticket.ticket_id)
        if expected is None:
            raise BarConcurrencyError("Bar Ticket must be loaded before saving")
        events = ticket.pull_events()
        if not events:
            raise BarConcurrencyError("Bar save requires new Domain Events")
        self._connection.execute(
            """INSERT INTO bar_ticket_streams(ticket_id,stream_version)
               VALUES(%s,0) ON CONFLICT(ticket_id) DO NOTHING""",
            (ticket.ticket_id,),
        )
        updated = self._connection.execute(
            """UPDATE bar_ticket_streams SET stream_version=%s
               WHERE ticket_id=%s AND stream_version=%s""",
            (ticket.version, ticket.ticket_id, expected),
        )
        if updated.rowcount != 1:
            raise BarConcurrencyError("The Bar Ticket changed. Review its current acknowledgement.")
        for sequence, event in enumerate(events, expected + 1):
            event_type, data, occurred_at = _event_to_data(event)
            self._connection.execute(
                """INSERT INTO bar_events(ticket_id,sequence,event_type,event_data,occurred_at)
                   VALUES(%s,%s,%s,%s,%s)""",
                (ticket.ticket_id, sequence, event_type, json.dumps(data), occurred_at),
            )


def _to_data(result: AcknowledgeBarTicketResult) -> dict[str, Any]:
    ticket = result.ticket
    return {
        "request_id": result.request_id,
        "ticket": {
            "ticket_id": ticket.ticket_id,
            "order_id": ticket.order_id,
            "customer_group_id": ticket.customer_group_id,
            "venue_id": ticket.venue_id,
            "submission_service_location_id": ticket.submission_service_location_id,
            "current_service_location_id": ticket.current_service_location_id,
            "responsible_service_staff_id": ticket.responsible_service_staff_id,
            "submitted_at": ticket.submitted_at.isoformat(),
            "items": [
                {
                    "order_item_id": i.order_item_id,
                    "name": i.name,
                    "quantity": str(i.quantity),
                    "note": i.note,
                }
                for i in ticket.items
            ],
            "acknowledged_by_id": ticket.acknowledged_by_id,
            "acknowledged_at": ticket.acknowledged_at.isoformat()
            if ticket.acknowledged_at
            else None,
            "ready_by_id": ticket.ready_by_id,
            "ready_at": ticket.ready_at.isoformat() if ticket.ready_at else None,
            "collected_by_id": ticket.collected_by_id,
            "collected_at": ticket.collected_at.isoformat() if ticket.collected_at else None,
            "delivered_by_id": ticket.delivered_by_id,
            "delivered_at": ticket.delivered_at.isoformat() if ticket.delivered_at else None,
        },
    }


def _from_data(data: dict[str, Any]) -> AcknowledgeBarTicketResult:
    t = data["ticket"]
    return AcknowledgeBarTicketResult(
        data["request_id"],
        BarTicketDTO(
            t["ticket_id"],
            t["order_id"],
            t["customer_group_id"],
            t["venue_id"],
            t["submission_service_location_id"],
            t["current_service_location_id"],
            t["responsible_service_staff_id"],
            datetime.fromisoformat(t["submitted_at"]),
            tuple(
                BarTicketItemDTO(i["order_item_id"], i["name"], Decimal(i["quantity"]), i["note"])
                for i in t["items"]
            ),
            t["acknowledged_by_id"],
            datetime.fromisoformat(t["acknowledged_at"]) if t["acknowledged_at"] else None,
            t.get("ready_by_id"),
            datetime.fromisoformat(t["ready_at"]) if t.get("ready_at") else None,
            t.get("collected_by_id"),
            datetime.fromisoformat(t["collected_at"]) if t.get("collected_at") else None,
            t.get("delivered_by_id"),
            datetime.fromisoformat(t["delivered_at"]) if t.get("delivered_at") else None,
        ),
    )


class PostgresBarReceiptStore:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> AcknowledgeBarTicketResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM bar_command_receipts WHERE request_id=%s", (request_id,)
        ).fetchone()
        return _from_data(row["result_data"]) if row else None

    def save(self, *, request_id: str, result: AcknowledgeBarTicketResult) -> None:
        self._connection.execute(
            "INSERT INTO bar_command_receipts(request_id,ticket_id,result_data) VALUES(%s,%s,%s)",
            (request_id, result.ticket.ticket_id, json.dumps(_to_data(result))),
        )


class PostgresBarUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, Any]] | None = None
        self._tickets: PostgresBarTicketRepository | None = None
        self._receipts: PostgresBarReceiptStore | None = None
        self._committed = False

    def __enter__(self) -> PostgresBarUnitOfWork:
        self._connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._tickets = PostgresBarTicketRepository(self._connection)
        self._receipts = PostgresBarReceiptStore(self._connection)
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

    @property
    def tickets(self) -> BarTicketRepository:
        if self._tickets is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._tickets

    @property
    def receipts(self) -> BarCommandReceiptStore:
        if self._receipts is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._receipts

    def commit(self) -> None:
        if self._connection is None:
            raise RuntimeError("the unit of work has not been entered")
        self._connection.commit()
        self._committed = True


class PostgresBarUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> BarUnitOfWork:
        return PostgresBarUnitOfWork(self._connection_string)
