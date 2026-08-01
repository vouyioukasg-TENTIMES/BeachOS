"""Application results and data-transfer representations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from beachos_api.packs.beachos.venue_opening.domain import (
    DepartmentReadiness,
    OpeningReport,
    ReadinessStatus,
    Venue,
)


@dataclass(frozen=True, slots=True)
class DepartmentReadinessDTO:
    """Application representation of one readiness declaration."""

    department_id: str
    responsible_person_id: str
    declared_by_id: str
    status: str
    declared_at: datetime
    reason: str | None
    comment: str | None

    @classmethod
    def from_domain(
        cls,
        declaration: DepartmentReadiness,
    ) -> DepartmentReadinessDTO:
        return cls(
            department_id=declaration.department_id,
            responsible_person_id=declaration.responsible_person_id,
            declared_by_id=declaration.declared_by_id,
            status=declaration.status.value,
            declared_at=declaration.declared_at,
            reason=declaration.reason,
            comment=declaration.comment,
        )


@dataclass(frozen=True, slots=True)
class OpeningReportDTO:
    """Application representation of the official Opening Report."""

    venue_id: str
    business_date: date
    opened_at: datetime
    host_id: str
    department_readiness: tuple[DepartmentReadinessDTO, ...]
    declaration_history: tuple[DepartmentReadinessDTO, ...]
    delays: tuple[DepartmentReadinessDTO, ...]
    blocking_issues: tuple[DepartmentReadinessDTO, ...]

    @classmethod
    def from_domain(cls, report: OpeningReport) -> OpeningReportDTO:
        return cls(
            venue_id=report.venue_id,
            business_date=report.business_date.value,
            opened_at=report.opened_at,
            host_id=report.host_id,
            department_readiness=tuple(
                DepartmentReadinessDTO.from_domain(declaration)
                for declaration in report.department_readiness
            ),
            declaration_history=tuple(
                DepartmentReadinessDTO.from_domain(declaration)
                for declaration in report.declaration_history
            ),
            delays=tuple(
                DepartmentReadinessDTO.from_domain(declaration) for declaration in report.delays
            ),
            blocking_issues=tuple(
                DepartmentReadinessDTO.from_domain(declaration)
                for declaration in report.blocking_issues
            ),
        )


@dataclass(frozen=True, slots=True)
class DeclareDepartmentReadinessResult:
    """Successful result of declaring department readiness."""

    request_id: str
    venue_id: str
    business_date: date
    declaration: DepartmentReadinessDTO


@dataclass(frozen=True, slots=True)
class OpenVenueResult:
    """Successful result of opening a Venue."""

    request_id: str
    report: OpeningReportDTO


@dataclass(frozen=True, slots=True)
class DepartmentContextDTO:
    """Current opening context for one mandatory Operational Department."""

    department_id: str
    name: str
    responsible_person_id: str
    current_readiness: DepartmentReadinessDTO | None


@dataclass(frozen=True, slots=True)
class DepartmentOwnerContextResult:
    """Opening context limited to departments owned by the current actor."""

    venue_id: str
    venue_name: str
    business_date: date
    opening_status: str
    departments: tuple[DepartmentContextDTO, ...]
    declaration_history: tuple[DepartmentReadinessDTO, ...]

    @classmethod
    def from_domain(cls, venue: Venue, *, actor_id: str) -> DepartmentOwnerContextResult:
        owned_departments = tuple(
            department
            for department in venue.opening_checklist.departments.values()
            if department.responsible_person_id == actor_id
        )
        owned_ids = {department.department_id for department in owned_departments}
        return cls(
            venue_id=venue.venue_id,
            venue_name=venue.name,
            business_date=venue.business_date.value,
            opening_status=venue.opening_status.value,
            departments=tuple(
                DepartmentContextDTO(
                    department_id=department.department_id,
                    name=department.name,
                    responsible_person_id=department.responsible_person_id,
                    current_readiness=(
                        DepartmentReadinessDTO.from_domain(current)
                        if (
                            current := venue.opening_checklist.current_declarations.get(
                                department.department_id
                            )
                        )
                        is not None
                        else None
                    ),
                )
                for department in owned_departments
            ),
            declaration_history=tuple(
                DepartmentReadinessDTO.from_domain(declaration)
                for declaration in venue.opening_checklist.declaration_history
                if declaration.department_id in owned_ids
            ),
        )


@dataclass(frozen=True, slots=True)
class AttentionItemDTO:
    """A confirmed opening fact requiring Host attention."""

    code: str
    importance: str
    message: str
    department_id: str | None


@dataclass(frozen=True, slots=True)
class VenueContextResult:
    """Authoritative read-only Host context for one Venue and Business Date."""

    venue_id: str
    venue_name: str
    business_date: date
    opening_status: str
    opening_report: OpeningReportDTO | None
    departments: tuple[DepartmentContextDTO, ...]
    outstanding_department_ids: tuple[str, ...]
    attention_queue: tuple[AttentionItemDTO, ...]

    @classmethod
    def from_domain(cls, venue: Venue) -> VenueContextResult:
        departments = tuple(
            DepartmentContextDTO(
                department_id=department.department_id,
                name=department.name,
                responsible_person_id=department.responsible_person_id,
                current_readiness=(
                    DepartmentReadinessDTO.from_domain(current)
                    if (
                        current := venue.opening_checklist.current_declarations.get(
                            department.department_id
                        )
                    )
                    is not None
                    else None
                ),
            )
            for department in venue.opening_checklist.departments.values()
        )
        outstanding = tuple(
            department.department_id
            for department in departments
            if department.current_readiness is None
            or department.current_readiness.status != ReadinessStatus.READY.value
        )
        attention: list[AttentionItemDTO] = []
        for department in departments:
            readiness = department.current_readiness
            if readiness is None:
                attention.append(
                    AttentionItemDTO(
                        code="MISSING_DECLARATION",
                        importance="ACTION_REQUIRED",
                        message=f"{department.name} has not declared readiness.",
                        department_id=department.department_id,
                    )
                )
            elif readiness.status == ReadinessStatus.BLOCKED.value:
                attention.append(
                    AttentionItemDTO(
                        code="DEPARTMENT_BLOCKED",
                        importance="CRITICAL",
                        message=f"{department.name} is BLOCKED: {readiness.reason}.",
                        department_id=department.department_id,
                    )
                )
            elif readiness.status == ReadinessStatus.NOT_READY.value:
                attention.append(
                    AttentionItemDTO(
                        code="DEPARTMENT_NOT_READY",
                        importance="ACTION_REQUIRED",
                        message=f"{department.name} is NOT READY: {readiness.reason}.",
                        department_id=department.department_id,
                    )
                )

        if not outstanding and venue.opening_report is None:
            attention.append(
                AttentionItemDTO(
                    code="READY_TO_OPEN",
                    importance="ACTION_REQUIRED",
                    message="Every mandatory department is READY. The Venue can be opened.",
                    department_id=None,
                )
            )

        return cls(
            venue_id=venue.venue_id,
            venue_name=venue.name,
            business_date=venue.business_date.value,
            opening_status=venue.opening_status.value,
            opening_report=(
                OpeningReportDTO.from_domain(venue.opening_report)
                if venue.opening_report is not None
                else None
            ),
            departments=departments,
            outstanding_department_ids=outstanding,
            attention_queue=tuple(attention),
        )


@dataclass(frozen=True, slots=True)
class ActivityLogRecord:
    """Facts required to record the successful sensitive opening action."""

    request_id: str
    actor_id: str
    venue_id: str
    business_date: date
    occurred_at: datetime
