"""PostgreSQL-backed Ordering vertical slice."""

from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import date
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from beachos_api.composition import (
    bar_service,
    bill_closing_service,
    billing_service,
    customer_group_completion_service,
    guest_departure_service,
    kitchen_service,
    ordering_service,
    payment_service,
    venue_closing_service,
)
from beachos_api.identity import (
    FakeBarAuthority,
    FakeBillClosingAuthority,
    FakeCustomerGroupCompletionAuthority,
    FakeGuestDepartureAuthority,
    FakeIdentityProvider,
    FakeKitchenAuthority,
    FakeOrderingAuthority,
    FakePaymentAuthority,
    FakeVenueOpeningAuthority,
)
from beachos_api.main import create_app
from beachos_api.packs.beachos.bar.application import BarService
from beachos_api.packs.beachos.bar.infrastructure import PostgresBarUnitOfWorkFactory
from beachos_api.packs.beachos.bill_closing.application import BillClosingService
from beachos_api.packs.beachos.bill_closing.infrastructure import (
    PostgresBillClosingUnitOfWorkFactory,
)
from beachos_api.packs.beachos.billing.application import BillingService
from beachos_api.packs.beachos.billing.infrastructure import PostgresBillReader
from beachos_api.packs.beachos.customer_completion.application import (
    CustomerGroupCompletionService,
)
from beachos_api.packs.beachos.customer_completion.infrastructure import (
    PostgresCompletionUnitOfWorkFactory,
)
from beachos_api.packs.beachos.guest_departure.application import GuestDepartureService
from beachos_api.packs.beachos.guest_departure.infrastructure import (
    PostgresDepartureUnitOfWorkFactory,
)
from beachos_api.packs.beachos.kitchen.application import KitchenService
from beachos_api.packs.beachos.kitchen.infrastructure import (
    PostgresKitchenUnitOfWorkFactory,
)
from beachos_api.packs.beachos.ordering.application import OrderingService
from beachos_api.packs.beachos.ordering.infrastructure import (
    PostgresOrderingUnitOfWorkFactory,
    UUIDIdentityGenerator,
)
from beachos_api.packs.beachos.payments.application import PaymentService
from beachos_api.packs.beachos.payments.infrastructure import (
    PostgresPaymentUnitOfWorkFactory,
    UUIDPaymentIdentities,
)
from beachos_api.packs.beachos.venue_closing.application import VenueClosingService
from beachos_api.packs.beachos.venue_closing.infrastructure import (
    PostgresVenueClosingUnitOfWorkFactory,
)
from beachos_api.packs.beachos.venue_opening.domain import BusinessDate
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
                """INSERT INTO venue_opening_venues VALUES
                ('venue-1','2026-08-01','Emerald Beach Club','OPEN',2)"""
            )
            connection.execute(
                """INSERT INTO venue_opening_departments VALUES
                ('venue-1','2026-08-01','operations',0,'Operations','development-host')"""
            )
            connection.execute(
                """INSERT INTO venue_opening_declarations VALUES
                ('venue-1','2026-08-01',1,'operations','development-host',
                 'development-host','READY','2026-08-01T08:00:00Z',NULL,NULL)"""
            )
            connection.execute(
                """INSERT INTO venue_opening_reports VALUES
                ('venue-1','2026-08-01','2026-08-01T08:05:00Z','development-host')"""
            )
            connection.execute(
                """
                INSERT INTO ordering_customer_groups VALUES
                ('group-1', 'venue-1', 'B-12', 'waiter-1', 'ACTIVE', 0),
                ('group-2', 'venue-1', 'B-13', 'waiter-1', 'ACTIVE', 0)
                """
            )
            connection.execute(
                """
                INSERT INTO guest_arrival_service_locations(
                    service_location_id,venue_id,visible_name,digital_identity,
                    location_type,initial_status,stream_version
                ) VALUES
                ('B-12','venue-1','Upper Table B-12','digital-b12','UPPER TABLE','AVAILABLE',2),
                ('B-13','venue-1','Upper Table B-13','digital-b13','UPPER TABLE','AVAILABLE',2)
                """
            )
            connection.execute(
                """
                INSERT INTO guest_arrival_events(
                    service_location_id,sequence,event_type,event_data,occurred_at
                ) VALUES
                ('B-12',1,'RESPONSIBLE_WAITER_ASSIGNED',
                 '{"customer_group_id":"group-1","service_location_id":"B-12","responsible_waiter_id":"waiter-1"}',
                 '2026-08-01T09:00:00Z'),
                ('B-12',2,'CUSTOMER_GROUP_OPENED',
                 '{"customer_group_id":"group-1","venue_id":"venue-1","service_location_id":"B-12","responsible_waiter_id":"waiter-1"}',
                 '2026-08-01T09:00:00Z'),
                ('B-13',1,'RESPONSIBLE_WAITER_ASSIGNED',
                 '{"customer_group_id":"group-2","service_location_id":"B-13","responsible_waiter_id":"waiter-1"}',
                 '2026-08-01T09:05:00Z'),
                ('B-13',2,'CUSTOMER_GROUP_OPENED',
                 '{"customer_group_id":"group-2","venue_id":"venue-1","service_location_id":"B-13","responsible_waiter_id":"waiter-1"}',
                 '2026-08-01T09:05:00Z')
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


class FixedBusinessDates:
    def current_for(self, *, venue_id: str) -> BusinessDate:
        del venue_id
        return BusinessDate(date(2026, 8, 1))


def test_real_api_persists_and_restores_one_atomic_order_round(
    postgres_connection_string: str,
) -> None:
    app = create_app()
    app.dependency_overrides[ordering_service] = lambda: service(postgres_connection_string)
    app.dependency_overrides[billing_service] = lambda: BillingService(
        PostgresBillReader(postgres_connection_string)
    )
    identities = FakeIdentityProvider()
    app.dependency_overrides[payment_service] = lambda: PaymentService(
        authority=FakePaymentAuthority(identities),
        clock=SystemClock(),
        identities=UUIDPaymentIdentities(),
        units=PostgresPaymentUnitOfWorkFactory(postgres_connection_string),
    )
    app.dependency_overrides[bill_closing_service] = lambda: BillClosingService(
        authority=FakeBillClosingAuthority(identities),
        clock=SystemClock(),
        units=PostgresBillClosingUnitOfWorkFactory(postgres_connection_string),
    )
    app.dependency_overrides[customer_group_completion_service] = (
        lambda: CustomerGroupCompletionService(
            authority=FakeCustomerGroupCompletionAuthority(identities),
            clock=SystemClock(),
            units=PostgresCompletionUnitOfWorkFactory(postgres_connection_string),
        )
    )
    app.dependency_overrides[guest_departure_service] = lambda: GuestDepartureService(
        authority=FakeGuestDepartureAuthority(identities),
        clock=SystemClock(),
        units=PostgresDepartureUnitOfWorkFactory(postgres_connection_string),
    )
    app.dependency_overrides[kitchen_service] = lambda: KitchenService(
        capabilities=FakeKitchenAuthority(identities),
        clock=SystemClock(),
        unit_of_work_factory=PostgresKitchenUnitOfWorkFactory(postgres_connection_string),
    )
    app.dependency_overrides[bar_service] = lambda: BarService(
        capabilities=FakeBarAuthority(identities),
        clock=SystemClock(),
        unit_of_work_factory=PostgresBarUnitOfWorkFactory(postgres_connection_string),
    )
    app.dependency_overrides[venue_closing_service] = lambda: VenueClosingService(
        authority=FakeVenueOpeningAuthority(identities),
        business_dates=FixedBusinessDates(),
        clock=SystemClock(),
        units=PostgresVenueClosingUnitOfWorkFactory(postgres_connection_string),
    )
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
    for ticket in response.json()["tickets"]:
        capability = ticket["destination"].lower()
        ticket_id = ticket["ticket_id"]
        assert (
            client.post(
                f"/{capability}/tickets/{ticket_id}/acknowledge",
                json={"request_id": f"ack-{ticket_id}"},
            ).status_code
            == 200
        )
        for action in ("mark_ready", "collect", "deliver"):
            progressed = client.post(
                f"/{capability}/tickets/{ticket_id}/{action}",
                json={"request_id": f"{action}-{ticket_id}"},
            )
            assert progressed.status_code == 200
    assert client.post("/orders", json=payload).json() == response.json()
    context = client.get("/ordering/context", params={"customer_group_id": "group-1"})
    assert context.status_code == 200
    assert len(context.json()["orders"]) == 1
    bill = client.get("/billing/customer-groups/group-1")
    assert bill.status_code == 200
    assert bill.json()["total"] == "18.00"
    assert bill.json()["balance"] == "18.00"
    assert len(bill.json()["lines"]) == 2

    payment_payload = {
        "request_id": "payment-request-1",
        "customer_group_id": "group-1",
        "amount": "18.00",
        "currency": "EUR",
    }
    payment = client.post("/payments/cash", json=payment_payload)
    assert payment.status_code == 200
    assert payment.json()["method"] == "CASH"
    assert payment.json()["balance"] == "0"
    assert client.post("/payments/cash", json=payment_payload).json() == payment.json()
    paid_bill = client.get("/billing/customer-groups/group-1").json()
    assert paid_bill["balance"] == "0.00"
    assert paid_bill["status"] == "FULLY_PAID"
    assert len(paid_bill["payments"]) == 1
    close_payload = {"request_id": "close-request-1", "customer_group_id": "group-1"}
    closed = client.post("/bills/close", json=close_payload)
    assert closed.status_code == 200
    assert closed.json()["customer_group_status"] == "ACTIVE"
    assert closed.json()["service_location_status"] == "OCCUPIED"
    assert client.post("/bills/close", json=close_payload).json() == closed.json()
    closed_bill = client.get("/billing/customer-groups/group-1").json()
    assert closed_bill["status"] == "CLOSED"
    assert len(closed_bill["lines"]) == 2 and len(closed_bill["payments"]) == 1
    rejected_order = client.post(
        "/orders",
        json={
            "request_id": "request-after-close",
            "customer_group_id": "group-1",
            "items": [{"menu_item_id": "coffee", "quantity": "1"}],
        },
    )
    assert rejected_order.status_code == 409
    premature_departure = client.post(
        "/customer-groups/group-1/depart",
        json={"request_id": "premature-departure"},
    )
    assert premature_departure.status_code == 409
    assert "COMPLETED" in premature_departure.json()["error"]["message"]
    completion_payload = {"request_id": "complete-request-1"}
    completion = client.post("/customer-groups/group-1/complete", json=completion_payload)
    assert completion.status_code == 200
    assert completion.json()["status"] == "COMPLETED"
    assert completion.json()["service_location_status"] == "OCCUPIED"
    assert completion.json()["service_location_released"] is False
    assert (
        client.post("/customer-groups/group-1/complete", json=completion_payload).json()
        == completion.json()
    )
    completion_context = client.get("/customer-groups/group-1/completion").json()
    assert completion_context["status"] == "COMPLETED"
    assert completion_context["can_complete"] is False

    no_bill_context = client.get("/customer-groups/group-2/completion")
    assert no_bill_context.status_code == 200
    assert no_bill_context.json()["bill_status"] is None
    no_bill_completion = client.post(
        "/customer-groups/group-2/complete",
        json={"request_id": "complete-request-2"},
    )
    assert no_bill_completion.status_code == 200
    assert no_bill_completion.json()["status"] == "COMPLETED"

    departure_context = client.get("/customer-groups/group-1/departure")
    assert departure_context.status_code == 200
    assert departure_context.json()["can_depart"] is True
    assert departure_context.json()["service_location_status"] == "OCCUPIED"
    departure_payload = {"request_id": "departure-request-1"}
    departure = client.post("/customer-groups/group-1/depart", json=departure_payload)
    assert departure.status_code == 200
    assert departure.json()["departure_status"] == "DEPARTED"
    assert departure.json()["service_location_status"] == "AVAILABLE"
    assert (
        client.post("/customer-groups/group-1/depart", json=departure_payload).json()
        == departure.json()
    )
    released_context = client.get("/customer-groups/group-1/departure").json()
    assert released_context["departure_status"] == "DEPARTED"
    assert released_context["service_location_status"] == "AVAILABLE"
    assert released_context["can_depart"] is False
    no_bill_departure = client.post(
        "/customer-groups/group-2/depart",
        json={"request_id": "departure-request-2"},
    )
    assert no_bill_departure.status_code == 200
    assert no_bill_departure.json()["service_location_status"] == "AVAILABLE"

    closing_context = client.get("/venue/closing-context", params={"venue_id": "venue-1"})
    assert closing_context.status_code == 200
    assert closing_context.json()["can_close"] is True
    assert closing_context.json()["readiness"] == {
        "active_customer_groups": 0,
        "occupied_service_locations": 0,
        "open_bills": 0,
        "unresolved_operational_work": 0,
    }
    closing_payload = {"request_id": "venue-close-1", "venue_id": "venue-1"}
    venue_closed = client.post("/venue/close", json=closing_payload)
    assert venue_closed.status_code == 200
    assert venue_closed.json()["status"] == "CLOSED_FOR_BUSINESS_DATE"
    assert client.post("/venue/close", json=closing_payload).json() == venue_closed.json()
    later_duplicate = client.post(
        "/venue/close",
        json={"request_id": "venue-close-2", "venue_id": "venue-1"},
    )
    assert later_duplicate.status_code == 200
    assert later_duplicate.json()["closing_report"] == venue_closed.json()["closing_report"]
    confirmed_closing = client.get("/venue/closing-context", params={"venue_id": "venue-1"}).json()
    assert confirmed_closing["closing_report"] == venue_closed.json()["closing_report"]

    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM ordering_events").fetchone()[0] == 8
        assert (
            connection.execute("SELECT count(*) FROM ordering_command_receipts").fetchone()[0] == 1
        )
        assert connection.execute("SELECT count(*) FROM payment_events").fetchone()[0] == 3
        assert connection.execute("SELECT count(*) FROM venue_closing_events").fetchone()[0] == 1
        assert connection.execute("SELECT count(*) FROM venue_closing_reports").fetchone()[0] == 1
        assert (
            connection.execute("SELECT count(*) FROM venue_closing_activity_log").fetchone()[0] == 1
        )
        assert (
            connection.execute("SELECT opening_status FROM venue_opening_venues").fetchone()[0]
            == "CLOSED_FOR_BUSINESS_DATE"
        )
        assert connection.execute("SELECT count(*) FROM payment_activity_log").fetchone()[0] == 1
        closing_logs = connection.execute(
            "SELECT count(*) FROM bill_closing_activity_log"
        ).fetchone()[0]
        assert closing_logs == 1
        assert connection.execute("SELECT count(*) FROM ordering_events").fetchone()[0] == 8
        assert (
            connection.execute(
                "SELECT status FROM ordering_customer_groups WHERE customer_group_id='group-1'"
            ).fetchone()[0]
            == "COMPLETED"
        )
        assert (
            connection.execute("SELECT count(*) FROM customer_group_completion_events").fetchone()[
                0
            ]
            == 2
        )
        assert (
            connection.execute(
                "SELECT count(*) FROM guest_arrival_events WHERE event_type='GUEST_DEPARTED'"
            ).fetchone()[0]
            == 2
        )
        assert (
            connection.execute("SELECT count(*) FROM guest_departure_activity_log").fetchone()[0]
            == 2
        )
        assert connection.execute("SELECT count(*) FROM ordering_events").fetchone()[0] == 8
        assert connection.execute("SELECT count(*) FROM payment_events").fetchone()[0] == 3
        assert (
            connection.execute(
                "SELECT count(*) FROM customer_group_completion_activity_log"
            ).fetchone()[0]
            == 2
        )

    for protected_statement in (
        "DELETE FROM venue_closing_events",
        "UPDATE venue_closing_reports SET closed_by_id='other'",
        "INSERT INTO ordering_customer_groups VALUES "
        "('late-group','venue-1','B-12','waiter-1','ACTIVE',0)",
    ):
        with (
            psycopg.connect(postgres_connection_string) as connection,
            pytest.raises(psycopg.DatabaseError),
        ):
            connection.execute(protected_statement)


def test_transaction_rolls_back_without_commit(postgres_connection_string: str) -> None:
    factory = PostgresOrderingUnitOfWorkFactory(postgres_connection_string)
    with factory.create() as unit:
        group = unit.customer_groups.get(customer_group_id="group-1")
        assert group is not None
        # Merely loading authoritative state cannot create persisted history.
    with psycopg.connect(postgres_connection_string) as connection:
        assert connection.execute("SELECT count(*) FROM ordering_events").fetchone()[0] == 0
