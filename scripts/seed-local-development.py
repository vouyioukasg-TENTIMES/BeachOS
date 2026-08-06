#!/usr/bin/env python3
"""Create non-operational local configuration for an empty BeachOS database."""

import os
from datetime import datetime, time, timedelta
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import psycopg


def main() -> None:
    if os.environ.get("APP_ENV") != "development":
        raise SystemExit("Refusing to seed outside APP_ENV=development.")

    connection_string = os.environ.get("BEACHOS_DATABASE_URL", "").strip()
    target = urlparse(connection_string)
    if target.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("Refusing to seed a non-local database.")

    expected_database = os.environ.get("POSTGRES_DB", "").strip()
    if not expected_database or target.path.removeprefix("/") != expected_database:
        raise SystemExit("BEACHOS_DATABASE_URL must name the local POSTGRES_DB.")

    timezone_name = "Europe/Athens"
    rollover = time(4)
    local_now = datetime.now(ZoneInfo(timezone_name))
    business_date = (local_now - timedelta(days=local_now.time() < rollover)).date()

    with psycopg.connect(connection_string) as connection:
        connection.execute(
            """
            INSERT INTO venue_business_date_policies (venue_id, timezone_name, rollover_time)
            VALUES ('venue-1', %s, %s)
            ON CONFLICT (venue_id) DO NOTHING
            """,
            (timezone_name, rollover),
        )
        connection.execute(
            """
            INSERT INTO venue_opening_venues (
                venue_id, business_date, venue_name, opening_status, aggregate_version
            ) VALUES ('venue-1', %s, 'Emerald Beach Club', 'CLOSED', 0)
            ON CONFLICT (venue_id, business_date) DO NOTHING
            """,
            (business_date,),
        )
        cursor = connection.cursor()
        cursor.executemany(
            """
            INSERT INTO venue_opening_departments (
                venue_id, business_date, department_id, display_order,
                department_name, responsible_person_id
            ) VALUES ('venue-1', %s, %s, %s, %s, %s)
            ON CONFLICT (venue_id, business_date, department_id) DO NOTHING
            """,
            [
                (business_date, "kitchen", 0, "Kitchen", "staff-kitchen"),
                (business_date, "bar", 1, "Bar", "staff-bar"),
            ],
        )
        cursor.executemany(
            """
            INSERT INTO guest_arrival_service_locations (
                service_location_id, venue_id, visible_name, digital_identity,
                location_type, initial_status, beach_sunbed_charge,
                charge_currency, charge_description
            ) VALUES (%s, 'venue-1', %s, %s, %s, 'AVAILABLE', %s, %s, %s)
            ON CONFLICT (service_location_id) DO NOTHING
            """,
            [
                (
                    "beach-a12",
                    "Beach A12",
                    "location-beach-a12",
                    "BEACH SUNBED",
                    20,
                    "EUR",
                    "Beach Sunbed charge",
                ),
                (
                    "pool-p07",
                    "Pool P07",
                    "location-pool-p07",
                    "POOL SUNBED",
                    None,
                    None,
                    None,
                ),
                (
                    "upper-u04",
                    "Upper U04",
                    "location-upper-u04",
                    "UPPER TABLE",
                    None,
                    None,
                    None,
                ),
            ],
        )
        cursor.executemany(
            """
            INSERT INTO ordering_menu_items (
                venue_id, menu_item_id, category_name, category_order, item_name,
                item_order, unit_price, currency, destination, available
            ) VALUES ('venue-1', %s, %s, %s, %s, %s, %s, 'EUR', %s, TRUE)
            ON CONFLICT (venue_id, menu_item_id) DO NOTHING
            """,
            [
                ("water", "Drinks", 0, "Water", 0, 3, "BAR"),
                ("coffee", "Drinks", 0, "Coffee", 1, 4.5, "BAR"),
                ("salad", "Food", 1, "Greek Salad", 0, 10, "KITCHEN"),
            ],
        )

    print(f"Local BeachOS configuration is ready for Business Date {business_date}.")


if __name__ == "__main__":
    main()
