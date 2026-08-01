"""PostgreSQL Activity Log adapter."""

import psycopg

from beachos_api.packs.beachos.venue_opening.application.dtos import (
    ActivityLogRecord,
)


class PostgresActivityLog:
    """Stages append-only Venue Opening Activity Log records."""

    def __init__(self, connection: psycopg.Connection[object]) -> None:
        self._connection = connection

    def record_venue_opened(self, record: ActivityLogRecord) -> None:
        self._connection.execute(
            """
            INSERT INTO venue_opening_activity_log (
                request_id,
                actor_id,
                venue_id,
                business_date,
                action_name,
                occurred_at
            )
            VALUES (%s, %s, %s, %s, 'VENUE_OPENED_FOR_BUSINESS_DATE', %s)
            """,
            (
                record.request_id,
                record.actor_id,
                record.venue_id,
                record.business_date,
                record.occurred_at,
            ),
        )
