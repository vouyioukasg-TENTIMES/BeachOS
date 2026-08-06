"""PostgreSQL Customer Group Completion adapters."""

import json
from datetime import datetime
from types import TracebackType
from typing import Any, cast

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.customer_completion.application.service import (
    CompleteCustomerGroupResult,
    Unit,
)
from beachos_api.packs.beachos.customer_completion.domain import (
    CustomerGroupCompleted,
    CustomerGroupCompletion,
)


class CompletionConcurrencyError(RuntimeError): ...


class GroupRepository:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._expected: dict[str, int] = {}

    def load(self, *, customer_group_id: str) -> CustomerGroupCompletion | None:
        row = self._connection.execute(
            "SELECT status FROM ordering_customer_groups WHERE customer_group_id=%s",
            (customer_group_id,),
        ).fetchone()
        if row is None:
            return None
        bill = self._connection.execute(
            """SELECT event_data->>'bill_id' AS bill_id FROM ordering_events
            WHERE customer_group_id=%s AND event_type='BILL_CREATED' LIMIT 1""",
            (customer_group_id,),
        ).fetchone()
        bill_status = None
        if bill:
            financial = self._connection.execute(
                """SELECT event_type FROM payment_events
                WHERE bill_id=%s ORDER BY sequence""",
                (bill["bill_id"],),
            ).fetchall()
            kinds = {event["event_type"] for event in financial}
            bill_status = (
                "CLOSED"
                if "BILL_CLOSED" in kinds
                else ("FULLY_PAID" if "BILL_FULLY_PAID" in kinds else "OPEN")
            )
        stream = self._connection.execute(
            """SELECT stream_version FROM customer_group_completion_streams
            WHERE customer_group_id=%s""",
            (customer_group_id,),
        ).fetchone()
        events = tuple(
            CustomerGroupCompleted(
                event["event_data"]["customer_group_id"],
                event["event_data"]["completed_by_id"],
                event["occurred_at"],
            )
            for event in self._connection.execute(
                """SELECT event_data,occurred_at FROM customer_group_completion_events
                WHERE customer_group_id=%s ORDER BY sequence""",
                (customer_group_id,),
            ).fetchall()
        )
        expected = stream["stream_version"] if stream else 0
        if expected != len(events):
            raise CompletionConcurrencyError("completion stream is inconsistent")
        self._expected[customer_group_id] = expected
        return CustomerGroupCompletion.restore(
            customer_group_id=customer_group_id,
            status=row["status"],
            bill_status=bill_status,
            events=events,
        )

    def save(self, group: CustomerGroupCompletion) -> None:
        expected = self._expected.get(group.customer_group_id)
        if expected is None:
            raise CompletionConcurrencyError("Customer Group must be loaded")
        if expected == 0:
            inserted = self._connection.execute(
                """INSERT INTO customer_group_completion_streams(
                    customer_group_id,stream_version
                ) VALUES(%s,%s) ON CONFLICT DO NOTHING""",
                (group.customer_group_id, group.version),
            )
            if inserted.rowcount != 1:
                raise CompletionConcurrencyError("completion state changed")
        else:
            raise CompletionConcurrencyError("Customer Group is already completed")
        updated = self._connection.execute(
            """UPDATE ordering_customer_groups SET status='COMPLETED'
            WHERE customer_group_id=%s AND status='ACTIVE'""",
            (group.customer_group_id,),
        )
        if updated.rowcount != 1:
            raise CompletionConcurrencyError("Customer Group is not ACTIVE")
        for sequence, event in enumerate(group.pull_events(), expected + 1):
            self._connection.execute(
                """INSERT INTO customer_group_completion_events(
                    customer_group_id,sequence,event_type,event_data,occurred_at
                ) VALUES(%s,%s,'CUSTOMER_GROUP_COMPLETED',%s,%s)""",
                (
                    group.customer_group_id,
                    sequence,
                    json.dumps(
                        {
                            "customer_group_id": event.customer_group_id,
                            "completed_by_id": event.completed_by_id,
                        }
                    ),
                    event.occurred_at,
                ),
            )


def _data(result: CompleteCustomerGroupResult) -> dict[str, object]:
    return {
        "request_id": result.request_id,
        "customer_group_id": result.customer_group_id,
        "status": result.status,
        "completed_by_id": result.completed_by_id,
        "completed_at": result.completed_at.isoformat(),
        "service_location_status": result.service_location_status,
        "service_location_released": result.service_location_released,
    }


class Receipts:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> CompleteCustomerGroupResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM customer_group_completion_receipts WHERE request_id=%s",
            (request_id,),
        ).fetchone()
        if not row:
            return None
        data = row["result_data"]
        return CompleteCustomerGroupResult(
            data["request_id"],
            data["customer_group_id"],
            data["status"],
            data["completed_by_id"],
            datetime.fromisoformat(data["completed_at"]),
            data["service_location_status"],
            data["service_location_released"],
        )

    def save(self, result: CompleteCustomerGroupResult) -> None:
        self._connection.execute(
            """INSERT INTO customer_group_completion_receipts(
                request_id,customer_group_id,result_data
            ) VALUES(%s,%s,%s)""",
            (result.request_id, result.customer_group_id, json.dumps(_data(result))),
        )


class Activity:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def record(self, *, result: CompleteCustomerGroupResult) -> None:
        self._connection.execute(
            """INSERT INTO customer_group_completion_activity_log(
                request_id,customer_group_id,actor_id,action_name,occurred_at
            ) VALUES(%s,%s,%s,'CUSTOMER_GROUP_COMPLETED',%s)""",
            (
                result.request_id,
                result.customer_group_id,
                result.completed_by_id,
                result.completed_at,
            ),
        )


class PostgresCompletionUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, Any]] | None = None
        self._committed = False

    def __enter__(self) -> "PostgresCompletionUnitOfWork":
        connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._connection = connection
        self.groups, self.receipts, self.activity = (
            GroupRepository(connection),
            Receipts(connection),
            Activity(connection),
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


class PostgresCompletionUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> Unit:
        return cast(Unit, PostgresCompletionUnitOfWork(self._connection_string))
