from datetime import UTC, datetime
from decimal import Decimal

import pytest

from beachos_api.packs.beachos.billing.domain import Bill, BillCreated, BillLineAdded
from beachos_api.packs.beachos.payments.application import (
    PaymentService,
    RecordCashPaymentCommand,
)
from beachos_api.packs.beachos.payments.application.service import PaymentApplicationError
from beachos_api.packs.beachos.payments.domain import (
    BillFullyPaid,
    PaymentAggregate,
    PaymentError,
    PaymentRecorded,
)

AT = datetime(2026, 8, 1, 18, tzinfo=UTC)


def aggregate(events: tuple[PaymentRecorded | BillFullyPaid, ...] = ()) -> PaymentAggregate:
    return PaymentAggregate.restore(
        bill_id="bill-1",
        customer_group_id="group-1",
        total=Decimal("28"),
        currency="EUR",
        events=events,
    )


def test_full_cash_payment_records_two_approved_events() -> None:
    payment = aggregate()
    recorded = payment.record_cash_payment(
        payment_id="payment-1",
        amount=Decimal("28"),
        currency="EUR",
        actor_id="cashier-1",
        at=AT,
    )
    events = payment.pull_events()
    assert recorded.method == "CASH"
    assert isinstance(events[0], PaymentRecorded)
    assert isinstance(events[1], BillFullyPaid)
    assert payment.fully_paid
    assert payment.version == 2


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("10"), Decimal("29")])
def test_partial_zero_and_excess_payments_are_rejected(amount: Decimal) -> None:
    with pytest.raises(PaymentError, match="only full Payment"):
        aggregate().record_cash_payment(
            payment_id="payment-1", amount=amount, currency="EUR", actor_id="cashier", at=AT
        )


def test_payment_cannot_be_recorded_twice_or_restored_without_fully_paid() -> None:
    event = PaymentRecorded(
        "payment-1", "bill-1", "group-1", Decimal("28"), "EUR", "CASH", "cashier", AT
    )
    with pytest.raises(PaymentError, match="Bill Fully Paid"):
        aggregate((event,))
    restored = aggregate((event, BillFullyPaid("bill-1", "group-1", AT)))
    with pytest.raises(PaymentError, match="already has"):
        restored.record_cash_payment(
            payment_id="payment-2", amount=Decimal("28"), currency="EUR", actor_id="cashier", at=AT
        )


def bill() -> Bill:
    return Bill.restore(
        (
            BillCreated("bill-1", "group-1", "EUR", AT),
            BillLineAdded(
                "bill-1",
                "line-1",
                "Service",
                Decimal("1"),
                Decimal("28"),
                Decimal("28"),
                "EUR",
                "ORDER_ITEM",
                AT,
            ),
        )
    )


class Authority:
    allowed = True

    def can_record_payment(self, **_: str) -> bool:
        return self.allowed


class Clock:
    def now(self) -> datetime:
        return AT


class Identities:
    def new_id(self, prefix: str) -> str:
        return f"{prefix}-1"


class Bills:
    value: Bill | None = bill()

    def get(self, **_: str) -> Bill | None:
        return self.value


class Payments:
    def __init__(self) -> None:
        self.value = aggregate()
        self.saved = False

    def load(self, _: Bill) -> PaymentAggregate:
        return self.value

    def save(self, _: PaymentAggregate) -> None:
        self.saved = True


class Receipts:
    def __init__(self) -> None:
        self.value = None

    def get(self, **_: str):
        return self.value

    def save(self, result):
        self.value = result


class Activity:
    recorded = False

    def record(self, **_: object) -> None:
        self.recorded = True


class Unit:
    def __init__(self) -> None:
        self.bills = Bills()
        self.payments = Payments()
        self.receipts = Receipts()
        self.activity = Activity()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, *_: object) -> None:
        pass

    def commit(self) -> None:
        self.committed = True


class Units:
    def __init__(self) -> None:
        self.unit = Unit()

    def create(self):
        return self.unit


def test_application_orchestrates_atomic_idempotent_payment() -> None:
    units = Units()
    service = PaymentService(
        authority=Authority(), clock=Clock(), identities=Identities(), units=units
    )
    command = RecordCashPaymentCommand("request-1", "cashier-1", "group-1", Decimal("28"), "EUR")
    first = service.record_cash_payment(command)
    second = service.record_cash_payment(command)
    assert first == second
    assert first.balance == 0 and first.bill_status == "FULLY_PAID"
    assert units.unit.payments.saved and units.unit.activity.recorded and units.unit.committed


def test_application_rejects_wrong_amount() -> None:
    service = PaymentService(
        authority=Authority(), clock=Clock(), identities=Identities(), units=Units()
    )
    with pytest.raises(PaymentApplicationError, match="only full Payment"):
        service.record_cash_payment(
            RecordCashPaymentCommand("request-1", "cashier", "group-1", Decimal("1"), "EUR")
        )
