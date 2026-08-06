#!/usr/bin/env python3
"""Apply committed BeachOS migrations to an explicitly local database."""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from beachos_api.packs.beachos.venue_opening.infrastructure import apply_migrations


def main() -> None:
    connection_string = os.environ.get("BEACHOS_DATABASE_URL", "").strip()
    if not connection_string:
        raise SystemExit("BEACHOS_DATABASE_URL is required. Copy .env.example to .env first.")

    target = urlparse(connection_string)
    if target.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("Refusing to migrate a non-local database.")

    expected_database = os.environ.get("POSTGRES_DB", "").strip()
    actual_database = target.path.removeprefix("/")
    if not expected_database or actual_database != expected_database:
        raise SystemExit("BEACHOS_DATABASE_URL must name the POSTGRES_DB configured in .env.")

    apply_migrations(connection_string)
    print(f"BeachOS database is ready: {actual_database} on {target.hostname}")


if __name__ == "__main__":
    main()
