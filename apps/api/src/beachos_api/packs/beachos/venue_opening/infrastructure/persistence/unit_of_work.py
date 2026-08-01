"""PostgreSQL unit-of-work adapter for Venue Opening."""

from __future__ import annotations

from types import TracebackType

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.venue_opening.application.ports import (
    ActivityLog,
    VenueOpeningUnitOfWork,
    VenueRepository,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.persistence.activity_log import (
    PostgresActivityLog,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.persistence.repository import (
    PostgresVenueRepository,
)


class PostgresVenueOpeningUnitOfWork:
    """Owns one short PostgreSQL transaction per Application Command."""

    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, object]] | None = None
        self._committed = False
        self._venues: PostgresVenueRepository | None = None
        self._activity_log: PostgresActivityLog | None = None

    @property
    def venues(self) -> VenueRepository:
        if self._venues is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._venues

    @property
    def activity_log(self) -> ActivityLog:
        if self._activity_log is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._activity_log

    def __enter__(self) -> PostgresVenueOpeningUnitOfWork:
        self._connection = psycopg.connect(
            self._connection_string,
            row_factory=dict_row,
        )
        self._venues = PostgresVenueRepository(self._connection)
        self._activity_log = PostgresActivityLog(self._connection)
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exception_type, exception, traceback
        if self._connection is None:
            return
        if not self._committed:
            self._connection.rollback()
        self._connection.close()

    def commit(self) -> None:
        if self._connection is None:
            raise RuntimeError("the unit of work has not been entered")
        self._connection.commit()
        self._committed = True


class PostgresVenueOpeningUnitOfWorkFactory:
    """Creates PostgreSQL-backed Venue Opening units of work."""

    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> VenueOpeningUnitOfWork:
        return PostgresVenueOpeningUnitOfWork(self._connection_string)
