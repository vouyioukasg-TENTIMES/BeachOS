"""Backend composition root for production adapters."""

import os

from beachos_api.identity import (
    FakeBarAuthority,
    FakeBillClosingAuthority,
    FakeCustomerGroupCompletionAuthority,
    FakeGuestArrivalAuthority,
    FakeGuestDepartureAuthority,
    FakeIdentityProvider,
    FakeKitchenAuthority,
    FakeOrderingAuthority,
    FakePaymentAuthority,
    FakeVenueOpeningAuthority,
)
from beachos_api.packs.beachos.bar.application import BarService
from beachos_api.packs.beachos.bar.infrastructure import PostgresBarUnitOfWorkFactory
from beachos_api.packs.beachos.bill_closing.application import BillClosingService
from beachos_api.packs.beachos.bill_closing.infrastructure import (
    PostgresBillClosingUnitOfWorkFactory,
)
from beachos_api.packs.beachos.billing.application import BillingService
from beachos_api.packs.beachos.billing.infrastructure import PostgresBillReader
from beachos_api.packs.beachos.customer_completion.application import (
    CustomerGroupCompletionService,
)
from beachos_api.packs.beachos.customer_completion.infrastructure import (
    PostgresCompletionUnitOfWorkFactory,
)
from beachos_api.packs.beachos.guest_arrival.application import GuestArrivalService
from beachos_api.packs.beachos.guest_arrival.infrastructure import (
    PostgresGuestArrivalUnitOfWorkFactory,
    PostgresVenueOpeningReader,
)
from beachos_api.packs.beachos.guest_arrival.infrastructure import (
    UUIDIdentityGenerator as GuestArrivalUUIDIdentityGenerator,
)
from beachos_api.packs.beachos.guest_departure.application import GuestDepartureService
from beachos_api.packs.beachos.guest_departure.infrastructure import (
    PostgresDepartureUnitOfWorkFactory,
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
from beachos_api.packs.beachos.payments.application import PaymentService
from beachos_api.packs.beachos.payments.infrastructure import (
    PostgresPaymentUnitOfWorkFactory,
    UUIDPaymentIdentities,
)
from beachos_api.packs.beachos.venue_closing.application import VenueClosingService
from beachos_api.packs.beachos.venue_closing.infrastructure import (
    PostgresVenueClosingUnitOfWorkFactory,
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


def payment_service() -> PaymentService:
    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return PaymentService(
        authority=FakePaymentAuthority(identities),
        clock=SystemClock(),
        identities=UUIDPaymentIdentities(),
        units=PostgresPaymentUnitOfWorkFactory(connection_string),
    )


def bill_closing_service() -> BillClosingService:
    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return BillClosingService(
        authority=FakeBillClosingAuthority(identities),
        clock=SystemClock(),
        units=PostgresBillClosingUnitOfWorkFactory(connection_string),
    )


def customer_group_completion_service() -> CustomerGroupCompletionService:
    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return CustomerGroupCompletionService(
        authority=FakeCustomerGroupCompletionAuthority(identities),
        clock=SystemClock(),
        units=PostgresCompletionUnitOfWorkFactory(connection_string),
    )


def guest_departure_service() -> GuestDepartureService:
    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    return GuestDepartureService(
        authority=FakeGuestDepartureAuthority(identities),
        clock=SystemClock(),
        units=PostgresDepartureUnitOfWorkFactory(connection_string),
    )


def venue_closing_service() -> VenueClosingService:
    connection_string = os.environ.get("BEACHOS_DATABASE_URL")
    if not connection_string:
        raise ConfigurationError("BEACHOS_DATABASE_URL is required")
    identities = FakeIdentityProvider()
    clock = SystemClock()
    return VenueClosingService(
        authority=FakeVenueOpeningAuthority(identities),
        business_dates=PostgresBusinessDateProvider(
            connection_string=connection_string, clock=clock
        ),
        clock=clock,
        units=PostgresVenueClosingUnitOfWorkFactory(connection_string),
    )
