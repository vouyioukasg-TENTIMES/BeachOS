"""Unit tests for the Venue Opening Domain."""

from datetime import UTC, date, datetime
from types import MappingProxyType
from unittest.mock import patch

import pytest

from beachos_api.packs.beachos.venue_opening.domain import (
    BusinessDate,
    DepartmentReadiness,
    DepartmentReadinessDeclared,
    OpeningChecklist,
    OpeningReport,
    OpeningStatus,
    OperationalDepartment,
    ReadinessStatus,
    Venue,
    VenueOpenedForBusinessDate,
    VenueOpeningError,
    VenueOpeningPolicy,
)

BUSINESS_DATE = BusinessDate(date(2026, 7, 26))
DECLARED_AT = datetime(2026, 7, 26, 7, 30, tzinfo=UTC)
OPENED_AT = datetime(2026, 7, 26, 8, 0, tzinfo=UTC)


def department(
    department_id: str = "kitchen",
    *,
    name: str = "Kitchen",
    responsible_person_id: str = "staff-kitchen",
) -> OperationalDepartment:
    return OperationalDepartment(
        department_id=department_id,
        name=name,
        responsible_person_id=responsible_person_id,
    )


def venue(
    departments: tuple[OperationalDepartment, ...] | None = None,
) -> Venue:
    return Venue(
        venue_id="venue-1",
        name="Emerald Beach Club",
        business_date=BUSINESS_DATE,
        mandatory_departments=departments
        if departments is not None
        else (
            department(),
            department(
                "bar",
                name="Bar",
                responsible_person_id="staff-bar",
            ),
        ),
    )


def declare_all_ready(subject: Venue) -> None:
    for configured_department in subject.opening_checklist.departments.values():
        subject.declare_department_readiness(
            department_id=configured_department.department_id,
            declared_by_id=configured_department.responsible_person_id,
            status=ReadinessStatus.READY,
            declared_at=DECLARED_AT,
        )


def open_venue(subject: Venue) -> OpeningReport:
    return subject.open_for_business_date(
        host_id="host-1",
        host_is_responsible=True,
        host_has_required_capability=True,
        opened_at=OPENED_AT,
        policy=VenueOpeningPolicy(),
    )


def test_business_date_is_orderable_and_requires_a_date() -> None:
    assert BusinessDate(date(2026, 7, 27)) > BUSINESS_DATE

    with pytest.raises(VenueOpeningError, match="business date must be a date"):
        BusinessDate("2026-07-26")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field", "kwargs"),
    [
        ("department id", {"department_id": " "}),
        ("department name", {"name": ""}),
        ("responsible person id", {"responsible_person_id": "\t"}),
    ],
)
def test_operational_department_requires_its_identity(
    field: str,
    kwargs: dict[str, str],
) -> None:
    values = {
        "department_id": "kitchen",
        "name": "Kitchen",
        "responsible_person_id": "staff-kitchen",
    }
    values.update(kwargs)

    with pytest.raises(VenueOpeningError, match=f"{field} is required"):
        OperationalDepartment(**values)


def test_operational_department_normalizes_text() -> None:
    subject = OperationalDepartment(
        department_id=" kitchen ",
        name=" Kitchen ",
        responsible_person_id=" staff-kitchen ",
    )

    assert subject.department_id == "kitchen"
    assert subject.name == "Kitchen"
    assert subject.responsible_person_id == "staff-kitchen"


@pytest.mark.parametrize("status", [ReadinessStatus.NOT_READY, ReadinessStatus.BLOCKED])
def test_non_ready_declarations_require_a_reason(status: ReadinessStatus) -> None:
    with pytest.raises(
        VenueOpeningError,
        match="NOT READY and BLOCKED require a reason",
    ):
        DepartmentReadiness(
            department_id="kitchen",
            responsible_person_id="staff-kitchen",
            declared_by_id="staff-kitchen",
            status=status,
            declared_at=DECLARED_AT,
            reason=" ",
        )


def test_ready_declaration_normalizes_optional_text() -> None:
    declaration = DepartmentReadiness(
        department_id=" kitchen ",
        responsible_person_id=" staff-kitchen ",
        declared_by_id=" staff-kitchen ",
        status=ReadinessStatus.READY,
        declared_at=DECLARED_AT,
        reason=" ",
        comment=" Ready for service ",
    )

    assert declaration.department_id == "kitchen"
    assert declaration.reason is None
    assert declaration.comment == "Ready for service"


