"""Guest Arrival Application Commands."""

from dataclasses import dataclass

from beachos_api.packs.beachos.guest_arrival.application.exceptions import (
    GuestArrivalValidationError,
)


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise GuestArrivalValidationError(f"{field} is required")
    return normalized


@dataclass(frozen=True, slots=True)
class OpenCustomerGroupCommand:
    request_id: str
    actor_id: str
    venue_id: str
    service_location_id: str
    physical_context_confirmed: bool
    waiter_accepts_responsibility: bool
    opening_charge_confirmed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _required(self.request_id, "request id"))
        object.__setattr__(self, "actor_id", _required(self.actor_id, "actor id"))
        object.__setattr__(self, "venue_id", _required(self.venue_id, "Venue id"))
        object.__setattr__(
            self, "service_location_id", _required(self.service_location_id, "Service Location id")
        )
