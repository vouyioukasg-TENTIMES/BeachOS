"""Pure event-sourced Bill Closing rules."""

from dataclasses import dataclass
from datetime import datetime


class BillClosingError(ValueError):
    """A Bill cannot be closed under the approved rules."""


@dataclass(frozen=True, slots=True)
class PaymentRecorded:
    bill_id: str
    customer_group_id: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BillFullyPaid:
    bill_id: str
    customer_group_id: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BillClosed:
    bill_id: str
    customer_group_id: str
    closed_by_id: str
    occurred_at: datetime


ClosingEvent = PaymentRecorded | BillFullyPaid | BillClosed


class BillClosingAggregate:
    def __init__(self, *, bill_id: str, customer_group_id: str) -> None:
        if not bill_id.strip() or not customer_group_id.strip():
            raise BillClosingError("Bill and Customer Group identities are required")
        self.bill_id = bill_id.strip()
        self.customer_group_id = customer_group_id.strip()
        self._payment_recorded = False
        self._fully_paid = False
        self._closed: BillClosed | None = None
        self._version = 0
        self._pending: list[BillClosed] = []

    @classmethod
    def restore(
        cls, *, bill_id: str, customer_group_id: str, events: tuple[ClosingEvent, ...]
    ) -> "BillClosingAggregate":
        aggregate = cls(bill_id=bill_id, customer_group_id=customer_group_id)
        for event in events:
            aggregate._apply(event)
            aggregate._version += 1
        return aggregate

    def close(self, *, actor_id: str, at: datetime) -> BillClosed:
        if not self._fully_paid:
            raise BillClosingError("only a FULLY_PAID Bill may be closed")
        if self._closed is not None:
            raise BillClosingError("Bill is already closed")
        if not actor_id.strip():
            raise BillClosingError("closing Staff identity is required")
        if at.tzinfo is None or at.utcoffset() is None:
            raise BillClosingError("closing time must include a timezone")
        event = BillClosed(self.bill_id, self.customer_group_id, actor_id.strip(), at)
        self._apply(event)
        self._pending.append(event)
        self._version += 1
        return event

    def _apply(self, event: ClosingEvent) -> None:
        if event.bill_id != self.bill_id or event.customer_group_id != self.customer_group_id:
            raise BillClosingError("financial event belongs to another Bill")
        if isinstance(event, PaymentRecorded):
            if self._payment_recorded:
                raise BillClosingError("Bill has duplicate Payment history")
            self._payment_recorded = True
        elif isinstance(event, BillFullyPaid):
            if not self._payment_recorded or self._fully_paid:
                raise BillClosingError("Bill Fully Paid must follow confirmed Payment")
            self._fully_paid = True
        elif not self._fully_paid or self._closed is not None:
            raise BillClosingError("Bill Closed must follow one fully paid state")
        else:
            self._closed = event

    def pull_events(self) -> tuple[BillClosed, ...]:
        events = tuple(self._pending)
        self._pending.clear()
        return events

    @property
    def closed(self) -> BillClosed | None:
        return self._closed

    @property
    def version(self) -> int:
        return self._version