@pytest.mark.parametrize(
    ("field", "kwargs"),
    [
        ("department id", {"department_id": ""}),
        ("responsible person id", {"responsible_person_id": ""}),
        ("declaring person id", {"declared_by_id": ""}),
    ],
)
def test_readiness_declaration_requires_attribution(
    field: str,
    kwargs: dict[str, str],
) -> None:
    values: dict[str, object] = {
        "department_id": "kitchen",
        "responsible_person_id": "staff-kitchen",
        "declared_by_id": "staff-kitchen",
        "status": ReadinessStatus.READY,
        "declared_at": DECLARED_AT,
    }
    values.update(kwargs)

    with pytest.raises(VenueOpeningError, match=f"{field} is required"):
        DepartmentReadiness(**values)  # type: ignore[arg-type]


def test_only_responsible_person_can_declare_readiness() -> None:
    with pytest.raises(
        VenueOpeningError,
        match="only the department's responsible person",
    ):
        DepartmentReadiness(
            department_id="kitchen",
            responsible_person_id="staff-kitchen",
            declared_by_id="host-1",
            status=ReadinessStatus.READY,
            declared_at=DECLARED_AT,
        )


def test_declaration_time_must_be_timezone_aware() -> None:
    with pytest.raises(
        VenueOpeningError,
        match="declaration time must include a timezone",
    ):
        DepartmentReadiness(
            department_id="kitchen",
            responsible_person_id="staff-kitchen",
            declared_by_id="staff-kitchen",
            status=ReadinessStatus.READY,
            declared_at=datetime(2026, 7, 26, 7, 30),
        )


def test_declaration_rejects_a_status_outside_the_approved_vocabulary() -> None:
    with pytest.raises(
        VenueOpeningError,
        match="readiness status must be READY, NOT READY, or BLOCKED",
    ):
        DepartmentReadiness(
            department_id="kitchen",
            responsible_person_id="staff-kitchen",
            declared_by_id="staff-kitchen",
            status="UNKNOWN",  # type: ignore[arg-type]
            declared_at=DECLARED_AT,
        )


def test_checklist_requires_unique_mandatory_department_ids() -> None:
    with pytest.raises(
        VenueOpeningError,
        match="mandatory department ids must be unique",
    ):
        OpeningChecklist((department(), department()))


def test_checklist_rejects_unknown_department_without_mutation() -> None:
    checklist = OpeningChecklist((department(),))

    with pytest.raises(
        VenueOpeningError,
        match="only for a mandatory department",
    ):
        checklist.declare(
            department_id="bar",
            declared_by_id="staff-bar",
            status=ReadinessStatus.READY,
            declared_at=DECLARED_AT,
        )

    assert checklist.current_declarations == {}
    assert checklist.declaration_history == ()


def test_checklist_exposes_read_only_views_and_tracks_missing_departments() -> None:
    checklist = OpeningChecklist((department(),))

    assert isinstance(checklist.departments, MappingProxyType)
    assert isinstance(checklist.current_declarations, MappingProxyType)
    assert checklist.missing_department_ids == ("kitchen",)

    with pytest.raises(TypeError):
        checklist.departments["bar"] = department("bar")  # type: ignore[index]


def test_checklist_snapshot_requires_every_declaration() -> None:
    checklist = OpeningChecklist((department(),))

    with pytest.raises(
        VenueOpeningError,
        match="every mandatory department must have a current declaration",
    ):
        checklist.snapshot()


def test_later_declaration_becomes_current_and_preserves_history() -> None:
    checklist = OpeningChecklist((department(),))
    not_ready = checklist.declare(
        department_id=" kitchen ",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.NOT_READY,
        declared_at=DECLARED_AT,
        reason="Preparation ongoing",
    )
    ready = checklist.declare(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=OPENED_AT,
    )

    assert checklist.current_declarations["kitchen"] is ready
    assert checklist.declaration_history == (not_ready, ready)
    assert checklist.missing_department_ids == ()
    assert checklist.snapshot() == (ready,)


def test_venue_starts_closed_with_approved_opening_scope() -> None:
    subject = venue()

    assert subject.venue_id == "venue-1"
    assert subject.name == "Emerald Beach Club"
    assert subject.business_date == BUSINESS_DATE
    assert subject.opening_status is OpeningStatus.CLOSED
    assert subject.opening_report is None
    assert subject.aggregate_version == 0
    assert subject.domain_events == ()


