"""PostgreSQL-backed Kitchen Operations vertical slice."""

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

from beachos_api.composition import kitchen_service
from beachos_api.identity import FakeIdentityProvider, FakeKitchenAuthority
from beachos_api.main import create_app
from beachos_api.packs.beachos.kitchen.application import KitchenService
from beachos_api.packs.beachos.kitchen.infrastructure import (
    PostgresKitchenUnitOfWorkFactory,
)
from beachos_api.packs.beachos.kitchen.infrastructure.errors import (
    KitchenConcurrencyError,
)
from beachos_api.packs.beachos.venue_opening.infrastructure import SystemClock, apply_migrations

pytestmark = pytest.mark.integration


@pytest.fixture
def postgres_connection_string() -> Iterator[str]:
    base = os.environ.get("BEACHOS_TEST_DATABASE_URL")
    if base is None:
        pytest.fail("BEACHOS_TEST_DATABASE_URL is required for PostgreSQL integration tests")
    if conninfo_to_dict(base).get("host", "") not in {"127.0.0.1", "localhost", "::1"}:
        pytest.fail("integration tests require an isolated local PostgreSQL instance")
    schema = f"beachos_kitchen_test_{uuid4().hex}"
    with psycopg.connect(base, autocommit=True) as connection:
        if connection.info.server_version // 10000 != 17:
            pytest.fail("integration tests require PostgreSQL 17")
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    isolated = make_conninfo(base, options=f"-c search_path={schema}")
    try:
        apply_migrations(isolated)
        source = {
            "ticket_id": "kitchen-1",
            "order_id": "order-1",
            "customer_group_id": "group-1",
            "service_location_id": "B-12",
            "responsible_waiter_id": "waiter-1",
            "created_at": "2026-07-26T10:00:00+00:00",
            "items": [
                {
                    "order_item_id": "item-1",
                    "menu_item_id": "salad",
                    "name": "Salad",
                    "quantity": "2",
                    "unit_price": "9.00",
                    "currency": "EUR",
                    "destination": "KITCHEN",
                    "note": "No salt",
                }
            ],
        }
        with psycopg.connect(isolated) as connection:
            connection.execute(
                """INSERT INTO venue_opening_venues VALUES
                ('venue-1','2026-08-01','Emerald Beach Club','OPEN',0)"""
            )
            connection.execute(
                """
                INSERT INTO ordering_customer_groups VALUES
                ('group-1', 'venue-1', 'B-12', 'waiter-1', 'ACTIVE', 1)
                """
            )
            connection.execute(
                """
                INSERT INTO ordering_events (
                    customer_group_id, sequence, event_type, event_data, occurred_at
                ) VALUES ('group-1', 1, 'KITCHEN_TICKET_CREATED', %s,
                          '2026-07-26T10:00:00+00:00')
                """,
                (json.dumps(source),),
            )
        yield isolated
    finally:
        with psycopg.connect(base, autocommit=True) as connection:
            connection.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


def service(connection_string: str) -> KitchenService:
    identities = FakeIdentityProvider()
    return KitchenService(
        capabilities=FakeKitchenAuthority(identities),
        clock=SystemClock(),
        unit_of_work_factory=PostgresKitchenUnitOfWorkFactory(connection_string),
    )


def test_context_acknowledgement_retry_and_restoration(
    postgres_connection_string: str,
) -> None:
    app = create_app()
    app.dependency_overrides[kitchen_service] = lambda: service(postgres_connection_string)
    client = TestClient(app)
    context = client.get("/kitchen/context", params={"venue_id": "venue-1"})
    assert context.status_code == 200
    assert context.json()["tickets"][0]["status"] == "NEW"
    payload = {"request_id": "request-1"}
    first = client.post("/kitchen/tickets/kitchen-1/acknowledge", json=payload)
    assert first.status_code == 200
    assert first.json()["ticket"]["status"] == "ACKNOWLEDGED"
    assert (
        client.post("/kitchen/tickets/kitchen-1/acknowledge", json=payload).json() == first.json()
    )
    for request_id, action, status in (
        ("ready-1", "mark_ready", "READY"),
        ("collect-1", "collect", "COLLECTED"),
        ("deliver-1", "deliver", "DELIVERED"),
    ):
        progressed = client.post(
            f"/kitchen/tickets/kitchen-1/{action}", json={"request_id": request_id}
        )
        assert progressed.status_code == 200 and progressed.json()["ticket"]["status"] == status
    assert (
        client.post("/kitchen/tickets/kitchen-1/deliver", json={"request_id": "deliver-1"}).json()[
            "ticket"
        ]["status"]
        == "DELIVERED"
    )
    restored = client.get("/kitchen/context", params={"venue_id": "venue-1"})
    assert restored.json()["tickets"][0]["status"] == "DELIVERED"
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM kitchen_events").fetchone()[0] == 4
        assert (
            connection.execute("SELECT count(*) FROM kitchen_command_receipts").fetchone()[0] == 4
        )


def test_unit_of_work_rolls_back_uncommitted_acknowledgement(
    postgres_connection_string: str,
) -> None:
    with PostgresKitchenUnitOfWorkFactory(postgres_connection_string).create() as unit:
        ticket = unit.tickets.get(ticket_id="kitchen-1")
        assert ticket is not None
        ticket.acknowledge(actor_id="staff-1", acknowledged_at=SystemClock().now())
        unit.tickets.save(ticket)
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM kitchen_events").fetchone()[0] == 0


def test_optimistic_concurrency_rejects_stale_acknowledgement(
    postgres_connection_string: str,
) -> None:
    factory = PostgresKitchenUnitOfWorkFactory(postgres_connection_string)
    with factory.create() as first, factory.create() as second:
        first_ticket = first.tickets.get(ticket_id="kitchen-1")
        second_ticket = second.tickets.get(ticket_id="kitchen-1")
        assert first_ticket is not None and second_ticket is not None
        first_ticket.acknowledge(actor_id="staff-1", acknowledged_at=SystemClock().now())
        second_ticket.acknowledge(actor_id="staff-2", acknowledged_at=SystemClock().now())
        first.tickets.save(first_ticket)
        first.commit()
        with pytest.raises(KitchenConcurrencyError):
            second.tickets.save(second_ticket)


def test_kitchen_history_cannot_be_changed_or_deleted(
    postgres_connection_string: str,
) -> None:
    app = create_app()
    app.dependency_overrides[kitchen_service] = lambda: service(postgres_connection_string)
    TestClient(app).post(
        "/kitchen/tickets/kitchen-1/acknowledge",
        json={"request_id": "request-immutable"},
    )
    with psycopg.connect(postgres_connection_string) as connection:
        with pytest.raises(psycopg.DatabaseError):
            connection.execute("DELETE FROM kitchen_events")
        connection.rollback()
        with pytest.raises(psycopg.DatabaseError):
            connection.execute("UPDATE kitchen_command_receipts SET ticket_id = 'other'")
