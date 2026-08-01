"""Bar Operations Domain and Application tests."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from beachos_api.composition import bar_service
from beachos_api.main import create_app
from beachos_api.packs.beachos.bar.application import (
    AcknowledgeBarTicketCommand,
    BarService,
    ProgressBarTicketCommand,
)
from beachos_api.packs.beachos.bar.application.exceptions import (
    BarAuthorizationDeniedError,
    BarBusinessRuleRejectedError,
    BarCommandValidationError,
    BarTicketNotFoundError,
)
from beachos_api.packs.beachos.bar.domain import (
    BarError,
    BarTicket,
    BarTicketAcknowledged,
    BarTicketItem,
)

NOW = datetime(2026, 8, 1, 10, tzinfo=UTC)


def ticket() -> BarTicket:
    return BarTicket(
        ticket_id="bar-1",
        order_id="order-1",
        customer_group_id="group-1",
        venue_id="venue-1",
        submission_service_location_id="a12",
        current_service_location_id="a12",
        responsible_service_staff_id="waiter-1",
        submitted_at=NOW,
        items=(BarTicketItem("item-1", "Water", Decimal("2"), None),),
    )


def test_acknowledgement_and_restoration():
    subject = ticket()
    subject.acknowledge(actor_id="bar-staff-1", acknowledged_at=NOW)
    events = subject.pull_events()
    assert events == (BarTicketAcknowledged("bar-1", "bar-staff-1", NOW),)
    restored = BarTicket.restore(
        ticket_id="bar-1",
        order_id="order-1",
        customer_group_id="group-1",
        venue_id="venue-1",
        submission_service_location_id="a12",
        current_service_location_id="a12",
        responsible_service_staff_id="waiter-1",
        submitted_at=NOW,
        items=subject.items,
        events=events,
    )
    assert (
        restored.acknowledged_by_id == "bar-staff-1"
        and restored.version == 1
        and restored.pull_events() == ()
    )


def test_domain_rejects_repeat_and_foreign_event():
    subject = ticket()
    subject.acknowledge(actor_id="staff", acknowledged_at=NOW)
    with pytest.raises(BarError, match="already"):
        subject.acknowledge(actor_id="staff", acknowledged_at=NOW)
    with pytest.raises(BarError, match="another Ticket"):
        BarTicket.restore(
            ticket_id="bar-1",
            order_id="order-1",
            customer_group_id="group-1",
            venue_id="venue-1",
            submission_service_location_id="a12",
            current_service_location_id="a12",
            responsible_service_staff_id="waiter-1",
            submitted_at=NOW,
            items=subject.items,
            events=(BarTicketAcknowledged("wrong", "staff", NOW),),
        )


class Capabilities:
    allowed = True

    def can_acknowledge_bar_ticket(self, **kwargs):
        return self.allowed

    def can_mark_bar_ticket_ready(self, **kwargs):
        return self.allowed

    def can_collect_ticket(self, **kwargs):
        return self.allowed

    def can_deliver_ticket(self, **kwargs):
        return self.allowed


class Clock:
    def now(self):
        return NOW


class Repo:
    def __init__(self, value):
        self.value = value
        self.saved = []

    def get(self, **kwargs):
        return self.value

    def list_for_venue(self, **kwargs):
        return (self.value,) if self.value else ()

    def save(self, value):
        self.saved.append(value)


class Receipts:
    def __init__(self):
        self.values = {}

    def get(self, **kwargs):
        return self.values.get(kwargs["request_id"])

    def save(self, **kwargs):
        self.values[kwargs["request_id"]] = kwargs["result"]


class Unit:
    def __init__(self, value):
        self.tickets = Repo(value)
        self.receipts = Receipts()
        self.commits = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def commit(self):
        self.commits += 1


class Factory:
    def __init__(self, unit):
        self.unit = unit

    def create(self):
        return self.unit


def test_application_context_acknowledgement_and_idempotency():
    unit = Unit(ticket())
    service = BarService(
        capabilities=Capabilities(), clock=Clock(), unit_of_work_factory=Factory(unit)
    )
    assert service.get_context(venue_id="venue-1").awaiting_acknowledgement_count == 1
    command = AcknowledgeBarTicketCommand("request-1", "bar-staff-1", "bar-1")
    first = service.acknowledge(command)
    assert service.acknowledge(command) == first
    assert unit.commits == 1 and first.ticket.status == "ACKNOWLEDGED"


def test_application_preserves_failures_and_validation():
    capabilities = Capabilities()
    capabilities.allowed = False
    denied = BarService(
        capabilities=capabilities, clock=Clock(), unit_of_work_factory=Factory(Unit(ticket()))
    )
    with pytest.raises(BarAuthorizationDeniedError):
        denied.acknowledge(AcknowledgeBarTicketCommand("r", "staff", "bar-1"))
    missing = BarService(
        capabilities=Capabilities(), clock=Clock(), unit_of_work_factory=Factory(Unit(None))
    )
    with pytest.raises(BarTicketNotFoundError):
        missing.acknowledge(AcknowledgeBarTicketCommand("r", "staff", "bar-1"))
    unit = Unit(ticket())
    service = BarService(
        capabilities=Capabilities(), clock=Clock(), unit_of_work_factory=Factory(unit)
    )
    service.acknowledge(AcknowledgeBarTicketCommand("r", "staff", "bar-1"))
    with pytest.raises(BarBusinessRuleRejectedError):
        service.acknowledge(AcknowledgeBarTicketCommand("r", "staff", "bar-2"))
    with pytest.raises(BarCommandValidationError):
        AcknowledgeBarTicketCommand("", "staff", "bar-1")


def test_http_vertical_slice_translates_context_and_command():
    unit = Unit(ticket())
    service = BarService(
        capabilities=Capabilities(), clock=Clock(), unit_of_work_factory=Factory(unit)
    )
    application = create_app()
    application.dependency_overrides[bar_service] = lambda: service
    client = TestClient(application)

    context = client.get("/bar/context", params={"venue_id": "venue-1"})
    acknowledged = client.post(
        "/bar/tickets/bar-1/acknowledge", json={"request_id": "request-http"}
    )

    assert context.status_code == 200
    assert context.json()["tickets"][0]["status"] == "NEW"
    assert acknowledged.status_code == 200
    assert acknowledged.json()["ticket"]["status"] == "ACKNOWLEDGED"


def test_complete_bar_fulfilment_flow_through_api():
    unit = Unit(ticket())
    service = BarService(
        capabilities=Capabilities(), clock=Clock(), unit_of_work_factory=Factory(unit)
    )
    application = create_app()
    application.dependency_overrides[bar_service] = lambda: service
    client = TestClient(application)
    assert (
        client.post("/bar/tickets/bar-1/acknowledge", json={"request_id": "a"}).status_code == 200
    )
    for request_id, action, expected in (
        ("r", "mark_ready", "READY"),
        ("c", "collect", "COLLECTED"),
        ("d", "deliver", "DELIVERED"),
    ):
        response = client.post(f"/bar/tickets/bar-1/{action}", json={"request_id": request_id})
        assert response.status_code == 200 and response.json()["ticket"]["status"] == expected
    assert (
        service.progress(
            ProgressBarTicketCommand("d", "development-host", "bar-1", "deliver")
        ).ticket.status
        == "DELIVERED"
    )
