"""Approved Guest Arrival Domain Events."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class ResponsibleWaiterAssigned:
    customer_group_id: str
    service_location_id: str
    responsible_waiter_id: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class CustomerGroupOpened:
    customer_group_id: str
    venue_id: str
    service_location_id: str
    responsible_waiter_id: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class FinancialObligationCreated:
    obligation_id: str
    customer_group_id: str
    source: str
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
    bill_line_id: str
    description: str
    amount: Decimal
    currency: str
    source: str
    occurred_at: datetime


GuestArrivalEvent = (
    ResponsibleWaiterAssigned
    | CustomerGroupOpened
    | FinancialObligationCreated
    | BillCreated
    | BillLineAdded
)
