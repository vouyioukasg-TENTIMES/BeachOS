"""PostgreSQL Venue aggregate repository."""

from typing import Any, cast

import psycopg
from psycopg import errors

from beachos_api.packs.beachos.venue_opening.domain import (
    BusinessDate,
    OpeningReport,
    OpeningStatus,
    Venue,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.errors import (
    AggregateNotLoadedError,
    OptimisticConcurrencyError,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.persistence.mapping import (
    restore_venue,
)

Key = tuple[str, BusinessDate]


class PostgresVenueRepository:
    """Maps complete Venue aggregates through one PostgreSQL connection."""

    def __init__(self, connection: psycopg.Connection[dict[str, Any]]) -> None:
        self._connection = connection
        self._loaded_versions: dict[Key, int] = {}
        self._loaded_history_lengths: dict[Key, int] = {}

    def get(
        self,
        *,
        venue_id: str,
        business_date: BusinessDate,
    ) -> Venue | None:
        venue_row = self._connection.execute(
            """
            SELECT
                venue_id,
                business_date,
                venue_name,
                opening_status,
                aggregate_version
            FROM venue_opening_venues
            WHERE venue_id = %s AND business_date = %s
            """,
            (venue_id, business_date.value),
        ).fetchone()
        if venue_row is None:
            return None

        department_rows = self._connection.execute(
            """
            SELECT
                department_id,
                department_name,
                responsible_person_id
            FROM venue_opening_departments
            WHERE venue_id = %s AND business_date = %s
            ORDER BY display_order
            """,
            (venue_id, business_date.value),
        ).fetchall()
        declaration_rows = self._connection.execute(
            """
            SELECT
                department_id,
                responsible_person_id,
                declared_by_id,
                readiness_status,
                declared_at,
                reason,
                comment
            FROM venue_opening_declarations
            WHERE venue_id = %s AND business_date = %s
            ORDER BY declaration_sequence
            """,
            (venue_id, business_date.value),
        ).fetchall()
        report_row = self._connection.execute(
            """
            SELECT opened_at, host_id
            FROM venue_opening_reports
            WHERE venue_id = %s AND business_date = %s
            """,
            (venue_id, business_date.value),
        ).fetchone()
        closing_report_row = self._connection.execute(
            """SELECT 1 FROM venue_closing_reports
            WHERE venue_id=%s AND business_date=%s""",
            (venue_id, business_date.value),
        ).fetchone()

        venue = restore_venue(
            venue_row=venue_row,
            department_rows=department_rows,
            declaration_rows=declaration_rows,
            report_row=report_row,
            closing_report_exists=closing_report_row is not None,
        )
        key = (venue_id, business_date)
        self._loaded_versions[key] = venue.aggregate_version
        self._loaded_history_lengths[key] = len(venue.opening_checklist.declaration_history)
        return venue

    def save(self, venue: Venue) -> None:
        key = (venue.venue_id, venue.business_date)
        expected_version = self._loaded_versions.get(key)
        if expected_version is None:
            self._insert_new(venue)
            return
        if venue.aggregate_version != expected_version + 1:
            raise AggregateNotLoadedError(
                "an existing Venue save requires exactly one new aggregate mutation"
            )

        updated = self._connection.execute(
            """
            UPDATE venue_opening_venues
            SET opening_status = %s, aggregate_version = %s
            WHERE
                venue_id = %s
                AND business_date = %s
                AND aggregate_version = %s
            """,
            (
                venue.opening_status.value,
                venue.aggregate_version,
                venue.venue_id,
                venue.business_date.value,
                expected_version,
            ),
        )
        if updated.rowcount != 1:
            raise OptimisticConcurrencyError("the Venue aggregate changed after it was loaded")

        history_start = self._loaded_history_lengths[key]
        self._insert_declarations(venue, history_start=history_start)
        if venue.opening_status is OpeningStatus.OPEN:
            self._insert_report(venue)

        self._loaded_versions[key] = venue.aggregate_version
        self._loaded_history_lengths[key] = len(venue.opening_checklist.declaration_history)

    def _insert_new(self, venue: Venue) -> None:
        try:
            self._connection.execute(
                """
                INSERT INTO venue_opening_venues (
                    venue_id,
                    business_date,
                    venue_name,
                    opening_status,
                    aggregate_version
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    venue.venue_id,
                    venue.business_date.value,
                    venue.name,
                    venue.opening_status.value,
                    venue.aggregate_version,
                ),
            )
        except errors.UniqueViolation as error:
            raise OptimisticConcurrencyError("the Venue aggregate already exists") from error

        for display_order, department in enumerate(venue.opening_checklist.departments.values()):
            self._connection.execute(
                """
                INSERT INTO venue_opening_departments (
                    venue_id,
                    business_date,
                    department_id,
                    display_order,
                    department_name,
                    responsible_person_id
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    venue.venue_id,
                    venue.business_date.value,
                    department.department_id,
                    display_order,
                    department.name,
                    department.responsible_person_id,
                ),
            )
        self._insert_declarations(venue, history_start=0)
        if venue.opening_status is OpeningStatus.OPEN:
            self._insert_report(venue)
        self._loaded_versions[(venue.venue_id, venue.business_date)] = venue.aggregate_version
        self._loaded_history_lengths[(venue.venue_id, venue.business_date)] = len(
            venue.opening_checklist.declaration_history
        )

    def _insert_declarations(self, venue: Venue, *, history_start: int) -> None:
        history = venue.opening_checklist.declaration_history
        for sequence, declaration in enumerate(
            history[history_start:],
            start=history_start + 1,
        ):
            self._connection.execute(
                """
                INSERT INTO venue_opening_declarations (
                    venue_id,
                    business_date,
                    declaration_sequence,
                    department_id,
                    responsible_person_id,
                    declared_by_id,
                    readiness_status,
                    declared_at,
                    reason,
                    comment
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    venue.venue_id,
                    venue.business_date.value,
                    sequence,
                    declaration.department_id,
                    declaration.responsible_person_id,
                    declaration.declared_by_id,
                    declaration.status.value,
                    declaration.declared_at,
                    declaration.reason,
                    declaration.comment,
                ),
            )

    def _insert_report(self, venue: Venue) -> None:
        report = cast(OpeningReport, venue.opening_report)
        self._connection.execute(
            """
            INSERT INTO venue_opening_reports (
                venue_id,
                business_date,
                opened_at,
                host_id
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                venue.venue_id,
                venue.business_date.value,
                report.opened_at,
                report.host_id,
            ),
        )
