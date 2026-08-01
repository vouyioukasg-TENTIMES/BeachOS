"""Application orchestration for Bill Closing."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from beachos_api.packs.beachos.bill_closing.domain import BillClosingAggregate, BillClosingError


class BillClosingApplicationError(RuntimeError): ...


class BillClosingAuthorizationError(BillClosingApplicationError): ...


class BillClosingNotFoundError(BillClosingApplicationError): ...


@dataclass(frozen=True, slots=True)
class CloseBillCommand:
    request_id: str
    actor_id: str
    customer_group_id: str


@dataclass(frozen=True, slots=True)
class CloseBillResult:
    request_id: str
    bill_id: str
    customer_group_id: str
    status: str
    closed_by_id: str
    closed_at: datetime
    customer_group_status: str = "ACTIVE"
    service_location_status: str = "OCCUPIED"


class Authority(Protocol):
    def can_close_bill(self, *, actor_id: str, customer_group_id: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class Bills(Protocol):
    def load(self, *, customer_group_id: str) -> BillClosingAggregate | None: ...
    def save(self, bill: BillClosingAggregate) -> None: ...


class Receipts(Protocol):
    def get(self, *, request_id: str) -> CloseBillResult | None: ...
    def save(self, result: CloseBillResult) -> None: ...


class Activity(Protocol):
    def record(self, *, result: CloseBillResult) -> None: ...


class Unit(Protocol):
    bills: Bills
    receipts: Receipts
    activity: Activity

    def __enter__(self) -> "Unit": ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> None: ...


class Units(Protocol):
    def create(self) -> Unit: ...


class BillClosingService:
    def __init__(self, *, authority: Authority, clock: Clock, units: Units) -> None:
        self._authority, self._clock, self._units = authority, clock, units

    def close_bill(self, command: CloseBillCommand) -> CloseBillResult:
        if not all(
            (
                command.request_id.strip(),
                command.actor_id.strip(),
                command.customer_group_id.strip(),
            )
        ):
            raise BillClosingApplicationError("request, actor, and Customer Group are required")
        if not self._authority.can_close_bill(
            actor_id=command.actor_id, customer_group_id=command.customer_group_id
        ):
            raise BillClosingAuthorizationError("Close Bill capability is required")
        with self._units.create() as unit:
            prior = unit.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.customer_group_id != command.customer_group_id:
                    raise BillClosingApplicationError("request identity was used for another Bill")
                return prior
            bill = unit.bills.load(customer_group_id=command.customer_group_id)
            if bill is None:
                raise BillClosingNotFoundError("Customer Group has no fully paid Bill")
            try:
                event = bill.close(actor_id=command.actor_id, at=self._clock.now())
            except BillClosingError as error:
                raise BillClosingApplicationError(str(error)) from error
            result = CloseBillResult(
                command.request_id,
                event.bill_id,
                event.customer_group_id,
                "CLOSED",
                event.closed_by_id,
                event.occurred_at,
            )
            unit.bills.save(bill)
            unit.receipts.save(result)
            unit.activity.record(result=result)
            unit.commit()
            return result
