"""Approved Bar Operations Domain Events."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class BarTicketAcknowledged:
    ticket_id: str
    acknowledged_by_id: str
    acknowledged_at: datetime


@dataclass(frozen=True, slots=True)
class BarTicketReady:
    ticket_id: str
    confirmed_by_id: str
    confirmed_at: datetime


@dataclass(frozen=True, slots=True)
class BarTicketCollected:
    ticket_id: str
    collected_by_id: str
    collected_at: datetime


@dataclass(frozen=True, slots=True)
class BarTicketDelivered:
    ticket_id: str
    delivered_by_id: str
    delivered_at: datetime


BarEvent = BarTicketAcknowledged | BarTicketReady | BarTicketCollected | BarTicketDelivered
