"""Framework-independent Kitchen Operations Domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from beachos_api.packs.beachos.kitchen.domain.events import (
    KitchenEvent,
    KitchenTicketAcknowledged,
    KitchenTicketCollected,
    KitchenTicketDelivered,
    KitchenTicketReady,
)


class KitchenError(ValueError):
    """A Kitchen action violates an approved business rule."""


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise KitchenError(f"{field} is required")
    return normalized


def _aware(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise KitchenError(f"{field} must include a timezone")
    return value


@dataclass(frozen=True, slots=True)
class KitchenTicketItem:
    order_item_id: str
    name: str
    quantity: Decimal
    note: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "order_item_id", _required(self.order_item_id, "Order Item id"))
        object.__setattr__(self, "name", _required(self.name, "Order Item name"))
        if not isinstance(self.quantity, Decimal) or not self.quantity.is_finite():
            raise KitchenError("Order Item quantity must be a finite decimal")
        if self.quantity <= 0:
            raise KitchenError("Order Item quantity must be greater than zero")
        if self.note is not None:
            object.__setattr__(self, "note", self.note.strip() or None)


class KitchenTicket:
    """Event-sourced Kitchen responsibility created by an accepted Order."""

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
        items: tuple[KitchenTicketItem, ...],
    ) -> None:
        self._ticket_id = _required(ticket_id, "Kitchen Ticket id")
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
            raise KitchenError("a Kitchen Ticket requires at least one Kitchen item")
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
        self._pending_events: list[KitchenEvent] = []

    @classmethod
    def restore(
        cls,
        *,
        ticket_id: str,
        order_id: str,
        customer_group_id: str,
        venue_id: str,
        submission_service_location_id: str,
        current_service_location_id: str,
        responsible_service_staff_id: str,
        submitted_at: datetime,
        items: tuple[KitchenTicketItem, ...],
        events: tuple[KitchenEvent, ...],
    ) -> KitchenTicket:
        ticket = cls(
            ticket_id=ticket_id,
            order_id=order_id,
            customer_group_id=customer_group_id,
            venue_id=venue_id,
            submission_service_location_id=submission_service_location_id,
            current_service_location_id=current_service_location_id,
            responsible_service_staff_id=responsible_service_staff_id,
            submitted_at=submitted_at,
            items=items,
        )
        for event in events:
            ticket._apply(event)
            ticket._version += 1
        return ticket

    def acknowledge(self, *, actor_id: str, acknowledged_at: datetime) -> None:
        if self._acknowledged_at is not None:
            raise KitchenError("Kitchen Ticket has already been acknowledged")
        self._record(
            KitchenTicketAcknowledged(
                ticket_id=self._ticket_id,
                acknowledged_by_id=_required(actor_id, "acknowledging Kitchen Staff id"),
                acknowledged_at=_aware(acknowledged_at, "acknowledgement time"),
            )
        )

    def mark_ready(self, *, actor_id: str, confirmed_at: datetime) -> None:
        if self._acknowledged_at is None:
            raise KitchenError("Kitchen Ticket must be acknowledged before it can be READY")
        if self._ready_at is not None:
            raise KitchenError("Kitchen Ticket is already READY")
        self._record(
            KitchenTicketReady(
                self._ticket_id,
                _required(actor_id, "Kitchen Staff id"),
                _aware(confirmed_at, "readiness time"),
            )
        )

    def collect(self, *, actor_id: str, collected_at: datetime) -> None:
        if self._ready_at is None:
            raise KitchenError("Kitchen Ticket must be READY before collection")
        if self._collected_at is not None:
            raise KitchenError("Kitchen Ticket is already COLLECTED")
        self._record(
            KitchenTicketCollected(
                self._ticket_id,
                _required(actor_id, "collector id"),
                _aware(collected_at, "collection time"),
            )
        )

    def deliver(self, *, actor_id: str, delivered_at: datetime) -> None:
        if self._collected_at is None:
            raise KitchenError("Kitchen Ticket must be COLLECTED before delivery")
        if self._delivered_at is not None:
            raise KitchenError("Kitchen Ticket is already DELIVERED")
        self._record(
            KitchenTicketDelivered(
                self._ticket_id,
                _required(actor_id, "delivery person id"),
                _aware(delivered_at, "delivery time"),
            )
        )

    def _record(self, event: KitchenEvent) -> None:
        self._apply(event)
        self._pending_events.append(event)
        self._version += 1

    def _apply(self, event: KitchenEvent) -> None:
        if event.ticket_id != self._ticket_id:
            raise KitchenError("Kitchen event belongs to another Ticket")
        if isinstance(event, KitchenTicketAcknowledged):
            if self._acknowledged_at is not None:
                raise KitchenError("Kitchen Ticket acknowledgement cannot be repeated")
            self._acknowledged_by_id = _required(
                event.acknowledged_by_id, "acknowledging Kitchen Staff id"
            )
            self._acknowledged_at = _aware(event.acknowledged_at, "acknowledgement time")
        elif isinstance(event, KitchenTicketReady):
            if self._acknowledged_at is None or self._ready_at is not None:
                raise KitchenError("Kitchen Ticket readiness sequence is invalid")
            self._ready_by_id = _required(event.confirmed_by_id, "Kitchen Staff id")
            self._ready_at = _aware(event.confirmed_at, "readiness time")
        elif isinstance(event, KitchenTicketCollected):
            if self._ready_at is None or self._collected_at is not None:
                raise KitchenError("Kitchen Ticket collection sequence is invalid")
            self._collected_by_id = _required(event.collected_by_id, "collector id")
            self._collected_at = _aware(event.collected_at, "collection time")
        elif isinstance(event, KitchenTicketDelivered):
            if self._collected_at is None or self._delivered_at is not None:
                raise KitchenError("Kitchen Ticket delivery sequence is invalid")
            self._delivered_by_id = _required(event.delivered_by_id, "delivery person id")
            self._delivered_at = _aware(event.delivered_at, "delivery time")

    def pull_events(self) -> tuple[KitchenEvent, ...]:
        events = tuple(self._pending_events)
        self._pending_events.clear()
        return events

    @property
    def ticket_id(self) -> str:
        return self._ticket_id

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def customer_group_id(self) -> str:
        return self._customer_group_id

    @property
    def venue_id(self) -> str:
        return self._venue_id

    @property
    def submission_service_location_id(self) -> str:
        return self._submission_service_location_id

    @property
    def current_service_location_id(self) -> str:
        return self._current_service_location_id

    @property
    def responsible_service_staff_id(self) -> str:
        return self._responsible_service_staff_id

    @property
    def submitted_at(self) -> datetime:
        return self._submitted_at

    @property
    def items(self) -> tuple[KitchenTicketItem, ...]:
        return self._items

    @property
    def acknowledged_by_id(self) -> str | None:
        return self._acknowledged_by_id

    @property
    def acknowledged_at(self) -> datetime | None:
        return self._acknowledged_at

    ready_by_id = property(lambda self: self._ready_by_id)
    ready_at = property(lambda self: self._ready_at)
    collected_by_id = property(lambda self: self._collected_by_id)
    collected_at = property(lambda self: self._collected_at)
    delivered_by_id = property(lambda self: self._delivered_by_id)
    delivered_at = property(lambda self: self._delivered_at)

    @property
    def version(self) -> int:
        return self._version