@pytest.mark.parametrize(
    ("field", "venue_id", "name"),
    [
        ("venue id", " ", "Emerald"),
        ("venue name", "venue-1", ""),
    ],
)
def test_venue_requires_identity(field: str, venue_id: str, name: str) -> None:
    with pytest.raises(VenueOpeningError, match=f"{field} is required"):
        Venue(
            venue_id=venue_id,
            name=name,
            business_date=BUSINESS_DATE,
            mandatory_departments=(department(),),
        )


def test_venue_records_only_the_official_readiness_event() -> None:
    subject = venue((department(),))

    declaration = subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.BLOCKED,
        declared_at=DECLARED_AT,
        reason="Equipment issue",
        comment="Maintenance is attending",
    )

    assert subject.opening_checklist.current_declarations["kitchen"] is declaration
    assert len(subject.domain_events) == 1
    event = subject.domain_events[0]
    assert isinstance(event, DepartmentReadinessDeclared)
    assert event.venue_id == subject.venue_id
    assert event.business_date == BUSINESS_DATE
    assert event.declaration is declaration
    assert event.occurred_at == DECLARED_AT
    assert subject.aggregate_version == 1


@pytest.mark.parametrize(
    ("departments", "expected"),
    [
        ((), "at least one mandatory department is required"),
        ((department(),), "every mandatory department must declare readiness"),
    ],
)
def test_policy_rejects_incomplete_opening_scope(
    departments: tuple[OperationalDepartment, ...],
    expected: str,
) -> None:
    checklist = OpeningChecklist(departments)

    with pytest.raises(VenueOpeningError, match=expected):
        VenueOpeningPolicy.ensure_can_open(
            checklist=checklist,
            opening_status=OpeningStatus.CLOSED,
            host_is_responsible=True,
            host_has_required_capability=True,
        )


@pytest.mark.parametrize("status", [ReadinessStatus.NOT_READY, ReadinessStatus.BLOCKED])
def test_policy_requires_every_current_declaration_to_be_ready(
    status: ReadinessStatus,
) -> None:
    checklist = OpeningChecklist((department(),))
    checklist.declare(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=status,
        declared_at=DECLARED_AT,
        reason="Still unresolved",
    )

    with pytest.raises(
        VenueOpeningError,
        match="every mandatory department must be READY",
    ):
        VenueOpeningPolicy.ensure_can_open(
            checklist=checklist,
            opening_status=OpeningStatus.CLOSED,
            host_is_responsible=True,
            host_has_required_capability=True,
        )


def test_policy_requires_host_responsibility() -> None:
    subject = venue((department(),))
    declare_all_ready(subject)

    with pytest.raises(
        VenueOpeningError,
        match="must hold Host responsibility",
    ):
        open_venue_with_authority(subject, host_is_responsible=False)


def test_policy_requires_explicit_capability() -> None:
    subject = venue((department(),))
    declare_all_ready(subject)

    with pytest.raises(
        VenueOpeningError,
        match="required Venue-opening Capability",
    ):
        open_venue_with_authority(subject, host_has_required_capability=False)


def open_venue_with_authority(
    subject: Venue,
    *,
    host_is_responsible: bool = True,
    host_has_required_capability: bool = True,
) -> OpeningReport:
    return subject.open_for_business_date(
        host_id="host-1",
        host_is_responsible=host_is_responsible,
        host_has_required_capability=host_has_required_capability,
        opened_at=OPENED_AT,
        policy=VenueOpeningPolicy(),
    )


def test_opening_requires_host_identity_and_timezone_aware_time() -> None:
    subject = venue((department(),))
    declare_all_ready(subject)

    with pytest.raises(VenueOpeningError, match="host id is required"):
        subject.open_for_business_date(
            host_id=" ",
            host_is_responsible=True,
            host_has_required_capability=True,
            opened_at=OPENED_AT,
            policy=VenueOpeningPolicy(),
        )

    with pytest.raises(
        VenueOpeningError,
        match="opening time must include a timezone",
    ):
        subject.open_for_business_date(
            host_id="host-1",
            host_is_responsible=True,
            host_has_required_capability=True,
            opened_at=datetime(2026, 7, 26, 8, 0),
            policy=VenueOpeningPolicy(),
        )


