"""Orchestration tests for the Venue Opening Application Layer."""

from __future__ import annotations

from datetime import UTC, date, datetime
from types import TracebackType
from unittest.mock import Mock

import pytest

from beachos_api.packs.beachos.venue_opening.application import (
    ActivityLogRecord,
    AuthorizationDeniedError,
    BusinessRuleRejectedError,
    CommandValidationError,
    DeclareDepartmentReadinessCommand,
    OpenVenueCommand,
    VenueContextMismatchError,
    VenueNotFoundError,
    VenueOpeningService,
)
from beachos_api.packs.beachos.venue_opening.application.ports import (
    ActivityLog,
    VenueOpeningUnitOfWork,
    VenueRepository,
)
from beachos_api.packs.beachos.venue_opening.domain import (
    BusinessDate,
    DepartmentReadinessDeclared,
    OperationalDepartment,
    ReadinessStatus,
    Venue,
    VenueOpenedForBusinessDate,
    VenueOpeningPolicy,
)

BUSINESS_DATE = BusinessDate(date(2026, 7, 26))
NOW = datetime(2026, 7, 26, 7, 45, tzinfo=UTC)


class FakeCapabilities:
    def __init__(
        self,
        *,
        can_declare: bool = True,
        can_open: bool = True,
    ) -> None:
        self.can_declare = can_declare
        self.can_open = can_open
        self.declare_calls: list[tuple[str, str, str]] = []
        self.open_calls: list[tuple[str, str]] = []

    def can_declare_department_readiness(
        self,
        *,
        actor_id: str,
        venue_id: str,
        department_id: str,
    ) -> bool:
        self.declare_calls.append((actor_id, venue_id, department_id))
        return self.can_declare

    def can_open_venue(self, *, actor_id: str, venue_id: str) -> bool:
        self.open_calls.append((actor_id, venue_id))
        return self.can_open


class FakeHostResponsibilities:
    def __init__(self, responsible: bool = True) -> None:
        self.responsible = responsible
        self.calls: list[tuple[str, str]] = []

    def is_responsible_host(self, *, actor_id: str, venue_id: str) -> bool:
        self.calls.append((actor_id, venue_id))
        return self.responsible


class FakeBusinessDates:
    def __init__(self, business_date: BusinessDate = BUSINESS_DATE) -> None:
        self.business_date = business_date
        self.calls: list[str] = []

    def current_for(self, *, venue_id: str) -> BusinessDate:
        self.calls.append(venue_id)
        return self.business_date


class FakeClock:
    def __init__(self, now: datetime = NOW) -> None:
        self.value = now
        self.calls = 0

    def now(self) -> datetime:
        self.calls += 1
        return self.value


class FakeVenueRepository:
    def __init__(self, venue: Venue | None) -> None:
        self.venue = venue
        self.get_calls: list[tuple[str, BusinessDate]] = []
        self.saved: list[Venue] = []

    def get(
        self,
        *,
        venue_id: str,
        business_date: BusinessDate,
    ) -> Venue | None:
        self.get_calls.append((venue_id, business_date))
        return self.venue

    def save(self, venue: Venue) -> None:
        self.saved.append(venue)


class FakeActivityLog:
    def __init__(self) -> None:
        self.records: list[ActivityLogRecord] = []

    def record_venue_opened(self, record: ActivityLogRecord) -> None:
        self.records.append(record)


class FakeUnitOfWork:
    venues: VenueRepository
    activity_log: ActivityLog

    def __init__(
        self,
        repository: FakeVenueRepository,
        activity_log: FakeActivityLog,
    ) -> None:
        self.venues = repository
        self.activity_log = activity_log
        self.entered = 0
        self.exited = 0
        self.exit_exception_type: type[BaseException] | None = None
        self.commits = 0

    def __enter__(self) -> FakeUnitOfWork:
        self.entered += 1
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exception, traceback
        self.exited += 1
        self.exit_exception_type = exception_type

    def commit(self) -> None:
        self.commits += 1


