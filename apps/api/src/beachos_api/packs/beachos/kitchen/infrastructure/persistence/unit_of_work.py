"""PostgreSQL Kitchen Operations unit of work."""

from __future__ import annotations

from types import TracebackType

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.kitchen.application.ports import (
    KitchenCommandReceiptStore,
    KitchenTicketRepository,
    KitchenUnitOfWork,
)
from beachos_api.packs.beachos.kitchen.infrastructure.persistence.adapters import (
    PostgresKitchenCommandReceiptStore,
    PostgresKitchenTicketRepository,
)


class PostgresKitchenUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, object]] | None = None
        self._tickets: PostgresKitchenTicketRepository | None = None
        self._receipts: PostgresKitchenCommandReceiptStore | None = None
        self._committed = False

    def __enter__(self) -> PostgresKitchenUnitOfWork:
        self._connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._tickets = PostgresKitchenTicketRepository(self._connection)
        self._receipts = PostgresKitchenCommandReceiptStore(self._connection)
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

    @property
    def tickets(self) -> KitchenTicketRepository:
        if self._tickets is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._tickets

    @property
    def receipts(self) -> KitchenCommandReceiptStore:
        if self._receipts is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._receipts

    def commit(self) -> None:
        if self._connection is None:
            raise RuntimeError("the unit of work has not been entered")
        self._connection.commit()
        self._committed = True


class PostgresKitchenUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> KitchenUnitOfWork:
        return PostgresKitchenUnitOfWork(self._connection_string)
