"""PostgreSQL-backed HTTP integration tests for the Venue Opening slice."""

from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import UTC, date, datetime
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from beachos_api.composition import guest_arrival_service, ordering_service, venue_opening_service
from beachos_api.identity import (
    FakeGuestArrivalAuthority,
    FakeIdentityProvider,
    FakeOrderingAuthority,
    FakeVenueOpeningAuthority,
)
from beachos_api.main import create_app
from beachos_api.packs.beachos.guest_arrival.application import GuestArrivalService
from beachos_api.packs.beachos.guest_arrival.infrastructure import (
    PostgresGuestArrivalUnitOfWorkFactory,
    PostgresVenueOpeningReader,
)
from beachos_api.packs.beachos.ordering.application import OrderingService
from beachos_api.packs.beachos.ordering.infrastructure import (
    PostgresOrderingUnitOfWorkFactory,
    UUIDIdentityGenerator,
)
from beachos_api.packs.beachos.venue_opening.application import VenueOpeningService
from beachos_api.packs.beachos.venue_opening.domain import (
    BusinessDate,
    OperationalDepartment,
    ReadinessStatus,
    Venue,
    VenueOpeningPolicy,
)
from beachos_api.packs.beachos.venue_opening.infrastructure import (
    PostgresVenueOpeningUnitOfWorkFactory,
    apply_migrations,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.errors import (
    OptimisticConcurrencyError,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.persistence.repository import (
    PostgresVenueRepository,
)

pytestmark = pytest.mark.integration

BUSINESS_DATE = BusinessDate(date(2026, 7, 26))
NOW = datetime(2026, 7, 26, 8, 0, tzinfo=UTC)


class FixedBusinessDate:
    def current_for(self, *, venue_id: str) -> BusinessDate:
        del venue_id
        return BUSINESS_DATE


class FixedClock:
    def now(self) -> datetime:
        return NOW


class FixedIds:
    def __init__(self) -> None:
        self._count = 0

    def new_id(self, prefix: str) -> str:
        self._count += 1
        return f"{prefix}-{self._count}"


@pytest.fixture
def postgres_connection_string() -> Iterator[str]:
    base = os.environ.get("BEACHOS_TEST_DATABASE_URL")
    if base is None:
        pytest.fail("BEACHOS_TEST_DATABASE_URL is required for PostgreSQL integration tests")
    if conninfo_to_dict(base).get("host", "") not in {"127.0.0.1", "localhost", "::1"}:
        pytest.fail("integration tests require an isolated local PostgreSQL instance")

    schema_name = f"beachos_api_test_{uuid4().hex}"
    with psycopg.connect(base, autocommit=True) as connection:
        if connection.info.server_version // 10000 != 17:
            pytest.fail("integration tests require PostgreSQL 17")
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name)))

    isolated = make_conninfo(base, options=f"-c search_path={schema_name}")
    try:
        apply_migrations(isolated)
        yield isolated
    finally:
        with psycopg.connect(base, autocommit=True) as connection:
            connection.execute(
                sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema_name))
            )


def _venue() -> Venue:
    return Venue(
        venue_id="venue-1",
        name="Emerald Beach Club",
        business_date=BUSINESS_DATE,
        mandatory_departments=(
            OperationalDepartment("kitchen", "Kitchen", "staff-kitchen"),
            OperationalDepartment("bar", "Bar", "staff-bar"),
        ),
    )


def _ready(venue: Venue, *, include_bar: bool = True) -> None:
    venue.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=NOW,
    )
    if include_bar:
        venue.declare_department_readiness(
            department_id="bar",
            declared_by_id="staff-bar",
            status=ReadinessStatus.READY,
            declared_at=NOW,
        )


def _persist(connection_string: str, venue: Venue) -> None:
    with PostgresVenueOpeningUnitOfWorkFactory(connection_string).create() as unit_of_work:
        unit_of_work.venues.save(venue)
        unit_of_work.commit()


def _service(connection_string: str) -> VenueOpeningService:
    identity = FakeIdentityProvider()
    authority = FakeVenueOpeningAuthority(identity)
    return VenueOpeningService(
        capabilities=authority,
        host_responsibilities=authority,
        business_dates=FixedBusinessDate(),
        clock=FixedClock(),
        unit_of_work_factory=PostgresVenueOpeningUnitOfWorkFactory(connection_string),
        policy=VenueOpeningPolicy(),
    )


