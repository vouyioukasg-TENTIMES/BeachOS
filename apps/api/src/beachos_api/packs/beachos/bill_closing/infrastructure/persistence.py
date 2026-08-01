"""PostgreSQL Bill Closing adapters."""

import json
from datetime import datetime
from types import TracebackType
from typing import Any, cast

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.bill_closing.application.service import CloseBillResult, Unit
from beachos_api.packs.beachos.bill_closing.domain import (
    BillClosed,
    BillClosingAggregate,
    BillFullyPaid,
    PaymentRecorded,
)
from beachos_api.packs.beachos.bill_closing.domain.model import ClosingEvent


class BillClosingConcurrencyError(RuntimeError): ...


class BillRepository:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._expected: dict[str, int] = {}

    def load(self, *, customer_group_id: str) -> BillClosingAggregate | None:
        stream = self._connection.execute(
            "SELECT bill_id,stream_version FROM payment_streams WHERE customer_group_id=%s",
            (customer_group_id,),
        ).fetchone()
        if stream is None:
            return None
        rows = self._connection.execute(
            """SELECT event_type,event_data,occurred_at FROM payment_events
            WHERE bill_id=%s ORDER BY sequence""",
            (stream["bill_id"],),
        ).fetchall()
        events: list[ClosingEvent] = []
        for row in rows:
            data, at = row["event_data"], row["occurred_at"]
            if row["event_type"] == "PAYMENT_RECORDED":
                events.append(PaymentRecorded(data["bill_id"], data["customer_group_id"], at))
            elif row["event_type"] == "BILL_FULLY_PAID":
                events.append(BillFullyPaid(data["bill_id"], data["customer_group_id"], at))
            elif row["event_type"] == "BILL_CLOSED":
                events.append(
                    BillClosed(data["bill_id"], data["customer_group_id"], data["closed_by_id"], at)
                )
        if stream["stream_version"] != len(rows):
            raise BillClosingConcurrencyError("financial event stream is inconsistent")
        self._expected[stream["bill_id"]] = stream["stream_version"]
        return BillClosingAggregate.restore(
            bill_id=stream["bill_id"], customer_group_id=customer_group_id, events=tuple(events)
        )

    def save(self, bill: BillClosingAggregate) -> None:
        expected = self._expected.get(bill.bill_id)
        if expected is None:
            raise BillClosingConcurrencyError("Bill must be loaded before closing")
        updated = self._connection.execute(
            """UPDATE payment_streams SET stream_version=%s
            WHERE bill_id=%s AND stream_version=%s""",
            (bill.version, bill.bill_id, expected),
        )
        if updated.rowcount != 1:
            raise BillClosingConcurrencyError("Bill changed. Reload before closing.")
        for sequence, event in enumerate(bill.pull_events(), expected + 1):
            self._connection.execute(
                """INSERT INTO payment_events(
                    bill_id,sequence,event_type,event_data,occurred_at
                ) VALUES(%s,%s,'BILL_CLOSED',%s,%s)""",
                (
                    bill.bill_id,
                    sequence,
                    json.dumps(
                        {
                            "bill_id": event.bill_id,
                            "customer_group_id": event.customer_group_id,
                            "closed_by_id": event.closed_by_id,
                        }
                    ),
                    event.occurred_at,
                ),
            )


def _data(result: CloseBillResult) -> dict[str, str]:
    return {
        "request_id": result.request_id,
        "bill_id": result.bill_id,
        "customer_group_id": result.customer_group_id,
        "status": result.status,
        "closed_by_id": result.closed_by_id,
        "closed_at": result.closed_at.isoformat(),
        "customer_group_status": result.customer_group_status,
        "service_location_status": result.service_location_status,
    }


class ReceiptStore:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> CloseBillResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM bill_closing_receipts WHERE request_id=%s", (request_id,)
        ).fetchone()
        if not row:
            return None
        data = row["result_data"]
        return CloseBillResult(
            data["request_id"],
            data["bill_id"],
            data["customer_group_id"],
            data["status"],
            data["closed_by_id"],
            datetime.fromisoformat(data["closed_at"]),
            data["customer_group_status"],
            data["service_location_status"],
        )

    def save(self, result: CloseBillResult) -> None:
        self._connection.execute(
            "INSERT INTO bill_closing_receipts(request_id,bill_id,result_data) VALUES(%s,%s,%s)",
            (result.request_id, result.bill_id, json.dumps(_data(result))),
        )


class ActivityLog:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def record(self, *, result: CloseBillResult) -> None:
        self._connection.execute(
            """INSERT INTO bill_closing_activity_log(
                request_id,bill_id,customer_group_id,actor_id,action_name,occurred_at
            ) VALUES(%s,%s,%s,%s,'BILL_CLOSED',%s)""",
            (
                result.request_id,
                result.bill_id,
                result.customer_group_id,
                result.closed_by_id,
                result.closed_at,
            ),
        )


class PostgresBillClosingUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, Any]] | None = None
        self._committed = False

    def __enter__(self) -> "PostgresBillClosingUnitOfWork":
        connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._connection = connection
        self.bills, self.receipts, self.activity = (
            BillRepository(connection),
            ReceiptStore(connection),
            ActivityLog(connection),
        )
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


class PostgresBillClosingUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> Unit:
        return cast(Unit, PostgresBillClosingUnitOfWork(self._connection_string))
