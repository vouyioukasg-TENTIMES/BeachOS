"""Kitchen Domain and Application behavior."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from beachos_api.packs.beachos.kitchen.application import (
    AcknowledgeKitchenTicketCommand,
    KitchenService,
    ProgressKitchenTicketCommand,
)
from beachos_api.packs.beachos.kitchen.application.exceptions import (
    KitchenAuthorizationDeniedError,
    KitchenBusinessRuleRejectedError,
    KitchenTicketNotFoundError,
)
from beachos_api.packs.beachos.kitchen.domain import (
    KitchenError,
    KitchenTicket,
    KitchenTicketAcknowledged,
    KitchenTicketCollected,
    KitchenTicketDelivered,
    KitchenTicketItem,
    KitchenTicketReady,
)

NOW = datetime(2026, 7, 26, 13, tzinfo=UTC)


def ticket() -> KitchenTicket:
    return KitchenTicket(
        ticket_id="kitchen-1",
        order_id="order-1",
        customer_group_id="group-1",
        venue_id="venue-1",
        submission_service_location_id="B-12",
        current_service_location_id="B-12",
        responsible_service_staff_id="waiter-1",
        submitted_at=NOW,
        items=(KitchenTicketItem("item-1", "Salad", Decimal("2"), " no salt "),),
    )


def test_acknowledgement_is_the_only_event_and_replays_without_new_events() -> None:
    target = ticket()
    target.acknowledge(actor_id="kitchen-staff-1", acknowledged_at=NOW)
    events = target.pull_events()
    assert events == (KitchenTicketAcknowledged("kitchen-1", "kitchen-staff-1", NOW),)
    restored = KitchenTicket.restore(
        ticket_id=target.ticket_id,
        order_id=target.order_id,
        customer_group_id=target.customer_group_id,
        venue_id=target.venue_id,
        submission_service_location_id=target.submission_service_location_id,
        current_service_location_id=target.current_service_location_id,
        responsible_service_staff_id=target.responsible_service_staff_id,
        submitted_at=target.submitted_at,
        items=target.items,
        events=events,
    )
    assert restored.acknowledged_by_id == "kitchen-staff-1"
    assert restored.version == 1
    assert restored.pull_events() == ()


def test_repeated_acknowledgement_is_forbidden() -> None:
    target = ticket()
    target.acknowledge(actor_id="staff", acknowledged_at=NOW)
    with pytest.raises(KitchenError, match="already"):
        target.acknowledge(actor_id="staff", acknowledged_at=NOW)


@pytest.mark.parametrize(
    "action",
    [
        lambda: KitchenTicketItem("", "Salad", Decimal("1"), None),
        lambda: KitchenTicketItem("item", "Salad", Decimal("0"), None),
        lambda: KitchenTicket(
            ticket_id="ticket",
            order_id="order",
            customer_group_id="group",
            venue_id="venue",
            submission_service_location_id="B-1",
            current_service_location_id="B-1",
            responsible_service_staff_id="staff",
            submitted_at=NOW,
            items=(),
        ),
    ],
)
def test_invalid_source_work_is_rejected(action) -> None:
    with pytest.raises(KitchenError):
        action()


class FakeClock:
    def now(self):
        return NOW


class Authority:
    def __init__(self, allowed: bool = True) -> None:
        self.allowed = allowed

    def can_acknowledge_kitchen_ticket(self, **kwargs):
        del kwargs
        return self.allowed

    def can_mark_kitchen_ticket_ready(self, **kwargs):
        return self.allowed

    def can_collect_ticket(self, **kwargs):
        return self.allowed

    def can_deliver_ticket(self, **kwargs):
        return self.allowed


class Tickets:
    def __init__(self, value):
        self.value = value
        self.saved = False

    def get(self, **kwargs):
        del kwargs
        return self.value

    def list_for_venue(self, **kwargs):
        del kwargs
        return (self.value,) if self.value else ()

    def save(self, value):
        assert value is self.value
        self.saved = True


class Receipts:
    def __init__(self):
        self.values = {}

    def get(self, **kwargs):
        return self.values.get(kwargs["request_id"])

    def save(self, **kwargs):
        self.values[kwargs["request_id"]] = kwargs["result"]


class Unit:
    def __init__(self, value):
        self.tickets = Tickets(value)
        self.receipts = Receipts()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        del args

    def commit(self):
        self.committed = True


class Factory:
    def __init__(self, unit):
        self.unit = unit

    def create(self):
        return self.unit


def service(unit: Unit, allowed: bool = True) -> KitchenService:
    return KitchenService(
        capabilities=Authority(allowed),
        clock=FakeClock(),
        unit_of_work_factory=Factory(unit),
    )


def test_application_lists_acknowledges_and_safely_retries() -> None:
    unit = Unit(ticket())
    application = service(unit)
    assert application.get_context(venue_id="venue-1").awaiting_acknowledgement_count == 1
    command = AcknowledgeKitchenTicketCommand("request-1", "staff-1", "kitchen-1")
    first = application.acknowledge(command)
    assert application.acknowledge(command) == first
    assert unit.tickets.saved and unit.committed


def test_application_rejects_missing_unauthorized_and_repeated_work() -> None:
    command = AcknowledgeKitchenTicketCommand("request-1", "staff-1", "kitchen-1")
    with pytest.raises(KitchenTicketNotFoundError):
        service(Unit(None)).acknowledge(command)
    with pytest.raises(KitchenAuthorizationDeniedError):
        service(Unit(ticket()), False).acknowledge(command)
    acknowledged = ticket()
    acknowledged.acknowledge(actor_id="other", acknowledged_at=NOW)
    acknowledged.pull_events()
    with pytest.raises(KitchenBusinessRuleRejectedError):
        service(Unit(acknowledged)).acknowledge(command)


def test_complete_kitchen_fulfilment_lifecycle_and_replay() -> None:
    target = ticket()
    target.acknowledge(actor_id="kitchen", acknowledged_at=NOW)
    target.mark_ready(actor_id="kitchen", confirmed_at=NOW)
    target.collect(actor_id="runner", collected_at=NOW)
    target.deliver(actor_id="waiter", delivered_at=NOW)
    events = target.pull_events()
    assert [type(event) for event in events] == [
        KitchenTicketAcknowledged,
        KitchenTicketReady,
        KitchenTicketCollected,
        KitchenTicketDelivered,
    ]
    restored = KitchenTicket.restore(
        ticket_id=target.ticket_id,
        order_id=target.order_id,
        customer_group_id=target.customer_group_id,
        venue_id=target.venue_id,
        submission_service_location_id=target.submission_service_location_id,
        current_service_location_id=target.current_service_location_id,
        responsible_service_staff_id=target.responsible_service_staff_id,
        submitted_at=target.submitted_at,
        items=target.items,
        events=events,
    )
    assert restored.delivered_by_id == "waiter" and restored.pull_events() == ()


def test_application_progress_is_sequential_and_idempotent() -> None:
    unit = Unit(ticket())
    application = service(unit)
    application.acknowledge(AcknowledgeKitchenTicketCommand("a", "staff", "kitchen-1"))
    ready = ProgressKitchenTicketCommand("r", "staff", "kitchen-1", "mark_ready")
    assert application.progress(ready).ticket.status == "READY"
    assert application.progress(ready).ticket.status == "READY"
    assert (
        application.progress(
            ProgressKitchenTicketCommand("c", "runner", "kitchen-1", "collect")
        ).ticket.status
        == "COLLECTED"
    )
    assert (
        application.progress(
            ProgressKitchenTicketCommand("d", "waiter", "kitchen-1", "deliver")
        ).ticket.status
        == "DELIVERED"
    )