class FakeUnitOfWorkFactory:
    def __init__(self, unit_of_work: FakeUnitOfWork) -> None:
        self.unit_of_work = unit_of_work
        self.calls = 0

    def create(self) -> VenueOpeningUnitOfWork:
        self.calls += 1
        return self.unit_of_work


def create_venue(
    *,
    venue_id: str = "venue-1",
    business_date: BusinessDate = BUSINESS_DATE,
) -> Venue:
    return Venue(
        venue_id=venue_id,
        name="Emerald Beach Club",
        business_date=business_date,
        mandatory_departments=(
            OperationalDepartment("kitchen", "Kitchen", "staff-kitchen"),
            OperationalDepartment("bar", "Bar", "staff-bar"),
        ),
    )


def make_service(
    venue: Venue | None,
    *,
    capabilities: FakeCapabilities | None = None,
    host_responsibilities: FakeHostResponsibilities | None = None,
    business_dates: FakeBusinessDates | None = None,
    clock: FakeClock | None = None,
) -> tuple[
    VenueOpeningService,
    FakeCapabilities,
    FakeHostResponsibilities,
    FakeBusinessDates,
    FakeClock,
    FakeVenueRepository,
    FakeActivityLog,
    FakeUnitOfWork,
    FakeUnitOfWorkFactory,
]:
    capability_port = capabilities or FakeCapabilities()
    host_port = host_responsibilities or FakeHostResponsibilities()
    date_port = business_dates or FakeBusinessDates()
    clock_port = clock or FakeClock()
    repository = FakeVenueRepository(venue)
    activity_log = FakeActivityLog()
    unit_of_work = FakeUnitOfWork(repository, activity_log)
    factory = FakeUnitOfWorkFactory(unit_of_work)
    service = VenueOpeningService(
        capabilities=capability_port,
        host_responsibilities=host_port,
        business_dates=date_port,
        clock=clock_port,
        unit_of_work_factory=factory,
        policy=VenueOpeningPolicy(),
    )
    return (
        service,
        capability_port,
        host_port,
        date_port,
        clock_port,
        repository,
        activity_log,
        unit_of_work,
        factory,
    )


@pytest.mark.parametrize(
    ("command_type", "field", "values"),
    [
        (OpenVenueCommand, "request id", ("", "host-1", "venue-1")),
        (OpenVenueCommand, "actor id", ("request-1", " ", "venue-1")),
        (OpenVenueCommand, "venue id", ("request-1", "host-1", "\t")),
    ],
)
def test_open_command_requires_structural_identity(
    command_type: type[OpenVenueCommand],
    field: str,
    values: tuple[str, str, str],
) -> None:
    with pytest.raises(CommandValidationError, match=f"{field} is required"):
        command_type(*values)


@pytest.mark.parametrize(
    ("field", "values"),
    [
        ("request id", ("", "staff-kitchen", "venue-1", "kitchen")),
        ("actor id", ("request-1", "", "venue-1", "kitchen")),
        ("venue id", ("request-1", "staff-kitchen", "", "kitchen")),
        ("department id", ("request-1", "staff-kitchen", "venue-1", "")),
    ],
)
def test_declaration_command_requires_structural_identity(
    field: str,
    values: tuple[str, str, str, str],
) -> None:
    with pytest.raises(CommandValidationError, match=f"{field} is required"):
        DeclareDepartmentReadinessCommand(*values, ReadinessStatus.READY)


def test_commands_normalize_identity_without_deciding_business_rules() -> None:
    open_command = OpenVenueCommand(" request-1 ", " host-1 ", " venue-1 ")
    declaration_command = DeclareDepartmentReadinessCommand(
        " request-2 ",
        " staff-kitchen ",
        " venue-1 ",
        " kitchen ",
        ReadinessStatus.BLOCKED,
        reason="Equipment issue",
    )

    assert (open_command.request_id, open_command.actor_id, open_command.venue_id) == (
        "request-1",
        "host-1",
        "venue-1",
    )
    assert declaration_command.request_id == "request-2"
    assert declaration_command.actor_id == "staff-kitchen"
    assert declaration_command.venue_id == "venue-1"
    assert declaration_command.department_id == "kitchen"


