"""PostgreSQL-backed Bar Operations vertical slice."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from beachos_api.composition import bar_service
from beachos_api.identity import FakeBarAuthority, FakeIdentityProvider
from beachos_api.main import create_app
from beachos_api.packs.beachos.bar.application import BarService
from beachos_api.packs.beachos.bar.infrastructure import PostgresBarUnitOfWorkFactory
from beachos_api.packs.beachos.bar.infrastructure.errors import BarConcurrencyError
from beachos_api.packs.beachos.venue_opening.infrastructure import SystemClock, apply_migrations

pytestmark = pytest.mark.integration


@pytest.fixture
def postgres_connection_string() -> Iterator[str]:
    base = os.environ.get("BEACHOS_TEST_DATABASE_URL")
    if base is None:
        pytest.fail("BEACHOS_TEST_DATABASE_URL is required for PostgreSQL integration tests")
    if conninfo_to_dict(base).get("host", "") not in {"127.0.0.1", "localhost", "::1"}:
        pytest.fail("integration tests require an isolated local PostgreSQL instance")
    schema = f"beachos_bar_test_{uuid4().hex}"
    with psycopg.connect(base, autocommit=True) as connection:
        if connection.info.server_version // 10000 != 17:
            pytest.fail("integration tests require PostgreSQL 17")
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    isolated = make_conninfo(base, options=f"-c search_path={schema}")
    try:
        apply_migrations(isolated)
        source = {
            "ticket_id": "bar-1",
            "order_id": "order-1",
            "customer_group_id": "group-1",
            "service_location_id": "B-12",
            "responsible_waiter_id": "waiter-1",
            "created_at": "2026-07-26T10:00:00+00:00",
            "items": [
                {
                    "order_item_id": "item-1",
                    "menu_item_id": "water",
                    "name": "Water",
                    "quantity": "2",
                    "unit_price": "3.00",
                    "currency": "EUR",
                    "destination": "BAR",
                    "note": None,
                }
            ],
        }
        with psycopg.connect(isolated) as connection:
            connection.execute(
                """INSERT INTO ordering_customer_groups VALUES
                   ('group-1','venue-1','B-12','waiter-1','ACTIVE',1)"""
            )
            connection.execute(
                """INSERT INTO ordering_events(
                       customer_group_id,sequence,event_type,event_data,occurred_at
                   ) VALUES(
                       'group-1',1,'BAR_TICKET_CREATED',%s,
                       '2026-07-26T10:00:00+00:00'
                   )""",
                (json.dumps(source),),
            )
        yield isolated
    finally:
        with psycopg.connect(base, autocommit=True) as connection:
            connection.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


def service(connection_string: str) -> BarService:
    return BarService(
        capabilities=FakeBarAuthority(FakeIdentityProvider()),
        clock=SystemClock(),
        unit_of_work_factory=PostgresBarUnitOfWorkFactory(connection_string),
    )


def test_context_acknowledgement_retry_restoration_and_immutable_history(
    postgres_connection_string: str,
):
    app = create_app()
    app.dependency_overrides[bar_service] = lambda: service(postgres_connection_string)
    client = TestClient(app)
    assert (
        client.get("/bar/context", params={"venue_id": "venue-1"}).json()["tickets"][0]["status"]
        == "NEW"
    )
    payload = {"request_id": "request-1"}
    first = client.post("/bar/tickets/bar-1/acknowledge", json=payload)
    assert first.status_code == 200 and first.json()["ticket"]["status"] == "ACKNOWLEDGED"
    assert client.post("/bar/tickets/bar-1/acknowledge", json=payload).json() == first.json()
    for request_id, action, status in (
        ("r", "mark_ready", "READY"),
        ("c", "collect", "COLLECTED"),
        ("d", "deliver", "DELIVERED"),
    ):
        progressed = client.post(f"/bar/tickets/bar-1/{action}", json={"request_id": request_id})
        assert progressed.status_code == 200 and progressed.json()["ticket"]["status"] == status
    assert (
        client.post("/bar/tickets/bar-1/deliver", json={"request_id": "d"}).json()["ticket"][
            "status"
        ]
        == "DELIVERED"
    )
    assert (
        client.get("/bar/context", params={"venue_id": "venue-1"}).json()["tickets"][0]["status"]
        == "DELIVERED"
    )
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM bar_events").fetchone()[0] == 4
        with pytest.raises(psycopg.DatabaseError):
            connection.execute("DELETE FROM bar_events")


def test_rollback_and_optimistic_concurrency(postgres_connection_string: str):
    factory = PostgresBarUnitOfWorkFactory(postgres_connection_string)
    with factory.create() as rollback:
        value = rollback.tickets.get(ticket_id="bar-1")
        assert value is not None
        value.acknowledge(actor_id="staff", acknowledged_at=SystemClock().now())
        rollback.tickets.save(value)
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM bar_events").fetchone()[0] == 0
    with factory.create() as first, factory.create() as second:
        one = first.tickets.get(ticket_id="bar-1")
        two = second.tickets.get(ticket_id="bar-1")
        assert one and two
        one.acknowledge(actor_id="one", acknowledged_at=SystemClock().now())
        two.acknowledge(actor_id="two", acknowledged_at=SystemClock().now())
        first.tickets.save(one)
        first.commit()
        with pytest.raises(BarConcurrencyError):
            second.tickets.save(two)
