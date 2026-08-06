"""PostgreSQL 17 integration tests for Venue Opening Infrastructure."""

from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import UTC, date, datetime
from uuid import uuid4

import psycopg
import pytest
from psycopg import errors, sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from beachos_api.packs.beachos.venue_opening.application import (
    DeclareDepartmentReadinessCommand,
    OpenVenueCommand,
    VenueOpeningService,
)
from beachos_api.packs.beachos.venue_opening.domain import (
    BusinessDate,
    OpeningStatus,
    OperationalDepartment,
    ReadinessStatus,
    Venue,
    VenueOpeningPolicy,
)
from beachos_api.packs.beachos.venue_opening.infrastructure import (
    PostgresBusinessDateProvider,
    PostgresVenueOpeningUnitOfWork,
    PostgresVenueOpeningUnitOfWorkFactory,
    SystemClock,
    apply_migrations,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.errors import (
    AggregateNotLoadedError,
    BusinessDatePolicyNotFoundError,
    InfrastructureError,
    MigrationChecksumError,
    OptimisticConcurrencyError,
)

pytestmark = pytest.mark.integration

BUSINESS_DATE = BusinessDate(date(2026, 7, 26))
NOW = datetime(2026, 7, 26, 8, 0, tzinfo=UTC)


@pytest.fixture
def postgres_connection_string() -> Iterator[str]:
    base_connection_string = os.environ.get("BEACHOS_TEST_DATABASE_URL")
    if base_connection_string is None:
        pytest.fail("BEACHOS_TEST_DATABASE_URL is required for PostgreSQL integration tests")

    parameters = conninfo_to_dict(base_connection_string)
    host = parameters.get("host", "")
    if host not in {"127.0.0.1", "localhost", "::1"}:
        pytest.fail("integration tests require an isolated local PostgreSQL instance")

    schema_name = f"beachos_test_{uuid4().hex}"
    with psycopg.connect(base_connection_string, autocommit=True) as connection:
        if connection.info.server_version // 10000 != 17:
            pytest.fail("integration tests require PostgreSQL 17")
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name)))

    isolated_connection_string = make_conninfo(
        base_connection_string,
        options=f"-c search_path={schema_name}",
    )
    try:
        apply_migrations(isolated_connection_string)
        yield isolated_connection_string
    finally:
        with psycopg.connect(base_connection_string, autocommit=True) as connection:
            connection.execute(
                sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema_name))
            )


def create_venue(venue_id: str = "venue-1") -> Venue:
    return Venue(
        venue_id=venue_id,
        name="Emerald Beach Club",
        business_date=BUSINESS_DATE,
        mandatory_departments=(
            OperationalDepartment("kitchen", "Kitchen", "staff-kitchen"),
            OperationalDepartment("bar", "Bar", "staff-bar"),
        ),
    )


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


def persist(
    factory: PostgresVenueOpeningUnitOfWorkFactory,
    subject: Venue,
) -> None:
    with factory.create() as unit_of_work:
        unit_of_work.venues.save(subject)
        unit_of_work.commit()


class AllowedCapabilities:
    def can_declare_department_readiness(
        self,
        *,
        actor_id: str,
        venue_id: str,
        department_id: str,
    ) -> bool:
        del actor_id, venue_id, department_id
        return True

    def can_open_venue(self, *, actor_id: str, venue_id: str) -> bool:
        del actor_id, venue_id
        return True


class ResponsibleHost:
    def is_responsible_host(self, *, actor_id: str, venue_id: str) -> bool:
        del actor_id, venue_id
        return True


class FixedBusinessDate:
    def current_for(self, *, venue_id: str) -> BusinessDate:
        del venue_id
        return BUSINESS_DATE


class FixedClock:
    def __init__(self, value: datetime = NOW) -> None:
        self.value = value

    def now(self) -> datetime:
        return self.value


