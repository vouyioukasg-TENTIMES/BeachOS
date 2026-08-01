"""PostgreSQL Ordering unit of work."""

from __future__ import annotations

from types import TracebackType

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.ordering.application.ports import (
    CommandReceiptStore,
    CustomerGroupRepository,
    MenuCatalog,
    OrderingUnitOfWork,
)
from beachos_api.packs.beachos.ordering.infrastructure.persistence.adapters import (
    PostgresCommandReceiptStore,
    PostgresCustomerGroupRepository,
    PostgresMenuCatalog,
)


class PostgresOrderingUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, object]] | None = None
        self._committed = False
        self._groups: PostgresCustomerGroupRepository | None = None
        self._menus: PostgresMenuCatalog | None = None
        self._receipts: PostgresCommandReceiptStore | None = None

    def __enter__(self) -> PostgresOrderingUnitOfWork:
        self._connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._groups = PostgresCustomerGroupRepository(self._connection)
        self._menus = PostgresMenuCatalog(self._connection)
        self._receipts = PostgresCommandReceiptStore(self._connection)
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
    def customer_groups(self) -> CustomerGroupRepository:
        if self._groups is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._groups

    @property
    def menus(self) -> MenuCatalog:
        if self._menus is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._menus

    @property
    def receipts(self) -> CommandReceiptStore:
        if self._receipts is None:
            raise RuntimeError("the unit of work has not been entered")
        return self._receipts

    def commit(self) -> None:
        if self._connection is None:
            raise RuntimeError("the unit of work has not been entered")
        self._connection.commit()
        self._committed = True


class PostgresOrderingUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> OrderingUnitOfWork:
        return PostgresOrderingUnitOfWork(self._connection_string)