def _client(connection_string: str) -> TestClient:
    application = create_app()
    application.dependency_overrides[venue_opening_service] = lambda: _service(connection_string)
    application.dependency_overrides[guest_arrival_service] = lambda: GuestArrivalService(
        authority=FakeGuestArrivalAuthority(FakeIdentityProvider()),
        clock=FixedClock(),
        identities=FixedIds(),
        venue_opening=PostgresVenueOpeningReader(connection_string, FixedBusinessDate()),
        unit_of_work_factory=PostgresGuestArrivalUnitOfWorkFactory(connection_string),
    )
    application.dependency_overrides[ordering_service] = lambda: OrderingService(
        capabilities=FakeOrderingAuthority(FakeIdentityProvider()),
        clock=FixedClock(),
        identities=UUIDIdentityGenerator(),
        unit_of_work_factory=PostgresOrderingUnitOfWorkFactory(connection_string),
    )
    return TestClient(application)


def _persist_open_venue(connection_string: str) -> None:
    venue = _venue()
    _ready(venue)
    venue.open_for_business_date(
        host_id="development-host",
        host_is_responsible=True,
        host_has_required_capability=True,
        opened_at=NOW,
        policy=VenueOpeningPolicy(),
    )
    venue.pull_domain_events()
    _persist(connection_string, venue)


def _seed_arrival_locations(connection_string: str) -> None:
    with psycopg.connect(connection_string) as connection:
        connection.execute(
            """
            INSERT INTO guest_arrival_service_locations(
                service_location_id,venue_id,visible_name,digital_identity,location_type,
                initial_status,beach_sunbed_charge,charge_currency,charge_description
            ) VALUES
                ('a12','venue-1','Beach A12','loc-a12','BEACH SUNBED','AVAILABLE',
                 20,'EUR','Beach Row 1 sunbed charge'),
                ('u04','venue-1','Upper Table U04','loc-u04','UPPER TABLE','AVAILABLE',
                 NULL,NULL,NULL),
                ('p07','venue-1','Pool P07','loc-p07','POOL SUNBED','UNAVAILABLE',NULL,NULL,NULL)
            """
        )


def test_successfully_opens_venue_end_to_end(postgres_connection_string: str) -> None:
    venue = _venue()
    _ready(venue)
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    response = _client(postgres_connection_string).post(
        "/venue/open",
        json={"request_id": "request-1", "venue_id": "venue-1"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "request_id": "request-1",
        "report": {
            "venue_id": "venue-1",
            "business_date": "2026-07-26",
            "opened_at": "2026-07-26T08:00:00Z",
            "host_id": "development-host",
            "department_readiness": [
                {
                    "department_id": "kitchen",
                    "responsible_person_id": "staff-kitchen",
                    "declared_by_id": "staff-kitchen",
                    "status": "READY",
                    "declared_at": "2026-07-26T08:00:00Z",
                    "reason": None,
                    "comment": None,
                },
                {
                    "department_id": "bar",
                    "responsible_person_id": "staff-bar",
                    "declared_by_id": "staff-bar",
                    "status": "READY",
                    "declared_at": "2026-07-26T08:00:00Z",
                    "reason": None,
                    "comment": None,
                },
            ],
            "declaration_history": [
                {
                    "department_id": "kitchen",
                    "responsible_person_id": "staff-kitchen",
                    "declared_by_id": "staff-kitchen",
                    "status": "READY",
                    "declared_at": "2026-07-26T08:00:00Z",
                    "reason": None,
                    "comment": None,
                },
                {
                    "department_id": "bar",
                    "responsible_person_id": "staff-bar",
                    "declared_by_id": "staff-bar",
                    "status": "READY",
                    "declared_at": "2026-07-26T08:00:00Z",
                    "reason": None,
                    "comment": None,
                },
            ],
            "delays": [],
            "blocking_issues": [],
        },
    }
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT opening_status FROM venue_opening_venues").fetchone() == (
            "OPEN",
        )
        assert connection.execute("SELECT actor_id FROM venue_opening_activity_log").fetchone() == (
            "development-host",
        )


def test_already_opened_is_a_business_conflict(postgres_connection_string: str) -> None:
    venue = _venue()
    _ready(venue)
    venue.open_for_business_date(
        host_id="development-host",
        host_is_responsible=True,
        host_has_required_capability=True,
        opened_at=NOW,
        policy=VenueOpeningPolicy(),
    )
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    response = _client(postgres_connection_string).post(
        "/venue/open",
        json={"request_id": "request-2", "venue_id": "venue-1"},
    )

    assert response.status_code == 409
    assert response.json()["error"] == {
        "code": "business_rule_rejected",
        "message": "the Venue is already open for this Business Date",
    }


