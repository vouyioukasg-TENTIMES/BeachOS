"""Dependency-inversion ports for Bar Operations."""

from datetime import datetime
from types import TracebackType
from typing import Protocol, Self

from beachos_api.packs.beachos.bar.domain import BarTicket

from .dtos import AcknowledgeBarTicketResult


class BarCapabilityVerifier(Protocol):
    def can_acknowledge_bar_ticket(
        self, *, actor_id: str, venue_id: str, ticket_id: str
    ) -> bool: ...
    def can_mark_bar_ticket_ready(
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


class BarTicketRepository(Protocol):
    def get(self, *, ticket_id: str) -> BarTicket | None: ...
    def list_for_venue(self, *, venue_id: str) -> tuple[BarTicket, ...]: ...
    def save(self, ticket: BarTicket) -> None: ...


class BarCommandReceiptStore(Protocol):
    def get(self, *, request_id: str) -> AcknowledgeBarTicketResult | None: ...
    def save(self, *, request_id: str, result: AcknowledgeBarTicketResult) -> None: ...


class BarUnitOfWork(Protocol):
    @property
    def tickets(self) -> BarTicketRepository: ...
    @property
    def receipts(self) -> BarCommandReceiptStore: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def commit(self) -> None: ...


class BarUnitOfWorkFactory(Protocol):
    def create(self) -> BarUnitOfWork: ...
