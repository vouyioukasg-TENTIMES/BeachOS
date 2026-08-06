"""Guest Departure Domain and Application tests."""

from datetime import UTC, datetime

import pytest

from beachos_api.packs.beachos.guest_arrival.domain import (
    CustomerGroupOpened,
    GuestArrivalError,
    GuestDeparted,
    ResponsibleWaiterAssigned,
    ServiceLocation,
    ServiceLocationStatus,
    ServiceLocationType,
)
from beachos_api.packs.beachos.guest_departure.application import (
    DepartCustomerGroupCommand,
    DepartureApplicationError,
    DepartureAuthorizationError,
    DepartureNotFoundError,
    GuestDepartureService,
)

AT = datetime(2026, 8, 1, 18, 10, tzinfo=UTC)


def occupied_location() -> ServiceLocation:
    return ServiceLocation.restore(
        service_location_id="location-1",
        venue_id="venue-1",
        visible_name="Upper Table 1",
        digital_identity="location-1-digital",
        location_type=ServiceLocationType.UPPER_TABLE,
        initial_status=ServiceLocationStatus.AVAILABLE,
        beach_sunbed_charge=None,
        charge_description=None,
        events=(
            ResponsibleWaiterAssigned("group-1", "location-1", "waiter-1", AT),
            CustomerGroupOpened("group-1", "venue-1", "location-1", "waiter-1", AT),
        ),
    )


def test_completed_group_departs_and_releases_location_once() -> None:
    location = occupied_location()
    location.depart_customer_group(
        customer_group_id="group-1",
        departed_by_id="staff-1",
        departed_at=AT,
        customer_group_is_completed=True,
    )
    event = location.pull_events()[0]
    assert event == GuestDeparted("group-1", "location-1", "staff-1", AT)
    assert location.status is ServiceLocationStatus.AVAILABLE
    assert location.active_customer_group is None
    with pytest.raises(GuestArrivalError, match="does not occupy"):
        location.depart_customer_group(
            customer_group_id="group-1",
            departed_by_id="staff-1",
            departed_at=AT,
            customer_group_is_completed=True,
        )


def test_active_group_cannot_depart_and_location_stays_occupied() -> None:
    location = occupied_location()
    with pytest.raises(GuestArrivalError, match="COMPLETED"):
        location.depart_customer_group(
            customer_group_id="group-1",
            departed_by_id="staff-1",
            departed_at=AT,
            customer_group_is_completed=False,
        )
    assert location.status is ServiceLocationStatus.OCCUPIED
    assert location.pull_events() == ()


def test_departure_restoration_is_event_sourced_and_structurally_safe() -> None:
    events = (
        ResponsibleWaiterAssigned("group-1", "location-1", "waiter-1", AT),
        CustomerGroupOpened("group-1", "venue-1", "location-1", "waiter-1", AT),
        GuestDeparted("group-1", "location-1", "staff-1", AT),
    )
    restored = ServiceLocation.restore(
        service_location_id="location-1",
        venue_id="venue-1",
        visible_name="Upper Table 1",
        digital_identity="digital-1",
        location_type=ServiceLocationType.UPPER_TABLE,
        initial_status=ServiceLocationStatus.AVAILABLE,
        beach_sunbed_charge=None,
        charge_description=None,
        events=events,
    )
    assert restored.status is ServiceLocationStatus.AVAILABLE
    assert restored.active_customer_group is None
    assert restored.version == 3
    assert restored.pull_events() == ()
    with pytest.raises(GuestArrivalError, match="must match"):
        ServiceLocation.restore(
            service_location_id="location-1",
            venue_id="venue-1",
            visible_name="Upper Table 1",
            digital_identity="digital-1",
            location_type=ServiceLocationType.UPPER_TABLE,
            initial_status=ServiceLocationStatus.AVAILABLE,
            beach_sunbed_charge=None,
            charge_description=None,
            events=(GuestDeparted("group-1", "location-1", "staff-1", AT),),
        )


class Authority:
    allowed = True

    def can_depart_customer_group(self, **_: str) -> bool:
        return self.allowed


class Clock:
    def now(self) -> datetime:
        return AT


class Locations:
    def __init__(self) -> None:
        self.location: ServiceLocation | None = occupied_location()
        self.saved = False

    def get_for_customer_group(self, **_: str) -> ServiceLocation | None:
        return self.location

    def save(self, _: ServiceLocation) -> None:
        self.saved = True


class Groups:
    value: str | None = "COMPLETED"

    def status(self, **_: str) -> str | None:
        return self.value


class Receipts:
    def __init__(self) -> None:
        self.value = None

    def get(self, **_: str):
        return self.value

    def save(self, value) -> None:
        self.value = value


class Activity:
    def __init__(self) -> None:
        self.recorded = False

    def record(self, **_: object) -> None:
        self.recorded = True


class Unit:
    def __init__(self) -> None:
        self.locations = Locations()
        self.customer_groups = Groups()
        self.receipts = Receipts()
        self.activity = Activity()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, *_: object) -> None:
        pass

    def commit(self) -> None:
        self.committed = True


class Units:
    def __init__(self) -> None:
        self.unit = Unit()

    def create(self):
        return self.unit


def test_application_context_and_departure_are_idempotent() -> None:
    units = Units()
    service = GuestDepartureService(authority=Authority(), clock=Clock(), units=units)
    context = service.get_context(customer_group_id="group-1")
    assert context.can_depart
    assert context.service_location_status == "OCCUPIED"
    command = DepartCustomerGroupCommand("request-1", "staff-1", "group-1")
    first = service.depart(command)
    second = service.depart(command)
    assert first == second
    assert first.service_location_status == "AVAILABLE"
    assert first.customer_group_status == "COMPLETED"
    assert units.unit.locations.saved
    assert units.unit.activity.recorded
    assert units.unit.committed


def test_application_rejects_active_missing_unauthorized_and_invalid_requests() -> None:
    units = Units()
    units.unit.customer_groups.value = "ACTIVE"
    service = GuestDepartureService(authority=Authority(), clock=Clock(), units=units)
    with pytest.raises(DepartureApplicationError, match="COMPLETED"):
        service.depart(DepartCustomerGroupCommand("request", "staff", "group-1"))
    with pytest.raises(DepartureApplicationError, match="required"):
        service.depart(DepartCustomerGroupCommand("", "staff", "group-1"))

    denied = Authority()
    denied.allowed = False
    with pytest.raises(DepartureAuthorizationError, match="capability"):
        GuestDepartureService(authority=denied, clock=Clock(), units=units).depart(
            DepartCustomerGroupCommand("request", "staff", "group-1")
        )

    units.unit.locations.location = None
    units.unit.customer_groups.value = None
    with pytest.raises(DepartureNotFoundError, match="not found"):
        service.get_context(customer_group_id="missing")
    with pytest.raises(DepartureNotFoundError, match="not found"):
        service.depart(DepartCustomerGroupCommand("request", "staff", "missing"))


def test_request_identity_cannot_be_reused_for_another_group() -> None:
    units = Units()
    service = GuestDepartureService(authority=Authority(), clock=Clock(), units=units)
    service.depart(DepartCustomerGroupCommand("request", "staff", "group-1"))
    with pytest.raises(DepartureApplicationError, match="another group"):
        service.depart(DepartCustomerGroupCommand("request", "staff", "group-2"))
