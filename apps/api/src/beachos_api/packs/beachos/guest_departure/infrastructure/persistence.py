"""PostgreSQL Guest Departure adapters."""

import json
from datetime import datetime
from types import TracebackType
from typing import Any, cast

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.guest_arrival.domain import ServiceLocation
from beachos_api.packs.beachos.guest_arrival.infrastructure.errors import (
    GuestArrivalConcurrencyError,
)
from beachos_api.packs.beachos.guest_arrival.infrastructure.persistence import (
    PostgresServiceLocationRepository,
)
from beachos_api.packs.beachos.guest_departure.application.service import (
    DepartureResult,
    Unit,
)


class DepartureConcurrencyError(RuntimeError):
    """The occupancy state changed during departure."""


class PostgresDepartureLocations:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._delegate = PostgresServiceLocationRepository(connection)

    def get_for_customer_group(self, *, customer_group_id: str) -> ServiceLocation | None:
        return self._delegate.get_for_customer_group(customer_group_id=customer_group_id)

    def save(self, location: ServiceLocation) -> None:
        try:
            self._delegate.save(location)
        except (GuestArrivalConcurrencyError, psycopg.errors.UniqueViolation) as error:
            raise DepartureConcurrencyError("Guest Departure state changed") from error


class PostgresCustomerGroupFacts:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def status(self, *, customer_group_id: str) -> str | None:
        row = self._connection.execute(
            "SELECT status FROM ordering_customer_groups WHERE customer_group_id=%s",
            (customer_group_id,),
        ).fetchone()
        return row["status"] if row else None


def _result_data(result: DepartureResult) -> dict[str, object]:
    return {
        "request_id": result.request_id,
        "customer_group_id": result.customer_group_id,
        "customer_group_status": result.customer_group_status,
        "departure_status": result.departure_status,
        "service_location_id": result.service_location_id,
        "service_location_name": result.service_location_name,
        "service_location_status": result.service_location_status,
        "departed_by_id": result.departed_by_id,
        "departed_at": result.departed_at.isoformat(),
    }


class PostgresDepartureReceipts:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> DepartureResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM guest_departure_receipts WHERE request_id=%s",
            (request_id,),
        ).fetchone()
        if row is None:
            return None
        data = row["result_data"]
        return DepartureResult(
            data["request_id"],
            data["customer_group_id"],
            data["customer_group_status"],
            data["departure_status"],
            data["service_location_id"],
            data["service_location_name"],
            data["service_location_status"],
            data["departed_by_id"],
            datetime.fromisoformat(data["departed_at"]),
        )

    def save(self, result: DepartureResult) -> None:
        self._connection.execute(
            """INSERT INTO guest_departure_receipts(
                request_id,customer_group_id,service_location_id,result_data
            ) VALUES(%s,%s,%s,%s)""",
            (
                result.request_id,
                result.customer_group_id,
                result.service_location_id,
                json.dumps(_result_data(result)),
            ),
        )


class PostgresDepartureActivity:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def record(self, *, result: DepartureResult) -> None:
        self._connection.execute(
            """INSERT INTO guest_departure_activity_log(
                request_id,customer_group_id,service_location_id,actor_id,
                action_name,occurred_at
            ) VALUES(%s,%s,%s,%s,'GUEST_DEPARTED',%s)""",
            (
                result.request_id,
                result.customer_group_id,
                result.service_location_id,
                result.departed_by_id,
                result.departed_at,
            ),
        )


class PostgresDepartureUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, Any]] | None = None
        self._committed = False

    def __enter__(self) -> "PostgresDepartureUnitOfWork":
        connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._connection = connection
        self.locations = PostgresDepartureLocations(connection)
        self.customer_groups = PostgresCustomerGroupFacts(connection)
        self.receipts = PostgresDepartureReceipts(connection)
        self.activity = PostgresDepartureActivity(connection)
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

    def commit(self) -> None:
        if self._connection is None:
            raise RuntimeError("unit of work is not entered")
        try:
            self._connection.commit()
        except psycopg.errors.UniqueViolation as error:
            raise DepartureConcurrencyError("Guest Departure state changed") from error
        self._committed = True


class PostgresDepartureUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> Unit:
        return cast(Unit, PostgresDepartureUnitOfWork(self._connection_string))