def test_missing_department_declaration_is_a_business_conflict(
    postgres_connection_string: str,
) -> None:
    venue = _venue()
    _ready(venue, include_bar=False)
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    response = _client(postgres_connection_string).post(
        "/venue/open",
        json={"request_id": "request-3", "venue_id": "venue-1"},
    )

    assert response.status_code == 409
    assert response.json()["error"] == {
        "code": "business_rule_rejected",
        "message": "every mandatory department must declare readiness before opening",
    }


def test_optimistic_concurrency_is_an_explicit_conflict(
    postgres_connection_string: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    venue = _venue()
    _ready(venue)
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    def conflict(_: PostgresVenueRepository, __: Venue) -> None:
        raise OptimisticConcurrencyError("simulated concurrent change")

    monkeypatch.setattr(PostgresVenueRepository, "save", conflict)
    response = _client(postgres_connection_string).post(
        "/venue/open",
        json={"request_id": "request-4", "venue_id": "venue-1"},
    )

    assert response.status_code == 409
    assert response.json()["error"] == {
        "code": "optimistic_concurrency_conflict",
        "message": "The Venue changed. Review the current opening state and try again.",
    }
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT opening_status FROM venue_opening_venues").fetchone() == (
            "CLOSED",
        )
        assert connection.execute("SELECT count(*) FROM venue_opening_activity_log").fetchone() == (
            0,
        )


