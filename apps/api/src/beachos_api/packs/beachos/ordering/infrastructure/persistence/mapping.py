"""Explicit JSON mappings for the Ordering event stream."""

from datetime import datetime
from decimal import Decimal
from typing import Any

from beachos_api.packs.beachos.ordering.domain import (
    BarTicket,
    BarTicketCreated,
    BillCreated,
    BillLine,
    BillLineAdded,
    Destination,
    FinancialObligationCreated,
    KitchenTicket,
    KitchenTicketCreated,
    Money,
    Order,
    OrderingEvent,
    OrderItem,
    OrderSubmitted,
)


def _item_to_data(item: OrderItem) -> dict[str, Any]:
    return {
        "order_item_id": item.order_item_id,
        "menu_item_id": item.menu_item_id,
        "name": item.name,
        "quantity": str(item.quantity),
        "unit_price": str(item.unit_price.amount),
        "currency": item.unit_price.currency,
        "destination": item.destination.value,
        "note": item.note,
    }


def _item_from_data(data: dict[str, Any]) -> OrderItem:
    return OrderItem(
        order_item_id=data["order_item_id"],
        menu_item_id=data["menu_item_id"],
        name=data["name"],
        quantity=Decimal(data["quantity"]),
        unit_price=Money(Decimal(data["unit_price"]), data["currency"]),
        destination=Destination(data["destination"]),
        note=data["note"],
    )


def event_to_data(event: OrderingEvent) -> tuple[str, dict[str, Any], datetime]:
    if isinstance(event, OrderSubmitted):
        order = event.order
        return (
            "ORDER_SUBMITTED",
            {
                "order_id": order.order_id,
                "customer_group_id": order.customer_group_id,
                "submitted_by_id": order.submitted_by_id,
                "submitted_at": order.submitted_at.isoformat(),
                "service_location_id": order.service_location_id,
                "responsible_waiter_id": order.responsible_waiter_id,
                "items": [_item_to_data(item) for item in order.items],
            },
            event.occurred_at,
        )
    if isinstance(event, KitchenTicketCreated | BarTicketCreated):
        ticket = event.ticket
        return (
            "KITCHEN_TICKET_CREATED"
            if isinstance(event, KitchenTicketCreated)
            else "BAR_TICKET_CREATED",
            {
                "ticket_id": ticket.ticket_id,
                "order_id": ticket.order_id,
                "customer_group_id": ticket.customer_group_id,
                "service_location_id": ticket.service_location_id,
                "responsible_waiter_id": ticket.responsible_waiter_id,
                "created_at": ticket.created_at.isoformat(),
                "items": [_item_to_data(item) for item in ticket.items],
            },
            event.occurred_at,
        )
    if isinstance(event, FinancialObligationCreated):
        return (
            "FINANCIAL_OBLIGATION_CREATED",
            {
                "obligation_id": event.obligation_id,
                "customer_group_id": event.customer_group_id,
                "order_item_id": event.order_item_id,
                "amount": str(event.amount),
                "currency": event.currency,
            },
            event.occurred_at,
        )
    if isinstance(event, BillCreated):
        return (
            "BILL_CREATED",
            {
                "bill_id": event.bill_id,
                "customer_group_id": event.customer_group_id,
                "currency": event.currency,
            },
            event.occurred_at,
        )
    if isinstance(event, BillLineAdded):
        line = event.line
        return (
            "BILL_LINE_ADDED",
            {
                "bill_id": event.bill_id,
                "bill_line_id": line.bill_line_id,
                "order_item_id": line.order_item_id,
                "description": line.description,
                "quantity": str(line.quantity),
                "unit_price": str(line.unit_price.amount),
                "amount": str(line.amount.amount),
                "currency": line.amount.currency,
            },
            event.occurred_at,
        )
    raise ValueError("unsupported Ordering event")


def event_from_data(event_type: str, data: dict[str, Any], occurred_at: datetime) -> OrderingEvent:
    if event_type == "ORDER_SUBMITTED":
        return OrderSubmitted(
            order=Order(
                order_id=data["order_id"],
                customer_group_id=data["customer_group_id"],
                submitted_by_id=data["submitted_by_id"],
                submitted_at=datetime.fromisoformat(data["submitted_at"]),
                service_location_id=data["service_location_id"],
                responsible_waiter_id=data["responsible_waiter_id"],
                items=tuple(_item_from_data(item) for item in data["items"]),
            ),
            occurred_at=occurred_at,
        )
    if event_type in {"KITCHEN_TICKET_CREATED", "BAR_TICKET_CREATED"}:
        ticket_type = KitchenTicket if event_type == "KITCHEN_TICKET_CREATED" else BarTicket
        ticket = ticket_type(
            ticket_id=data["ticket_id"],
            order_id=data["order_id"],
            customer_group_id=data["customer_group_id"],
            service_location_id=data["service_location_id"],
            responsible_waiter_id=data["responsible_waiter_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            items=tuple(_item_from_data(item) for item in data["items"]),
        )
        if isinstance(ticket, KitchenTicket):
            return KitchenTicketCreated(ticket, occurred_at)
        return BarTicketCreated(ticket, occurred_at)
    if event_type == "FINANCIAL_OBLIGATION_CREATED":
        return FinancialObligationCreated(
            data["obligation_id"],
            data["customer_group_id"],
            data["order_item_id"],
            Decimal(data["amount"]),
            data["currency"],
            occurred_at,
        )
    if event_type == "BILL_CREATED":
        return BillCreated(
            data["bill_id"], data["customer_group_id"], data["currency"], occurred_at
        )
    if event_type == "BILL_LINE_ADDED":
        return BillLineAdded(
            bill_id=data["bill_id"],
            line=BillLine(
                data["bill_line_id"],
                data["order_item_id"],
                data["description"],
                Decimal(data["quantity"]),
                Money(Decimal(data["unit_price"]), data["currency"]),
                Money(Decimal(data["amount"]), data["currency"]),
            ),
            occurred_at=occurred_at,
        )
    raise ValueError(f"unsupported Ordering event type: {event_type}")
