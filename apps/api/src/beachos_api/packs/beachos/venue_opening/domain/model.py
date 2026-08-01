"""Framework-independent business model for daily Venue Opening."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from beachos_api.packs.beachos.venue_opening.domain.events import (
        DepartmentReadinessDeclared,
        VenueOpenedForBusinessDate,
    )


class VenueOpeningError(ValueError):
    """Raised when an attempted Venue Opening action breaks an approved rule."""


def _required_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise VenueOpeningError(f"{field_name} is required")
    return normalized


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _aware(moment: datetime, field_name: str) -> datetime:
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise VenueOpeningError(f"{field_name} must include a timezone")
    return moment


@dataclass(frozen=True, slots=True, order=True)
class BusinessDate:
    """The Venue operating day to which the opening belongs."""

    value: date

    def __post_init__(self) -> None:
        if not isinstance(self.value, date):
            raise VenueOpeningError("business date must be a date")


class OpeningStatus(StrEnum):
    """The approved daily opening states of a Venue."""

    CLOSED = "CLOSED"
    OPEN = "OPEN"


class ReadinessStatus(StrEnum):
    """The approved readiness declarations."""

    READY = "READY"
    NOT_READY = "NOT READY"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class OperationalDepartment:
    """A Venue department responsible for one area of opening readiness."""

    department_id: str
    name: str
    responsible_person_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "department_id",
            _required_text(self.department_id, "department id"),
        )
        object.__setattr__(self, "name", _required_text(self.name, "department name"))
        object.__setattr__(
            self,
            "responsible_person_id",
            _required_text(self.responsible_person_id, "responsible person id"),
        )


@dataclass(frozen=True, slots=True)
class DepartmentReadiness:
    """One attributable readiness declaration for an Operational Department."""

    department_id: str
    responsible_person_id: str
    declared_by_id: str
    status: ReadinessStatus
    declared_at: datetime
    reason: str | None = None
    comment: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "department_id",
            _required_text(self.department_id, "department id"),
        )
        object.__setattr__(
            self,
            "responsible_person_id",
            _required_text(self.responsible_person_id, "responsible person id"),
        )
        object.__setattr__(
            self,
            "declared_by_id",
            _required_text(self.declared_by_id, "declaring person id"),
        )
        object.__setattr__(self, "declared_at", _aware(self.declared_at, "declaration time"))
        if not isinstance(self.status, ReadinessStatus):
            raise VenueOpeningError("readiness status must be READY, NOT READY, or BLOCKED")

        if self.declared_by_id != self.responsible_person_id:
            raise VenueOpeningError(
                "only the department's responsible person may declare readiness"
            )

        reason = _optional_text(self.reason)
        comment = _optional_text(self.comment)
        object.__setattr__(self, "reason", reason)
        object.__setattr__(self, "comment", comment)

        if self.status in {ReadinessStatus.NOT_READY, ReadinessStatus.BLOCKED} and reason is None:
            raise VenueOpeningError("NOT READY and BLOCKED require a reason")


@dataclass(frozen=True, slots=True)
class OpeningReport:
    """Permanent snapshot of the facts at the completed opening."""

    venue_id: str
    business_date: BusinessDate
    opened_at: datetime
    host_id: str
    department_readiness: tuple[DepartmentReadiness, ...]
    declaration_history: tuple[DepartmentReadiness, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "venue_id", _required_text(self.venue_id, "venue id"))
        object.__setattr__(self, "host_id", _required_text(self.host_id, "host id"))
        object.__setattr__(self, "opened_at", _aware(self.opened_at, "opening time"))
        if not self.department_readiness:
            raise VenueOpeningError("an Opening Report requires mandatory department readiness")
        department_ids = {declaration.department_id for declaration in self.department_readiness}
        if len(department_ids) != len(self.department_readiness):
            raise VenueOpeningError(
                "an Opening Report requires one current declaration per department"
            )
        if any(
            declaration.status is not ReadinessStatus.READY
            for declaration in self.department_readiness
        ):
            raise VenueOpeningError("an Opening Report may contain only READY current declarations")

    @property
    def delays(self) -> tuple[DepartmentReadiness, ...]:
        """Prior NOT READY declarations that explain opening delay."""

        return tuple(
            declaration
            for declaration in self.declaration_history
            if declaration.status is ReadinessStatus.NOT_READY
        )

    @property
    def blocking_issues(self) -> tuple[DepartmentReadiness, ...]:
        """Prior BLOCKED declarations that explain opening blockers."""

        return tuple(
            declaration
            for declaration in self.declaration_history
            if declaration.status is ReadinessStatus.BLOCKED
        )


class OpeningChecklist:
    """Current and historical declarations for all mandatory departments."""

    def __init__(self, departments: tuple[OperationalDepartment, ...]) -> None:
        by_id = {department.department_id: department for department in departments}
        if len(by_id) != len(departments):
            raise VenueOpeningError("mandatory department ids must be unique")
        self._departments: Final[dict[str, OperationalDepartment]] = by_id
        self._current: dict[str, DepartmentReadiness] = {}
        self._history: list[DepartmentReadiness] = []

    @classmethod
    def _restore(
        cls,
        *,
        departments: tuple[OperationalDepartment, ...],
        declaration_history: tuple[DepartmentReadiness, ...],
    ) -> OpeningChecklist:
        checklist = cls(departments)
        previous_time: datetime | None = None
        for declaration in declaration_history:
            department = checklist._departments.get(declaration.department_id)
            if department is None:
                raise VenueOpeningError(
                    "restored declaration must belong to a mandatory department"
                )
            if declaration.responsible_person_id != department.responsible_person_id:
                raise VenueOpeningError(
                    "restored declaration responsible person must match the department"
                )
            if previous_time is not None and declaration.declared_at < previous_time:
                raise VenueOpeningError(
                    "restored declaration history must be in chronological order"
                )
            checklist._history.append(declaration)
            checklist._current[declaration.department_id] = declaration
            previous_time = declaration.declared_at
        return checklist

    @property
    def departments(self) -> Mapping[str, OperationalDepartment]:
        return MappingProxyType(self._departments)

    @property
    def current_declarations(self) -> Mapping[str, DepartmentReadiness]:
        return MappingProxyType(self._current)

    @property
    def declaration_history(self) -> tuple[DepartmentReadiness, ...]:
        return tuple(self._history)

    @property
    def missing_department_ids(self) -> tuple[str, ...]:
        return tuple(
            department_id
            for department_id in self._departments
            if department_id not in self._current
        )

    def declare(
        self,
        *,
        department_id: str,
        declared_by_id: str,
        status: ReadinessStatus,
        declared_at: datetime,
        reason: str | None = None,
        comment: str | None = None,
    ) -> DepartmentReadiness:
        normalized_department_id = _required_text(department_id, "department id")
        department = self._departments.get(normalized_department_id)
        if department is None:
            raise VenueOpeningError("readiness may be declared only for a mandatory department")

        declaration = DepartmentReadiness(
            department_id=department.department_id,
            responsible_person_id=department.responsible_person_id,
            declared_by_id=declared_by_id,
            status=status,
            declared_at=declared_at,
            reason=reason,
            comment=comment,
        )
        self._current[department.department_id] = declaration
        self._history.append(declaration)
        return declaration

    def snapshot(self) -> tuple[DepartmentReadiness, ...]:
        if self.missing_department_ids:
            raise VenueOpeningError("every mandatory department must have a current declaration")
        return tuple(self._current[department_id] for department_id in self._departments)


class VenueOpeningPolicy:
    """Approved eligibility and authority rules for opening a Venue."""

    @staticmethod
    def ensure_can_open(
        *,
        checklist: OpeningChecklist,
        opening_status: OpeningStatus,
        host_is_responsible: bool,
        host_has_required_capability: bool,
    ) -> None:
        if opening_status is OpeningStatus.OPEN:
            raise VenueOpeningError("the Venue is already open for this Business Date")
        if not checklist.departments:
            raise VenueOpeningError("at least one mandatory department is required")
        if checklist.missing_department_ids:
            raise VenueOpeningError(
                "every mandatory department must declare readiness before opening"
            )
        if any(
            declaration.status is not ReadinessStatus.READY
            for declaration in checklist.current_declarations.values()
        ):
            raise VenueOpeningError("every mandatory department must be READY before opening")
        if not host_is_responsible:
            raise VenueOpeningError("the opening actor must hold Host responsibility")
        if not host_has_required_capability:
            raise VenueOpeningError("the Host must hold the required Venue-opening Capability")


class Venue:
    """Aggregate protecting one Venue's opening for one Business Date."""

    def __init__(
        self,
        *,
        venue_id: str,
        name: str,
        business_date: BusinessDate,
        mandatory_departments: tuple[OperationalDepartment, ...],
    ) -> None:
        self._venue_id: Final[str] = _required_text(venue_id, "venue id")
        self._name: Final[str] = _required_text(name, "venue name")
        self._business_date: Final[BusinessDate] = business_date
        self._opening_status = OpeningStatus.CLOSED
        self._opening_checklist = OpeningChecklist(mandatory_departments)
        self._opening_report: OpeningReport | None = None
        self._aggregate_version = 0
        self._domain_events: list[DepartmentReadinessDeclared | VenueOpenedForBusinessDate] = []

    @classmethod
    def restore(
        cls,
        *,
        venue_id: str,
        name: str,
        business_date: BusinessDate,
        mandatory_departments: tuple[OperationalDepartment, ...],
        declaration_history: tuple[DepartmentReadiness, ...],
        opening_status: OpeningStatus,
        opening_report: OpeningReport | None,
        aggregate_version: int,
    ) -> Venue:
        """Reconstruct authoritative state without performing a business action."""

        if (
            not isinstance(aggregate_version, int)
            or isinstance(aggregate_version, bool)
            or aggregate_version < 0
        ):
            raise VenueOpeningError("aggregate version must be a non-negative integer")
        if not isinstance(opening_status, OpeningStatus):
            raise VenueOpeningError("opening status must be CLOSED or OPEN")

        venue = cls(
            venue_id=venue_id,
            name=name,
            business_date=business_date,
            mandatory_departments=mandatory_departments,
        )
        checklist = OpeningChecklist._restore(
            departments=mandatory_departments,
            declaration_history=declaration_history,
        )

        expected_version = len(declaration_history)
        if opening_status is OpeningStatus.OPEN:
            expected_version += 1
            if opening_report is None:
                raise VenueOpeningError("an open restored Venue requires an Opening Report")
            if (
                opening_report.venue_id != venue.venue_id
                or opening_report.business_date != business_date
            ):
                raise VenueOpeningError(
                    "restored Opening Report must match the Venue and Business Date"
                )
            if opening_report.declaration_history != declaration_history:
                raise VenueOpeningError("restored Opening Report must preserve declaration history")
            if opening_report.department_readiness != checklist.snapshot():
                raise VenueOpeningError(
                    "restored Opening Report must match current department readiness"
                )
        elif opening_report is not None:
            raise VenueOpeningError("a closed restored Venue cannot have an Opening Report")

        if aggregate_version != expected_version:
            raise VenueOpeningError(
                "aggregate version must match the restored Venue mutation history"
            )

        venue._opening_checklist = checklist
        venue._opening_status = opening_status
        venue._opening_report = opening_report
        venue._aggregate_version = aggregate_version
        return venue

    @property
    def venue_id(self) -> str:
        return self._venue_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def business_date(self) -> BusinessDate:
        return self._business_date

    @property
    def opening_status(self) -> OpeningStatus:
        return self._opening_status

    @property
    def opening_checklist(self) -> OpeningChecklist:
        return self._opening_checklist

    @property
    def opening_report(self) -> OpeningReport | None:
        return self._opening_report

    @property
    def aggregate_version(self) -> int:
        return self._aggregate_version

    @property
    def domain_events(
        self,
    ) -> tuple[DepartmentReadinessDeclared | VenueOpenedForBusinessDate, ...]:
        return tuple(self._domain_events)

    def declare_department_readiness(
        self,
        *,
        department_id: str,
        declared_by_id: str,
        status: ReadinessStatus,
        declared_at: datetime,
        reason: str | None = None,
        comment: str | None = None,
    ) -> DepartmentReadiness:
        if self._opening_status is OpeningStatus.OPEN:
            raise VenueOpeningError("opening readiness cannot be changed after the Venue is open")

        declaration = self._opening_checklist.declare(
            department_id=department_id,
            declared_by_id=declared_by_id,
            status=status,
            declared_at=declared_at,
            reason=reason,
            comment=comment,
        )

        from beachos_api.packs.beachos.venue_opening.domain.events import (
            DepartmentReadinessDeclared,
        )

        self._domain_events.append(
            DepartmentReadinessDeclared(
                venue_id=self._venue_id,
                business_date=self._business_date,
                declaration=declaration,
                occurred_at=declaration.declared_at,
            )
        )
        self._aggregate_version += 1
        return declaration

    def open_for_business_date(
        self,
        *,
        host_id: str,
        host_is_responsible: bool,
        host_has_required_capability: bool,
        opened_at: datetime,
        policy: VenueOpeningPolicy,
    ) -> OpeningReport:
        normalized_host_id = _required_text(host_id, "host id")
        aware_opened_at = _aware(opened_at, "opening time")
        policy.ensure_can_open(
            checklist=self._opening_checklist,
            opening_status=self._opening_status,
            host_is_responsible=host_is_responsible,
            host_has_required_capability=host_has_required_capability,
        )
        current_readiness = self._opening_checklist.snapshot()
        report = OpeningReport(
            venue_id=self._venue_id,
            business_date=self._business_date,
            opened_at=aware_opened_at,
            host_id=normalized_host_id,
            department_readiness=current_readiness,
            declaration_history=self._opening_checklist.declaration_history,
        )

        from beachos_api.packs.beachos.venue_opening.domain.events import (
            VenueOpenedForBusinessDate,
        )

        self._opening_status = OpeningStatus.OPEN
        self._opening_report = report
        self._domain_events.append(
            VenueOpenedForBusinessDate(
                venue_id=self._venue_id,
                business_date=self._business_date,
                host_id=normalized_host_id,
                opening_report=report,
                occurred_at=aware_opened_at,
            )
        )
        self._aggregate_version += 1
        return report

    def pull_domain_events(
        self,
    ) -> tuple[DepartmentReadinessDeclared | VenueOpenedForBusinessDate, ...]:
        events = tuple(self._domain_events)
        self._domain_events.clear()
        return events
