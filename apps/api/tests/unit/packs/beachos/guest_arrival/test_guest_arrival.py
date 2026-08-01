"""Guest Arrival Domain and Application tests."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from beachos_api.packs.beachos.guest_arrival.application import (
    GuestArrivalService,
    OpenCustomerGroupCommand,
)
from beachos_api.packs.beachos.guest_arrival.application.exceptions import (
    GuestArrivalAuthorizationError,
    GuestArrivalBusinessRuleError,
    GuestArrivalNotFoundError,
    GuestArrivalValidationError,
)
from beachos_api.packs.beachos.guest_arrival.domain import (
    BillCreated,
    BillLineAdded,
    CustomerGroupOpened,
    FinancialObligationCreated,
    GuestArrivalError,
    Money,
    ResponsibleWaiterAssigned,
    ServiceLocation,
    ServiceLocationStatus,
    ServiceLocationType,
)

NOW = datetime(2026, 8, 1, 9, tzinfo=UTC)


def location(kind=ServiceLocationType.BEACH_SUNBED, status=ServiceLocationStatus.AVAILABLE):
    return ServiceLocation(
        service_location_id="a12",
        venue_id="venue-1",
        visible_name="Beach A12",
        digital_identity="loc-a12",
        location_type=kind,
        status=status,
        beach_sunbed_charge=Money(Decimal("20"), "EUR")
        if kind is ServiceLocationType.BEACH_SUNBED
        else None,
        charge_description="Beach Row 1 sunbed charge"
        if kind is ServiceLocationType.BEACH_SUNBED
        else None,
    )


def open_group(subject, **changes):
    values = dict(
        customer_group_id="group-1",
        responsible_waiter_id="staff-waiter-1",
        opened_by_id="staff-waiter-1",
        opened_at=NOW,
        venue_is_open=True,
        waiter_is_eligible=True,
        waiter_has_capability=True,
        waiter_accepts_responsibility=True,
        physical_context_confirmed=True,
        opening_charge_confirmed=True,
        obligation_id="obligation-1",
        bill_id="bill-1",
        bill_line_id="line-1",
    )
    values.update(changes)
    return subject.open_customer_group(**values)


def test_beach_sunbed_opening_is_one_complete_event_sourced_outcome():
    subject = location()
    group = open_group(subject)
    events = subject.pull_events()
    assert [type(event) for event in events] == [
        ResponsibleWaiterAssigned,
        CustomerGroupOpened,
        FinancialObligationCreated,
        BillCreated,
        BillLineAdded,
    ]
    assert group.bill_id == "bill-1"
    assert group.opening_obligation == Money(Decimal("20"), "EUR")
    assert subject.status is ServiceLocationStatus.OCCUPIED
    assert subject.version == 5
    restored = ServiceLocation.restore(
        service_location_id="a12",
        venue_id="venue-1",
        visible_name="Beach A12",
        digital_identity="loc-a12",
        location_type=ServiceLocationType.BEACH_SUNBED,
        initial_status=ServiceLocationStatus.AVAILABLE,
        beach_sunbed_charge=Money(Decimal("20"), "EUR"),
        charge_description="Beach Row 1 sunbed charge",
        events=events,
    )
    assert restored.active_customer_group == group
    assert restored.pull_events() == ()


def test_non_beach_location_opens_without_financial_events():
    subject = location(ServiceLocationType.UPPER_TABLE)
    group = open_group(
        subject, opening_charge_confirmed=False, obligation_id=None, bill_id=None, bill_line_id=None
    )
    assert group.bill_id is None
    assert [type(event) for event in subject.pull_events()] == [
        ResponsibleWaiterAssigned,
        CustomerGroupOpened,
    ]


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"venue_is_open": False}, "Venue must be open"),
        ({"physical_context_confirmed": False}, "physical and digital"),
        ({"waiter_accepts_responsibility": False}, "accept responsibility"),
        ({"waiter_is_eligible": False}, "not eligible"),
        ({"opened_by_id": "host-1"}, "only the Responsible Waiter"),
        ({"opening_charge_confirmed": False}, "confirm the Beach Sunbed charge"),
    ],
)
def test_opening_rejects_every_approved_blocker(changes, message):
    subject = location()
    with pytest.raises(GuestArrivalError, match=message):
        open_group(subject, **changes)
    assert subject.status is ServiceLocationStatus.AVAILABLE
    assert subject.history == ()


@pytest.mark.parametrize(
    "status",
    [
        ServiceLocationStatus.OCCUPIED,
        ServiceLocationStatus.UNAVAILABLE,
        ServiceLocationStatus.RETIRED,
    ],
)
def test_unavailable_location_cannot_open(status):
    with pytest.raises(GuestArrivalError, match="not available"):
        open_group(location(status=status))


def test_opening_cannot_be_repeated():
    subject = location()
    open_group(subject)
    with pytest.raises(GuestArrivalError, match="not available"):
        open_group(subject, customer_group_id="group-2")


@pytest.mark.parametrize(
    "factory",
    [
        lambda: Money(Decimal("NaN"), "EUR"),
        lambda: Money(Decimal("-1"), "EUR"),
        lambda: Money(Decimal("1"), " "),
        lambda: ServiceLocation(
            service_location_id="",
            venue_id="v",
            visible_name="A",
            digital_identity="d",
            location_type=ServiceLocationType.OTHER,
        ),
        lambda: ServiceLocation(
            service_location_id="a",
            venue_id="v",
            visible_name="A",
            digital_identity="d",
            location_type="TABLE",
        ),
    ],
)
def test_value_objects_and_location_identity_reject_invalid_structure(factory):
    with pytest.raises(GuestArrivalError):
        factory()


def test_non_beach_location_cannot_create_opening_finance():
    with pytest.raises(GuestArrivalError, match="cannot create a Bill"):
        open_group(location(ServiceLocationType.UPPER_TABLE), opening_charge_confirmed=False)


def test_beach_opening_requires_configured_obligation():
    subject = ServiceLocation(
        service_location_id="a12",
        venue_id="venue-1",
        visible_name="A12",
        digital_identity="loc-a12",
        location_type=ServiceLocationType.BEACH_SUNBED,
    )
    with pytest.raises(GuestArrivalError, match="obligation cannot be confirmed"):
        open_group(subject)


def test_restoration_rejects_impossible_event_sequences():
    wrong = CustomerGroupOpened("group", "venue-1", "other", "waiter", NOW)
    values = dict(
        service_location_id="a12",
        venue_id="venue-1",
        visible_name="A12",
        digital_identity="d",
        location_type=ServiceLocationType.UPPER_TABLE,
        initial_status=ServiceLocationStatus.AVAILABLE,
        beach_sunbed_charge=None,
        charge_description=None,
    )
    with pytest.raises(GuestArrivalError, match="another Service Location"):
        ServiceLocation.restore(**values, events=(wrong,))
    with pytest.raises(GuestArrivalError, match="Bill must belong"):
        ServiceLocation.restore(**values, events=(BillCreated("bill", "group", "EUR", NOW),))


class Authority:
    allowed = True

    def can_view_arrival(self, **kwargs):
        return self.allowed

    def can_open_customer_group(self, **kwargs):
        return self.allowed

    def is_eligible_responsible_waiter(self, **kwargs):
        return self.allowed


class Clock:
    def now(self):
        return NOW


class Ids:
    count = 0

    def new_id(self, prefix):
        self.count += 1
        return f"{prefix}-{self.count}"


class Opening:
    value = ("Emerald", "2026-08-01", True)

    def current(self, **kwargs):
        return self.value


class Locations:
    def __init__(self, item):
        self.item = item
        self.saved = []

    def list_for_venue(self, **kwargs):
        return (self.item,)

    def get(self, **kwargs):
        return self.item

    def get_by_digital_identity(self, **kwargs):
        return self.item if kwargs["digital_identity"] == "loc-a12" else None

    def save(self, item):
        self.saved.append(item)


class Receipts:
    value = None

    def get(self, **kwargs):
        return self.value

    def save(self, **kwargs):
        self.value = kwargs["result"]


class Recorder:
    def __init__(self):
        self.values = []

    def provision(self, item):
        self.values.append(item)

    def record_customer_group_opened(self, item):
        self.values.append(item)


class Unit:
    def __init__(self, item):
        self.locations = Locations(item)
        self.receipts = Receipts()
        self.ordering = Recorder()
        self.activity_log = Recorder()
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


def service(item=None, authority=None, opening=None):
    unit = Unit(item or location())
    return GuestArrivalService(
        authority=authority or Authority(),
        clock=Clock(),
        identities=Ids(),
        venue_opening=opening or Opening(),
        unit_of_work_factory=Factory(unit),
    ), unit


def test_application_exposes_context_and_identification_without_mutation():
    subject, unit = service()
    context = subject.get_context(actor_id="host", venue_id="venue-1")
    identified = subject.identify(actor_id="host", venue_id="venue-1", digital_identity=" loc-a12 ")
    assert context.venue_open is True
    assert context.operational_confidence == "CONFIRMED"
    assert identified.visible_name == "Beach A12"
    assert unit.locations.saved == []


def test_application_opens_atomically_and_retries_from_receipt():
    subject, unit = service()
    command = OpenCustomerGroupCommand(
        "request-1", "staff-waiter-1", "venue-1", "a12", True, True, True
    )
    first = subject.open_customer_group(command)
    second = subject.open_customer_group(command)
    assert second == first
    assert unit.commits == 1
    assert len(unit.locations.saved) == 1
    assert len(unit.ordering.values) == 1
    assert len(unit.activity_log.values) == 1


def test_application_preserves_authority_and_venue_uncertainty():
    denied = Authority()
    denied.allowed = False
    subject, _ = service(authority=denied)
    with pytest.raises(GuestArrivalAuthorizationError):
        subject.get_context(actor_id="host", venue_id="venue-1")
    closed = Opening()
    closed.value = ("Emerald", "2026-08-01", False)
    subject, _ = service(opening=closed)
    with pytest.raises(GuestArrivalBusinessRuleError, match="Venue must be open"):
        subject.open_customer_group(
            OpenCustomerGroupCommand("r", "staff-waiter-1", "venue-1", "a12", True, True, True)
        )


def test_application_reports_missing_contexts():
    no_venue = Opening()
    no_venue.value = None
    subject, _ = service(opening=no_venue)
    with pytest.raises(GuestArrivalNotFoundError):
        subject.get_context(actor_id="host", venue_id="venue-1")
    subject, unit = service()
    with pytest.raises(GuestArrivalNotFoundError):
        subject.identify(actor_id="host", venue_id="venue-1", digital_identity="missing")
    unit.locations.item = None
    with pytest.raises(GuestArrivalNotFoundError):
        subject.open_customer_group(
            OpenCustomerGroupCommand("r", "staff-waiter-1", "venue-1", "a12", True, True, True)
        )


def test_application_rejects_unauthorized_actions_and_receipt_reuse():
    denied = Authority()
    denied.allowed = False
    subject, _ = service(authority=denied)
    with pytest.raises(GuestArrivalAuthorizationError):
        subject.identify(actor_id="host", venue_id="venue-1", digital_identity="loc-a12")
    with pytest.raises(GuestArrivalAuthorizationError):
        subject.open_customer_group(
            OpenCustomerGroupCommand("r", "staff-waiter-1", "venue-1", "a12", True, True, True)
        )
    subject, unit = service()
    first = subject.open_customer_group(
        OpenCustomerGroupCommand("r", "staff-waiter-1", "venue-1", "a12", True, True, True)
    )
    unit.receipts.value = first
    with pytest.raises(GuestArrivalBusinessRuleError, match="another Service Location"):
        subject.open_customer_group(
            OpenCustomerGroupCommand("r", "staff-waiter-1", "venue-1", "other", True, True, True)
        )


def test_command_requires_structural_identity():
    with pytest.raises(GuestArrivalValidationError, match="request id is required"):
        OpenCustomerGroupCommand(" ", "waiter", "venue", "a12", True, True, False)
