"""Explicit mappings for Kitchen source and event data."""

from datetime import datetime
from decimal import Decimal
from typing import Any

from beachos_api.packs.beachos.kitchen.domain import (
    KitchenEvent,
    KitchenTicketAcknowledged,
    KitchenTicketCollected,
    KitchenTicketDelivered,
    KitchenTicketItem,
    KitchenTicketReady,
)


def source_items_from_data(data: dict[str, Any]) -> tuple[KitchenTicketItem, ...]:
    return tuple(
        KitchenTicketItem(
            order_item_id=item["order_item_id"],
            name=item["name"],
            quantity=Decimal(item["quantity"]),
            note=item["note"],
        )
        for item in data["items"]
    )


def event_to_data(event: KitchenEvent) -> tuple[str, dict[str, Any], datetime]:
    if isinstance(event, KitchenTicketReady):
        return (
            "KITCHEN_TICKET_READY",
            {"ticket_id": event.ticket_id, "confirmed_by_id": event.confirmed_by_id},
            event.confirmed_at,
        )
    if isinstance(event, KitchenTicketCollected):
        return (
            "KITCHEN_TICKET_COLLECTED",
            {"ticket_id": event.ticket_id, "collected_by_id": event.collected_by_id},
            event.collected_at,
        )
    if isinstance(event, KitchenTicketDelivered):
        return (
            "KITCHEN_TICKET_DELIVERED",
            {"ticket_id": event.ticket_id, "delivered_by_id": event.delivered_by_id},
            event.delivered_at,
        )
    return (
        "KITCHEN_TICKET_ACKNOWLEDGED",
        {
            "ticket_id": event.ticket_id,
            "acknowledged_by_id": event.acknowledged_by_id,
            "acknowledged_at": event.acknowledged_at.isoformat(),
        },
        event.acknowledged_at,
    )


def event_from_data(event_type: str, data: dict[str, Any], occurred_at: datetime) -> KitchenEvent:
    if event_type == "KITCHEN_TICKET_READY":
        return KitchenTicketReady(data["ticket_id"], data["confirmed_by_id"], occurred_at)
    if event_type == "KITCHEN_TICKET_COLLECTED":
        return KitchenTicketCollected(data["ticket_id"], data["collected_by_id"], occurred_at)
    if event_type == "KITCHEN_TICKET_DELIVERED":
        return KitchenTicketDelivered(data["ticket_id"], data["delivered_by_id"], occurred_at)
    if event_type != "KITCHEN_TICKET_ACKNOWLEDGED":
        raise ValueError(f"unsupported Kitchen event type: {event_type}")
    return KitchenTicketAcknowledged(
        ticket_id=data["ticket_id"],
        acknowledged_by_id=data["acknowledged_by_id"],
        acknowledged_at=occurred_at,
    )