def test_context_returns_readiness_outstanding_departments_and_attention(
    postgres_connection_string: str,
) -> None:
    venue = Venue(
        venue_id="venue-1",
        name="Emerald Beach Club",
        business_date=BUSINESS_DATE,
        mandatory_departments=(
            OperationalDepartment("kitchen", "Kitchen", "staff-kitchen"),
            OperationalDepartment("bar", "Bar", "staff-bar"),
            OperationalDepartment("cleaning", "Cleaning", "staff-cleaning"),
            OperationalDepartment("maintenance", "Maintenance", "staff-maintenance"),
        ),
    )
    venue.declare_department_readiness(
        department_id="kitchen",
        declared_by_id="staff-kitchen",
        status=ReadinessStatus.READY,
        declared_at=NOW,
    )
    venue.declare_department_readiness(
        department_id="bar",
        declared_by_id="staff-bar",
        status=ReadinessStatus.BLOCKED,
        declared_at=NOW,
        reason="Ice machine failure",
    )
    venue.declare_department_readiness(
        department_id="cleaning",
        declared_by_id="staff-cleaning",
        status=ReadinessStatus.NOT_READY,
        declared_at=NOW,
        reason="Beach not cleaned",
    )
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    response = _client(postgres_connection_string).get(
        "/venue/context",
        params={"venue_id": "venue-1"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["venue_name"] == "Emerald Beach Club"
    assert body["business_date"] == "2026-07-26"
    assert body["opening_status"] == "CLOSED"
    assert body["opening_report"] is None
    assert len(body["department_readiness"]) == 4
    assert body["department_readiness"][0]["current_readiness"]["status"] == "READY"
    assert body["department_readiness"][3]["current_readiness"] is None
    assert body["outstanding_departments"] == ["bar", "cleaning", "maintenance"]
    assert [item["code"] for item in body["attention_queue"]] == [
        "DEPARTMENT_BLOCKED",
        "DEPARTMENT_NOT_READY",
        "MISSING_DECLARATION",
    ]
    assert body["attention_queue"][0]["importance"] == "CRITICAL"
    assert "Ice machine failure" in body["attention_queue"][0]["message"]


def test_context_reports_ready_to_open_without_mutation(
    postgres_connection_string: str,
) -> None:
    venue = _venue()
    _ready(venue)
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    response = _client(postgres_connection_string).get(
        "/venue/context",
        params={"venue_id": "venue-1"},
    )

    assert response.status_code == 200
    assert response.json()["outstanding_departments"] == []
    assert response.json()["attention_queue"] == [
        {
            "code": "READY_TO_OPEN",
            "importance": "ACTION_REQUIRED",
            "message": "Every mandatory department is READY. The Venue can be opened.",
            "department_id": None,
        }
    ]
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute(
            "SELECT opening_status, aggregate_version FROM venue_opening_venues"
        ).fetchone() == ("CLOSED", 2)


def test_context_returns_current_opening_report(
    postgres_connection_string: str,
) -> None:
    venue = _venue()
    _ready(venue)
    venue.open_for_business_date(
        host_id="development-host",
        host_is_responsible=True,
        host_has_required_capability=True,
        opened_at=NOW,
        policy=VenueOpeningPolicy(),
    )
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    response = _client(postgres_connection_string).get(
        "/venue/context",
        params={"venue_id": "venue-1"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["opening_status"] == "OPEN"
    assert body["outstanding_departments"] == []
    assert body["attention_queue"] == []
    assert body["opening_report"]["host_id"] == "development-host"
    assert body["opening_report"]["opened_at"] == "2026-07-26T08:00:00Z"


def test_context_requires_venue_id(postgres_connection_string: str) -> None:
    response = _client(postgres_connection_string).get("/venue/context")

    assert response.status_code == 422


def test_department_owner_sees_only_their_department_and_own_history(
    postgres_connection_string: str,
) -> None:
    venue = _venue()
    venue.declare_department_readiness(
        department_id="bar",
        declared_by_id="staff-bar",
        status=ReadinessStatus.BLOCKED,
        declared_at=NOW,
        reason="Ice machine failure",
    )
    venue.pull_domain_events()
    _persist(postgres_connection_string, venue)

    response = _client(postgres_connection_string).get(
        "/venue/department-readiness/context",
        params={"venue_id": "venue-1"},
        headers={"X-BeachOS-Development-Actor": "staff-kitchen"},
    )

    assert response.status_code == 200
    body = response.json()
    assert [item["department_id"] for item in body["departments"]] == ["kitchen"]
    assert body["departments"][0]["current_readiness"] is None
    assert body["declaration_history"] == []
    assert "staff-bar" not in response.text
    assert "Ice machine failure" not in response.text


def test_department_owner_declares_updates_and_host_sees_current_state(
    postgres_connection_string: str,
) -> None:
    _persist(postgres_connection_string, _venue())
    client = _client(postgres_connection_string)
    headers = {"X-BeachOS-Development-Actor": "staff-kitchen"}

    blocked = client.post(
        "/venue/departments/kitchen/readiness",
        headers=headers,
        json={
            "request_id": "declaration-1",
            "venue_id": "venue-1",
            "status": "BLOCKED",
            "reason": "Equipment issue",
            "comment": "Maintenance is attending",
        },
    )
    ready = client.post(
        "/venue/departments/kitchen/readiness",
        headers=headers,
        json={
            "request_id": "declaration-2",
            "venue_id": "venue-1",
            "status": "READY",
        },
    )
    owner_context = client.get(
        "/venue/department-readiness/context",
        params={"venue_id": "venue-1"},
        headers=headers,
    )
    host_context = client.get("/venue/context", params={"venue_id": "venue-1"})

    assert blocked.status_code == ready.status_code == 200
    assert blocked.json()["declaration"]["reason"] == "Equipment issue"
    assert ready.json()["declaration"]["status"] == "READY"
    assert [item["status"] for item in owner_context.json()["declaration_history"]] == [
        "BLOCKED",
        "READY",
    ]
    assert host_context.json()["department_readiness"][0]["current_readiness"]["status"] == "READY"
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute(
            "SELECT readiness_status FROM venue_opening_declarations ORDER BY declaration_sequence"
        ).fetchall() == [("BLOCKED",), ("READY",)]


def test_readiness_rejects_missing_reason_wrong_owner_and_missing_identity(
    postgres_connection_string: str,
) -> None:
    _persist(postgres_connection_string, _venue())
    client = _client(postgres_connection_string)
    payload = {
        "request_id": "declaration-1",
        "venue_id": "venue-1",
        "status": "NOT READY",
    }

    missing_reason = client.post(
        "/venue/departments/kitchen/readiness",
        headers={"X-BeachOS-Development-Actor": "staff-kitchen"},
        json=payload,
    )
    wrong_owner = client.post(
        "/venue/departments/kitchen/readiness",
        headers={"X-BeachOS-Development-Actor": "staff-bar"},
        json={**payload, "status": "READY"},
    )
    missing_identity = client.get(
        "/venue/department-readiness/context",
        params={"venue_id": "venue-1"},
    )

    assert missing_reason.status_code == 409
    assert "require a reason" in missing_reason.text
    assert wrong_owner.status_code == 409
    assert "responsible person" in wrong_owner.text
    assert missing_identity.status_code == 422


def test_unassigned_actor_cannot_view_any_department(postgres_connection_string: str) -> None:
    _persist(postgres_connection_string, _venue())

    response = _client(postgres_connection_string).get(
        "/venue/department-readiness/context",
        params={"venue_id": "venue-1"},
        headers={"X-BeachOS-Development-Actor": "staff-unknown"},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_guest_arrival_context_identification_and_atomic_beach_opening(
    postgres_connection_string: str,
) -> None:
    _persist_open_venue(postgres_connection_string)
    _seed_arrival_locations(postgres_connection_string)
    client = _client(postgres_connection_string)

    context = client.get("/guest-arrival/context", params={"venue_id": "venue-1"})
    identified = client.get(
        "/guest-arrival/service-locations/identify",
        params={"venue_id": "venue-1", "digital_identity": "loc-a12"},
    )
    opened = client.post(
        "/guest-arrival/customer-groups/open",
        headers={"X-BeachOS-Development-Actor": "staff-waiter-1"},
        json={
            "request_id": "arrival-1",
            "venue_id": "venue-1",
            "service_location_id": "a12",
            "physical_context_confirmed": True,
            "waiter_accepts_responsibility": True,
            "opening_charge_confirmed": True,
        },
    )

    assert context.status_code == identified.status_code == opened.status_code == 200
    assert context.json()["venue_open"] is True
    assert len(context.json()["locations"]) == 3
    assert identified.json()["visible_name"] == "Beach A12"
    group = opened.json()["customer_group"]
    assert group["responsible_waiter_id"] == "staff-waiter-1"
    assert group["opening_obligation"] == "20"
    assert group["currency"] == "EUR"
    ordering_context = client.get(
        "/ordering/context",
        params={"customer_group_id": group["customer_group_id"]},
    )
    assert ordering_context.status_code == 200
    assert ordering_context.json()["bill"]["total"] == "20"
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute(
            "SELECT count(*) FROM guest_arrival_events WHERE service_location_id='a12'"
        ).fetchone() == (5,)
        assert connection.execute("SELECT count(*) FROM guest_arrival_activity_log").fetchone() == (
            1,
        )
        assert connection.execute(
            "SELECT stream_version FROM ordering_customer_groups WHERE customer_group_id=%s",
            (group["customer_group_id"],),
        ).fetchone() == (3,)


def test_guest_arrival_non_beach_opening_has_no_bill_and_retry_is_idempotent(
    postgres_connection_string: str,
) -> None:
    _persist_open_venue(postgres_connection_string)
    _seed_arrival_locations(postgres_connection_string)
    client = _client(postgres_connection_string)
    payload = {
        "request_id": "arrival-2",
        "venue_id": "venue-1",
        "service_location_id": "u04",
        "physical_context_confirmed": True,
        "waiter_accepts_responsibility": True,
        "opening_charge_confirmed": False,
    }
    headers = {"X-BeachOS-Development-Actor": "staff-waiter-2"}

    first = client.post("/guest-arrival/customer-groups/open", headers=headers, json=payload)
    second = client.post("/guest-arrival/customer-groups/open", headers=headers, json=payload)

    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["customer_group"]["bill_id"] is None
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute(
            "SELECT count(*) FROM guest_arrival_events WHERE service_location_id='u04'"
        ).fetchone() == (2,)


def test_guest_arrival_preserves_blockers_and_uncertainty(postgres_connection_string: str) -> None:
    _persist_open_venue(postgres_connection_string)
    _seed_arrival_locations(postgres_connection_string)
    client = _client(postgres_connection_string)
    base = {
        "request_id": "arrival-3",
        "venue_id": "venue-1",
        "service_location_id": "a12",
        "physical_context_confirmed": False,
        "waiter_accepts_responsibility": True,
        "opening_charge_confirmed": True,
    }

    mismatch = client.post(
        "/guest-arrival/customer-groups/open",
        headers={"X-BeachOS-Development-Actor": "staff-waiter-1"},
        json=base,
    )
    host_attempt = client.post(
        "/guest-arrival/customer-groups/open",
        headers={"X-BeachOS-Development-Actor": "development-host"},
        json={**base, "physical_context_confirmed": True},
    )
    missing_identity = client.get(
        "/guest-arrival/service-locations/identify",
        params={"venue_id": "venue-1", "digital_identity": "unknown"},
    )

    assert mismatch.status_code == 409
    assert "physical and digital" in mismatch.text
    assert host_attempt.status_code == 403
    assert missing_identity.status_code == 404
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM guest_arrival_events").fetchone() == (0,)
