"""Kitchen Application Commands."""

from dataclasses import dataclass

from beachos_api.packs.beachos.kitchen.application.exceptions import (
    KitchenCommandValidationError,
)


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise KitchenCommandValidationError(f"{field} is required")
    return normalized


@dataclass(frozen=True, slots=True)
class AcknowledgeKitchenTicketCommand:
    request_id: str
    actor_id: str
    ticket_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _required(self.request_id, "request id"))
        object.__setattr__(self, "actor_id", _required(self.actor_id, "actor id"))
        object.__setattr__(self, "ticket_id", _required(self.ticket_id, "Kitchen Ticket id"))


@dataclass(frozen=True, slots=True)
class ProgressKitchenTicketCommand:
    request_id: str
    actor_id: str
    ticket_id: str
    action: str

    def __post_init__(self) -> None:
        for name in ("request_id", "actor_id", "ticket_id"):
            object.__setattr__(self, name, _required(getattr(self, name), name.replace("_", " ")))
        action = self.action.strip().upper()
        if action not in {"MARK_READY", "COLLECT", "DELIVER"}:
            raise KitchenCommandValidationError("Kitchen fulfilment action is invalid")
        object.__setattr__(self, "action", action)