def service(connection_string: str) -> VenueOpeningService:
    return VenueOpeningService(
        capabilities=AllowedCapabilities(),
        host_responsibilities=ResponsibleHost(),
        business_dates=FixedBusinessDate(),
        clock=FixedClock(),
        unit_of_work_factory=PostgresVenueOpeningUnitOfWorkFactory(connection_string),
        policy=VenueOpeningPolicy(),
    )


def test_migrations_are_versioned_idempotent_and_checksummed(
    postgres_connection_string: str,
) -> None:
    apply_migrations(postgres_connection_string)
    with psycopg.connect(postgres_connection_string) as connection:
        applied = connection.execute(
            """
            SELECT version, migration_name
            FROM beachos_schema_migrations
            """
        ).fetchall()
        assert applied == [
            ("0001", "0001_venue_opening.sql"),
            ("0002", "0002_ordering.sql"),
            ("0003", "0003_kitchen_operations.sql"),
            ("0004", "0004_guest_arrival.sql"),
            ("0005", "0005_bar_operations.sql"),
            ("0006", "0006_basic_fulfilment.sql"),
            ("0007", "0007_cash_payments.sql"),
            ("0008", "0008_bill_closing.sql"),
            ("0009", "0009_customer_group_completion.sql"),
            ("0010", "0010_guest_departure.sql"),
            ("0011", "0011_venue_closing.sql"),
        ]
        connection.execute(
            """
            UPDATE beachos_schema_migrations
            SET checksum = 'invalid'
            WHERE version = '0001'
            """
        )

    with pytest.raises(MigrationChecksumError, match="different checksum"):
        apply_migrations(postgres_connection_string)


def test_aggregate_persistence_and_closed_restoration(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    subject = create_venue()
    subject.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.BLOCKED,
        declared_at=NOW,
        reason="Equipment issue",
        comment="Maintenance attending",
    )
    expected_events = subject.pull_domain_events()
    persist(factory, subject)

    with factory.create() as unit_of_work:
        restored = unit_of_work.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )

    assert restored is not None
    assert restored.name == subject.name
    assert restored.opening_status is OpeningStatus.CLOSED
    assert restored.opening_report is None
    assert restored.aggregate_version == 1
    assert restored.domain_events == ()
    assert restored.opening_checklist.declaration_history == (
        expected_events[0].declaration,  # type: ignore[union-attr]
    )
    assert tuple(restored.opening_checklist.departments) == ("kitchen", "bar")


def test_open_aggregate_report_and_activity_log_are_restored_atomically(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    subject = create_venue()
    mark_all_ready(subject)
    subject.pull_domain_events()
    persist(factory, subject)

    result = service(postgres_connection_string).open_venue(
        OpenVenueCommand("request-open", "host-1", "venue-1")
    )

    with factory.create() as unit_of_work:
        restored = unit_of_work.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )
    with psycopg.connect(postgres_connection_string) as connection:
        activity = connection.execute(
            """
            SELECT request_id, actor_id, action_name, occurred_at
            FROM venue_opening_activity_log
            """
        ).fetchone()

    assert restored is not None
    assert restored.opening_status is OpeningStatus.OPEN
    assert restored.aggregate_version == 3
    assert restored.opening_report is not None
    assert restored.opening_report.host_id == "host-1"
    assert restored.opening_report.opened_at == NOW
    assert len(restored.opening_report.department_readiness) == 2
    assert restored.domain_events == ()
    assert result.report.business_date == BUSINESS_DATE.value
    assert activity == (
        "request-open",
        "host-1",
        "VENUE_OPENED_FOR_BUSINESS_DATE",
        NOW,
    )


