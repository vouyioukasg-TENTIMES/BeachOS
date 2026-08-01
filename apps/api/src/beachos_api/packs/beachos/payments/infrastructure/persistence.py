"""PostgreSQL adapters for atomic, event-sourced Cash Payment recording."""

import json
from datetime import datetime
from decimal import Decimal
from types import TracebackType
from typing import Any, cast
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.billing.domain import Bill
from beachos_api.packs.beachos.billing.infrastructure.persistence import PostgresBillReader
from beachos_api.packs.beachos.payments.application.service import PaymentResult, Unit
from beachos_api.packs.beachos.payments.domain import (
    BillFullyPaid,
    PaymentAggregate,
    PaymentRecorded,
)


class PaymentConcurrencyError(RuntimeError): ...


class UUIDPaymentIdentities:
    def new_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid4()}"


class ConnectionBillReader:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, customer_group_id: str) -> Bill | None:
        rows = self._connection.execute(
            """SELECT event_type,event_data,occurred_at FROM ordering_events
            WHERE customer_group_id=%s AND event_type IN ('BILL_CREATED','BILL_LINE_ADDED')
            ORDER BY sequence""",
            (customer_group_id,),
        ).fetchall()
        if not rows:
            return None
        return Bill.restore(tuple(PostgresBillReader._map(row) for row in rows))


def _event_from_row(row: dict[str, Any]) -> PaymentRecorded | BillFullyPaid:
    data, at = row["event_data"], row["occurred_at"]
    if row["event_type"] == "PAYMENT_RECORDED":
        return PaymentRecorded(
            data["payment_id"],
            data["bill_id"],
            data["customer_group_id"],
            Decimal(data["amount"]),
            data["currency"],
            data["method"],
            data["recorded_by_id"],
            at,
        )
    return BillFullyPaid(data["bill_id"], data["customer_group_id"], at)


class PaymentRepository:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._expected: dict[str, int] = {}

    def load(self, bill: Bill) -> PaymentAggregate:
        row = self._connection.execute(
            "SELECT stream_version FROM payment_streams WHERE bill_id=%s", (bill.bill_id,)
        ).fetchone()
        event_rows = self._connection.execute(
            """SELECT event_type,event_data,occurred_at FROM payment_events
            WHERE bill_id=%s ORDER BY sequence""",
            (bill.bill_id,),
        ).fetchall()
        events = tuple(
            _event_from_row(event)
            for event in event_rows
            if event["event_type"] in {"PAYMENT_RECORDED", "BILL_FULLY_PAID"}
        )
        expected = row["stream_version"] if row else 0
        if expected != len(event_rows):
            raise PaymentConcurrencyError("Payment event stream is inconsistent")
        self._expected[bill.bill_id] = expected
        return PaymentAggregate.restore(
            bill_id=bill.bill_id,
            customer_group_id=bill.customer_group_id,
            total=bill.total,
            currency=bill.currency,
            events=events,
        )

    def save(self, aggregate: PaymentAggregate) -> None:
        expected = self._expected.get(aggregate.bill_id)
        if expected is None:
            raise PaymentConcurrencyError("Payment aggregate must be loaded before saving")
        if expected == 0:
            inserted = self._connection.execute(
                """INSERT INTO payment_streams(bill_id,customer_group_id,stream_version)
                VALUES(%s,%s,%s) ON CONFLICT DO NOTHING""",
                (aggregate.bill_id, aggregate.customer_group_id, aggregate.version),
            )
            if inserted.rowcount != 1:
                raise PaymentConcurrencyError("Bill Payment state changed; reload before retrying")
        else:
            updated = self._connection.execute(
                """UPDATE payment_streams SET stream_version=%s
                WHERE bill_id=%s AND stream_version=%s""",
                (aggregate.version, aggregate.bill_id, expected),
            )
            if updated.rowcount != 1:
                raise PaymentConcurrencyError("Bill Payment state changed; reload before retrying")
        for sequence, event in enumerate(aggregate.pull_events(), expected + 1):
            if isinstance(event, PaymentRecorded):
                kind = "PAYMENT_RECORDED"
                data = {
                    "payment_id": event.payment_id,
                    "bill_id": event.bill_id,
                    "customer_group_id": event.customer_group_id,
                    "amount": str(event.amount),
                    "currency": event.currency,
                    "method": event.method,
                    "recorded_by_id": event.recorded_by_id,
                }
            else:
                kind = "BILL_FULLY_PAID"
                data = {"bill_id": event.bill_id, "customer_group_id": event.customer_group_id}
            self._connection.execute(
                """INSERT INTO payment_events(
                    bill_id,sequence,event_type,event_data,occurred_at
                ) VALUES(%s,%s,%s,%s,%s)""",
                (aggregate.bill_id, sequence, kind, json.dumps(data), event.occurred_at),
            )


def _result_data(result: PaymentResult) -> dict[str, str]:
    return {
        key: str(value)
        for key, value in {
            "request_id": result.request_id,
            "payment_id": result.payment_id,
            "bill_id": result.bill_id,
            "customer_group_id": result.customer_group_id,
            "amount": result.amount,
            "currency": result.currency,
            "method": result.method,
            "recorded_by_id": result.recorded_by_id,
            "recorded_at": result.recorded_at.isoformat(),
            "balance": result.balance,
            "bill_status": result.bill_status,
        }.items()
    }


class ReceiptStore:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> PaymentResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM payment_command_receipts WHERE request_id=%s", (request_id,)
        ).fetchone()
        if not row:
            return None
        data = row["result_data"]
        return PaymentResult(
            data["request_id"],
            data["payment_id"],
            data["bill_id"],
            data["customer_group_id"],
            Decimal(data["amount"]),
            data["currency"],
            data["method"],
            data["recorded_by_id"],
            datetime.fromisoformat(data["recorded_at"]),
            Decimal(data["balance"]),
            data["bill_status"],
        )

    def save(self, result: PaymentResult) -> None:
        self._connection.execute(
            "INSERT INTO payment_command_receipts(request_id,bill_id,result_data) VALUES(%s,%s,%s)",
            (result.request_id, result.bill_id, json.dumps(_result_data(result))),
        )


class ActivityLog:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def record(self, *, result: PaymentResult) -> None:
        self._connection.execute(
            """INSERT INTO payment_activity_log(
                request_id,payment_id,bill_id,customer_group_id,actor_id,
                action_name,amount,currency,occurred_at
            ) VALUES(%s,%s,%s,%s,%s,'PAYMENT_RECORDED',%s,%s,%s)""",
            (
                result.request_id,
                result.payment_id,
                result.bill_id,
                result.customer_group_id,
                result.recorded_by_id,
                result.amount,
                result.currency,
                result.recorded_at,
            ),
        )


class PostgresPaymentUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, Any]] | None = None
        self._committed = False

    def __enter__(self) -> "PostgresPaymentUnitOfWork":
        connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._connection = connection
        self.bills = ConnectionBillReader(connection)
        self.payments = PaymentRepository(connection)
        self.receipts = ReceiptStore(connection)
        self.activity = ActivityLog(connection)
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exception_type, exception, traceback
        if self._connection is not None:
            if not self._committed:
                self._connection.rollback()
            self._connection.close()

    def commit(self) -> None:
        if self._connection is None:
            raise RuntimeError("unit of work is not entered")
        self._connection.commit()
        self._committed = True


class PostgresPaymentUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> Unit:
        return cast(Unit, PostgresPaymentUnitOfWork(self._connection_string))
