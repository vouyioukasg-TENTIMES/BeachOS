"""Ordering Application results."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from beachos_api.packs.beachos.ordering.domain import (
    BarTicket,
    Bill,
    CustomerGroup,
    KitchenTicket,
    MenuItem,
    Order,
    OrderItem,
)


@dataclass(frozen=True, slots=True)
class MenuItemDTO:
    menu_item_id: str
    name: str
    category_name: str
    unit_price: Decimal
    currency: str
    destination: str

    @classmethod
    def from_domain(cls, item: MenuItem) -> MenuItemDTO:
        return cls(
            item.menu_item_id,
            item.name,
            item.category_name,
            item.price.amount,
            item.price.currency,
            item.destination.value,
        )


@dataclass(frozen=True, slots=True)
class OrderItemDTO:
    order_item_id: str
    menu_item_id: str
    name: str
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    currency: str
    destination: str
    note: str | None

    @classmethod
    def from_domain(cls, item: OrderItem) -> OrderItemDTO:
        return cls(
            item.order_item_id,
            item.menu_item_id,
            item.name,
            item.quantity,
            item.unit_price.amount,
            item.total.amount,
            item.unit_price.currency,
            item.destination.value,
            item.note,
        )


@dataclass(frozen=True, slots=True)
class TicketDTO:
    ticket_id: str
    destination: str
    item_ids: tuple[str, ...]

    @classmethod
    def from_kitchen(cls, ticket: KitchenTicket) -> TicketDTO:
        return cls(ticket.ticket_id, "KITCHEN", tuple(item.order_item_id for item in ticket.items))

    @classmethod
    def from_bar(cls, ticket: BarTicket) -> TicketDTO:
        return cls(ticket.ticket_id, "BAR", tuple(item.order_item_id for item in ticket.items))


@dataclass(frozen=True, slots=True)
class OrderDTO:
    order_id: str
    customer_group_id: str
    submitted_at: datetime
    submitted_by_id: str
    service_location_id: str
    responsible_waiter_id: str
    items: tuple[OrderItemDTO, ...]

    @classmethod
    def from_domain(cls, order: Order) -> OrderDTO:
        return cls(
            order.order_id,
            order.customer_group_id,
            order.submitted_at,
            order.submitted_by_id,
            order.service_location_id,
            order.responsible_waiter_id,
            tuple(OrderItemDTO.from_domain(item) for item in order.items),
        )


@dataclass(frozen=True, slots=True)
class BillDTO:
    bill_id: str
    currency: str
    total: Decimal
    line_count: int

    @classmethod
    def from_domain(cls, bill: Bill) -> BillDTO:
        return cls(bill.bill_id, bill.currency, bill.total, len(bill.lines))


@dataclass(frozen=True, slots=True)
class SubmitOrderResult:
    request_id: str
    order: OrderDTO
    tickets: tuple[TicketDTO, ...]
    bill: BillDTO | None


@dataclass(frozen=True, slots=True)
class OrderingContextResult:
    customer_group_id: str
    venue_id: str
    service_location_id: str
    responsible_waiter_id: str
    status: str
    orders: tuple[OrderDTO, ...]
    bill: BillDTO | None
    menu_items: tuple[MenuItemDTO, ...]

    @classmethod
    def from_domain(
        cls,
        group: CustomerGroup,
        menu_items: tuple[MenuItem, ...],
    ) -> OrderingContextResult:
        return cls(
            group.customer_group_id,
            group.venue_id,
            group.service_location_id,
            group.responsible_waiter_id,
            group.status.value,
            tuple(OrderDTO.from_domain(order) for order in group.orders),
            BillDTO.from_domain(group.bill) if group.bill is not None else None,
            tuple(MenuItemDTO.from_domain(item) for item in menu_items),
        )