def test_declare_readiness_orchestrates_ports_domain_save_and_commit() -> None:
    subject = create_venue()
    (
        service,
        capabilities,
        _,
        business_dates,
        clock,
        repository,
        activity_log,
        unit_of_work,
        factory,
    ) = make_service(subject)
    commit_mock = Mock(wraps=unit_of_work.commit)
    unit_of_work.commit = commit_mock  # type: ignore[method-assign]
    command = DeclareDepartmentReadinessCommand(
        request_id="request-1",
        actor_id="staff-kitchen",
        venue_id="venue-1",
        department_id="kitchen",
        status=ReadinessStatus.BLOCKED,
        reason="Equipment issue",
        comment="Maintenance is attending",
    )

    result = service.declare_department_readiness(command)

    assert business_dates.calls == ["venue-1"]
    assert capabilities.declare_calls == [("staff-kitchen", "venue-1", "kitchen")]
    assert repository.get_calls == [("venue-1", BUSINESS_DATE)]
    assert clock.calls == 1
    assert repository.saved == [subject]
    assert activity_log.records == []
    assert unit_of_work.entered == unit_of_work.exited == unit_of_work.commits == 1
    commit_mock.assert_called_once_with()
    assert unit_of_work.exit_exception_type is None
    assert factory.calls == 1
    assert result.request_id == "request-1"
    assert result.venue_id == "venue-1"
    assert result.business_date == BUSINESS_DATE.value
    assert result.declaration.department_id == "kitchen"
    assert result.declaration.responsible_person_id == "staff-kitchen"
    assert result.declaration.declared_by_id == "staff-kitchen"
    assert result.declaration.status == "BLOCKED"
    assert result.declaration.declared_at == NOW
    assert result.declaration.reason == "Equipment issue"
    assert result.declaration.comment == "Maintenance is attending"
    assert isinstance(subject.domain_events[-1], DepartmentReadinessDeclared)


def test_department_owner_context_contains_only_owned_department_and_history() -> None:
    subject = create_venue()
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.BLOCKED,
        declared_at=NOW,
        reason="Equipment issue",
    )
    subject.declare_department_readiness(
        department_id="bar",
        declared_by_id="staff-bar",
        status=ReadinessStatus.READY,
        declared_at=NOW,
    )
    service, capabilities, _, _, _, repository, _, unit_of_work, _ = make_service(subject)

    result = service.get_department_owner_context(
        actor_id="staff-kitchen",
        venue_id="venue-1",
    )

    assert [department.department_id for department in result.departments] == ["kitchen"]
    assert result.departments[0].current_readiness is not None
    assert result.departments[0].current_readiness.status == "BLOCKED"
    assert [item.department_id for item in result.declaration_history] == ["kitchen"]
    assert capabilities.declare_calls == [("staff-kitchen", "venue-1", "kitchen")]
    assert repository.saved == []
    assert unit_of_work.commits == 0


@pytest.mark.parametrize("actor_id", ["staff-unknown", "staff-kitchen"])
def test_department_owner_context_denies_unassigned_or_uncapable_actor(actor_id: str) -> None:
    subject = create_venue()
    capabilities = FakeCapabilities(can_declare=actor_id != "staff-kitchen")
    service, _, _, _, _, _, _, _, _ = make_service(subject, capabilities=capabilities)

    with pytest.raises(AuthorizationDeniedError, match="not a configured department owner"):
        service.get_department_owner_context(actor_id=actor_id, venue_id="venue-1")


def test_declaration_authorization_denial_stops_before_loading_or_time() -> None:
    subject = create_venue()
    capabilities = FakeCapabilities(can_declare=False)
    (
        service,
        _,
        _,
        business_dates,
        clock,
        repository,
        _,
        unit_of_work,
        factory,
    ) = make_service(subject, capabilities=capabilities)
    command = DeclareDepartmentReadinessCommand(
        "request-1",
        "staff-kitchen",
        "venue-1",
        "kitchen",
        ReadinessStatus.READY,
    )

    with pytest.raises(AuthorizationDeniedError, match="lacks authority"):
        service.declare_department_readiness(command)

    assert business_dates.calls == ["venue-1"]
    assert repository.get_calls == []
    assert clock.calls == 0
    assert unit_of_work.commits == 0
    assert factory.calls == 0


