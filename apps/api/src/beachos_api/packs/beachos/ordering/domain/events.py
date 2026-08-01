"""Approved Ordering Domain Events."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from beachos_api.packs.beachos.ordering.domain.model import (
    BarTicket,
    BillLine,
    KitchenTicket,
    Order,
)


@dataclass(frozen=True, slots=True)
class OrderSubmitted:
    order: Order
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class KitchenTicketCreated:
    ticket: KitchenTicket
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BarTicketCreated:
    ticket: BarTicket
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class FinancialObligationCreated:
    obligation_id: str
    customer_group_id: str
    order_item_id: str | None
    amount: Decimal
    currency: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BillCreated:
    bill_id: str
    customer_group_id: str
    currency: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class BillLineAdded:
    bill_id: str
    line: BillLine
    occurred_at: datetime


OrderingEvent = (
    OrderSubmitted
    | KitchenTicketCreated
    | BarTicketCreated
    | FinancialObligationCreated
    | BillCreated
    | BillLineAdded
)