def test_successful_opening_creates_immutable_report_and_official_event() -> None:
    subject = venue()
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.NOT_READY,
        declared_at=DECLARED_AT,
        reason="Preparation ongoing",
        comment="Ten minutes remaining",
    )
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.BLOCKED,
        declared_at=DECLARED_AT,
        reason="Equipment issue",
    )
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=OPENED_AT,
    )
    subject.declare_department_readiness(
        department_id="bar",
        declared_by_id="staff-bar",
        status=ReadinessStatus.READY,
        declared_at=OPENED_AT,
    )

    report = open_venue(subject)

    assert subject.opening_status is OpeningStatus.OPEN
    assert subject.opening_report is report
    assert report.venue_id == subject.venue_id
    assert report.business_date == BUSINESS_DATE
    assert report.opened_at == OPENED_AT
    assert report.host_id == "host-1"
    assert len(report.department_readiness) == 2
    assert all(item.status is ReadinessStatus.READY for item in report.department_readiness)
    assert len(report.declaration_history) == 4
    assert len(report.delays) == 1
    assert len(report.blocking_issues) == 1
    assert subject.aggregate_version == 5

    event = subject.domain_events[-1]
    assert isinstance(event, VenueOpenedForBusinessDate)
    assert event.venue_id == subject.venue_id
    assert event.business_date == BUSINESS_DATE
    assert event.host_id == "host-1"
    assert event.opening_report is report
    assert event.occurred_at == OPENED_AT

    with pytest.raises(AttributeError):
        report.host_id = "someone-else"  # type: ignore[misc]


def test_venue_cannot_open_twice_or_change_readiness_after_opening() -> None:
    subject = venue((department(),))
    declare_all_ready(subject)
    open_venue(subject)

    with pytest.raises(VenueOpeningError, match="already open"):
        open_venue(subject)

    with pytest.raises(
        VenueOpeningError,
        match="cannot be changed after the Venue is open",
    ):
        subject.declare_department_readiness(
            department_id="kitchen",
            declared_by_id="staff-kitchen",
            status=ReadinessStatus.BLOCKED,
            declared_at=OPENED_AT,
            reason="New live issue",
        )


def test_failed_opening_changes_no_state_and_produces_no_opening_event() -> None:
    subject = venue((department(),))
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.BLOCKED,
        declared_at=DECLARED_AT,
        reason="Equipment issue",
    )
    events_before = subject.domain_events

    with pytest.raises(VenueOpeningError):
        open_venue(subject)

    assert subject.opening_status is OpeningStatus.CLOSED
    assert subject.opening_report is None
    assert subject.domain_events == events_before
    assert not any(isinstance(event, VenueOpenedForBusinessDate) for event in subject.domain_events)


def test_domain_events_are_pulled_once() -> None:
    subject = venue((department(),))
    declare_all_ready(subject)

    events = subject.pull_domain_events()

    assert len(events) == 1
    assert isinstance(events[0], DepartmentReadinessDeclared)
    assert subject.pull_domain_events() == ()


def test_opening_report_protects_required_facts() -> None:
    ready = DepartmentReadiness(
        department_id="kitchen",
        responsible_person_id="staff-kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=DECLARED_AT,
    )
    not_ready = DepartmentReadiness(
        department_id="kitchen",
        responsible_person_id="staff-kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.NOT_READY,
        declared_at=DECLARED_AT,
        reason="Preparation ongoing",
    )

    with pytest.raises(VenueOpeningError, match="venue id is required"):
        OpeningReport("", BUSINESS_DATE, OPENED_AT, "host-1", (ready,), (ready,))
    with pytest.raises(VenueOpeningError, match="host id is required"):
        OpeningReport("venue-1", BUSINESS_DATE, OPENED_AT, "", (ready,), (ready,))
    with pytest.raises(VenueOpeningError, match="opening time must include a timezone"):
        OpeningReport(
            "venue-1",
            BUSINESS_DATE,
            datetime(2026, 7, 26, 8, 0),
            "host-1",
            (ready,),
            (ready,),
        )
    with pytest.raises(
        VenueOpeningError,
        match="requires mandatory department readiness",
    ):
        OpeningReport("venue-1", BUSINESS_DATE, OPENED_AT, "host-1", (), ())
    with pytest.raises(
        VenueOpeningError,
        match="one current declaration per department",
    ):
        OpeningReport(
            "venue-1",
            BUSINESS_DATE,
            OPENED_AT,
            "host-1",
            (ready, ready),
            (ready,),
        )
    with pytest.raises(
        VenueOpeningError,
        match="only READY current declarations",
    ):
        OpeningReport(
            "venue-1",
            BUSINESS_DATE,
            OPENED_AT,
            "host-1",
            (not_ready,),
            (not_ready,),
        )


