"""Dependency-inversion ports for Kitchen Operations."""

from datetime import datetime
from types import TracebackType
from typing import Protocol, Self

from beachos_api.packs.beachos.kitchen.application.dtos import (
    AcknowledgeKitchenTicketResult,
)
from beachos_api.packs.beachos.kitchen.domain import KitchenTicket


class KitchenCapabilityVerifier(Protocol):
    def can_acknowledge_kitchen_ticket(
        self, *, actor_id: str, venue_id: str, ticket_id: str
    ) -> bool: ...

    def can_mark_kitchen_ticket_ready(
        self, *, actor_id: str, venue_id: str, ticket_id: str
    ) -> bool: ...
    def can_collect_ticket(
        self, *, actor_id: str, venue_id: str, responsible_service_staff_id: str
    ) -> bool: ...
    def can_deliver_ticket(
        self, *, actor_id: str, venue_id: str, responsible_service_staff_id: str
    ) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class KitchenTicketRepository(Protocol):
    def get(self, *, ticket_id: str) -> KitchenTicket | None: ...

    def list_for_venue(self, *, venue_id: str) -> tuple[KitchenTicket, ...]: ...

    def save(self, ticket: KitchenTicket) -> None: ...


class KitchenCommandReceiptStore(Protocol):
    def get(self, *, request_id: str) -> AcknowledgeKitchenTicketResult | None: ...

    def save(self, *, request_id: str, result: AcknowledgeKitchenTicketResult) -> None: ...


class KitchenUnitOfWork(Protocol):
    @property
    def tickets(self) -> KitchenTicketRepository: ...

    @property
    def receipts(self) -> KitchenCommandReceiptStore: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...


class KitchenUnitOfWorkFactory(Protocol):
    def create(self) -> KitchenUnitOfWork: ...