def test_repository_can_persist_an_authoritative_new_open_aggregate(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    subject = create_venue()
    mark_all_ready(subject)
    subject.open_for_business_date(
        host_id="host-1",
        host_is_responsible=True,
        host_has_required_capability=True,
        opened_at=NOW,
        policy=VenueOpeningPolicy(),
    )
    subject.pull_domain_events()

    persist(factory, subject)

    with factory.create() as unit_of_work:
        restored = unit_of_work.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )
    assert restored is not None
    assert restored.opening_status is OpeningStatus.OPEN
    assert restored.opening_report is not None
    assert restored.opening_report.host_id == "host-1"
    assert restored.aggregate_version == 3
    assert restored.domain_events == ()


def test_transaction_rolls_back_when_unit_of_work_is_not_committed(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    subject = create_venue()

    with factory.create() as unit_of_work:
        unit_of_work.venues.save(subject)

    with factory.create() as unit_of_work:
        assert (
            unit_of_work.venues.get(
                venue_id="venue-1",
                business_date=BUSINESS_DATE,
            )
            is None
        )


def test_optimistic_concurrency_rejects_stale_aggregate(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    persist(factory, create_venue())

    with factory.create() as first, factory.create() as second:
        first_venue = first.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )
        second_venue = second.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )
        assert first_venue is not None
        assert second_venue is not None

        first_venue.declare_department_readiness(
            department_id="kitchen",
            declared_by_id="staff-kitchen",
            status=ReadinessStatus.READY,
            declared_at=NOW,
        )
        second_venue.declare_department_readiness(
            department_id="bar",
            declared_by_id="staff-bar",
            status=ReadinessStatus.READY,
            declared_at=NOW,
        )
        first.venues.save(first_venue)
        first.commit()

        with pytest.raises(OptimisticConcurrencyError, match="changed after"):
            second.venues.save(second_venue)

    with factory.create() as unit_of_work:
        restored = unit_of_work.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )
    assert restored is not None
    assert tuple(restored.opening_checklist.current_declarations) == ("kitchen",)
    assert restored.aggregate_version == 1


