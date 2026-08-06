"""Temporary development identity for the first backend vertical slice."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class DevelopmentIdentity:
    """Fixed development identity facts; not an authentication mechanism."""

    actor_id: str
    capabilities: frozenset[str]
    has_venue_access: bool

    @property
    def host_id(self) -> str:
        """Compatibility name used by the existing temporary delivery boundary."""

        return self.actor_id


class FakeIdentityProvider:
    """Provides the approved temporary Host identity during development only."""

    _host_identity: Final = DevelopmentIdentity(
        actor_id="development-host",
        capabilities=frozenset(
            {
                "ACKNOWLEDGE_BAR_TICKET",
                "ACKNOWLEDGE_KITCHEN_TICKET",
                "COLLECT_TICKET",
                "CLOSE_BILL",
                "COMPLETE_CUSTOMER_GROUP",
                "DELIVER_TICKET",
                "DEPART_CUSTOMER_GROUP",
                "MARK_BAR_TICKET_READY",
                "MARK_KITCHEN_TICKET_READY",
                "OPEN_VENUE",
                "CLOSE_VENUE",
                "RECORD_PAYMENTS",
                "SUBMIT_ORDER",
            }
        ),
        has_venue_access=True,
    )

    def current(self) -> DevelopmentIdentity:
        return self._host_identity

    def identity_for(self, actor_id: str) -> DevelopmentIdentity:
        """Return an explicitly selected temporary development identity."""

        normalized = actor_id.strip()
        if not normalized or normalized == self._host_identity.actor_id:
            return self._host_identity
        return DevelopmentIdentity(
            actor_id=normalized,
            capabilities=frozenset(
                {"DECLARE_DEPARTMENT_READINESS", "OPEN_CUSTOMER_GROUP"}
                if normalized.startswith("staff-waiter-")
                else {"DECLARE_DEPARTMENT_READINESS"}
            ),
            has_venue_access=True,
        )


def development_identity() -> DevelopmentIdentity:
    """Resolve the default temporary request identity through dependency injection."""

    return FakeIdentityProvider().current()


class FakeVenueOpeningAuthority:
    """Adapts the temporary identity to Application-owned authority ports."""

    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_declare_department_readiness(
        self,
        *,
        actor_id: str,
        venue_id: str,
        department_id: str,
    ) -> bool:
        del venue_id, department_id
        identity = self._identities.identity_for(actor_id)
        return (
            actor_id == identity.actor_id
            and identity.has_venue_access
            and "DECLARE_DEPARTMENT_READINESS" in identity.capabilities
        )

    def can_open_venue(self, *, actor_id: str, venue_id: str) -> bool:
        del venue_id
        identity = self._identities.current()
        return (
            actor_id == identity.host_id
            and identity.has_venue_access
            and "OPEN_VENUE" in identity.capabilities
        )

    def can_close_venue(self, *, actor_id: str, venue_id: str) -> bool:
        del venue_id
        identity = self._identities.current()
        return (
            actor_id == identity.actor_id
            and identity.has_venue_access
            and "CLOSE_VENUE" in identity.capabilities
        )

    def is_responsible_host(self, *, actor_id: str, venue_id: str) -> bool:
        del venue_id
        identity = self._identities.current()
        return actor_id == identity.host_id and identity.has_venue_access


class FakeOrderingAuthority:
    """Adapts the temporary identity to the Ordering authority port."""

    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_submit_order(self, *, actor_id: str, venue_id: str, customer_group_id: str) -> bool:
        del venue_id, customer_group_id
        identity = self._identities.current()
        return (
            actor_id == identity.host_id
            and identity.has_venue_access
            and "SUBMIT_ORDER" in identity.capabilities
        )


class FakePaymentAuthority:
    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_record_payment(self, *, actor_id: str, customer_group_id: str) -> bool:
        del customer_group_id
        identity = self._identities.current()
        return (
            actor_id == identity.actor_id
            and identity.has_venue_access
            and "RECORD_PAYMENTS" in identity.capabilities
        )


class FakeBillClosingAuthority:
    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_close_bill(self, *, actor_id: str, customer_group_id: str) -> bool:
        del customer_group_id
        identity = self._identities.current()
        return (
            actor_id == identity.actor_id
            and identity.has_venue_access
            and "CLOSE_BILL" in identity.capabilities
        )


class FakeCustomerGroupCompletionAuthority:
    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_complete_customer_group(self, *, actor_id: str, customer_group_id: str) -> bool:
        del customer_group_id
        identity = self._identities.current()
        return (
            actor_id == identity.actor_id
            and identity.has_venue_access
            and "COMPLETE_CUSTOMER_GROUP" in identity.capabilities
        )


class FakeGuestDepartureAuthority:
    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_depart_customer_group(self, *, actor_id: str, customer_group_id: str) -> bool:
        del customer_group_id
        identity = self._identities.current()
        return (
            actor_id == identity.actor_id
            and identity.has_venue_access
            and "DEPART_CUSTOMER_GROUP" in identity.capabilities
        )


class FakeKitchenAuthority:
    """Adapts the temporary identity to the Kitchen authority port."""

    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_acknowledge_kitchen_ticket(
        self, *, actor_id: str, venue_id: str, ticket_id: str
    ) -> bool:
        del venue_id, ticket_id
        identity = self._identities.current()
        return (
            actor_id == identity.host_id
            and identity.has_venue_access
            and "ACKNOWLEDGE_KITCHEN_TICKET" in identity.capabilities
        )

    def can_mark_kitchen_ticket_ready(
        self, *, actor_id: str, venue_id: str, ticket_id: str
    ) -> bool:
        del venue_id, ticket_id
        identity = self._identities.current()
        return (
            actor_id == identity.actor_id and "MARK_KITCHEN_TICKET_READY" in identity.capabilities
        )

    def can_collect_ticket(
        self, *, actor_id: str, venue_id: str, responsible_service_staff_id: str
    ) -> bool:
        del venue_id
        identity = self._identities.current()
        return actor_id == responsible_service_staff_id or (
            actor_id == identity.actor_id and "COLLECT_TICKET" in identity.capabilities
        )

    def can_deliver_ticket(
        self, *, actor_id: str, venue_id: str, responsible_service_staff_id: str
    ) -> bool:
        del venue_id
        identity = self._identities.current()
        return actor_id == responsible_service_staff_id or (
            actor_id == identity.actor_id and "DELIVER_TICKET" in identity.capabilities
        )


class FakeBarAuthority:
    """Adapts the temporary identity to the Bar authority port."""

    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_acknowledge_bar_ticket(self, *, actor_id: str, venue_id: str, ticket_id: str) -> bool:
        del venue_id, ticket_id
        identity = self._identities.current()
        return (
            actor_id == identity.host_id
            and identity.has_venue_access
            and "ACKNOWLEDGE_BAR_TICKET" in identity.capabilities
        )

    def can_mark_bar_ticket_ready(self, *, actor_id: str, venue_id: str, ticket_id: str) -> bool:
        del venue_id, ticket_id
        identity = self._identities.current()
        return actor_id == identity.actor_id and "MARK_BAR_TICKET_READY" in identity.capabilities

    def can_collect_ticket(
        self, *, actor_id: str, venue_id: str, responsible_service_staff_id: str
    ) -> bool:
        del venue_id
        identity = self._identities.current()
        return actor_id == responsible_service_staff_id or (
            actor_id == identity.actor_id and "COLLECT_TICKET" in identity.capabilities
        )

    def can_deliver_ticket(
        self, *, actor_id: str, venue_id: str, responsible_service_staff_id: str
    ) -> bool:
        del venue_id
        identity = self._identities.current()
        return actor_id == responsible_service_staff_id or (
            actor_id == identity.actor_id and "DELIVER_TICKET" in identity.capabilities
        )


class FakeGuestArrivalAuthority:
    """Adapts temporary development identities to Guest Arrival ports."""

    def __init__(self, identities: FakeIdentityProvider) -> None:
        self._identities = identities

    def can_view_arrival(self, *, actor_id: str, venue_id: str) -> bool:
        del venue_id
        identity = self._identities.identity_for(actor_id)
        return actor_id == identity.actor_id and identity.has_venue_access

    def can_open_customer_group(self, *, actor_id: str, venue_id: str) -> bool:
        del venue_id
        identity = self._identities.identity_for(actor_id)
        return (
            actor_id == identity.actor_id
            and identity.has_venue_access
            and "OPEN_CUSTOMER_GROUP" in identity.capabilities
        )

    def is_eligible_responsible_waiter(self, *, actor_id: str, venue_id: str) -> bool:
        del venue_id
        return actor_id.startswith("staff-waiter-")
