"""Application orchestration for confirmed Cash Payment."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from beachos_api.packs.beachos.billing.domain import Bill
from beachos_api.packs.beachos.payments.domain import PaymentAggregate, PaymentError


class PaymentApplicationError(RuntimeError): ...


class PaymentNotFoundError(PaymentApplicationError): ...


class PaymentAuthorizationError(PaymentApplicationError): ...


@dataclass(frozen=True, slots=True)
class RecordCashPaymentCommand:
    request_id: str
    actor_id: str
    customer_group_id: str
    amount: Decimal
    currency: str


@dataclass(frozen=True, slots=True)
class PaymentResult:
    request_id: str
    payment_id: str
    bill_id: str
    customer_group_id: str
    amount: Decimal
    currency: str
    method: str
    recorded_by_id: str
    recorded_at: datetime
    balance: Decimal
    bill_status: str


class Authority(Protocol):
    def can_record_payment(self, *, actor_id: str, customer_group_id: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class Identities(Protocol):
    def new_id(self, prefix: str) -> str: ...


class Payments(Protocol):
    def load(self, bill: Bill) -> PaymentAggregate: ...
    def save(self, aggregate: PaymentAggregate) -> None: ...


class Bills(Protocol):
    def get(self, *, customer_group_id: str) -> Bill | None: ...


class Receipts(Protocol):
    def get(self, *, request_id: str) -> PaymentResult | None: ...
    def save(self, result: PaymentResult) -> None: ...


class Activity(Protocol):
    def record(self, *, result: PaymentResult) -> None: ...


class Unit(Protocol):
    bills: Bills
    payments: Payments
    receipts: Receipts
    activity: Activity

    def __enter__(self) -> "Unit": ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> None: ...


class Units(Protocol):
    def create(self) -> Unit: ...


class PaymentService:
    def __init__(self, *, authority: Authority, clock: Clock, identities: Identities, units: Units):
        self._authority, self._clock, self._identities, self._units = (
            authority,
            clock,
            identities,
            units,
        )

    def record_cash_payment(self, command: RecordCashPaymentCommand) -> PaymentResult:
        if not all(
            (
                command.request_id.strip(),
                command.actor_id.strip(),
                command.customer_group_id.strip(),
            )
        ):
            raise PaymentApplicationError("request, actor, and Customer Group are required")
        if not self._authority.can_record_payment(
            actor_id=command.actor_id, customer_group_id=command.customer_group_id
        ):
            raise PaymentAuthorizationError("Record Payments capability is required")
        with self._units.create() as unit:
            prior = unit.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.customer_group_id != command.customer_group_id:
                    raise PaymentApplicationError("request identity was used for another Payment")
                return prior
            bill = unit.bills.get(customer_group_id=command.customer_group_id)
            if bill is None:
                raise PaymentNotFoundError("Customer Group has no Bill")
            aggregate = unit.payments.load(bill)
            try:
                payment = aggregate.record_cash_payment(
                    payment_id=self._identities.new_id("payment"),
                    amount=command.amount,
                    currency=command.currency,
                    actor_id=command.actor_id,
                    at=self._clock.now(),
                )
            except PaymentError as error:
                raise PaymentApplicationError(str(error)) from error
            result = PaymentResult(
                command.request_id,
                payment.payment_id,
                bill.bill_id,
                bill.customer_group_id,
                payment.amount,
                payment.currency,
                payment.method,
                payment.recorded_by_id,
                payment.occurred_at,
                Decimal("0"),
                "FULLY_PAID",
            )
            unit.payments.save(aggregate)
            unit.receipts.save(result)
            unit.activity.record(result=result)
            unit.commit()
            return result
