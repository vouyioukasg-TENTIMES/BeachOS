"""Authoritative server clock adapter."""

from datetime import UTC, datetime


class SystemClock:
    """Returns timezone-aware UTC instants from the server clock."""

    def now(self) -> datetime:
        return datetime.now(UTC)
