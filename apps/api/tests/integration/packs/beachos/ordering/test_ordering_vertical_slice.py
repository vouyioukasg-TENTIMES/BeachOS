"""PostgreSQL-backed Ordering vertical slice."""

from __future__ import annotations

import os
from collections.abc import Iterator
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from beachos_api.composition import ordering_service
from beachos_api.identity import FakeIdentityProvider, FakeOrderingAuthority
from beachos_api.main import create_app
from beachos_api.packs.beachos.ordering.application import OrderingService
from beachos_api.packs.beachos.ordering.infrastructure import (
    PostgresOrderingUnitOfWorkFactory,
    UUIDIdentityGenerator,
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
    schema = f"beachos_ordering_test_{uuid4().hex}"
    with psycopg.connect(base, autocommit=True) as connection:
        if connection.info.server_version // 10000 != 17:
            pytest.fail("integration tests require PostgreSQL 17")
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    isolated = make_conninfo(base, options=f"-c search_path={schema}")
    try:
        apply_migrations(isolated)
        with psycopg.connect(isolated) as connection:
            connection.execute(
                """
                INSERT INTO ordering_customer_groups VALUES
                ('group-1', 'venue-1', 'B-12', 'waiter-1', 'ACTIVE', 0)
                """
            )
            connection.execute(
                """
                INSERT INTO ordering_menu_items VALUES
                ('venue-1', 'coffee', 'Drinks', 1, 'Coffee', 1, 4.50, 'EUR', 'BAR', TRUE),
                ('venue-1', 'salad', 'Food', 2, 'Salad', 1, 9.00, 'EUR', 'KITCHEN', TRUE),
                ('venue-1', 'water', 'Drinks', 1, 'Water', 2, 0, 'EUR',
                 'NO PREPARATION', TRUE)
                """
            )
        yield isolated
    finally:
        with psycopg.connect(base, autocommit=True) as connection:
            connection.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


def service(connection_string: str) -> OrderingService:
    identities = FakeIdentityProvider()
    return OrderingService(
        capabilities=FakeOrderingAuthority(identities),
        clock=SystemClock(),
        identities=UUIDIdentityGenerator(),
        unit_of_work_factory=PostgresOrderingUnitOfWorkFactory(connection_string),
    )


def test_real_api_persists_and_restores_one_atomic_order_round(
    postgres_connection_string: str,
) -> None:
    app = create_app()
    app.dependency_overrides[ordering_service] = lambda: service(postgres_connection_string)
    client = TestClient(app)
    payload = {
        "request_id": "request-1",
        "customer_group_id": "group-1",
        "items": [
            {"menu_item_id": "coffee", "quantity": "2"},
            {"menu_item_id": "salad", "quantity": "1", "note": "No salt"},
        ],
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 200
    assert response.json()["bill"]["total"] == "18.00"
    assert {ticket["destination"] for ticket in response.json()["tickets"]} == {
        "BAR",
        "KITCHEN",
    }
    assert client.post("/orders", json=payload).json() == response.json()
    context = client.get("/ordering/context", params={"customer_group_id": "group-1"})
    assert context.status_code == 200
    assert len(context.json()["orders"]) == 1

    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM ordering_events").fetchone()[0] == 8
        assert (
            connection.execute("SELECT count(*) FROM ordering_command_receipts").fetchone()[0] == 1
        )


def test_transaction_rolls_back_without_commit(postgres_connection_string: str) -> None:
    factory = PostgresOrderingUnitOfWorkFactory(postgres_connection_string)
    with factory.create() as unit:
        group = unit.customer_groups.get(customer_group_id="group-1")
        assert group is not None
        # Merely loading authoritative state cannot create persisted history.
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM ordering_events").fetchone()[0] == 0
