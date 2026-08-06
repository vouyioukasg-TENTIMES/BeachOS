"""PostgreSQL Venue Closing adapters."""

import json
from datetime import date, datetime
from types import TracebackType
from typing import Any, cast

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.venue_closing.application.service import (
    CloseVenueResult,
    Unit,
)
from beachos_api.packs.beachos.venue_closing.domain import (
    ClosingReadiness,
    ClosingReport,
    VenueClosed,
    VenueClosing,
)


class VenueClosingConcurrencyError(RuntimeError):
    """The Venue or closing readiness changed concurrently."""


class PostgresClosingVenues:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._expected: dict[tuple[str, date], int] = {}

    def get(self, *, venue_id: str, business_date: date) -> VenueClosing | None:
        row = self._connection.execute(
            """SELECT opening_status,aggregate_version FROM venue_opening_venues
            WHERE venue_id=%s AND business_date=%s""",
            (venue_id, business_date),
        ).fetchone()
        if row is None:
            return None
        report = self._connection.execute(
            """SELECT closed_at,closed_by_id,active_customer_groups,
            occupied_service_locations,open_bills,unresolved_operational_work
            FROM venue_closing_reports WHERE venue_id=%s AND business_date=%s""",
            (venue_id, business_date),
        ).fetchone()
        event = None
        if report is not None:
            readiness = ClosingReadiness(
                report["active_customer_groups"],
                report["occupied_service_locations"],
                report["open_bills"],
                report["unresolved_operational_work"],
            )
            closing_report = ClosingReport(
                venue_id,
                business_date,
                report["closed_at"],
                report["closed_by_id"],
                readiness,
            )
            event = VenueClosed(
                venue_id,
                business_date,
                report["closed_by_id"],
                closing_report,
                report["closed_at"],
            )
        self._expected[(venue_id, business_date)] = row["aggregate_version"]
        return VenueClosing.restore(
            venue_id=venue_id,
            business_date=business_date,
            status=row["opening_status"],
            event=event,
        )

    def save(self, venue: VenueClosing) -> None:
        key = (venue.venue_id, venue.business_date)
        expected = self._expected.get(key)
        if expected is None:
            raise VenueClosingConcurrencyError("Venue must be loaded before closing")
        events = venue.pull_events()
        if len(events) != 1:
            raise VenueClosingConcurrencyError("Venue Closing requires one new event")
        event = events[0]
        updated = self._connection.execute(
            """UPDATE venue_opening_venues
            SET opening_status='CLOSED_FOR_BUSINESS_DATE',aggregate_version=%s
            WHERE venue_id=%s AND business_date=%s
              AND opening_status='OPEN' AND aggregate_version=%s""",
            (expected + 1, venue.venue_id, venue.business_date, expected),
        )
        if updated.rowcount != 1:
            raise VenueClosingConcurrencyError("Venue Closing state changed")
        report = event.closing_report
        self._connection.execute(
            """INSERT INTO venue_closing_events(
                venue_id,business_date,event_type,event_data,occurred_at
            ) VALUES(%s,%s,'VENUE_CLOSED',%s,%s)""",
            (
                venue.venue_id,
                venue.business_date,
                json.dumps({"closed_by_id": event.closed_by_id}),
                event.occurred_at,
            ),
        )
        self._connection.execute(
            """INSERT INTO venue_closing_reports(
                venue_id,business_date,closed_at,closed_by_id,
                active_customer_groups,occupied_service_locations,
                open_bills,unresolved_operational_work
            ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                report.venue_id,
                report.business_date,
                report.closed_at,
                report.closed_by_id,
                report.readiness.active_customer_groups,
                report.readiness.occupied_service_locations,
                report.readiness.open_bills,
                report.readiness.unresolved_operational_work,
            ),
        )


class PostgresClosingReadiness:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def current(self, *, venue_id: str) -> ClosingReadiness:
        self._connection.execute(
            """LOCK TABLE ordering_customer_groups,guest_arrival_events,
            ordering_events,payment_events,kitchen_events,bar_events IN SHARE MODE"""
        )
        active_row = self._connection.execute(
            """SELECT count(*) AS count FROM ordering_customer_groups
            WHERE venue_id=%s AND status='ACTIVE'""",
            (venue_id,),
        ).fetchone()
        occupied_row = self._connection.execute(
            """WITH latest_occupancy AS (
                SELECT DISTINCT ON (location.service_location_id)
                    location.service_location_id,event.event_type
                FROM guest_arrival_service_locations AS location
                JOIN guest_arrival_events AS event
                  ON event.service_location_id=location.service_location_id
                WHERE location.venue_id=%s
                  AND event.event_type IN ('CUSTOMER_GROUP_OPENED','GUEST_DEPARTED')
                ORDER BY location.service_location_id,event.sequence DESC
            ) SELECT count(*) AS count FROM latest_occupancy
              WHERE event_type='CUSTOMER_GROUP_OPENED'""",
            (venue_id,),
        ).fetchone()
        open_bills_row = self._connection.execute(
            """SELECT count(*) AS count FROM ordering_events AS bill
            JOIN ordering_customer_groups AS customer_group
              ON customer_group.customer_group_id=bill.customer_group_id
            WHERE customer_group.venue_id=%s AND bill.event_type='BILL_CREATED'
              AND NOT EXISTS (
                SELECT 1 FROM payment_events AS payment
                WHERE payment.bill_id=bill.event_data->>'bill_id'
                  AND payment.event_type='BILL_CLOSED'
              )""",
            (venue_id,),
        ).fetchone()
        unresolved_row = self._connection.execute(
            """WITH tickets AS (
                SELECT event.event_type,event.event_data->>'ticket_id' AS ticket_id
                FROM ordering_events AS event
                JOIN ordering_customer_groups AS customer_group
                  ON customer_group.customer_group_id=event.customer_group_id
                WHERE customer_group.venue_id=%s
                  AND event.event_type IN ('KITCHEN_TICKET_CREATED','BAR_TICKET_CREATED')
            )
            SELECT count(*) AS count FROM tickets WHERE
              CASE WHEN event_type='KITCHEN_TICKET_CREATED' THEN COALESCE((
                SELECT event_type FROM kitchen_events
                WHERE kitchen_events.ticket_id=tickets.ticket_id
                ORDER BY sequence DESC LIMIT 1
              ),'') ELSE COALESCE((
                SELECT event_type FROM bar_events
                WHERE bar_events.ticket_id=tickets.ticket_id
                ORDER BY sequence DESC LIMIT 1
              ),'') END NOT IN ('KITCHEN_TICKET_DELIVERED','BAR_TICKET_DELIVERED')""",
            (venue_id,),
        ).fetchone()
        if None in (active_row, occupied_row, open_bills_row, unresolved_row):
            raise RuntimeError("Venue Closing readiness query returned no result")
        return ClosingReadiness(
            cast(dict[str, Any], active_row)["count"],
            cast(dict[str, Any], occupied_row)["count"],
            cast(dict[str, Any], open_bills_row)["count"],
            cast(dict[str, Any], unresolved_row)["count"],
        )


def _result_data(result: CloseVenueResult) -> dict[str, object]:
    report = result.closing_report
    return {
        "request_id": result.request_id,
        "status": result.status,
        "closing_report": {
            "venue_id": report.venue_id,
            "business_date": report.business_date.isoformat(),
            "closed_at": report.closed_at.isoformat(),
            "closed_by_id": report.closed_by_id,
            "active_customer_groups": report.active_customer_groups,
            "occupied_service_locations": report.occupied_service_locations,
            "open_bills": report.open_bills,
            "unresolved_operational_work": report.unresolved_operational_work,
        },
    }


class PostgresClosingReceipts:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def get(self, *, request_id: str) -> CloseVenueResult | None:
        row = self._connection.execute(
            "SELECT result_data FROM venue_closing_receipts WHERE request_id=%s",
            (request_id,),
        ).fetchone()
        if row is None:
            return None
        data = row["result_data"]
        report = data["closing_report"]
        from beachos_api.packs.beachos.venue_closing.application import ClosingReportDTO

        return CloseVenueResult(
            data["request_id"],
            data["status"],
            ClosingReportDTO(
                report["venue_id"],
                date.fromisoformat(report["business_date"]),
                datetime.fromisoformat(report["closed_at"]),
                report["closed_by_id"],
                report["active_customer_groups"],
                report["occupied_service_locations"],
                report["open_bills"],
                report["unresolved_operational_work"],
            ),
        )

    def save(self, result: CloseVenueResult) -> None:
        self._connection.execute(
            """INSERT INTO venue_closing_receipts(request_id,venue_id,business_date,result_data)
            VALUES(%s,%s,%s,%s)""",
            (
                result.request_id,
                result.closing_report.venue_id,
                result.closing_report.business_date,
                json.dumps(_result_data(result)),
            ),
        )


class PostgresClosingActivity:
    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection

    def record(self, *, result: CloseVenueResult) -> None:
        report = result.closing_report
        self._connection.execute(
            """INSERT INTO venue_closing_activity_log(
                request_id,venue_id,business_date,actor_id,action_name,occurred_at
            ) VALUES(%s,%s,%s,%s,'VENUE_CLOSED',%s)""",
            (
                result.request_id,
                report.venue_id,
                report.business_date,
                report.closed_by_id,
                report.closed_at,
            ),
        )


class PostgresVenueClosingUnitOfWork:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection: psycopg.Connection[dict[str, Any]] | None = None
        self._committed = False

    def __enter__(self) -> "PostgresVenueClosingUnitOfWork":
        connection = psycopg.connect(self._connection_string, row_factory=dict_row)
        self._connection = connection
        self.venues = PostgresClosingVenues(connection)
        self.readiness = PostgresClosingReadiness(connection)
        self.receipts = PostgresClosingReceipts(connection)
        self.activity = PostgresClosingActivity(connection)
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


class PostgresVenueClosingUnitOfWorkFactory:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    def create(self) -> Unit:
        return cast(Unit, PostgresVenueClosingUnitOfWork(self._connection_string))
