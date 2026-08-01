"""Dependency-inversion ports owned by the Venue Opening Application Layer."""

from datetime import datetime
from types import TracebackType
from typing import Protocol, Self

from beachos_api.packs.beachos.venue_opening.application.dtos import (
    ActivityLogRecord,
)
from beachos_api.packs.beachos.venue_opening.domain import BusinessDate, Venue


class CapabilityVerifier(Protocol):
    """Verifies explicit action authority without inferring it from a Role."""

    def can_declare_department_readiness(
        self,
        *,
        actor_id: str,
        venue_id: str,
        department_id: str,
    ) -> bool: ...

    def can_open_venue(self, *, actor_id: str, venue_id: str) -> bool: ...


class HostResponsibilityVerifier(Protocol):
    """Confirms Host responsibility independently from Capability."""

    def is_responsible_host(self, *, actor_id: str, venue_id: str) -> bool: ...


class BusinessDateProvider(Protocol):
    """Provides the authoritative current Business Date for a Venue."""

    def current_for(self, *, venue_id: str) -> BusinessDate: ...


class Clock(Protocol):
    """Provides authoritative event time."""

    def now(self) -> datetime: ...


class VenueRepository(Protocol):
    """Loads and stages Venue aggregates without exposing storage details."""

    def get(
        self,
        *,
        venue_id: str,
        business_date: BusinessDate,
    ) -> Venue | None: ...

    def save(self, venue: Venue) -> None: ...


class ActivityLog(Protocol):
    """Stages the required accountable record for successful Venue opening."""

    def record_venue_opened(self, record: ActivityLogRecord) -> None: ...


class VenueOpeningUnitOfWork(Protocol):
    """Defines the atomic Application boundary for state and Activity Log."""

    @property
    def venues(self) -> VenueRepository: ...

    @property
    def activity_log(self) -> ActivityLog: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...


class VenueOpeningUnitOfWorkFactory(Protocol):
    """Creates one isolated consistency boundary per Command."""

    def create(self) -> VenueOpeningUnitOfWork: ...
