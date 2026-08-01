"""PostgreSQL Ordering adapters."""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from typing import Any

import psycopg

from beachos_api.packs.beachos.ordering.application.dtos import (
    BillDTO,
    OrderDTO,
    OrderItemDTO,
    SubmitOrderResult,
    TicketDTO,
)
from beachos_api.packs.beachos.ordering.domain import (
    CustomerGroup,
    CustomerGroupStatus,
    Destination,
    MenuItem,
    Money,
)
from beachos_api.packs.beachos.ordering.infrastructure.errors import (
    OrderingConcurrencyError,
)
from beachos_api.packs.beachos.ordering.infrastructure.persistence.mapping import (
    event_from_data,
    event_to_data,
)


class PostgresCustomerGroupRepository:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._loaded_versions: dict[str, int] = {}

    def get(self, *, customer_group_id: str) -> CustomerGroup | None:
        row = self._connection.execute(
            """
            SELECT customer_group_id, venue_id, service_location_id,
                   responsible_waiter_id, status, stream_version
            FROM ordering_customer_groups
            WHERE customer_group_id = %s
            """,
            (customer_group_id,),
        ).fetchone()
        if row is None:
            return None
        event_rows = self._connection.execute(
            """
            SELECT event_type, event_data, occurred_at
            FROM ordering_events
            WHERE customer_group_id = %s
            ORDER BY sequence
            """,
            (customer_group_id,),
        ).fetchall()
        events = tuple(
            event_from_data(event["event_type"], event["event_data"], event["occurred_at"])
            for event in event_rows
        )
        closed_row = self._connection.execute(
            """SELECT EXISTS(
                    SELECT 1 FROM payment_events
                    WHERE event_type='BILL_CLOSED'
                      AND event_data->>'customer_group_id'=%s
                ) AS closed""",
            (customer_group_id,),
        ).fetchone()
        if closed_row is None:
            raise OrderingConcurrencyError("Bill closing state is unavailable")
        bill_closed = closed_row["closed"]
        group = CustomerGroup.restore(
            customer_group_id=row["customer_group_id"],
            venue_id=row["venue_id"],
            service_location_id=row["service_location_id"],
            responsible_waiter_id=row["responsible_waiter_id"],
            status=CustomerGroupStatus(row["status"]),
            events=events,
            bill_closed=bill_closed,
        )
        if group.version != row["stream_version"]:
            raise OrderingConcurrencyError("Ordering event stream version is inconsistent")
        self._loaded_versions[customer_group_id] = group.version
        return group

    def save(self, customer_group: CustomerGroup) -> None:
        expected = self._loaded_versions.get(customer_group.customer_group_id)
        if expected is None:
            raise OrderingConcurrencyError("Customer Group must be loaded before saving")
        events = customer_group.pull_events()
        if not events:
            raise OrderingConcurrencyError("Ordering save requires new Domain Events")
        updated = self._connection.execute(
            """
            UPDATE ordering_customer_groups
            SET stream_version = %s
            WHERE customer_group_id = %s AND stream_version = %s
            """,
            (customer_group.version, customer_group.customer_group_id, expected),
        )
        if updated.rowcount != 1:
            raise OrderingConcurrencyError(
                "The Customer Group changed. Review the current Order state."
            )
        for sequence, event in enumerate(events, start=expected + 1):
            event_type, event_data, occurred_at = event_to_data(event)
            self._connection.execute(
                """
                INSERT INTO ordering_events (
                    customer_group_id, sequence, event_type, event_data, occurred_at
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    customer_group.customer_group_id,
                    sequence,
                    event_type,
                    json.dumps(event_data),
                    occurred_at,
                ),
            )
        self._loaded_versions[customer_group.customer_group_id] = customer_group.version


class PostgresMenuCatalog:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def available_for_venue(self, *, venue_id: str) -> tuple[MenuItem, ...]:
        rows = self._connection.execute(
            """
            SELECT menu_item_id, item_name, category_name, unit_price,
                   currency, destination, available
            FROM ordering_menu_items
            WHERE venue_id = %s AND available = TRUE
            ORDER BY category_order, item_order
            """,
            (venue_id,),
        ).fetchall()
        return tuple(
            MenuItem(
                menu_item_id=row["menu_item_id"],
                name=row["item_name"],
                category_name=row["category_name"],
                price=Money(Decimal(row["unit_price"]), row["currency"]),
                destination=Destination(row["destination"]),
                available=row["available"],
            )
            for row in rows
        )


def _result_to_data(result: SubmitOrderResult) -> dict[str, Any]:
    return {
        "request_id": result.request_id,
        "order": {
            "order_id": result.order.order_id,
            "customer_group_id": result.order.customer_group_id,
            "submitted_at": result.order.submitted_at.isoformat(),
            "submitted_by_id": result.order.submitted_by_id,
            "service_location_id": result.order.service_location_id,
            "responsible_waiter_id": result.order.responsible_waiter_id,
            "items": [
                {
                    "order_item_id": item.order_item_id,
                    "menu_item_id": item.menu_item_id,
                    "name": item.name,
                    "quantity": str(item.quantity),
                    "unit_price": str(item.unit_price),
                    "amount": str(item.amount),
                    "currency": item.currency,
                    "destination": item.destination,
                    "note": item.note,
                }
                for item in result.order.items
            ],
        },
        "tickets": [
            {
                "ticket_id": ticket.ticket_id,
                "destination": ticket.destination,
                "item_ids": list(ticket.item_ids),
            }
            for ticket in result.tickets
        ],
        "bill": (
            {
                "bill_id": result.bill.bill_id,
                "currency": result.bill.currency,
                "total": str(result.bill.total),
                "line_count": result.bill.line_count,
            }
            if result.bill
            else None
        ),
    }


def _result_from_data(data: dict[str, Any]) -> SubmitOrderResult:
    order = data["order"]
    bill = data["bill"]
    return SubmitOrderResult(
        request_id=data["request_id"],
        order=OrderDTO(
            order_id=order["order_id"],
            customer_group_id=order["customer_group_id"],
            submitted_at=datetime.fromisoformat(order["submitted_at"]),
            submitted_by_id=order["submitted_by_id"],
            service_location_id=order["service_location_id"],
            responsible_waiter_id=order["responsible_waiter_id"],
            items=tuple(
                OrderItemDTO(
                    item["order_item_id"],
                    item["menu_item_id"],
                    item["name"],
                    Decimal(item["quantity"]),
                    Decimal(item["unit_price"]),
                    Decimal(item["amount"]),
                    item["currency"],
                    item["destination"],
                    item["note"],
                )
                for item in order["items"]
            ),
        ),
        tickets=tuple(
            TicketDTO(ticket["ticket_id"], ticket["destination"], tuple(ticket["item_ids"]))
            for ticket in data["tickets"]
        ),
        bill=(
            BillDTO(
                bill["bill_id"],
                bill["currency"],
                Decimal(bill["total"]),
                bill["line_count"],
            )
            if bill
            else None
        ),
    )


class PostgresCommandReceiptStore:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> SubmitOrderResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM ordering_command_receipts WHERE request_id = %s",
            (request_id,),
        ).fetchone()
        return _result_from_data(row["result_data"]) if row else None

    def save(self, *, request_id: str, result: SubmitOrderResult) -> None:
        self._connection.execute(
            """
            INSERT INTO ordering_command_receipts (request_id, customer_group_id, result_data)
            VALUES (%s, %s, %s)
            """,
            (
                request_id,
                result.order.customer_group_id,
                json.dumps(_result_to_data(result)),
            ),
        )
