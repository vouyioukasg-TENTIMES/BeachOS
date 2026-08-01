"""Pure event-sourced Domain for the approved Cash/full-Payment MVP."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


class PaymentError(ValueError):
    """A Payment would violate an approved financial rule."""


@dataclass(frozen=True, slots=True)
class PaymentRecorded:
    payment_id: str
    bill_id: str
    customer_group_id: str
    amount: Decimal
    currency: str
    method: str
    recorded_by_id: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BillFullyPaid:
    bill_id: str
    customer_group_id: str
    occurred_at: datetime


PaymentEvent = PaymentRecorded | BillFullyPaid


class PaymentAggregate:
    def __init__(
        self, *, bill_id: str, customer_group_id: str, total: Decimal, currency: str
    ) -> None:
        if not bill_id.strip() or not customer_group_id.strip():
            raise PaymentError("Bill and Customer Group identities are required")
        if total <= 0 or not total.is_finite():
            raise PaymentError("a Payment requires a positive finite Bill Balance")
        if not currency.strip():
            raise PaymentError("currency is required")
        self.bill_id = bill_id.strip()
        self.customer_group_id = customer_group_id.strip()
        self.total = total
        self.currency = currency.strip().upper()
        self._payment: PaymentRecorded | None = None
        self._fully_paid = False
        self._version = 0
        self._pending: list[PaymentEvent] = []

    @classmethod
    def restore(
        cls,
        *,
        bill_id: str,
        customer_group_id: str,
        total: Decimal,
        currency: str,
        events: tuple[PaymentEvent, ...],
    ) -> "PaymentAggregate":
        aggregate = cls(
            bill_id=bill_id,
            customer_group_id=customer_group_id,
            total=total,
            currency=currency,
        )
        for event in events:
            aggregate._apply(event)
            aggregate._version += 1
        if aggregate._payment is not None and not aggregate._fully_paid:
            raise PaymentError("confirmed full Payment history must include Bill Fully Paid")
        return aggregate

    def record_cash_payment(
        self, *, payment_id: str, amount: Decimal, currency: str, actor_id: str, at: datetime
    ) -> PaymentRecorded:
        if self._payment is not None:
            raise PaymentError("this Bill already has a confirmed Payment")
        if amount != self.total:
            raise PaymentError("the MVP accepts only full Payment of the current Balance")
        if currency.strip().upper() != self.currency:
            raise PaymentError("Payment currency must match the Bill")
        if not payment_id.strip() or not actor_id.strip():
            raise PaymentError("Payment and recording Staff identities are required")
        if at.tzinfo is None or at.utcoffset() is None:
            raise PaymentError("Payment time must include a timezone")
        recorded = PaymentRecorded(
            payment_id.strip(),
            self.bill_id,
            self.customer_group_id,
            amount,
            self.currency,
            "CASH",
            actor_id.strip(),
            at,
        )
        self._record(recorded)
        self._record(BillFullyPaid(self.bill_id, self.customer_group_id, at))
        return recorded

    def _record(self, event: PaymentEvent) -> None:
        self._apply(event)
        self._pending.append(event)
        self._version += 1

    def _apply(self, event: PaymentEvent) -> None:
        if event.bill_id != self.bill_id or event.customer_group_id != self.customer_group_id:
            raise PaymentError("Payment history belongs to another Bill")
        if isinstance(event, PaymentRecorded):
            if (
                self._payment is not None
                or event.method != "CASH"
                or event.amount <= 0
                or event.amount > self.total
            ):
                raise PaymentError("persisted Payment history is invalid for the MVP")
            if event.currency != self.currency:
                raise PaymentError("persisted Payment currency does not match the Bill")
            self._payment = event
        elif self._payment is None or self._fully_paid:
            raise PaymentError("Bill Fully Paid must follow one confirmed Payment")
        else:
            self._fully_paid = True

    def pull_events(self) -> tuple[PaymentEvent, ...]:
        events = tuple(self._pending)
        self._pending.clear()
        return events

    @property
    def payment(self) -> PaymentRecorded | None:
        return self._payment

    @property
    def fully_paid(self) -> bool:
        return self._fully_paid

    @property
    def version(self) -> int:
        return self._version