def open_state_for_restoration() -> tuple[
    tuple[OperationalDepartment, ...],
    tuple[DepartmentReadiness, ...],
    OpeningReport,
]:
    departments = (
        department(),
        department("bar", name="Bar", responsible_person_id="staff-bar"),
    )
    history = (
        DepartmentReadiness(
            department_id="kitchen",
            responsible_person_id="staff-kitchen",
            declared_by_id="staff-kitchen",
            status=ReadinessStatus.BLOCKED,
            declared_at=DECLARED_AT,
            reason="Equipment issue",
        ),
        DepartmentReadiness(
            department_id="kitchen",
            responsible_person_id="staff-kitchen",
            declared_by_id="staff-kitchen",
            status=ReadinessStatus.READY,
            declared_at=OPENED_AT,
        ),
        DepartmentReadiness(
            department_id="bar",
            responsible_person_id="staff-bar",
            declared_by_id="staff-bar",
            status=ReadinessStatus.READY,
            declared_at=OPENED_AT,
        ),
    )
    report = OpeningReport(
        venue_id="venue-1",
        business_date=BUSINESS_DATE,
        opened_at=OPENED_AT,
        host_id="host-1",
        department_readiness=(history[1], history[2]),
        declaration_history=history,
    )
    return departments, history, report


def test_restore_reproduces_open_state_without_replaying_actions_or_events() -> None:
    departments, history, report = open_state_for_restoration()

    with (
        patch.object(
            Venue,
            "declare_department_readiness",
            side_effect=AssertionError("declaration replayed"),
        ) as declare_action,
        patch.object(
            Venue,
            "open_for_business_date",
            side_effect=AssertionError("opening replayed"),
        ) as open_action,
    ):
        restored = Venue.restore(
            venue_id="venue-1",
            name="Emerald Beach Club",
            business_date=BUSINESS_DATE,
            mandatory_departments=departments,
            declaration_history=history,
            opening_status=OpeningStatus.OPEN,
            opening_report=report,
            aggregate_version=4,
        )

    declare_action.assert_not_called()
    open_action.assert_not_called()
    assert restored.venue_id == "venue-1"
    assert restored.name == "Emerald Beach Club"
    assert restored.business_date == BUSINESS_DATE
    assert restored.opening_status is OpeningStatus.OPEN
    assert restored.opening_report is report
    assert restored.opening_checklist.declaration_history == history
    assert restored.opening_checklist.snapshot() == report.department_readiness
    assert restored.aggregate_version == 4
    assert restored.domain_events == ()


def test_restore_reproduces_closed_state_and_preserves_normal_mutation_rules() -> None:
    departments = (department(),)
    declaration = DepartmentReadiness(
        department_id="kitchen",
        responsible_person_id="staff-kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.NOT_READY,
        declared_at=DECLARED_AT,
        reason="Preparation ongoing",
    )
    restored = Venue.restore(
        venue_id="venue-1",
        name="Emerald Beach Club",
        business_date=BUSINESS_DATE,
        mandatory_departments=departments,
        declaration_history=(declaration,),
        opening_status=OpeningStatus.CLOSED,
        opening_report=None,
        aggregate_version=1,
    )

    assert restored.domain_events == ()
    assert restored.aggregate_version == 1
    restored.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=OPENED_AT,
    )
    assert restored.aggregate_version == 2
    assert len(restored.domain_events) == 1


@pytest.mark.parametrize("aggregate_version", [-1, True, 1.5])
def test_restore_rejects_invalid_aggregate_version(aggregate_version: object) -> None:
    with pytest.raises(
        VenueOpeningError,
        match="aggregate version must be a non-negative integer",
    ):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=(),
            declaration_history=(),
            opening_status=OpeningStatus.CLOSED,
            opening_report=None,
            aggregate_version=aggregate_version,  # type: ignore[arg-type]
        )


