"""PostgreSQL Kitchen Operations adapters."""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from typing import Any

import psycopg

from beachos_api.packs.beachos.kitchen.application.dtos import (
    AcknowledgeKitchenTicketResult,
    KitchenTicketDTO,
    KitchenTicketItemDTO,
)
from beachos_api.packs.beachos.kitchen.domain import KitchenTicket
from beachos_api.packs.beachos.kitchen.infrastructure.errors import (
    KitchenConcurrencyError,
)
from beachos_api.packs.beachos.kitchen.infrastructure.persistence.mapping import (
    event_from_data,
    event_to_data,
    source_items_from_data,
)


class PostgresKitchenTicketRepository:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._loaded_versions: dict[str, int] = {}

    def _from_source_row(self, row: dict[str, Any]) -> KitchenTicket:
        ticket_id = row["event_data"]["ticket_id"]
        event_rows = self._connection.execute(
            """
            SELECT event_type, event_data, occurred_at
            FROM kitchen_events
            WHERE ticket_id = %s
            ORDER BY sequence
            """,
            (ticket_id,),
        ).fetchall()
        events = tuple(
            event_from_data(event["event_type"], event["event_data"], event["occurred_at"])
            for event in event_rows
        )
        ticket = KitchenTicket.restore(
            ticket_id=ticket_id,
            order_id=row["event_data"]["order_id"],
            customer_group_id=row["customer_group_id"],
            venue_id=row["venue_id"],
            submission_service_location_id=row["event_data"]["service_location_id"],
            current_service_location_id=row["current_service_location_id"],
            responsible_service_staff_id=row["event_data"]["responsible_waiter_id"],
            submitted_at=datetime.fromisoformat(row["event_data"]["created_at"]),
            items=source_items_from_data(row["event_data"]),
            events=events,
        )
        stream_version = row["stream_version"] or 0
        if ticket.version != stream_version:
            raise KitchenConcurrencyError("Kitchen event stream version is inconsistent")
        self._loaded_versions[ticket_id] = ticket.version
        return ticket

    def get(self, *, ticket_id: str) -> KitchenTicket | None:
        row = self._connection.execute(
            """
            SELECT event_data, events.customer_group_id, groups.venue_id,
                   groups.service_location_id AS current_service_location_id,
                   streams.stream_version
            FROM ordering_events AS events
            JOIN ordering_customer_groups AS groups
              ON groups.customer_group_id = events.customer_group_id
            LEFT JOIN kitchen_ticket_streams AS streams
              ON streams.ticket_id = events.event_data ->> 'ticket_id'
            WHERE events.event_type = 'KITCHEN_TICKET_CREATED'
              AND events.event_data ->> 'ticket_id' = %s
            """,
            (ticket_id,),
        ).fetchone()
        return self._from_source_row(row) if row else None

    def list_for_venue(self, *, venue_id: str) -> tuple[KitchenTicket, ...]:
        rows = self._connection.execute(
            """
            SELECT event_data, events.customer_group_id, groups.venue_id,
                   groups.service_location_id AS current_service_location_id,
                   streams.stream_version
            FROM ordering_events AS events
            JOIN ordering_customer_groups AS groups
              ON groups.customer_group_id = events.customer_group_id
            LEFT JOIN kitchen_ticket_streams AS streams
              ON streams.ticket_id = events.event_data ->> 'ticket_id'
            WHERE events.event_type = 'KITCHEN_TICKET_CREATED'
              AND groups.venue_id = %s
            ORDER BY events.occurred_at, events.event_data ->> 'ticket_id'
            """,
            (venue_id,),
        ).fetchall()
        return tuple(self._from_source_row(row) for row in rows)

    def save(self, ticket: KitchenTicket) -> None:
        expected = self._loaded_versions.get(ticket.ticket_id)
        if expected is None:
            raise KitchenConcurrencyError("Kitchen Ticket must be loaded before saving")
        events = ticket.pull_events()
        if not events:
            raise KitchenConcurrencyError("Kitchen save requires new Domain Events")
        self._connection.execute(
            """
            INSERT INTO kitchen_ticket_streams (ticket_id, stream_version)
            VALUES (%s, 0)
            ON CONFLICT (ticket_id) DO NOTHING
            """,
            (ticket.ticket_id,),
        )
        updated = self._connection.execute(
            """
            UPDATE kitchen_ticket_streams
            SET stream_version = %s
            WHERE ticket_id = %s AND stream_version = %s
            """,
            (ticket.version, ticket.ticket_id, expected),
        )
        if updated.rowcount != 1:
            raise KitchenConcurrencyError(
                "The Kitchen Ticket changed. Review its current acknowledgement."
            )
        for sequence, event in enumerate(events, start=expected + 1):
            event_type, event_data, occurred_at = event_to_data(event)
            self._connection.execute(
                """
                INSERT INTO kitchen_events (
                    ticket_id, sequence, event_type, event_data, occurred_at
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    ticket.ticket_id,
                    sequence,
                    event_type,
                    json.dumps(event_data),
                    occurred_at,
                ),
            )
        self._loaded_versions[ticket.ticket_id] = ticket.version


def _result_to_data(result: AcknowledgeKitchenTicketResult) -> dict[str, Any]:
    ticket = result.ticket
    return {
        "request_id": result.request_id,
        "ticket": {
            "ticket_id": ticket.ticket_id,
            "order_id": ticket.order_id,
            "customer_group_id": ticket.customer_group_id,
            "venue_id": ticket.venue_id,
            "submission_service_location_id": ticket.submission_service_location_id,
            "current_service_location_id": ticket.current_service_location_id,
            "responsible_service_staff_id": ticket.responsible_service_staff_id,
            "submitted_at": ticket.submitted_at.isoformat(),
            "items": [
                {
                    "order_item_id": item.order_item_id,
                    "name": item.name,
                    "quantity": str(item.quantity),
                    "note": item.note,
                }
                for item in ticket.items
            ],
            "acknowledged_by_id": ticket.acknowledged_by_id,
            "acknowledged_at": (
                ticket.acknowledged_at.isoformat() if ticket.acknowledged_at else None
            ),
            "ready_by_id": ticket.ready_by_id,
            "ready_at": ticket.ready_at.isoformat() if ticket.ready_at else None,
            "collected_by_id": ticket.collected_by_id,
            "collected_at": ticket.collected_at.isoformat() if ticket.collected_at else None,
            "delivered_by_id": ticket.delivered_by_id,
            "delivered_at": ticket.delivered_at.isoformat() if ticket.delivered_at else None,
        },
    }


def _result_from_data(data: dict[str, Any]) -> AcknowledgeKitchenTicketResult:
    ticket = data["ticket"]
    return AcknowledgeKitchenTicketResult(
        request_id=data["request_id"],
        ticket=KitchenTicketDTO(
            ticket_id=ticket["ticket_id"],
            order_id=ticket["order_id"],
            customer_group_id=ticket["customer_group_id"],
            venue_id=ticket["venue_id"],
            submission_service_location_id=ticket["submission_service_location_id"],
            current_service_location_id=ticket["current_service_location_id"],
            responsible_service_staff_id=ticket["responsible_service_staff_id"],
            submitted_at=datetime.fromisoformat(ticket["submitted_at"]),
            items=tuple(
                KitchenTicketItemDTO(
                    item["order_item_id"],
                    item["name"],
                    Decimal(item["quantity"]),
                    item["note"],
                )
                for item in ticket["items"]
            ),
            acknowledged_by_id=ticket["acknowledged_by_id"],
            acknowledged_at=(
                datetime.fromisoformat(ticket["acknowledged_at"])
                if ticket["acknowledged_at"]
                else None
            ),
            ready_by_id=ticket.get("ready_by_id"),
            ready_at=datetime.fromisoformat(ticket["ready_at"]) if ticket.get("ready_at") else None,
            collected_by_id=ticket.get("collected_by_id"),
            collected_at=datetime.fromisoformat(ticket["collected_at"])
            if ticket.get("collected_at")
            else None,
            delivered_by_id=ticket.get("delivered_by_id"),
            delivered_at=datetime.fromisoformat(ticket["delivered_at"])
            if ticket.get("delivered_at")
            else None,
        ),
    )


class PostgresKitchenCommandReceiptStore:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> AcknowledgeKitchenTicketResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM kitchen_command_receipts WHERE request_id = %s",
            (request_id,),
        ).fetchone()
        return _result_from_data(row["result_data"]) if row else None

    def save(self, *, request_id: str, result: AcknowledgeKitchenTicketResult) -> None:
        self._connection.execute(
            """
            INSERT INTO kitchen_command_receipts (request_id, ticket_id, result_data)
            VALUES (%s, %s, %s)
            """,
            (
                request_id,
                result.ticket.ticket_id,
                json.dumps(_result_to_data(result)),
            ),
        )
