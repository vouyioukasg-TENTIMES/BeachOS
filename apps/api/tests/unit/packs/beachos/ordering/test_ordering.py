"""Ordering Domain and Application behavior."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from beachos_api.packs.beachos.ordering.application import (
    OrderingService,
    SubmitOrderCommand,
    SubmitOrderItem,
)
from beachos_api.packs.beachos.ordering.application.exceptions import (
    OrderingAuthorizationDeniedError,
    OrderingBusinessRuleRejectedError,
)
from beachos_api.packs.beachos.ordering.domain import (
    BarTicketCreated,
    BillCreated,
    CustomerGroup,
    CustomerGroupStatus,
    Destination,
    DraftOrderItem,
    FinancialObligationCreated,
    KitchenTicketCreated,
    MenuItem,
    Money,
    OrderingError,
    OrderSubmitted,
)

NOW = datetime(2026, 7, 26, 12, tzinfo=UTC)


def menu_item(item_id: str, destination: Destination, price: str = "5.00") -> MenuItem:
    return MenuItem(
        item_id,
        item_id.title(),
        Money(Decimal(price), "eur"),
        destination,
        True,
        "Menu",
    )


def group(status: CustomerGroupStatus = CustomerGroupStatus.ACTIVE) -> CustomerGroup:
    return CustomerGroup(
        customer_group_id="group-1",
        venue_id="venue-1",
        service_location_id="B-12",
        responsible_waiter_id="waiter-1",
        status=status,
    )


def submit(target: CustomerGroup, items: tuple[DraftOrderItem, ...] | None = None):
    return target.submit_order(
        order_id="order-1",
        submitted_by_id="staff-1",
        submitted_at=NOW,
        draft_items=items
        or (
            DraftOrderItem("item-1", menu_item("coffee", Destination.BAR), Decimal("2")),
            DraftOrderItem(
                "item-2", menu_item("salad", Destination.KITCHEN), Decimal("1"), " no salt "
            ),
        ),
        kitchen_ticket_id="kitchen-1",
        bar_ticket_id="bar-1",
        bill_id="bill-1",
        obligation_ids=("obligation-1", "obligation-2"),
        bill_line_ids=("line-1", "line-2"),
    )


def test_submission_is_an_immutable_round_with_routing_bill_and_context() -> None:
    target = group()
    order = submit(target)
    events = target.pull_events()

    assert order.service_location_id == "B-12"
    assert order.responsible_waiter_id == "waiter-1"
    assert order.items[1].note == "no salt"
    assert target.bill is not None and target.bill.total == Decimal("15.00")
    assert [type(event) for event in events].count(OrderSubmitted) == 1
    assert any(isinstance(event, KitchenTicketCreated) for event in events)
    assert any(isinstance(event, BarTicketCreated) for event in events)
    assert any(isinstance(event, BillCreated) for event in events)
    assert len([event for event in events if isinstance(event, FinancialObligationCreated)]) == 2

    restored = CustomerGroup.restore(
        customer_group_id="group-1",
        venue_id="venue-1",
        service_location_id="B-12",
        responsible_waiter_id="waiter-1",
        status=CustomerGroupStatus.ACTIVE,
        events=events,
    )
    assert restored.orders == target.orders
    assert restored.bill == target.bill
    assert restored.version == len(events)
    assert restored.pull_events() == ()


def test_no_preparation_and_free_item_create_neither_ticket_nor_bill() -> None:
    target = group()
    item = DraftOrderItem(
        "item-free",
        menu_item("water", Destination.NO_PREPARATION, "0"),
        Decimal("1"),
    )
    target.submit_order(
        order_id="order-free",
        submitted_by_id="staff-1",
        submitted_at=NOW,
        draft_items=(item,),
        kitchen_ticket_id=None,
        bar_ticket_id=None,
        bill_id="",
        obligation_ids=(),
        bill_line_ids=(),
    )
    assert target.bill is None
    assert target.kitchen_tickets == ()
    assert target.bar_tickets == ()


@pytest.mark.parametrize(
    "action",
    [
        lambda: submit(group(CustomerGroupStatus.COMPLETED)),
        lambda: group().submit_order(
            order_id="order",
            submitted_by_id="staff",
            submitted_at=NOW,
            draft_items=(),
            kitchen_ticket_id=None,
            bar_ticket_id=None,
            bill_id="",
            obligation_ids=(),
            bill_line_ids=(),
        ),
        lambda: DraftOrderItem(
            "item",
            MenuItem(
                "x",
                "X",
                Money(Decimal("1"), "EUR"),
                Destination.BAR,
                False,
                "Menu",
            ),
            Decimal("1"),
        ),
        lambda: DraftOrderItem("item", menu_item("x", Destination.BAR), Decimal("0")),
    ],
)
def test_invalid_ordering_actions_are_rejected(action) -> None:
    with pytest.raises(OrderingError):
        action()


class FakeClock:
    def now(self):
        return NOW


class FakeIds:
    def __init__(self) -> None:
        self.count = 0

    def new_id(self, purpose: str) -> str:
        self.count += 1
        return f"{purpose}-{self.count}"


class FakeAuthority:
    def __init__(self, allowed: bool = True) -> None:
        self.allowed = allowed

    def can_submit_order(self, **kwargs) -> bool:
        del kwargs
        return self.allowed


class FakeGroups:
    def __init__(self, value: CustomerGroup | None) -> None:
        self.value = value
        self.saved = False

    def get(self, **kwargs):
        del kwargs
        return self.value

    def save(self, value):
        assert value is self.value
        self.saved = True


class FakeMenus:
    def available_for_venue(self, **kwargs):
        del kwargs
        return (menu_item("coffee", Destination.BAR),)


class FakeReceipts:
    def __init__(self):
        self.value = None

    def get(self, **kwargs):
        del kwargs
        return self.value

    def save(self, **kwargs):
        self.value = kwargs["result"]


class FakeUnitOfWork:
    def __init__(self, value):
        self.customer_groups = FakeGroups(value)
        self.menus = FakeMenus()
        self.receipts = FakeReceipts()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        del args

    def commit(self):
        self.committed = True


class FakeFactory:
    def __init__(self, unit):
        self.unit = unit

    def create(self):
        return self.unit


def test_application_orchestrates_submission_and_idempotent_retry() -> None:
    unit = FakeUnitOfWork(group())
    service = OrderingService(
        capabilities=FakeAuthority(),
        clock=FakeClock(),
        identities=FakeIds(),
        unit_of_work_factory=FakeFactory(unit),
    )
    command = SubmitOrderCommand(
        "request-1", "staff-1", "group-1", (SubmitOrderItem("coffee", Decimal("1")),)
    )
    first = service.submit_order(command)
    second = service.submit_order(command)
    assert first == second
    assert unit.customer_groups.saved and unit.committed


def test_application_rejects_missing_authority_and_unavailable_item() -> None:
    command = SubmitOrderCommand(
        "request-1", "staff-1", "group-1", (SubmitOrderItem("missing", Decimal("1")),)
    )
    denied = OrderingService(
        capabilities=FakeAuthority(False),
        clock=FakeClock(),
        identities=FakeIds(),
        unit_of_work_factory=FakeFactory(FakeUnitOfWork(group())),
    )
    with pytest.raises(OrderingAuthorizationDeniedError):
        denied.submit_order(command)
    service = OrderingService(
        capabilities=FakeAuthority(),
        clock=FakeClock(),
        identities=FakeIds(),
        unit_of_work_factory=FakeFactory(FakeUnitOfWork(group())),
    )
    with pytest.raises(OrderingBusinessRuleRejectedError):
        service.submit_order(command)