def test_restore_rejects_unknown_opening_status() -> None:
    with pytest.raises(VenueOpeningError, match="opening status must be CLOSED or OPEN"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=(),
            declaration_history=(),
            opening_status="UNKNOWN",  # type: ignore[arg-type]
            opening_report=None,
            aggregate_version=0,
        )


def test_restore_rejects_declaration_for_unknown_department() -> None:
    declaration = DepartmentReadiness(
        department_id="bar",
        responsible_person_id="staff-bar",
        declared_by_id="staff-bar",
        status=ReadinessStatus.READY,
        declared_at=DECLARED_AT,
    )

    with pytest.raises(VenueOpeningError, match="must belong to a mandatory department"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=(department(),),
            declaration_history=(declaration,),
            opening_status=OpeningStatus.CLOSED,
            opening_report=None,
            aggregate_version=1,
        )


def test_restore_rejects_changed_department_responsibility() -> None:
    declaration = DepartmentReadiness(
        department_id="kitchen",
        responsible_person_id="former-responsible",
        declared_by_id="former-responsible",
        status=ReadinessStatus.READY,
        declared_at=DECLARED_AT,
    )

    with pytest.raises(VenueOpeningError, match="responsible person must match"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=(department(),),
            declaration_history=(declaration,),
            opening_status=OpeningStatus.CLOSED,
            opening_report=None,
            aggregate_version=1,
        )


def test_restore_rejects_out_of_order_declaration_history() -> None:
    later = DepartmentReadiness(
        department_id="kitchen",
        responsible_person_id="staff-kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=OPENED_AT,
    )
    earlier = DepartmentReadiness(
        department_id="kitchen",
        responsible_person_id="staff-kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.NOT_READY,
        declared_at=DECLARED_AT,
        reason="Preparation ongoing",
    )

    with pytest.raises(VenueOpeningError, match="chronological order"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=(department(),),
            declaration_history=(later, earlier),
            opening_status=OpeningStatus.CLOSED,
            opening_report=None,
            aggregate_version=2,
        )


def test_restore_rejects_report_state_inconsistent_with_venue() -> None:
    departments, history, report = open_state_for_restoration()

    with pytest.raises(VenueOpeningError, match="open restored Venue requires"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=departments,
            declaration_history=history,
            opening_status=OpeningStatus.OPEN,
            opening_report=None,
            aggregate_version=4,
        )

    with pytest.raises(VenueOpeningError, match="must match the Venue and Business Date"):
        Venue.restore(
            venue_id="different-venue",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=departments,
            declaration_history=history,
            opening_status=OpeningStatus.OPEN,
            opening_report=report,
            aggregate_version=4,
        )

    with pytest.raises(VenueOpeningError, match="closed restored Venue cannot have"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=departments,
            declaration_history=history,
            opening_status=OpeningStatus.CLOSED,
            opening_report=report,
            aggregate_version=3,
        )


def test_restore_rejects_report_history_or_current_snapshot_mismatch() -> None:
    departments, history, report = open_state_for_restoration()
    report_with_short_history = OpeningReport(
        venue_id="venue-1",
        business_date=BUSINESS_DATE,
        opened_at=OPENED_AT,
        host_id="host-1",
        department_readiness=report.department_readiness,
        declaration_history=history[1:],
    )
    stale_report = OpeningReport(
        venue_id="venue-1",
        business_date=BUSINESS_DATE,
        opened_at=OPENED_AT,
        host_id="host-1",
        department_readiness=(history[2], history[1]),
        declaration_history=history,
    )

    with pytest.raises(VenueOpeningError, match="preserve declaration history"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=departments,
            declaration_history=history,
            opening_status=OpeningStatus.OPEN,
            opening_report=report_with_short_history,
            aggregate_version=4,
        )

    with pytest.raises(VenueOpeningError, match="match current department readiness"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=departments,
            declaration_history=history,
            opening_status=OpeningStatus.OPEN,
            opening_report=stale_report,
            aggregate_version=4,
        )


def test_restore_rejects_version_that_does_not_match_mutation_history() -> None:
    with pytest.raises(VenueOpeningError, match="must match the restored Venue mutation history"):
        Venue.restore(
            venue_id="venue-1",
            name="Emerald",
            business_date=BUSINESS_DATE,
            mandatory_departments=(),
            declaration_history=(),
            opening_status=OpeningStatus.CLOSED,
            opening_report=None,
            aggregate_version=1,
        )
