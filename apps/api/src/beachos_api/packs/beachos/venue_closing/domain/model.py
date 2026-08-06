"""Framework-independent Venue Closing Domain."""

from dataclasses import dataclass
from datetime import date, datetime


class VenueClosingError(ValueError):
    """Venue Closing would violate an approved invariant."""


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise VenueClosingError(f"{field} is required")
    return normalized


@dataclass(frozen=True, slots=True)
class ClosingReadiness:
    active_customer_groups: int
    occupied_service_locations: int
    open_bills: int
    unresolved_operational_work: int

    def __post_init__(self) -> None:
        values = (
            self.active_customer_groups,
            self.occupied_service_locations,
            self.open_bills,
            self.unresolved_operational_work,
        )
        if any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values
        ):
            raise VenueClosingError("closing readiness counts must be non-negative integers")

    @property
    def blockers(self) -> tuple[str, ...]:
        blockers: list[str] = []
        if self.active_customer_groups:
            blockers.append(f"{self.active_customer_groups} ACTIVE Customer Group(s) remain")
        if self.occupied_service_locations:
            blockers.append(
                f"{self.occupied_service_locations} occupied Service Location(s) remain"
            )
        if self.open_bills:
            blockers.append(f"{self.open_bills} open Bill(s) remain")
        if self.unresolved_operational_work:
            blockers.append(
                f"{self.unresolved_operational_work} unresolved operational work item(s) remain"
            )
        return tuple(blockers)


@dataclass(frozen=True, slots=True)
class ClosingReport:
    venue_id: str
    business_date: date
    closed_at: datetime
    closed_by_id: str
    readiness: ClosingReadiness

    def __post_init__(self) -> None:
        object.__setattr__(self, "venue_id", _required(self.venue_id, "Venue id"))
        object.__setattr__(self, "closed_by_id", _required(self.closed_by_id, "closing actor id"))
        if self.closed_at.tzinfo is None or self.closed_at.utcoffset() is None:
            raise VenueClosingError("closing time must include a timezone")
        if self.readiness.blockers:
            raise VenueClosingError("a Closing Report cannot contain unresolved blockers")


@dataclass(frozen=True, slots=True)
class VenueClosed:
    venue_id: str
    business_date: date
    closed_by_id: str
    closing_report: ClosingReport
    occurred_at: datetime


class VenueClosing:
    """Protects the final transition of one Venue Business Date."""

    def __init__(self, *, venue_id: str, business_date: date, status: str) -> None:
        self.venue_id = _required(venue_id, "Venue id")
        self.business_date = business_date
        if status not in {"CLOSED", "OPEN", "CLOSED_FOR_BUSINESS_DATE"}:
            raise VenueClosingError("Venue status is invalid")
        self._initial_status = status
        self._event: VenueClosed | None = None
        self._pending: list[VenueClosed] = []

    @classmethod
    def restore(
        cls,
        *,
        venue_id: str,
        business_date: date,
        status: str,
        event: VenueClosed | None,
    ) -> "VenueClosing":
        venue = cls(venue_id=venue_id, business_date=business_date, status=status)
        if event is not None:
            venue._apply(event)
        if status == "CLOSED_FOR_BUSINESS_DATE" and event is None:
            raise VenueClosingError("closed Venue state requires its immutable event")
        if status != "CLOSED_FOR_BUSINESS_DATE" and event is not None:
            raise VenueClosingError("an unclosed Venue cannot contain a closing event")
        return venue

    def close(
        self,
        *,
        actor_id: str,
        closed_at: datetime,
        readiness: ClosingReadiness,
    ) -> VenueClosed:
        if self.status != "OPEN":
            raise VenueClosingError("only an OPEN Venue may be closed")
        if readiness.blockers:
            raise VenueClosingError("; ".join(readiness.blockers))
        report = ClosingReport(
            self.venue_id,
            self.business_date,
            closed_at,
            actor_id,
            readiness,
        )
        event = VenueClosed(
            self.venue_id,
            self.business_date,
            report.closed_by_id,
            report,
            report.closed_at,
        )
        self._apply(event)
        self._pending.append(event)
        return event

    def _apply(self, event: VenueClosed) -> None:
        if event.venue_id != self.venue_id or event.business_date != self.business_date:
            raise VenueClosingError("closing event belongs to another Venue Business Date")
        if (
            event.closing_report.venue_id != self.venue_id
            or event.closing_report.business_date != self.business_date
            or event.closed_by_id != event.closing_report.closed_by_id
            or event.occurred_at != event.closing_report.closed_at
        ):
            raise VenueClosingError("closing event and Closing Report must describe the same fact")
        if self._event is not None:
            raise VenueClosingError("Venue is already closed for this Business Date")
        self._event = event

    def pull_events(self) -> tuple[VenueClosed, ...]:
        events = tuple(self._pending)
        self._pending.clear()
        return events

    @property
    def status(self) -> str:
        return "CLOSED_FOR_BUSINESS_DATE" if self._event else self._initial_status

    @property
    def closing_event(self) -> VenueClosed | None:
        return self._event
