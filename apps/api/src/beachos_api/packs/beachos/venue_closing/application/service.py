"""Venue Closing application orchestration."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol

from beachos_api.packs.beachos.venue_closing.domain import (
    ClosingReadiness,
    ClosingReport,
    VenueClosing,
    VenueClosingError,
)
from beachos_api.packs.beachos.venue_opening.domain import BusinessDate


class VenueClosingApplicationError(RuntimeError):
    """Venue Closing could not produce its approved outcome."""


class VenueClosingAuthorizationError(VenueClosingApplicationError):
    """The actor lacks the closing capability."""


class VenueClosingNotFoundError(VenueClosingApplicationError):
    """The current Venue Business Date does not exist."""


@dataclass(frozen=True, slots=True)
class CloseVenueCommand:
    request_id: str
    actor_id: str
    venue_id: str


@dataclass(frozen=True, slots=True)
class ClosingReportDTO:
    venue_id: str
    business_date: date
    closed_at: datetime
    closed_by_id: str
    active_customer_groups: int
    occupied_service_locations: int
    open_bills: int
    unresolved_operational_work: int

    @classmethod
    def from_domain(cls, report: ClosingReport) -> "ClosingReportDTO":
        return cls(
            report.venue_id,
            report.business_date,
            report.closed_at,
            report.closed_by_id,
            report.readiness.active_customer_groups,
            report.readiness.occupied_service_locations,
            report.readiness.open_bills,
            report.readiness.unresolved_operational_work,
        )


@dataclass(frozen=True, slots=True)
class ClosingContextResult:
    venue_id: str
    business_date: date
    status: str
    readiness: ClosingReadiness
    blockers: tuple[str, ...]
    can_close: bool
    closing_report: ClosingReportDTO | None


@dataclass(frozen=True, slots=True)
class CloseVenueResult:
    request_id: str
    status: str
    closing_report: ClosingReportDTO


class Authority(Protocol):
    def can_close_venue(self, *, actor_id: str, venue_id: str) -> bool: ...


class BusinessDates(Protocol):
    def current_for(self, *, venue_id: str) -> BusinessDate: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class Venues(Protocol):
    def get(self, *, venue_id: str, business_date: date) -> VenueClosing | None: ...
    def save(self, venue: VenueClosing) -> None: ...


class Readiness(Protocol):
    def current(self, *, venue_id: str) -> ClosingReadiness: ...


class Receipts(Protocol):
    def get(self, *, request_id: str) -> CloseVenueResult | None: ...
    def save(self, result: CloseVenueResult) -> None: ...


class Activity(Protocol):
    def record(self, *, result: CloseVenueResult) -> None: ...


class Unit(Protocol):
    venues: Venues
    readiness: Readiness
    receipts: Receipts
    activity: Activity

    def __enter__(self) -> "Unit": ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> None: ...


class Units(Protocol):
    def create(self) -> Unit: ...


class VenueClosingService:
    def __init__(
        self,
        *,
        authority: Authority,
        business_dates: BusinessDates,
        clock: Clock,
        units: Units,
    ) -> None:
        self._authority = authority
        self._business_dates = business_dates
        self._clock = clock
        self._units = units

    def get_context(self, *, venue_id: str) -> ClosingContextResult:
        business_date = self._business_dates.current_for(venue_id=venue_id).value
        with self._units.create() as unit:
            venue = unit.venues.get(venue_id=venue_id, business_date=business_date)
            if venue is None:
                raise VenueClosingNotFoundError("Venue Closing context was not found")
            readiness = unit.readiness.current(venue_id=venue_id)
            event = venue.closing_event
            return ClosingContextResult(
                venue_id,
                business_date,
                venue.status,
                readiness,
                readiness.blockers,
                venue.status == "OPEN" and not readiness.blockers,
                ClosingReportDTO.from_domain(event.closing_report) if event else None,
            )

    def close(self, command: CloseVenueCommand) -> CloseVenueResult:
        if not all(
            (command.request_id.strip(), command.actor_id.strip(), command.venue_id.strip())
        ):
            raise VenueClosingApplicationError("request, actor, and Venue are required")
        if not self._authority.can_close_venue(
            actor_id=command.actor_id, venue_id=command.venue_id
        ):
            raise VenueClosingAuthorizationError("Close Venue capability is required")
        business_date = self._business_dates.current_for(venue_id=command.venue_id).value
        with self._units.create() as unit:
            prior = unit.receipts.get(request_id=command.request_id)
            if prior is not None:
                return prior
            venue = unit.venues.get(venue_id=command.venue_id, business_date=business_date)
            if venue is None:
                raise VenueClosingNotFoundError("Venue Closing context was not found")
            if venue.closing_event is not None:
                return CloseVenueResult(
                    command.request_id,
                    venue.status,
                    ClosingReportDTO.from_domain(venue.closing_event.closing_report),
                )
            readiness = unit.readiness.current(venue_id=command.venue_id)
            try:
                event = venue.close(
                    actor_id=command.actor_id,
                    closed_at=self._clock.now(),
                    readiness=readiness,
                )
            except VenueClosingError as error:
                raise VenueClosingApplicationError(str(error)) from error
            result = CloseVenueResult(
                command.request_id,
                venue.status,
                ClosingReportDTO.from_domain(event.closing_report),
            )
            unit.venues.save(venue)
            unit.receipts.save(result)
            unit.activity.record(result=result)
            unit.commit()
            return result
