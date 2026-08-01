"""Guest Arrival dependency-inversion ports."""

from datetime import datetime
from types import TracebackType
from typing import Protocol, Self

from beachos_api.packs.beachos.guest_arrival.application.dtos import (
    ActivityLogRecord,
    OpenCustomerGroupResult,
)
from beachos_api.packs.beachos.guest_arrival.domain import ServiceLocation


class GuestArrivalAuthority(Protocol):
    def can_view_arrival(self, *, actor_id: str, venue_id: str) -> bool: ...
    def can_open_customer_group(self, *, actor_id: str, venue_id: str) -> bool: ...
    def is_eligible_responsible_waiter(self, *, actor_id: str, venue_id: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class IdentityGenerator(Protocol):
    def new_id(self, prefix: str) -> str: ...


class VenueOpeningReader(Protocol):
    def current(self, *, venue_id: str) -> tuple[str, str, bool] | None: ...


class ServiceLocationRepository(Protocol):
    def list_for_venue(self, *, venue_id: str) -> tuple[ServiceLocation, ...]: ...
    def get(self, *, service_location_id: str) -> ServiceLocation | None: ...
    def get_by_digital_identity(
        self, *, venue_id: str, digital_identity: str
    ) -> ServiceLocation | None: ...
    def save(self, location: ServiceLocation) -> None: ...


class CommandReceiptStore(Protocol):
    def get(self, *, request_id: str) -> OpenCustomerGroupResult | None: ...
    def save(self, *, request_id: str, result: OpenCustomerGroupResult) -> None: ...


class OrderingProvisioner(Protocol):
    def provision(self, location: ServiceLocation) -> None: ...


class ActivityLog(Protocol):
    def record_customer_group_opened(self, record: ActivityLogRecord) -> None: ...


class GuestArrivalUnitOfWork(Protocol):
    @property
    def locations(self) -> ServiceLocationRepository: ...
    @property
    def receipts(self) -> CommandReceiptStore: ...
    @property
    def ordering(self) -> OrderingProvisioner: ...
    @property
    def activity_log(self) -> ActivityLog: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def commit(self) -> None: ...


class GuestArrivalUnitOfWorkFactory(Protocol):
    def create(self) -> GuestArrivalUnitOfWork: ...
