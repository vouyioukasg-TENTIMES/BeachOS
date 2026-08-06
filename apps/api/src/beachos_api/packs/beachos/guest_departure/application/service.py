"""Guest Departure application use cases."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from beachos_api.packs.beachos.guest_arrival.domain import (
    GuestArrivalError,
    GuestDeparted,
    ServiceLocation,
)


class DepartureApplicationError(RuntimeError):
    """The departure command could not produce its approved outcome."""


class DepartureAuthorizationError(DepartureApplicationError):
    """The actor lacks the required capability."""


class DepartureNotFoundError(DepartureApplicationError):
    """The Customer Group or its Service Location does not exist."""


@dataclass(frozen=True, slots=True)
class DepartCustomerGroupCommand:
    request_id: str
    actor_id: str
    customer_group_id: str


@dataclass(frozen=True, slots=True)
class DepartureContextResult:
    customer_group_id: str
    customer_group_status: str
    departure_status: str
    service_location_id: str
    service_location_name: str
    service_location_status: str
    can_depart: bool
    next_action: str


@dataclass(frozen=True, slots=True)
class DepartureResult:
    request_id: str
    customer_group_id: str
    customer_group_status: str
    departure_status: str
    service_location_id: str
    service_location_name: str
    service_location_status: str
    departed_by_id: str
    departed_at: datetime


class Authority(Protocol):
    def can_depart_customer_group(self, *, actor_id: str, customer_group_id: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class Locations(Protocol):
    def get_for_customer_group(self, *, customer_group_id: str) -> ServiceLocation | None: ...
    def save(self, location: ServiceLocation) -> None: ...


class CustomerGroups(Protocol):
    def status(self, *, customer_group_id: str) -> str | None: ...


class Receipts(Protocol):
    def get(self, *, request_id: str) -> DepartureResult | None: ...
    def save(self, result: DepartureResult) -> None: ...


class Activity(Protocol):
    def record(self, *, result: DepartureResult) -> None: ...


class Unit(Protocol):
    locations: Locations
    customer_groups: CustomerGroups
    receipts: Receipts
    activity: Activity

    def __enter__(self) -> "Unit": ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> None: ...


class Units(Protocol):
    def create(self) -> Unit: ...


def _departure(location: ServiceLocation, customer_group_id: str) -> GuestDeparted | None:
    return next(
        (
            event
            for event in reversed(location.history)
            if isinstance(event, GuestDeparted) and event.customer_group_id == customer_group_id
        ),
        None,
    )


class GuestDepartureService:
    def __init__(self, *, authority: Authority, clock: Clock, units: Units) -> None:
        self._authority = authority
        self._clock = clock
        self._units = units

    def get_context(self, *, customer_group_id: str) -> DepartureContextResult:
        with self._units.create() as unit:
            location = unit.locations.get_for_customer_group(customer_group_id=customer_group_id)
            status = unit.customer_groups.status(customer_group_id=customer_group_id)
            if location is None or status is None:
                raise DepartureNotFoundError("Customer Group departure context was not found")
            departed = _departure(location, customer_group_id)
            can_depart = status == "COMPLETED" and departed is None
            return DepartureContextResult(
                customer_group_id,
                status,
                "DEPARTED" if departed else "NOT_DEPARTED",
                location.service_location_id,
                location.visible_name,
                location.status.value,
                can_depart,
                "DEPART_CUSTOMER_GROUP" if can_depart else "NONE",
            )

    def depart(self, command: DepartCustomerGroupCommand) -> DepartureResult:
        if not all(
            (
                command.request_id.strip(),
                command.actor_id.strip(),
                command.customer_group_id.strip(),
            )
        ):
            raise DepartureApplicationError("request, actor, and Customer Group are required")
        if not self._authority.can_depart_customer_group(
            actor_id=command.actor_id,
            customer_group_id=command.customer_group_id,
        ):
            raise DepartureAuthorizationError("Depart Customer Group capability is required")

        with self._units.create() as unit:
            prior = unit.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.customer_group_id != command.customer_group_id:
                    raise DepartureApplicationError("request identity belongs to another group")
                return prior
            location = unit.locations.get_for_customer_group(
                customer_group_id=command.customer_group_id
            )
            status = unit.customer_groups.status(customer_group_id=command.customer_group_id)
            if location is None or status is None:
                raise DepartureNotFoundError("Customer Group departure context was not found")
            try:
                location.depart_customer_group(
                    customer_group_id=command.customer_group_id,
                    departed_by_id=command.actor_id,
                    departed_at=self._clock.now(),
                    customer_group_is_completed=status == "COMPLETED",
                )
            except GuestArrivalError as error:
                raise DepartureApplicationError(str(error)) from error
            event = next(
                event
                for event in location.history
                if isinstance(event, GuestDeparted)
                and event.customer_group_id == command.customer_group_id
            )
            result = DepartureResult(
                command.request_id,
                command.customer_group_id,
                status,
                "DEPARTED",
                location.service_location_id,
                location.visible_name,
                location.status.value,
                event.departed_by_id,
                event.occurred_at,
            )
            unit.locations.save(location)
            unit.receipts.save(result)
            unit.activity.record(result=result)
            unit.commit()
            return result
