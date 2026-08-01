"""Explicit projection from existing authoritative financial event streams."""

from datetime import datetime
from decimal import Decimal
from typing import Any

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.billing.domain import (
    Bill,
    BillCreated,
    BillLineAdded,
    PaymentRecorded,
)


class PostgresBillReader:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def get(self, *, customer_group_id: str) -> Bill | None:
        with psycopg.connect(self._connection_string, row_factory=dict_row) as connection:
            rows = connection.execute(
                """
                SELECT event_type,event_data,occurred_at
                FROM ordering_events
                WHERE customer_group_id=%s
                  AND event_type IN ('BILL_CREATED','BILL_LINE_ADDED')
                ORDER BY sequence
                """,
                (customer_group_id,),
            ).fetchall()
            payment_rows = connection.execute(
                """SELECT event_data,occurred_at FROM payment_events
                WHERE event_type='PAYMENT_RECORDED'
                  AND event_data->>'customer_group_id'=%s ORDER BY sequence""",
                (customer_group_id,),
            ).fetchall()
        if not rows:
            return None
        events = (
            *tuple(self._map(row) for row in rows),
            *tuple(
                PaymentRecorded(
                    row["event_data"]["payment_id"],
                    row["event_data"]["bill_id"],
                    Decimal(row["event_data"]["amount"]),
                    row["event_data"]["currency"],
                    row["event_data"]["method"],
                    row["event_data"]["recorded_by_id"],
                    row["occurred_at"],
                )
                for row in payment_rows
            ),
        )
        return Bill.restore(events)

    @staticmethod
    def _map(row: dict[str, Any]) -> BillCreated | BillLineAdded:
        data = row["event_data"]
        at: datetime = row["occurred_at"]
        if row["event_type"] == "BILL_CREATED":
            return BillCreated(data["bill_id"], data["customer_group_id"], data["currency"], at)
        quantity = Decimal(data.get("quantity", "1"))
        amount = Decimal(data["amount"])
        return BillLineAdded(
            data["bill_id"],
            data["bill_line_id"],
            data["description"],
            quantity,
            Decimal(data.get("unit_price", data["amount"])),
            amount,
            data["currency"],
            data.get("source", "ORDER_ITEM"),
            at,
        )
