"""Dependency-inversion ports for Ordering."""

from datetime import datetime
from types import TracebackType
from typing import Protocol, Self

from beachos_api.packs.beachos.ordering.application.dtos import SubmitOrderResult
from beachos_api.packs.beachos.ordering.domain import CustomerGroup, MenuItem


class OrderingCapabilityVerifier(Protocol):
    def can_submit_order(self, *, actor_id: str, venue_id: str, customer_group_id: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class IdentityGenerator(Protocol):
    def new_id(self, prefix: str) -> str: ...


class CustomerGroupRepository(Protocol):
    def get(self, *, customer_group_id: str) -> CustomerGroup | None: ...

    def save(self, customer_group: CustomerGroup) -> None: ...


class MenuCatalog(Protocol):
    def available_for_venue(self, *, venue_id: str) -> tuple[MenuItem, ...]: ...


class CommandReceiptStore(Protocol):
    def get(self, *, request_id: str) -> SubmitOrderResult | None: ...

    def save(self, *, request_id: str, result: SubmitOrderResult) -> None: ...


class OrderingUnitOfWork(Protocol):
    @property
    def customer_groups(self) -> CustomerGroupRepository: ...

    @property
    def menus(self) -> MenuCatalog: ...

    @property
    def receipts(self) -> CommandReceiptStore: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...


class OrderingUnitOfWorkFactory(Protocol):
    def create(self) -> OrderingUnitOfWork: ...
