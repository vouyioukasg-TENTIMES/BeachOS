"""Backend composition root for production adapters."""

import os

from beachos_api.identity import (
    FakeBarAuthority,
    FakeGuestArrivalAuthority,
    FakeIdentityProvider,
    FakeKitchenAuthority,
    FakeOrderingAuthority,
    FakeVenueOpeningAuthority,
)
from beachos_api.packs.beachos.bar.application import BarService
from beachos_api.packs.beachos.bar.infrastructure import PostgresBarUnitOfWorkFactory
from beachos_api.packs.beachos.billing.application import BillingService
from beachos_api.packs.beachos.billing.infrastructure import PostgresBillReader
from beachos_api.packs.beachos.guest_arrival.application import GuestArrivalService
from beachos_api.packs.beachos.guest_arrival.infrastructure import (
    PostgresGuestArrivalUnitOfWorkFactory,
    PostgresVenueOpeningReader,
)
from beachos_api.packs.beachos.guest_arrival.infrastructure import (
    UUIDIdentityGenerator as GuestArrivalUUIDIdentityGenerator,
)
from beachos_api.packs.beachos.kitchen.application import KitchenService
from beachos_api.packs.beachos.kitchen.infrastructure import (
    PostgresKitchenUnitOfWorkFactory,
)
from beachos_api.packs.beachos.ordering.application import OrderingService
from beachos_api.packs.beachos.ordering.infrastructure import (
    PostgresOrderingUnitOfWorkFactory,
    UUIDIdentityGenerator,
)
from beachos_api.packs.beachos.venue_opening.application import VenueOpeningService
from beachos_api.packs.beachos.venue_opening.domain import VenueOpeningPolicy
from beachos_api.packs.beachos.venue_opening.infrastructure import (
    PostgresBusinessDateProvider,
    PostgresVenueOpeningUnitOfWorkFactory,
    SystemClock,
)


class ConfigurationError(RuntimeError):
    """The process lacks configuration required to serve a capability."""


def venue_opening_service() -> VenueOpeningService:
    """Wire the approved Venue Opening Application service to its adapters."""

    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")

    clock = SystemClock()
    identities = FakeIdentityProvider()
    authority = FakeVenueOpeningAuthority(identities)
    return VenueOpeningService(
        capabilities=authority,
        host_responsibilities=authority,
        business_dates=PostgresBusinessDateProvider(
            connection_string=connection_string,
            clock=clock,
        ),
        clock=clock,
        unit_of_work_factory=PostgresVenueOpeningUnitOfWorkFactory(connection_string),
        policy=VenueOpeningPolicy(),
    )


def guest_arrival_service() -> GuestArrivalService:
    """Wire Guest Arrival ports at the composition boundary."""

    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return GuestArrivalService(
        authority=FakeGuestArrivalAuthority(identities),
        clock=SystemClock(),
        identities=GuestArrivalUUIDIdentityGenerator(),
        venue_opening=PostgresVenueOpeningReader(
            connection_string,
            PostgresBusinessDateProvider(connection_string=connection_string, clock=SystemClock()),
        ),
        unit_of_work_factory=PostgresGuestArrivalUnitOfWorkFactory(connection_string),
    )


def ordering_service() -> OrderingService:
    """Wire Ordering ports without exposing infrastructure beyond this root."""

    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return OrderingService(
        capabilities=FakeOrderingAuthority(identities),
        clock=SystemClock(),
        identities=UUIDIdentityGenerator(),
        unit_of_work_factory=PostgresOrderingUnitOfWorkFactory(connection_string),
    )


def kitchen_service() -> KitchenService:
    """Wire Kitchen Operations ports at the composition boundary."""

    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return KitchenService(
        capabilities=FakeKitchenAuthority(identities),
        clock=SystemClock(),
        unit_of_work_factory=PostgresKitchenUnitOfWorkFactory(connection_string),
    )


def bar_service() -> BarService:
    """Wire Bar Operations ports at the composition boundary."""
    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return BarService(
        capabilities=FakeBarAuthority(identities),
        clock=SystemClock(),
        unit_of_work_factory=PostgresBarUnitOfWorkFactory(connection_string),
    )


def billing_service() -> BillingService:
    """Wire the read-only authoritative Billing projection."""
    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    return BillingService(PostgresBillReader(connection_string))
