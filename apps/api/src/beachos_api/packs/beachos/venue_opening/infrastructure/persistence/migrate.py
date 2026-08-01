"""Minimal runner for committed, checksummed SQL migrations."""

from hashlib import sha256
from importlib.resources import files

import psycopg
from psycopg import sql

from beachos_api.packs.beachos.venue_opening.infrastructure.errors import (
    MigrationChecksumError,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.persistence import (
    migrations,
)

MIGRATIONS = (
    ("0001", "0001_venue_opening.sql"),
    ("0002", "0002_ordering.sql"),
    ("0003", "0003_kitchen_operations.sql"),
    ("0004", "0004_guest_arrival.sql"),
    ("0005", "0005_bar_operations.sql"),
    ("0006", "0006_basic_fulfilment.sql"),
    ("0007", "0007_cash_payments.sql"),
)


def apply_migrations(connection_string: str) -> None:
    """Apply each committed migration once and verify applied checksums."""

    with psycopg.connect(connection_string) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS beachos_schema_migrations (
                version text PRIMARY KEY,
                migration_name text NOT NULL,
                checksum text NOT NULL,
                applied_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        for version, migration_name in MIGRATIONS:
            migration = files(migrations).joinpath(migration_name).read_bytes()
            checksum = sha256(migration).hexdigest()
            applied = connection.execute(
                """
                SELECT checksum
                FROM beachos_schema_migrations
                WHERE version = %s
                """,
                (version,),
            ).fetchone()
            if applied is not None:
                if applied[0] != checksum:
                    raise MigrationChecksumError(
                        f"applied migration {version} has a different checksum"
                    )
                continue

            connection.execute(sql.SQL(migration.decode("utf-8")))
            connection.execute(
                """
                INSERT INTO beachos_schema_migrations (
                    version,
                    migration_name,
                    checksum
                )
                VALUES (%s, %s, %s)
                """,
                (version, migration_name, checksum),
            )
