"""Bar Application results."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from beachos_api.packs.beachos.bar.domain import BarTicket, BarTicketItem


@dataclass(frozen=True, slots=True)
class BarTicketItemDTO:
    order_item_id: str
    name: str
    quantity: Decimal
    note: str | None

    @classmethod
    def from_domain(cls, item: BarTicketItem) -> BarTicketItemDTO:
        return cls(item.order_item_id, item.name, item.quantity, item.note)


@dataclass(frozen=True, slots=True)
class BarTicketDTO:
    ticket_id: str
    order_id: str
    customer_group_id: str
    venue_id: str
    submission_service_location_id: str
    current_service_location_id: str
    responsible_service_staff_id: str
    submitted_at: datetime
    items: tuple[BarTicketItemDTO, ...]
    acknowledged_by_id: str | None
    acknowledged_at: datetime | None
    ready_by_id: str | None
    ready_at: datetime | None
    collected_by_id: str | None
    collected_at: datetime | None
    delivered_by_id: str | None
    delivered_at: datetime | None

    @property
    def status(self) -> str:
        if self.delivered_at:
            return "DELIVERED"
        if self.collected_at:
            return "COLLECTED"
        if self.ready_at:
            return "READY"
        return "ACKNOWLEDGED" if self.acknowledged_at else "NEW"

    @property
    def current_responsibility(self) -> str:
        return {
            "NEW": "BAR",
            "ACKNOWLEDGED": "BAR",
            "READY": "COLLECTOR",
            "COLLECTED": "DELIVERY",
            "DELIVERED": "COMPLETE",
        }[self.status]

    @property
    def current_responsible_person_id(self) -> str:
        return (
            self.delivered_by_id
            or self.collected_by_id
            or (self.responsible_service_staff_id if self.ready_at else None)
            or self.acknowledged_by_id
            or self.responsible_service_staff_id
        )

    @property
    def next_action(self) -> str:
        return {
            "NEW": "ACKNOWLEDGE",
            "ACKNOWLEDGED": "MARK_READY",
            "READY": "COLLECT",
            "COLLECTED": "DELIVER",
            "DELIVERED": "NONE",
        }[self.status]

    @classmethod
    def from_domain(cls, ticket: BarTicket) -> BarTicketDTO:
        return cls(
            ticket.ticket_id,
            ticket.order_id,
            ticket.customer_group_id,
            ticket.venue_id,
            ticket.submission_service_location_id,
            ticket.current_service_location_id,
            ticket.responsible_service_staff_id,
            ticket.submitted_at,
            tuple(BarTicketItemDTO.from_domain(item) for item in ticket.items),
            ticket.acknowledged_by_id,
            ticket.acknowledged_at,
            ticket.ready_by_id,
            ticket.ready_at,
            ticket.collected_by_id,
            ticket.collected_at,
            ticket.delivered_by_id,
            ticket.delivered_at,
        )


@dataclass(frozen=True, slots=True)
class BarContextResult:
    venue_id: str
    tickets: tuple[BarTicketDTO, ...]

    @property
    def awaiting_acknowledgement_count(self) -> int:
        return sum(ticket.acknowledged_at is None for ticket in self.tickets)


@dataclass(frozen=True, slots=True)
class AcknowledgeBarTicketResult:
    request_id: str
    ticket: BarTicketDTO
