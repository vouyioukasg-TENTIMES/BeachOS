"""Persistence-neutral, event-restored Billing Domain."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


class BillingError(ValueError):
    """Persisted financial facts cannot form a valid Bill."""


def _required(value: str, name: str) -> str:
    value = value.strip()
    if not value:
        raise BillingError(f"{name} is required")
    return value


@dataclass(frozen=True, slots=True)
class BillCreated:
    bill_id: str
    customer_group_id: str
    currency: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BillLineAdded:
    bill_id: str
    bill_line_id: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    currency: str
    source: str
    occurred_at: datetime


BillingEvent = BillCreated | BillLineAdded


@dataclass(frozen=True, slots=True)
class BillLine:
    bill_line_id: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    currency: str
    source: str
    occurred_at: datetime


class Bill:
    """One Customer Group's immutable running financial history."""

    def __init__(self) -> None:
        self._bill_id: str | None = None
        self._customer_group_id: str | None = None
        self._currency: str | None = None
        self._lines: list[BillLine] = []
        self._version = 0

    @classmethod
    def restore(cls, events: tuple[BillingEvent, ...]) -> "Bill":
        bill = cls()
        for event in events:
            bill._apply(event)
            bill._version += 1
        if bill._bill_id is None:
            raise BillingError("Bill history must begin with Bill Created")
        return bill

    def _apply(self, event: BillingEvent) -> None:
        if isinstance(event, BillCreated):
            if self._bill_id is not None:
                raise BillingError("a Customer Group may have only one Bill")
            self._bill_id = _required(event.bill_id, "Bill id")
            self._customer_group_id = _required(event.customer_group_id, "Customer Group id")
            self._currency = _required(event.currency, "currency").upper()
            return
        if self._bill_id is None or event.bill_id != self._bill_id:
            raise BillingError("Bill Line must belong to the restored Bill")
        if event.currency.upper() != self._currency:
            raise BillingError("Bill Line currency must match the Bill")
        if event.quantity <= 0 or event.unit_price < 0 or event.amount < 0:
            raise BillingError("Bill Line financial values are invalid")
        if any(line.bill_line_id == event.bill_line_id for line in self._lines):
            raise BillingError("Bill Line id must be unique")
        self._lines.append(
            BillLine(
                _required(event.bill_line_id, "Bill Line id"),
                _required(event.description, "Bill Line description"),
                event.quantity,
                event.unit_price,
                event.amount,
                event.currency.upper(),
                _required(event.source, "Bill Line source"),
                event.occurred_at,
            )
        )

    @property
    def bill_id(self) -> str:
        if self._bill_id is None:
            raise BillingError("Bill has not been restored")
        return self._bill_id

    @property
    def customer_group_id(self) -> str:
        if self._customer_group_id is None:
            raise BillingError("Bill has not been restored")
        return self._customer_group_id

    @property
    def currency(self) -> str:
        if self._currency is None:
            raise BillingError("Bill has not been restored")
        return self._currency

    @property
    def lines(self) -> tuple[BillLine, ...]:
        return tuple(self._lines)

    @property
    def total(self) -> Decimal:
        return sum((line.amount for line in self._lines), Decimal("0"))

    @property
    def version(self) -> int:
        return self._version
