"""Guest Arrival Application results."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from beachos_api.packs.beachos.guest_arrival.domain import CustomerGroup, ServiceLocation


@dataclass(frozen=True, slots=True)
class ServiceLocationDTO:
    service_location_id: str
    visible_name: str
    digital_identity: str
    location_type: str
    status: str
    active_customer_group_id: str | None
    opening_charge: Decimal | None
    currency: str | None
    charge_description: str | None

    @classmethod
    def from_domain(cls, value: ServiceLocation) -> "ServiceLocationDTO":
        charge = value.beach_sunbed_charge
        return cls(
            value.service_location_id,
            value.visible_name,
            value.digital_identity,
            value.location_type.value,
            value.status.value,
            value.active_customer_group.customer_group_id if value.active_customer_group else None,
            charge.amount if charge else None,
            charge.currency if charge else None,
            value.charge_description,
        )


@dataclass(frozen=True, slots=True)
class GuestArrivalContextResult:
    venue_id: str
    venue_name: str
    business_date: str
    venue_open: bool
    operational_confidence: str
    locations: tuple[ServiceLocationDTO, ...]


@dataclass(frozen=True, slots=True)
class CustomerGroupDTO:
    customer_group_id: str
    venue_id: str
    service_location_id: str
    responsible_waiter_id: str
    opened_at: datetime
    bill_id: str | None
    opening_obligation: Decimal | None
    currency: str | None

    @classmethod
    def from_domain(cls, value: CustomerGroup) -> "CustomerGroupDTO":
        return cls(
            value.customer_group_id,
            value.venue_id,
            value.service_location_id,
            value.responsible_waiter_id,
            value.opened_at,
            value.bill_id,
            value.opening_obligation.amount if value.opening_obligation else None,
            value.opening_obligation.currency if value.opening_obligation else None,
        )


@dataclass(frozen=True, slots=True)
class OpenCustomerGroupResult:
    request_id: str
    customer_group: CustomerGroupDTO
    service_location: ServiceLocationDTO


@dataclass(frozen=True, slots=True)
class ActivityLogRecord:
    request_id: str
    actor_id: str
    venue_id: str
    service_location_id: str
    customer_group_id: str
    occurred_at: datetime
