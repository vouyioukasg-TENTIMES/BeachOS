"""PostgreSQL-backed Venue Business Date policy adapter."""

from datetime import timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import psycopg
from psycopg.rows import dict_row

from beachos_api.packs.beachos.venue_opening.application.ports import Clock
from beachos_api.packs.beachos.venue_opening.domain import BusinessDate
from beachos_api.packs.beachos.venue_opening.infrastructure.errors import (
    BusinessDatePolicyNotFoundError,
    InfrastructureError,
)


class PostgresBusinessDateProvider:
    """Derives Business Date from authoritative time and Venue policy."""

    def __init__(self, *, connection_string: str, clock: Clock) -> None:
        self._connection_string = connection_string
        self._clock = clock

    def current_for(self, *, venue_id: str) -> BusinessDate:
        with psycopg.connect(self._connection_string, row_factory=dict_row) as connection:
            row = connection.execute(
                """
                SELECT timezone_name, rollover_time
                FROM venue_business_date_policies
                WHERE venue_id = %s
                """,
                (venue_id,),
            ).fetchone()

        if row is None:
            raise BusinessDatePolicyNotFoundError("no Business Date policy exists for the Venue")

        try:
            timezone = ZoneInfo(row["timezone_name"])
        except ZoneInfoNotFoundError as error:
            raise InfrastructureError("the Venue Business Date timezone is unavailable") from error

        local_now = self._clock.now().astimezone(timezone)
        business_date = local_now.date()
        if local_now.timetz().replace(tzinfo=None) < row["rollover_time"]:
            business_date -= timedelta(days=1)
        return BusinessDate(business_date)
