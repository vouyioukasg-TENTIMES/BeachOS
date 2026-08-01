"""Bar Application Commands."""

from dataclasses import dataclass

from .exceptions import BarCommandValidationError


@dataclass(frozen=True, slots=True)
class AcknowledgeBarTicketCommand:
    request_id: str
    actor_id: str
    ticket_id: str

    def __post_init__(self) -> None:
        for field in ("request_id", "actor_id", "ticket_id"):
            value = getattr(self, field).strip()
            if not value:
                raise BarCommandValidationError(f"{field.replace('_', ' ')} is required")
            object.__setattr__(self, field, value)


@dataclass(frozen=True, slots=True)
class ProgressBarTicketCommand:
    request_id: str
    actor_id: str
    ticket_id: str
    action: str

    def __post_init__(self) -> None:
        for field in ("request_id", "actor_id", "ticket_id"):
            value = getattr(self, field).strip()
            if not value:
                raise BarCommandValidationError(f"{field.replace('_', ' ')} is required")
            object.__setattr__(self, field, value)
        action = self.action.strip().upper()
        if action not in {"MARK_READY", "COLLECT", "DELIVER"}:
            raise BarCommandValidationError("Bar fulfilment action is invalid")
        object.__setattr__(self, "action", action)