def test_activity_log_failure_rolls_back_opening_report_and_venue_state(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    first = create_venue("venue-1")
    second = create_venue("venue-2")
    mark_all_ready(first)
    mark_all_ready(second)
    first.pull_domain_events()
    second.pull_domain_events()
    persist(factory, first)
    persist(factory, second)
    application = service(postgres_connection_string)
    application.open_venue(OpenVenueCommand("duplicate-request", "host-1", "venue-1"))

    with pytest.raises(errors.UniqueViolation):
        application.open_venue(OpenVenueCommand("duplicate-request", "host-1", "venue-2"))

    with factory.create() as unit_of_work:
        restored = unit_of_work.venues.get(
            venue_id="venue-2",
            business_date=BUSINESS_DATE,
        )
    with psycopg.connect(postgres_connection_string) as connection:
        report_count = connection.execute(
            """
            SELECT count(*)
            FROM venue_opening_reports
            WHERE venue_id = 'venue-2'
            """
        ).fetchone()
        activity_count = connection.execute(
            "SELECT count(*) FROM venue_opening_activity_log"
        ).fetchone()

    assert restored is not None
    assert restored.opening_status is OpeningStatus.CLOSED
    assert restored.opening_report is None
    assert restored.aggregate_version == 2
    assert report_count == (0,)
    assert activity_count == (1,)


def test_historical_declarations_reports_and_activity_logs_are_immutable(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    subject = create_venue()
    mark_all_ready(subject)
    subject.pull_domain_events()
    persist(factory, subject)
    service(postgres_connection_string).open_venue(
        OpenVenueCommand("request-open", "host-1", "venue-1")
    )

    protected_statements = (
        "DELETE FROM venue_opening_declarations",
        "UPDATE venue_opening_reports SET host_id = 'different-host'",
        "DELETE FROM venue_opening_activity_log",
    )
    for statement in protected_statements:
        with (
            psycopg.connect(postgres_connection_string) as connection,
            pytest.raises(
                errors.RaiseException,
                match="immutable BeachOS history",
            ),
        ):
            connection.execute(statement)


def test_repository_rejects_duplicate_insert_and_save_without_new_mutation(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    persist(factory, create_venue())

    with pytest.raises(OptimisticConcurrencyError, match="already exists"):
        persist(factory, create_venue())

    with factory.create() as unit_of_work:
        restored = unit_of_work.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )
        assert restored is not None
        with pytest.raises(AggregateNotLoadedError, match="one new aggregate mutation"):
            unit_of_work.venues.save(restored)


def test_business_date_provider_uses_venue_timezone_and_rollover(
    postgres_connection_string: str,
) -> None:
    with psycopg.connect(postgres_connection_string) as connection:
        connection.execute(
            """
            INSERT INTO venue_business_date_policies (
                venue_id,
                timezone_name,
                rollover_time
            )
            VALUES ('venue-1', 'Europe/Athens', '04:00:00')
            """
        )

    before_rollover = PostgresBusinessDateProvider(
        connection_string=postgres_connection_string,
        clock=FixedClock(datetime(2026, 7, 26, 0, 30, tzinfo=UTC)),
    )
    after_rollover = PostgresBusinessDateProvider(
        connection_string=postgres_connection_string,
        clock=FixedClock(datetime(2026, 7, 26, 2, 30, tzinfo=UTC)),
    )

    assert before_rollover.current_for(venue_id="venue-1") == BusinessDate(date(2026, 7, 25))
    assert after_rollover.current_for(venue_id="venue-1") == BusinessDate(date(2026, 7, 26))


def test_business_date_provider_rejects_missing_or_invalid_policy(
    postgres_connection_string: str,
) -> None:
    provider = PostgresBusinessDateProvider(
        connection_string=postgres_connection_string,
        clock=FixedClock(),
    )
    with pytest.raises(BusinessDatePolicyNotFoundError, match="no Business Date policy"):
        provider.current_for(venue_id="missing")

    with psycopg.connect(postgres_connection_string) as connection:
        connection.execute(
            """
            INSERT INTO venue_business_date_policies (
                venue_id,
                timezone_name,
                rollover_time
            )
            VALUES ('venue-1', 'Invalid/Timezone', '04:00:00')
            """
        )
    with pytest.raises(InfrastructureError, match="timezone is unavailable"):
        provider.current_for(venue_id="venue-1")


def test_system_clock_returns_timezone_aware_utc() -> None:
    current = SystemClock().now()

    assert current.tzinfo is UTC
    assert current.utcoffset() is not None


def test_unit_of_work_rejects_adapter_access_before_enter(
    postgres_connection_string: str,
) -> None:
    unit_of_work = PostgresVenueOpeningUnitOfWork(postgres_connection_string)

    with pytest.raises(RuntimeError, match="has not been entered"):
        _ = unit_of_work.venues
    with pytest.raises(RuntimeError, match="has not been entered"):
        _ = unit_of_work.activity_log
    with pytest.raises(RuntimeError, match="has not been entered"):
        unit_of_work.commit()
    unit_of_work.__exit__(None, None, None)


def test_service_persists_readiness_through_application_ports(
    postgres_connection_string: str,
) -> None:
    factory = PostgresVenueOpeningUnitOfWorkFactory(postgres_connection_string)
    persist(factory, create_venue())
    application = service(postgres_connection_string)

    result = application.declare_department_readiness(
        DeclareDepartmentReadinessCommand(
            request_id="request-ready",
            actor_id="staff-kitchen",
            venue_id="venue-1",
            department_id="kitchen",
            status=ReadinessStatus.NOT_READY,
            reason="Preparation ongoing",
        )
    )

    with factory.create() as unit_of_work:
        restored = unit_of_work.venues.get(
            venue_id="venue-1",
            business_date=BUSINESS_DATE,
        )
    assert restored is not None
    assert result.declaration.declared_at == NOW
    assert (
        restored.opening_checklist.current_declarations["kitchen"].status
        is ReadinessStatus.NOT_READY
    )
    assert restored.domain_events == ()
