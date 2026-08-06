"""Explicit mappings between PostgreSQL rows and the Venue aggregate."""

from collections.abc import Sequence
from typing import Any

from beachos_api.packs.beachos.venue_opening.domain import (
    BusinessDate,
    DepartmentReadiness,
    OpeningReport,
    OpeningStatus,
    OperationalDepartment,
    ReadinessStatus,
    Venue,
)

Row = dict[str, Any]


def restore_venue(
    *,
    venue_row: Row,
    department_rows: Sequence[Row],
    declaration_rows: Sequence[Row],
    report_row: Row | None,
    closing_report_exists: bool = False,
) -> Venue:
    """Map authoritative rows to a Domain aggregate without replay."""

    business_date = BusinessDate(venue_row["business_date"])
    departments = tuple(
        OperationalDepartment(
            department_id=row["department_id"],
            name=row["department_name"],
            responsible_person_id=row["responsible_person_id"],
        )
        for row in department_rows
    )
    history = tuple(
        DepartmentReadiness(
            department_id=row["department_id"],
            responsible_person_id=row["responsible_person_id"],
            declared_by_id=row["declared_by_id"],
            status=ReadinessStatus(row["readiness_status"]),
            declared_at=row["declared_at"],
            reason=row["reason"],
            comment=row["comment"],
        )
        for row in declaration_rows
    )
    opening_status = OpeningStatus(venue_row["opening_status"])
    report: OpeningReport | None = None
    if report_row is not None:
        latest_by_department: dict[str, DepartmentReadiness] = {}
        for declaration in history:
            latest_by_department[declaration.department_id] = declaration
        report = OpeningReport(
            venue_id=venue_row["venue_id"],
            business_date=business_date,
            opened_at=report_row["opened_at"],
            host_id=report_row["host_id"],
            department_readiness=tuple(
                latest_by_department[department.department_id] for department in departments
            ),
            declaration_history=history,
        )

    return Venue.restore(
        venue_id=venue_row["venue_id"],
        name=venue_row["venue_name"],
        business_date=business_date,
        mandatory_departments=departments,
        declaration_history=history,
        opening_status=opening_status,
        opening_report=report,
        aggregate_version=venue_row["aggregate_version"],
        closing_report_exists=closing_report_exists,
    )
