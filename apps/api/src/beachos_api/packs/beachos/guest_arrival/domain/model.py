"""Framework-independent Guest Arrival Domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from beachos_api.packs.beachos.guest_arrival.domain.events import GuestArrivalEvent


class GuestArrivalError(ValueError):
    """An arrival action violates an approved business rule."""


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise GuestArrivalError(f"{field} is required")
    return normalized


def _aware(value: datetime, action: str = "opening") -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise GuestArrivalError(f"{action} time must include a timezone")
    return value


class ServiceLocationStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    UNAVAILABLE = "UNAVAILABLE"
    RETIRED = "RETIRED"


class ServiceLocationType(StrEnum):
    BEACH_SUNBED = "BEACH SUNBED"
    POOL_SUNBED = "POOL SUNBED"
    UPPER_TABLE = "UPPER TABLE"
    OTHER = "OTHER"


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal) or not self.amount.is_finite():
            raise GuestArrivalError("money amount must be an exact finite decimal")
        if self.amount < 0:
            raise GuestArrivalError("money amount cannot be negative")
        object.__setattr__(self, "currency", _required(self.currency, "currency").upper())


@dataclass(frozen=True, slots=True)
class CustomerGroup:
    customer_group_id: str
    venue_id: str
    service_location_id: str
    responsible_waiter_id: str
    opened_at: datetime
    bill_id: str | None = None
    opening_obligation: Money | None = None


class ServiceLocation:
    """Aggregate protecting identification, occupancy, and Customer Group opening."""

    def __init__(
        self,
        *,
        service_location_id: str,
        venue_id: str,
        visible_name: str,
        digital_identity: str,
        location_type: ServiceLocationType,
        status: ServiceLocationStatus = ServiceLocationStatus.AVAILABLE,
        beach_sunbed_charge: Money | None = None,
        charge_description: str | None = None,
    ) -> None:
        self._service_location_id = _required(service_location_id, "Service Location id")
        self._venue_id = _required(venue_id, "Venue id")
        self._visible_name = _required(visible_name, "visible name")
        self._digital_identity = _required(digital_identity, "Digital Identity")
        if not isinstance(location_type, ServiceLocationType):
            raise GuestArrivalError("Service Location type is invalid")
        if not isinstance(status, ServiceLocationStatus):
            raise GuestArrivalError("Service Location status is invalid")
        self._location_type = location_type
        self._initial_status = status
        self._status = status
        self._beach_sunbed_charge = beach_sunbed_charge
        self._charge_description = (
            _required(charge_description, "charge description")
            if charge_description is not None
            else None
        )
        self._active_customer_group: CustomerGroup | None = None
        self._history: list[GuestArrivalEvent] = []
        self._pending: list[GuestArrivalEvent] = []
        self._version = 0

    @classmethod
    def restore(
        cls,
        *,
        service_location_id: str,
        venue_id: str,
        visible_name: str,
        digital_identity: str,
        location_type: ServiceLocationType,
        initial_status: ServiceLocationStatus,
        beach_sunbed_charge: Money | None,
        charge_description: str | None,
        events: tuple[GuestArrivalEvent, ...],
    ) -> ServiceLocation:
        location = cls(
            service_location_id=service_location_id,
            venue_id=venue_id,
            visible_name=visible_name,
            digital_identity=digital_identity,
            location_type=location_type,
            status=initial_status,
            beach_sunbed_charge=beach_sunbed_charge,
            charge_description=charge_description,
        )
        for event in events:
            location._apply(event)
            location._history.append(event)
            location._version += 1
        return location

    def open_customer_group(
        self,
        *,
        customer_group_id: str,
        responsible_waiter_id: str,
        opened_by_id: str,
        opened_at: datetime,
        venue_is_open: bool,
        waiter_is_eligible: bool,
        waiter_has_capability: bool,
        waiter_accepts_responsibility: bool,
        physical_context_confirmed: bool,
        opening_charge_confirmed: bool,
        obligation_id: str | None,
        bill_id: str | None,
        bill_line_id: str | None,
    ) -> CustomerGroup:
        from beachos_api.packs.beachos.guest_arrival.domain.events import (
            BillCreated,
            BillLineAdded,
            CustomerGroupOpened,
            FinancialObligationCreated,
            ResponsibleWaiterAssigned,
        )

        group_id = _required(customer_group_id, "Customer Group id")
        waiter_id = _required(responsible_waiter_id, "Responsible Waiter id")
        if _required(opened_by_id, "opening actor id") != waiter_id:
            raise GuestArrivalError("only the Responsible Waiter may open the Customer Group")
        moment = _aware(opened_at)
        if not venue_is_open:
            raise GuestArrivalError("the Venue must be open before a Customer Group can open")
        if self._status is not ServiceLocationStatus.AVAILABLE:
            raise GuestArrivalError("the Service Location is not available")
        if self._active_customer_group is not None:
            raise GuestArrivalError("the Service Location already has an active Customer Group")
        if not physical_context_confirmed:
            raise GuestArrivalError("the physical and digital Service Location must be confirmed")
        if not waiter_is_eligible or not waiter_has_capability:
            raise GuestArrivalError("the Responsible Waiter is not eligible to open this group")
        if not waiter_accepts_responsibility:
            raise GuestArrivalError("the Responsible Waiter must accept responsibility")

        charge = self._beach_sunbed_charge
        if self._location_type is ServiceLocationType.BEACH_SUNBED:
            if charge is None or self._charge_description is None:
                raise GuestArrivalError("the Beach Sunbed obligation cannot be confirmed")
            if not opening_charge_confirmed:
                raise GuestArrivalError(
                    "the Responsible Waiter must confirm the Beach Sunbed charge"
                )
            obligation = _required(obligation_id or "", "Financial Obligation id")
            bill = _required(bill_id or "", "Bill id")
            line = _required(bill_line_id or "", "Bill Line id")
        else:
            if any(value is not None for value in (obligation_id, bill_id, bill_line_id)):
                raise GuestArrivalError(
                    "a Service Location without an opening obligation cannot create a Bill"
                )
            obligation = bill = line = ""

        self._record(
            ResponsibleWaiterAssigned(group_id, self._service_location_id, waiter_id, moment)
        )
        self._record(
            CustomerGroupOpened(
                group_id,
                self._venue_id,
                self._service_location_id,
                waiter_id,
                moment,
            )
        )
        if charge is not None:
            self._record(
                FinancialObligationCreated(
                    obligation,
                    group_id,
                    "BEACH SUNBED OPENING",
                    charge.amount,
                    charge.currency,
                    moment,
                )
            )
            self._record(BillCreated(bill, group_id, charge.currency, moment))
            self._record(
                BillLineAdded(
                    bill,
                    line,
                    self._charge_description or "Beach Sunbed charge",
                    charge.amount,
                    charge.currency,
                    "BEACH SUNBED OPENING",
                    moment,
                )
            )
        group = self.active_customer_group
        if group is None:
            raise GuestArrivalError("Customer Group opening did not complete")
        return group

    def depart_customer_group(
        self,
        *,
        customer_group_id: str,
        departed_by_id: str,
        departed_at: datetime,
        customer_group_is_completed: bool,
    ) -> None:
        from beachos_api.packs.beachos.guest_arrival.domain.events import GuestDeparted

        group_id = _required(customer_group_id, "Customer Group id")
        actor_id = _required(departed_by_id, "departure actor id")
        moment = _aware(departed_at, "departure")
        group = self._active_customer_group
        if group is None or group.customer_group_id != group_id:
            raise GuestArrivalError("the Customer Group does not occupy this Service Location")
        if not customer_group_is_completed:
            raise GuestArrivalError("only a COMPLETED Customer Group may depart")
        self._record(GuestDeparted(group_id, self._service_location_id, actor_id, moment))

    def _record(self, event: GuestArrivalEvent) -> None:
        self._apply(event)
        self._history.append(event)
        self._pending.append(event)
        self._version += 1

    def _apply(self, event: GuestArrivalEvent) -> None:
        from beachos_api.packs.beachos.guest_arrival.domain.events import (
            BillCreated,
            CustomerGroupOpened,
            FinancialObligationCreated,
            GuestDeparted,
            ResponsibleWaiterAssigned,
        )

        if isinstance(event, ResponsibleWaiterAssigned):
            return
        if isinstance(event, CustomerGroupOpened):
            if event.service_location_id != self._service_location_id:
                raise GuestArrivalError("Customer Group event belongs to another Service Location")
            if self._active_customer_group is not None:
                raise GuestArrivalError("event stream contains duplicate active Customer Groups")
            self._active_customer_group = CustomerGroup(
                event.customer_group_id,
                event.venue_id,
                event.service_location_id,
                event.responsible_waiter_id,
                event.occurred_at,
            )
            self._status = ServiceLocationStatus.OCCUPIED
        elif isinstance(event, BillCreated):
            group = self._active_customer_group
            if group is None or group.customer_group_id != event.customer_group_id:
                raise GuestArrivalError("Bill must belong to the active Customer Group")
            self._active_customer_group = CustomerGroup(
                group.customer_group_id,
                group.venue_id,
                group.service_location_id,
                group.responsible_waiter_id,
                group.opened_at,
                event.bill_id,
                group.opening_obligation,
            )
        elif isinstance(event, FinancialObligationCreated):
            group = self._active_customer_group
            if group is None or group.customer_group_id != event.customer_group_id:
                raise GuestArrivalError("obligation must belong to the active Customer Group")
            self._active_customer_group = CustomerGroup(
                group.customer_group_id,
                group.venue_id,
                group.service_location_id,
                group.responsible_waiter_id,
                group.opened_at,
                group.bill_id,
                Money(event.amount, event.currency),
            )
        elif isinstance(event, GuestDeparted):
            group = self._active_customer_group
            if event.service_location_id != self._service_location_id:
                raise GuestArrivalError("departure event belongs to another Service Location")
            if group is None or group.customer_group_id != event.customer_group_id:
                raise GuestArrivalError("departure must match the occupying Customer Group")
            self._active_customer_group = None
            self._status = ServiceLocationStatus.AVAILABLE

    def pull_events(self) -> tuple[GuestArrivalEvent, ...]:
        events = tuple(self._pending)
        self._pending.clear()
        return events

    @property
    def service_location_id(self) -> str:
        return self._service_location_id

    @property
    def venue_id(self) -> str:
        return self._venue_id

    @property
    def visible_name(self) -> str:
        return self._visible_name

    @property
    def digital_identity(self) -> str:
        return self._digital_identity

    @property
    def location_type(self) -> ServiceLocationType:
        return self._location_type

    @property
    def status(self) -> ServiceLocationStatus:
        return self._status

    @property
    def active_customer_group(self) -> CustomerGroup | None:
        return self._active_customer_group

    @property
    def beach_sunbed_charge(self) -> Money | None:
        return self._beach_sunbed_charge

    @property
    def charge_description(self) -> str | None:
        return self._charge_description

    @property
    def history(self) -> tuple[GuestArrivalEvent, ...]:
        return tuple(self._history)

    @property
    def version(self) -> int:
        return self._version
