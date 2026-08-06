"""Customer Group Completion application use cases."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from beachos_api.packs.beachos.customer_completion.domain import (
    CustomerGroupCompletion,
    CustomerGroupCompletionError,
)


class CompletionApplicationError(RuntimeError): ...


class CompletionAuthorizationError(CompletionApplicationError): ...


class CompletionNotFoundError(CompletionApplicationError): ...


@dataclass(frozen=True, slots=True)
class CompleteCustomerGroupCommand:
    request_id: str
    actor_id: str
    customer_group_id: str


@dataclass(frozen=True, slots=True)
class CompletionContextResult:
    customer_group_id: str
    status: str
    bill_status: str | None
    can_complete: bool
    next_action: str
    service_location_status: str = "OCCUPIED"


@dataclass(frozen=True, slots=True)
class CompleteCustomerGroupResult:
    request_id: str
    customer_group_id: str
    status: str
    completed_by_id: str
    completed_at: datetime
    service_location_status: str = "OCCUPIED"
    service_location_released: bool = False


class Authority(Protocol):
    def can_complete_customer_group(self, *, actor_id: str, customer_group_id: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class Groups(Protocol):
    def load(self, *, customer_group_id: str) -> CustomerGroupCompletion | None: ...
    def save(self, group: CustomerGroupCompletion) -> None: ...


class Receipts(Protocol):
    def get(self, *, request_id: str) -> CompleteCustomerGroupResult | None: ...
    def save(self, result: CompleteCustomerGroupResult) -> None: ...


class Activity(Protocol):
    def record(self, *, result: CompleteCustomerGroupResult) -> None: ...


class Unit(Protocol):
    groups: Groups
    receipts: Receipts
    activity: Activity

    def __enter__(self) -> "Unit": ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> None: ...


class Units(Protocol):
    def create(self) -> Unit: ...


class CustomerGroupCompletionService:
    def __init__(self, *, authority: Authority, clock: Clock, units: Units) -> None:
        self._authority, self._clock, self._units = authority, clock, units

    def get_context(self, *, customer_group_id: str) -> CompletionContextResult:
        with self._units.create() as unit:
            group = unit.groups.load(customer_group_id=customer_group_id)
            if group is None:
                raise CompletionNotFoundError("Customer Group was not found")
            can_complete = group.status == "ACTIVE" and group.bill_status in {None, "CLOSED"}
            return CompletionContextResult(
                group.customer_group_id,
                group.status,
                group.bill_status,
                can_complete,
                "COMPLETE_CUSTOMER_GROUP" if can_complete else "NONE",
            )

    def complete(self, command: CompleteCustomerGroupCommand) -> CompleteCustomerGroupResult:
        if not all(
            (
                command.request_id.strip(),
                command.actor_id.strip(),
                command.customer_group_id.strip(),
            )
        ):
            raise CompletionApplicationError("request, actor, and Customer Group are required")
        if not self._authority.can_complete_customer_group(
            actor_id=command.actor_id, customer_group_id=command.customer_group_id
        ):
            raise CompletionAuthorizationError("Complete Customer Group capability is required")
        with self._units.create() as unit:
            prior = unit.receipts.get(request_id=command.request_id)
            if prior:
                if prior.customer_group_id != command.customer_group_id:
                    raise CompletionApplicationError("request identity belongs to another group")
                return prior
            group = unit.groups.load(customer_group_id=command.customer_group_id)
            if group is None:
                raise CompletionNotFoundError("Customer Group was not found")
            try:
                event = group.complete(actor_id=command.actor_id, at=self._clock.now())
            except CustomerGroupCompletionError as error:
                raise CompletionApplicationError(str(error)) from error
            result = CompleteCustomerGroupResult(
                command.request_id,
                event.customer_group_id,
                "COMPLETED",
                event.completed_by_id,
                event.occurred_at,
            )
            unit.groups.save(group)
            unit.receipts.save(result)
            unit.activity.record(result=result)
            unit.commit()
            return result
