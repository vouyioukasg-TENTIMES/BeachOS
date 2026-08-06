"""Pure Customer Group Completion Domain."""

from dataclasses import dataclass
from datetime import datetime


class CustomerGroupCompletionError(ValueError):
    """Completion would violate an approved lifecycle rule."""


@dataclass(frozen=True, slots=True)
class CustomerGroupCompleted:
    customer_group_id: str
    completed_by_id: str
    occurred_at: datetime


class CustomerGroupCompletion:
    def __init__(self, *, customer_group_id: str, status: str, bill_status: str | None) -> None:
        if not customer_group_id.strip():
            raise CustomerGroupCompletionError("Customer Group identity is required")
        if status not in {"ACTIVE", "COMPLETED"}:
            raise CustomerGroupCompletionError("Customer Group status is invalid")
        if bill_status not in {None, "OPEN", "FULLY_PAID", "CLOSED"}:
            raise CustomerGroupCompletionError("Bill status is invalid")
        self.customer_group_id = customer_group_id.strip()
        self._initial_status = status
        self.bill_status = bill_status
        self._completed: CustomerGroupCompleted | None = None
        self._version = 0
        self._pending: list[CustomerGroupCompleted] = []

    @classmethod
    def restore(
        cls,
        *,
        customer_group_id: str,
        status: str,
        bill_status: str | None,
        events: tuple[CustomerGroupCompleted, ...],
    ) -> "CustomerGroupCompletion":
        group = cls(customer_group_id=customer_group_id, status=status, bill_status=bill_status)
        for event in events:
            group._apply(event)
            group._version += 1
        if status == "COMPLETED" and group._completed is None:
            raise CustomerGroupCompletionError("Completed state requires its immutable event")
        if status == "ACTIVE" and group._completed is not None:
            raise CustomerGroupCompletionError("Active state cannot contain a completion event")
        return group

    def complete(self, *, actor_id: str, at: datetime) -> CustomerGroupCompleted:
        if self.status != "ACTIVE":
            raise CustomerGroupCompletionError("only an ACTIVE Customer Group may be completed")
        if self.bill_status is not None and self.bill_status != "CLOSED":
            raise CustomerGroupCompletionError("the Customer Group Bill must already be CLOSED")
        if not actor_id.strip():
            raise CustomerGroupCompletionError("completing Staff identity is required")
        if at.tzinfo is None or at.utcoffset() is None:
            raise CustomerGroupCompletionError("completion time must include a timezone")
        event = CustomerGroupCompleted(self.customer_group_id, actor_id.strip(), at)
        self._apply(event)
        self._pending.append(event)
        self._version += 1
        return event

    def _apply(self, event: CustomerGroupCompleted) -> None:
        if event.customer_group_id != self.customer_group_id:
            raise CustomerGroupCompletionError("completion event belongs to another Customer Group")
        if self._completed is not None:
            raise CustomerGroupCompletionError("Customer Group is already completed")
        self._completed = event

    def pull_events(self) -> tuple[CustomerGroupCompleted, ...]:
        events = tuple(self._pending)
        self._pending.clear()
        return events

    @property
    def status(self) -> str:
        return "COMPLETED" if self._completed else self._initial_status

    @property
    def completed(self) -> CustomerGroupCompleted | None:
        return self._completed

    @property
    def version(self) -> int:
        return self._version
