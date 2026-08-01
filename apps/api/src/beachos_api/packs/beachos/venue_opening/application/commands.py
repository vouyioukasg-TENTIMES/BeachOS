"""Commands accepted by the Venue Opening Application Layer."""

from dataclasses import dataclass

from beachos_api.packs.beachos.venue_opening.application.exceptions import (
    CommandValidationError,
)
from beachos_api.packs.beachos.venue_opening.domain import ReadinessStatus


def _required(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise CommandValidationError(f"{field_name} is required")
    return normalized


@dataclass(frozen=True, slots=True)
class OpenVenueCommand:
    """An authenticated actor's intention to open one Venue."""

    request_id: str
    actor_id: str
    venue_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _required(self.request_id, "request id"))
        object.__setattr__(self, "actor_id", _required(self.actor_id, "actor id"))
        object.__setattr__(self, "venue_id", _required(self.venue_id, "venue id"))


@dataclass(frozen=True, slots=True)
class DeclareDepartmentReadinessCommand:
    """A responsible person's intention to declare current readiness."""

    request_id: str
    actor_id: str
    venue_id: str
    department_id: str
    status: ReadinessStatus
    reason: str | None = None
    comment: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _required(self.request_id, "request id"))
        object.__setattr__(self, "actor_id", _required(self.actor_id, "actor id"))
        object.__setattr__(self, "venue_id", _required(self.venue_id, "venue id"))
        object.__setattr__(
            self,
            "department_id",
            _required(self.department_id, "department id"),
        )
