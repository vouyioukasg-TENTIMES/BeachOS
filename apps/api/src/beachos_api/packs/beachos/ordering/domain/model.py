"""Framework-independent Ordering Domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from beachos_api.packs.beachos.ordering.domain.events import OrderingEvent


class OrderingError(ValueError):
    """An Ordering action violates an approved business rule."""


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise OrderingError(f"{field} is required")
    return normalized


def _optional(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _aware(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise OrderingError(f"{field} must include a timezone")
    return value


class Destination(StrEnum):
    BAR = "BAR"
    KITCHEN = "KITCHEN"
    NO_PREPARATION = "NO PREPARATION"


class CustomerGroupStatus(StrEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal) or not self.amount.is_finite():
            raise OrderingError("money amount must be an exact finite decimal")
        if self.amount < 0:
            raise OrderingError("money amount cannot be negative")
        object.__setattr__(self, "currency", _required(self.currency, "currency").upper())


@dataclass(frozen=True, slots=True)
class MenuItem:
    menu_item_id: str
    name: str
    price: Money
    destination: Destination
    available: bool
    category_name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "menu_item_id", _required(self.menu_item_id, "Menu Item id"))
        object.__setattr__(self, "name", _required(self.name, "Menu Item name"))
        object.__setattr__(
            self, "category_name", _required(self.category_name, "Menu Category name")
        )
        if not isinstance(self.destination, Destination):
            raise OrderingError("preparation destination must be Bar, Kitchen, or No Preparation")


@dataclass(frozen=True, slots=True)
class DraftOrderItem:
    order_item_id: str
    menu_item: MenuItem
    quantity: Decimal
    note: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "order_item_id", _required(self.order_item_id, "Order Item id"))
        if not isinstance(self.quantity, Decimal) or not self.quantity.is_finite():
            raise OrderingError("Order Item quantity must be a finite decimal")
        if self.quantity <= 0:
            raise OrderingError("Order Item quantity must be greater than zero")
        if not self.menu_item.available:
            raise OrderingError(f"{self.menu_item.name} is not currently available")
        object.__setattr__(self, "note", _optional(self.note))


@dataclass(frozen=True, slots=True)
class OrderItem:
    order_item_id: str
    menu_item_id: str
    name: str
    quantity: Decimal
    unit_price: Money
    destination: Destination
    note: str | None

    @property
    def total(self) -> Money:
        return Money(self.quantity * self.unit_price.amount, self.unit_price.currency)


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    customer_group_id: str
    submitted_by_id: str
    submitted_at: datetime
    service_location_id: str
    responsible_waiter_id: str
    items: tuple[OrderItem, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "order_id", _required(self.order_id, "Order id"))
        object.__setattr__(
            self, "customer_group_id", _required(self.customer_group_id, "Customer Group id")
        )
        object.__setattr__(
            self, "submitted_by_id", _required(self.submitted_by_id, "submitting Staff Member id")
        )
        object.__setattr__(
            self, "service_location_id", _required(self.service_location_id, "Service Location id")
        )
        object.__setattr__(
            self,
            "responsible_waiter_id",
            _required(self.responsible_waiter_id, "Responsible Waiter id"),
        )
        object.__setattr__(self, "submitted_at", _aware(self.submitted_at, "submission time"))
        if not self.items:
            raise OrderingError("an Order requires at least one Order Item")
        currencies = {item.unit_price.currency for item in self.items}
        if len(currencies) != 1:
            raise OrderingError("all Order Items must use one currency")


@dataclass(frozen=True, slots=True)
class KitchenTicket:
    ticket_id: str
    order_id: str
    customer_group_id: str
    service_location_id: str
    responsible_waiter_id: str
    created_at: datetime
    items: tuple[OrderItem, ...]


@dataclass(frozen=True, slots=True)
class BarTicket:
    ticket_id: str
    order_id: str
    customer_group_id: str
    service_location_id: str
    responsible_waiter_id: str
    created_at: datetime
    items: tuple[OrderItem, ...]


@dataclass(frozen=True, slots=True)
class BillLine:
    bill_line_id: str
    order_item_id: str | None
    description: str
    quantity: Decimal
    unit_price: Money
    amount: Money


@dataclass(frozen=True, slots=True)
class Bill:
    bill_id: str
    customer_group_id: str
    currency: str
    lines: tuple[BillLine, ...] = ()

    @property
    def total(self) -> Decimal:
        return sum((line.amount.amount for line in self.lines), Decimal("0"))


class CustomerGroup:
    """Event-sourced ordering boundary for one approved Customer Group."""

    def __init__(
        self,
        *,
        customer_group_id: str,
        venue_id: str,
        service_location_id: str,
        responsible_waiter_id: str,
        status: CustomerGroupStatus,
    ) -> None:
        self._customer_group_id = _required(customer_group_id, "Customer Group id")
        self._venue_id = _required(venue_id, "Venue id")
        self._service_location_id = _required(service_location_id, "Service Location id")
        self._responsible_waiter_id = _required(responsible_waiter_id, "Responsible Waiter id")
        if not isinstance(status, CustomerGroupStatus):
            raise OrderingError("Customer Group status must be ACTIVE or COMPLETED")
        self._status = status
        self._orders: list[Order] = []
        self._kitchen_tickets: list[KitchenTicket] = []
        self._bar_tickets: list[BarTicket] = []
        self._bill: Bill | None = None
        self._version = 0
        self._pending_events: list[OrderingEvent] = []

    @classmethod
    def restore(
        cls,
        *,
        customer_group_id: str,
        venue_id: str,
        service_location_id: str,
        responsible_waiter_id: str,
        status: CustomerGroupStatus,
        events: tuple[OrderingEvent, ...],
    ) -> CustomerGroup:
        group = cls(
            customer_group_id=customer_group_id,
            venue_id=venue_id,
            service_location_id=service_location_id,
            responsible_waiter_id=responsible_waiter_id,
            status=status,
        )
        for event in events:
            group._apply(event)
            group._version += 1
        return group

    def submit_order(
        self,
        *,
        order_id: str,
        submitted_by_id: str,
        submitted_at: datetime,
        draft_items: tuple[DraftOrderItem, ...],
        kitchen_ticket_id: str | None,
        bar_ticket_id: str | None,
        bill_id: str,
        obligation_ids: tuple[str, ...],
        bill_line_ids: tuple[str, ...],
    ) -> Order:
        from beachos_api.packs.beachos.ordering.domain.events import (
            BarTicketCreated,
            BillCreated,
            BillLineAdded,
            FinancialObligationCreated,
            KitchenTicketCreated,
            OrderSubmitted,
        )

        if self._status is not CustomerGroupStatus.ACTIVE:
            raise OrderingError("a Completed Customer Group cannot receive a new Order")
        if not draft_items:
            raise OrderingError("an Order requires at least one Order Item")

        order_items = tuple(
            OrderItem(
                order_item_id=item.order_item_id,
                menu_item_id=item.menu_item.menu_item_id,
                name=item.menu_item.name,
                quantity=item.quantity,
                unit_price=item.menu_item.price,
                destination=item.menu_item.destination,
                note=item.note,
            )
            for item in draft_items
        )
        order = Order(
            order_id=order_id,
            customer_group_id=self._customer_group_id,
            submitted_by_id=submitted_by_id,
            submitted_at=submitted_at,
            service_location_id=self._service_location_id,
            responsible_waiter_id=self._responsible_waiter_id,
            items=order_items,
        )
        if any(existing.order_id == order.order_id for existing in self._orders):
            raise OrderingError("Order id must be unique within the Customer Group")
        positive_items = tuple(item for item in order.items if item.total.amount > 0)
        if len(obligation_ids) != len(positive_items) or len(bill_line_ids) != len(positive_items):
            raise OrderingError("every positive Order Item requires one financial identity")
        if self._bill is not None and any(
            item.unit_price.currency != self._bill.currency for item in positive_items
        ):
            raise OrderingError("Order currency must match the Customer Group Bill")

        self._record(OrderSubmitted(order=order, occurred_at=submitted_at))

        kitchen_items = tuple(
            item for item in order.items if item.destination is Destination.KITCHEN
        )
        if kitchen_items:
            if kitchen_ticket_id is None:
                raise OrderingError("Kitchen work requires a Kitchen Ticket id")
            self._record(
                KitchenTicketCreated(
                    ticket=KitchenTicket(
                        ticket_id=_required(kitchen_ticket_id, "Kitchen Ticket id"),
                        order_id=order.order_id,
                        customer_group_id=self._customer_group_id,
                        service_location_id=self._service_location_id,
                        responsible_waiter_id=self._responsible_waiter_id,
                        created_at=submitted_at,
                        items=kitchen_items,
                    ),
                    occurred_at=submitted_at,
                )
            )
        elif kitchen_ticket_id is not None:
            raise OrderingError("an Order without Kitchen items cannot create a Kitchen Ticket")

        bar_items = tuple(item for item in order.items if item.destination is Destination.BAR)
        if bar_items:
            if bar_ticket_id is None:
                raise OrderingError("Bar work requires a Bar Ticket id")
            self._record(
                BarTicketCreated(
                    ticket=BarTicket(
                        ticket_id=_required(bar_ticket_id, "Bar Ticket id"),
                        order_id=order.order_id,
                        customer_group_id=self._customer_group_id,
                        service_location_id=self._service_location_id,
                        responsible_waiter_id=self._responsible_waiter_id,
                        created_at=submitted_at,
                        items=bar_items,
                    ),
                    occurred_at=submitted_at,
                )
            )
        elif bar_ticket_id is not None:
            raise OrderingError("an Order without Bar items cannot create a Bar Ticket")

        if positive_items and self._bill is None:
            currency = positive_items[0].unit_price.currency
            self._record(
                BillCreated(
                    bill_id=_required(bill_id, "Bill id"),
                    customer_group_id=self._customer_group_id,
                    currency=currency,
                    occurred_at=submitted_at,
                )
            )

        for index, item in enumerate(positive_items):
            total = item.total
            current_bill = self._bill
            if current_bill is None:
                raise OrderingError("a positive Financial Obligation requires a Bill")
            if current_bill.currency != total.currency:
                raise OrderingError("Order currency must match the Customer Group Bill")
            self._record(
                FinancialObligationCreated(
                    obligation_id=_required(obligation_ids[index], "Financial Obligation id"),
                    customer_group_id=self._customer_group_id,
                    order_item_id=item.order_item_id,
                    amount=total.amount,
                    currency=total.currency,
                    occurred_at=submitted_at,
                )
            )
            self._record(
                BillLineAdded(
                    bill_id=current_bill.bill_id,
                    line=BillLine(
                        bill_line_id=_required(bill_line_ids[index], "Bill Line id"),
                        order_item_id=item.order_item_id,
                        description=item.name,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                        amount=total,
                    ),
                    occurred_at=submitted_at,
                )
            )
        return order

    def _record(self, event: OrderingEvent) -> None:
        self._apply(event)
        self._pending_events.append(event)
        self._version += 1

    def _apply(self, event: OrderingEvent) -> None:
        from beachos_api.packs.beachos.ordering.domain.events import (
            BarTicketCreated,
            BillCreated,
            BillLineAdded,
            FinancialObligationCreated,
            KitchenTicketCreated,
            OrderSubmitted,
        )

        if isinstance(event, OrderSubmitted):
            self._orders.append(event.order)
        elif isinstance(event, KitchenTicketCreated):
            self._kitchen_tickets.append(event.ticket)
        elif isinstance(event, BarTicketCreated):
            self._bar_tickets.append(event.ticket)
        elif isinstance(event, BillCreated):
            if self._bill is not None:
                raise OrderingError("a Customer Group may have only one Bill")
            self._bill = Bill(event.bill_id, event.customer_group_id, event.currency)
        elif isinstance(event, BillLineAdded):
            if self._bill is None or self._bill.bill_id != event.bill_id:
                raise OrderingError("Bill Line must belong to the Customer Group Bill")
            self._bill = Bill(
                self._bill.bill_id,
                self._bill.customer_group_id,
                self._bill.currency,
                (*self._bill.lines, event.line),
            )
        elif isinstance(event, FinancialObligationCreated):
            return
        else:
            raise OrderingError("unsupported Ordering event")

    def pull_events(self) -> tuple[OrderingEvent, ...]:
        events = tuple(self._pending_events)
        self._pending_events.clear()
        return events

    @property
    def customer_group_id(self) -> str:
        return self._customer_group_id

    @property
    def venue_id(self) -> str:
        return self._venue_id

    @property
    def service_location_id(self) -> str:
        return self._service_location_id

    @property
    def responsible_waiter_id(self) -> str:
        return self._responsible_waiter_id

    @property
    def status(self) -> CustomerGroupStatus:
        return self._status

    @property
    def orders(self) -> tuple[Order, ...]:
        return tuple(self._orders)

    @property
    def kitchen_tickets(self) -> tuple[KitchenTicket, ...]:
        return tuple(self._kitchen_tickets)

    @property
    def bar_tickets(self) -> tuple[BarTicket, ...]:
        return tuple(self._bar_tickets)

    @property
    def bill(self) -> Bill | None:
        return self._bill

    @property
    def version(self) -> int:
        return self._version
