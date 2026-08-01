"""Official Domain Events produced by Venue Opening."""

from dataclasses import dataclass
from datetime import datetime

from beachos_api.packs.beachos.venue_opening.domain.model import (
    BusinessDate,
    DepartmentReadiness,
    OpeningReport,
)


@dataclass(frozen=True, slots=True)
class DepartmentReadinessDeclared:
    """A responsible person declared an Operational Department's readiness."""

    venue_id: str
    business_date: BusinessDate
    declaration: DepartmentReadiness
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class VenueOpenedForBusinessDate:
    """A Venue officially began operation for one Business Date."""

    venue_id: str
    business_date: BusinessDate
    host_id: str
    opening_report: OpeningReport
    occurred_at: datetime
