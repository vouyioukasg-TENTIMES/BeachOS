"""Venue Closing Domain and Application tests."""

from datetime import UTC, date, datetime

import pytest

from beachos_api.packs.beachos.venue_closing.application import (
    CloseVenueCommand,
    VenueClosingApplicationError,
    VenueClosingAuthorizationError,
    VenueClosingNotFoundError,
    VenueClosingService,
)
from beachos_api.packs.beachos.venue_closing.domain import (
    ClosingReadiness,
    VenueClosed,
    VenueClosing,
    VenueClosingError,
)
from beachos_api.packs.beachos.venue_opening.domain import BusinessDate

DAY = date(2026, 8, 1)
AT = datetime(2026, 8, 1, 23, 30, tzinfo=UTC)
READY = ClosingReadiness(0, 0, 0, 0)


def test_open_venue_closes_with_one_permanent_report_and_event() -> None:
    venue = VenueClosing.restore(venue_id="venue-1", business_date=DAY, status="OPEN", event=None)
    event = venue.close(actor_id="manager-1", closed_at=AT, readiness=READY)
    assert event == VenueClosed("venue-1", DAY, "manager-1", event.closing_report, AT)
    assert event.closing_report.readiness == READY
    assert venue.status == "CLOSED_FOR_BUSINESS_DATE"
    assert venue.pull_events() == (event,)
    with pytest.raises(VenueClosingError, match="only an OPEN Venue"):
        venue.close(actor_id="manager-1", closed_at=AT, readiness=READY)


@pytest.mark.parametrize(
    ("readiness", "message"),
    [
        (ClosingReadiness(1, 0, 0, 0), "ACTIVE Customer Group"),
        (ClosingReadiness(0, 1, 0, 0), "occupied Service Location"),
        (ClosingReadiness(0, 0, 1, 0), "open Bill"),
        (ClosingReadiness(0, 0, 0, 1), "unresolved operational work"),
    ],
)
def test_every_approved_closing_blocker_is_enforced(
    readiness: ClosingReadiness, message: str
) -> None:
    venue = VenueClosing.restore(venue_id="venue-1", business_date=DAY, status="OPEN", event=None)
    with pytest.raises(VenueClosingError, match=message):
        venue.close(actor_id="manager-1", closed_at=AT, readiness=readiness)
    assert venue.status == "OPEN"
    assert venue.pull_events() == ()


def test_unopened_venue_and_invalid_restoration_are_rejected() -> None:
    venue = VenueClosing.restore(venue_id="venue-1", business_date=DAY, status="CLOSED", event=None)
    with pytest.raises(VenueClosingError, match="only an OPEN Venue"):
        venue.close(actor_id="manager-1", closed_at=AT, readiness=READY)
    with pytest.raises(VenueClosingError, match="immutable event"):
        VenueClosing.restore(
            venue_id="venue-1",
            business_date=DAY,
            status="CLOSED_FOR_BUSINESS_DATE",
            event=None,
        )


class Authority:
    allowed = True

    def can_close_venue(self, **_: str) -> bool:
        return self.allowed


class Dates:
    def current_for(self, **_: str) -> BusinessDate:
        return BusinessDate(DAY)


class Clock:
    def now(self) -> datetime:
        return AT


class Venues:
    def __init__(self) -> None:
        self.venue: VenueClosing | None = VenueClosing.restore(
            venue_id="venue-1", business_date=DAY, status="OPEN", event=None
        )
        self.saved = False

    def get(self, **_: object) -> VenueClosing | None:
        return self.venue

    def save(self, _: VenueClosing) -> None:
        self.saved = True


class Readiness:
    value = READY

    def current(self, **_: str) -> ClosingReadiness:
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
        self.venues = Venues()
        self.readiness = Readiness()
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


def service(units: Units, authority: Authority | None = None) -> VenueClosingService:
    return VenueClosingService(
        authority=authority or Authority(),
        business_dates=Dates(),
        clock=Clock(),
        units=units,
    )


def test_application_context_close_and_duplicate_are_idempotent() -> None:
    units = Units()
    subject = service(units)
    context = subject.get_context(venue_id="venue-1")
    assert context.can_close and context.blockers == ()
    command = CloseVenueCommand("request-1", "manager-1", "venue-1")
    first = subject.close(command)
    second = subject.close(command)
    duplicate_attempt = subject.close(CloseVenueCommand("request-2", "manager-1", "venue-1"))
    assert first == second
    assert duplicate_attempt.closing_report == first.closing_report
    assert first.status == "CLOSED_FOR_BUSINESS_DATE"
    assert units.unit.venues.saved
    assert units.unit.activity.recorded
    assert units.unit.committed


def test_application_preserves_blockers_authority_validation_and_missing_state() -> None:
    units = Units()
    units.unit.readiness.value = ClosingReadiness(1, 1, 1, 1)
    subject = service(units)
    context = subject.get_context(venue_id="venue-1")
    assert not context.can_close and len(context.blockers) == 4
    with pytest.raises(VenueClosingApplicationError, match="ACTIVE Customer Group"):
        subject.close(CloseVenueCommand("request", "manager", "venue-1"))
    with pytest.raises(VenueClosingApplicationError, match="required"):
        subject.close(CloseVenueCommand("", "manager", "venue-1"))

    denied = Authority()
    denied.allowed = False
    with pytest.raises(VenueClosingAuthorizationError, match="capability"):
        service(units, denied).close(CloseVenueCommand("request", "manager", "venue-1"))

    units.unit.venues.venue = None
    with pytest.raises(VenueClosingNotFoundError, match="not found"):
        subject.get_context(venue_id="missing")
    with pytest.raises(VenueClosingNotFoundError, match="not found"):
        subject.close(CloseVenueCommand("request", "manager", "missing"))
