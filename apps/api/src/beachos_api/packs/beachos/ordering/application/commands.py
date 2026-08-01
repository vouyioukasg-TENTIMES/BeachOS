"""Ordering Application Commands."""

from dataclasses import dataclass
from decimal import Decimal

from beachos_api.packs.beachos.ordering.application.exceptions import (
    OrderingCommandValidationError,
)


def _required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise OrderingCommandValidationError(f"{field} is required")
    return normalized


@dataclass(frozen=True, slots=True)
class SubmitOrderItem:
    menu_item_id: str
    quantity: Decimal
    note: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "menu_item_id", _required(self.menu_item_id, "Menu Item id"))


@dataclass(frozen=True, slots=True)
class SubmitOrderCommand:
    request_id: str
    actor_id: str
    customer_group_id: str
    items: tuple[SubmitOrderItem, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _required(self.request_id, "request id"))
        object.__setattr__(self, "actor_id", _required(self.actor_id, "actor id"))
        object.__setattr__(
            self,
            "customer_group_id",
            _required(self.customer_group_id, "Customer Group id"),
        )
