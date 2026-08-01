"""Framework-independent Bar Operations Domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from beachos_api.packs.beachos.bar.domain.events import (
    BarEvent,
    BarTicketAcknowledged,
    BarTicketCollected,
    BarTicketDelivered,
    BarTicketReady,
)


class BarError(ValueError):
    """A Bar action violates an approved business rule."""


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise BarError(f"{field} is required")
    return normalized


def _aware(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise BarError(f"{field} must include a timezone")
    return value


@dataclass(frozen=True, slots=True)
class BarTicketItem:
    order_item_id: str
    name: str
    quantity: Decimal
    note: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "order_item_id", _required(self.order_item_id, "Order Item id"))
        object.__setattr__(self, "name", _required(self.name, "Order Item name"))
        if not isinstance(self.quantity, Decimal) or not self.quantity.is_finite():
            raise BarError("Order Item quantity must be a finite decimal")
        if self.quantity <= 0:
            raise BarError("Order Item quantity must be greater than zero")
        if self.note is not None:
            object.__setattr__(self, "note", self.note.strip() or None)


class BarTicket:
    """Event-sourced Bar responsibility created by an accepted Order."""

    def __init__(
        self,
        *,
        ticket_id: str,
        order_id: str,
        customer_group_id: str,
        venue_id: str,
        submission_service_location_id: str,
        current_service_location_id: str,
        responsible_service_staff_id: str,
        submitted_at: datetime,
        items: tuple[BarTicketItem, ...],
    ) -> None:
        self._ticket_id = _required(ticket_id, "Bar Ticket id")
        self._order_id = _required(order_id, "Order id")
        self._customer_group_id = _required(customer_group_id, "Customer Group id")
        self._venue_id = _required(venue_id, "Venue id")
        self._submission_service_location_id = _required(
            submission_service_location_id, "submission Service Location id"
        )
        self._current_service_location_id = _required(
            current_service_location_id, "current Service Location id"
        )
        self._responsible_service_staff_id = _required(
            responsible_service_staff_id, "Responsible Service Staff id"
        )
        self._submitted_at = _aware(submitted_at, "submission time")
        if not items:
            raise BarError("a Bar Ticket requires at least one Bar item")
        self._items = items
        self._acknowledged_by_id: str | None = None
        self._acknowledged_at: datetime | None = None
        self._ready_by_id: str | None = None
        self._ready_at: datetime | None = None
        self._collected_by_id: str | None = None
        self._collected_at: datetime | None = None
        self._delivered_by_id: str | None = None
        self._delivered_at: datetime | None = None
        self._version = 0
        self._pending_events: list[BarEvent] = []

    @classmethod
    def restore(cls, *, events: tuple[BarEvent, ...], **state: object) -> BarTicket:
        ticket = cls(**state)  # type: ignore[arg-type]
        for event in events:
            ticket._apply(event)
            ticket._version += 1
        return ticket

    def acknowledge(self, *, actor_id: str, acknowledged_at: datetime) -> None:
        if self._acknowledged_at is not None:
            raise BarError("Bar Ticket has already been acknowledged")
        self._record(
            BarTicketAcknowledged(
                self._ticket_id,
                _required(actor_id, "acknowledging Bar Staff id"),
                _aware(acknowledged_at, "acknowledgement time"),
            )
        )

    def mark_ready(self, *, actor_id: str, confirmed_at: datetime) -> None:
        if self._acknowledged_at is None:
            raise BarError("Bar Ticket must be acknowledged before it can be READY")
        if self._ready_at is not None:
            raise BarError("Bar Ticket is already READY")
        self._record(
            BarTicketReady(
                self._ticket_id,
                _required(actor_id, "Bar Staff id"),
                _aware(confirmed_at, "readiness time"),
            )
        )

    def collect(self, *, actor_id: str, collected_at: datetime) -> None:
        if self._ready_at is None:
            raise BarError("Bar Ticket must be READY before collection")
        if self._collected_at is not None:
            raise BarError("Bar Ticket is already COLLECTED")
        self._record(
            BarTicketCollected(
                self._ticket_id,
                _required(actor_id, "collector id"),
                _aware(collected_at, "collection time"),
            )
        )

    def deliver(self, *, actor_id: str, delivered_at: datetime) -> None:
        if self._collected_at is None:
            raise BarError("Bar Ticket must be COLLECTED before delivery")
        if self._delivered_at is not None:
            raise BarError("Bar Ticket is already DELIVERED")
        self._record(
            BarTicketDelivered(
                self._ticket_id,
                _required(actor_id, "delivery person id"),
                _aware(delivered_at, "delivery time"),
            )
        )

    def _record(self, event: BarEvent) -> None:
        self._apply(event)
        self._pending_events.append(event)
        self._version += 1

    def _apply(self, event: BarEvent) -> None:
        if event.ticket_id != self._ticket_id:
            raise BarError("Bar event belongs to another Ticket")
        if isinstance(event, BarTicketAcknowledged):
            if self._acknowledged_at is not None:
                raise BarError("Bar Ticket acknowledgement cannot be repeated")
            self._acknowledged_by_id = _required(
                event.acknowledged_by_id, "acknowledging Bar Staff id"
            )
            self._acknowledged_at = _aware(event.acknowledged_at, "acknowledgement time")
        elif isinstance(event, BarTicketReady):
            if self._acknowledged_at is None or self._ready_at is not None:
                raise BarError("Bar Ticket readiness sequence is invalid")
            self._ready_by_id = _required(event.confirmed_by_id, "Bar Staff id")
            self._ready_at = _aware(event.confirmed_at, "readiness time")
        elif isinstance(event, BarTicketCollected):
            if self._ready_at is None or self._collected_at is not None:
                raise BarError("Bar Ticket collection sequence is invalid")
            self._collected_by_id = _required(event.collected_by_id, "collector id")
            self._collected_at = _aware(event.collected_at, "collection time")
        elif isinstance(event, BarTicketDelivered):
            if self._collected_at is None or self._delivered_at is not None:
                raise BarError("Bar Ticket delivery sequence is invalid")
            self._delivered_by_id = _required(event.delivered_by_id, "delivery person id")
            self._delivered_at = _aware(event.delivered_at, "delivery time")

    def pull_events(self) -> tuple[BarEvent, ...]:
        events = tuple(self._pending_events)
        self._pending_events.clear()
        return events

    ticket_id = property(lambda self: self._ticket_id)
    order_id = property(lambda self: self._order_id)
    customer_group_id = property(lambda self: self._customer_group_id)
    venue_id = property(lambda self: self._venue_id)
    submission_service_location_id = property(lambda self: self._submission_service_location_id)
    current_service_location_id = property(lambda self: self._current_service_location_id)
    responsible_service_staff_id = property(lambda self: self._responsible_service_staff_id)
    submitted_at = property(lambda self: self._submitted_at)
    items = property(lambda self: self._items)
    acknowledged_by_id = property(lambda self: self._acknowledged_by_id)
    acknowledged_at = property(lambda self: self._acknowledged_at)
    ready_by_id = property(lambda self: self._ready_by_id)
    ready_at = property(lambda self: self._ready_at)
    collected_by_id = property(lambda self: self._collected_by_id)
    collected_at = property(lambda self: self._collected_at)
    delivered_by_id = property(lambda self: self._delivered_by_id)
    delivered_at = property(lambda self: self._delivered_at)
    version = property(lambda self: self._version)
