"""Approved Kitchen Operations Domain Events."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class KitchenTicketAcknowledged:
    ticket_id: str
    acknowledged_by_id: str
    acknowledged_at: datetime


@dataclass(frozen=True, slots=True)
class KitchenTicketReady:
    ticket_id: str
    confirmed_by_id: str
    confirmed_at: datetime


@dataclass(frozen=True, slots=True)
class KitchenTicketCollected:
    ticket_id: str
    collected_by_id: str
    collected_at: datetime


@dataclass(frozen=True, slots=True)
class KitchenTicketDelivered:
    ticket_id: str
    delivered_by_id: str
    delivered_at: datetime


KitchenEvent = (
    KitchenTicketAcknowledged | KitchenTicketReady | KitchenTicketCollected | KitchenTicketDelivered
)
