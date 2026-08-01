"""Billing use cases: explain the current running Bill."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from beachos_api.packs.beachos.billing.domain import Bill


class BillReader(Protocol):
    def get(self, *, customer_group_id: str) -> Bill | None: ...


@dataclass(frozen=True, slots=True)
class BillLineDTO:
    bill_line_id: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    currency: str
    source: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BillDTO:
    bill_id: str
    customer_group_id: str
    currency: str
    total: Decimal
    balance: Decimal
    status: str
    lines: tuple[BillLineDTO, ...]
    payments: tuple["PaymentDTO", ...]
    closed_by_id: str | None
    closed_at: datetime | None
    version: int


@dataclass(frozen=True, slots=True)
class PaymentDTO:
    payment_id: str
    amount: Decimal
    currency: str
    method: str
    recorded_by_id: str
    recorded_at: datetime


class BillingService:
    def __init__(self, reader: BillReader) -> None:
        self._reader = reader

    def get_bill(self, *, customer_group_id: str) -> BillDTO | None:
        bill = self._reader.get(customer_group_id=customer_group_id)
        if bill is None:
            return None
        return BillDTO(
            bill.bill_id,
            bill.customer_group_id,
            bill.currency,
            bill.total,
            bill.balance,
            "CLOSED" if bill.closed else "FULLY_PAID" if bill.balance == 0 else "OPEN",
            tuple(
                BillLineDTO(
                    line.bill_line_id,
                    line.description,
                    line.quantity,
                    line.unit_price,
                    line.amount,
                    line.currency,
                    line.source,
                    line.occurred_at,
                )
                for line in bill.lines
            ),
            tuple(
                PaymentDTO(
                    payment.payment_id,
                    payment.amount,
                    payment.currency,
                    payment.method,
                    payment.recorded_by_id,
                    payment.occurred_at,
                )
                for payment in bill.payments
            ),
            bill.closed.closed_by_id if bill.closed else None,
            bill.closed.occurred_at if bill.closed else None,
            bill.version,
        )