@pytest.mark.parametrize(
    ("actor_id", "status", "reason", "expected"),
    [
        (
            "staff-kitchen",
            ReadinessStatus.BLOCKED,
            None,
            "NOT READY and BLOCKED require a reason",
        ),
        (
            "host-1",
            ReadinessStatus.READY,
            None,
            "only the department's responsible person",
        ),
    ],
)
def test_domain_rejection_is_translated_without_saving(
    actor_id: str,
    status: ReadinessStatus,
    reason: str | None,
    expected: str,
) -> None:
    subject = create_venue()
    service, _, _, _, _, repository, _, unit_of_work, _ = make_service(subject)
    command = DeclareDepartmentReadinessCommand(
        "request-1",
        actor_id,
        "venue-1",
        "kitchen",
        status,
        reason=reason,
    )

    with pytest.raises(BusinessRuleRejectedError, match=expected) as raised:
        service.declare_department_readiness(command)

    assert raised.value.__cause__ is not None
    assert repository.saved == []
    assert unit_of_work.commits == 0
    assert unit_of_work.exit_exception_type is BusinessRuleRejectedError


def test_missing_venue_is_an_explicit_application_failure() -> None:
    service, _, _, _, clock, repository, _, unit_of_work, _ = make_service(None)
    command = DeclareDepartmentReadinessCommand(
        "request-1",
        "staff-kitchen",
        "venue-1",
        "kitchen",
        ReadinessStatus.READY,
    )

    with pytest.raises(VenueNotFoundError, match="not found"):
        service.declare_department_readiness(command)

    assert repository.get_calls == [("venue-1", BUSINESS_DATE)]
    assert clock.calls == 0
    assert unit_of_work.commits == 0
    assert unit_of_work.exit_exception_type is VenueNotFoundError


@pytest.mark.parametrize(
    "returned_venue",
    [
        create_venue(venue_id="venue-2"),
        create_venue(business_date=BusinessDate(date(2026, 7, 25))),
    ],
)
def test_repository_context_mismatch_is_rejected(returned_venue: Venue) -> None:
    service, _, _, _, _, repository, _, unit_of_work, _ = make_service(returned_venue)
    command = DeclareDepartmentReadinessCommand(
        "request-1",
        "staff-kitchen",
        "venue-1",
        "kitchen",
        ReadinessStatus.READY,
    )

    with pytest.raises(VenueContextMismatchError, match="outside the requested"):
        service.declare_department_readiness(command)

    assert repository.saved == []
    assert unit_of_work.commits == 0


def mark_all_ready(subject: Venue) -> None:
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=NOW,
    )
    subject.declare_department_readiness(
        department_id="bar",
        declared_by_id="staff-bar",
        status=ReadinessStatus.READY,
        declared_at=NOW,
    )
    subject.pull_domain_events()


def test_open_venue_orchestrates_authority_domain_activity_and_commit() -> None:
    subject = create_venue()
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.BLOCKED,
        declared_at=NOW,
        reason="Equipment issue",
    )
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=NOW,
    )
    subject.declare_department_readiness(
        department_id="bar",
        declared_by_id="staff-bar",
        status=ReadinessStatus.READY,
        declared_at=NOW,
    )
    subject.pull_domain_events()
    (
        service,
        capabilities,
        host_responsibilities,
        business_dates,
        clock,
        repository,
        activity_log,
        unit_of_work,
        factory,
    ) = make_service(subject)

    result = service.open_venue(OpenVenueCommand("request-open", "host-1", "venue-1"))

    assert business_dates.calls == ["venue-1"]
    assert capabilities.open_calls == [("host-1", "venue-1")]
    assert host_responsibilities.calls == [("host-1", "venue-1")]
    assert repository.get_calls == [("venue-1", BUSINESS_DATE)]
    assert clock.calls == 1
    assert repository.saved == [subject]
    assert unit_of_work.entered == unit_of_work.exited == unit_of_work.commits == 1
    assert factory.calls == 1
    assert activity_log.records == [
        ActivityLogRecord(
            request_id="request-open",
            actor_id="host-1",
            venue_id="venue-1",
            business_date=BUSINESS_DATE.value,
            occurred_at=NOW,
        )
    ]
    assert result.request_id == "request-open"
    assert result.report.venue_id == "venue-1"
    assert result.report.business_date == BUSINESS_DATE.value
    assert result.report.opened_at == NOW
    assert result.report.host_id == "host-1"
    assert len(result.report.department_readiness) == 2
    assert len(result.report.declaration_history) == 3
    assert result.report.delays == ()
    assert len(result.report.blocking_issues) == 1
    assert isinstance(subject.domain_events[-1], VenueOpenedForBusinessDate)


def test_open_capability_denial_stops_all_remaining_orchestration() -> None:
    subject = create_venue()
    capabilities = FakeCapabilities(can_open=False)
    (
        service,
        _,
        host_responsibilities,
        business_dates,
        clock,
        repository,
        activity_log,
        unit_of_work,
        factory,
    ) = make_service(subject, capabilities=capabilities)

    with pytest.raises(AuthorizationDeniedError, match="lacks authority"):
        service.open_venue(OpenVenueCommand("request-1", "host-1", "venue-1"))

    assert business_dates.calls == ["venue-1"]
    assert host_responsibilities.calls == []
    assert repository.get_calls == []
    assert clock.calls == 0
    assert activity_log.records == []
    assert unit_of_work.commits == 0
    assert factory.calls == 0


def test_host_responsibility_fact_is_decided_by_domain_policy() -> None:
    subject = create_venue()
    mark_all_ready(subject)
    host_responsibilities = FakeHostResponsibilities(responsible=False)
    service, _, _, _, _, repository, activity_log, unit_of_work, _ = make_service(
        subject,
        host_responsibilities=host_responsibilities,
    )

    with pytest.raises(BusinessRuleRejectedError, match="Host responsibility"):
        service.open_venue(OpenVenueCommand("request-1", "host-1", "venue-1"))

    assert repository.saved == []
    assert activity_log.records == []
    assert unit_of_work.commits == 0


def test_opening_readiness_rejection_is_domain_owned() -> None:
    subject = create_venue()
    service, _, _, _, _, repository, activity_log, unit_of_work, _ = make_service(subject)

    with pytest.raises(BusinessRuleRejectedError, match="must declare readiness"):
        service.open_venue(OpenVenueCommand("request-1", "host-1", "venue-1"))

    assert repository.saved == []
    assert activity_log.records == []
    assert unit_of_work.commits == 0


def test_technical_port_failure_is_not_misreported_as_business_rejection() -> None:
    class FailingClock:
        def now(self) -> datetime:
            raise RuntimeError("clock unavailable")

    subject = create_venue()
    mark_all_ready(subject)
    service, _, _, _, _, repository, activity_log, unit_of_work, _ = make_service(
        subject,
        clock=FailingClock(),  # type: ignore[arg-type]
    )

    with pytest.raises(RuntimeError, match="clock unavailable"):
        service.open_venue(OpenVenueCommand("request-1", "host-1", "venue-1"))

    assert repository.saved == []
    assert activity_log.records == []
    assert unit_of_work.commits == 0
    assert unit_of_work.exit_exception_type is RuntimeError


def test_activity_log_failure_prevents_commit_and_remains_technical() -> None:
    class FailingActivityLog:
        def record_venue_opened(self, record: ActivityLogRecord) -> None:
            del record
            raise RuntimeError("activity log unavailable")

    subject = create_venue()
    mark_all_ready(subject)
    (
        service,
        _,
        _,
        _,
        _,
        repository,
        _,
        unit_of_work,
        _,
    ) = make_service(subject)
    unit_of_work.activity_log = FailingActivityLog()

    with pytest.raises(RuntimeError, match="activity log unavailable"):
        service.open_venue(OpenVenueCommand("request-1", "host-1", "venue-1"))

    assert repository.saved == [subject]
    assert unit_of_work.commits == 0
    assert unit_of_work.exit_exception_type is RuntimeError
