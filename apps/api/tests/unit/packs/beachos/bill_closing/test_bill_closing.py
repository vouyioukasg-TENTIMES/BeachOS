from datetime import UTC, datetime

import pytest

from beachos_api.packs.beachos.bill_closing.application import (
    BillClosingService,
    CloseBillCommand,
)
from beachos_api.packs.beachos.bill_closing.application.service import BillClosingApplicationError
from beachos_api.packs.beachos.bill_closing.domain import (
    BillClosed,
    BillClosingAggregate,
    BillClosingError,
    BillFullyPaid,
    PaymentRecorded,
)

AT = datetime(2026, 8, 1, 18, 5, tzinfo=UTC)


def paid() -> BillClosingAggregate:
    return BillClosingAggregate.restore(
        bill_id="bill-1",
        customer_group_id="group-1",
        events=(
            PaymentRecorded("bill-1", "group-1", AT),
            BillFullyPaid("bill-1", "group-1", AT),
        ),
    )


def test_only_fully_paid_bill_closes_once_without_other_state_changes() -> None:
    bill = paid()
    event = bill.close(actor_id="cashier-1", at=AT)
    assert event == BillClosed("bill-1", "group-1", "cashier-1", AT)
    assert bill.pull_events() == (event,)
    assert bill.version == 3
    with pytest.raises(BillClosingError, match="already closed"):
        bill.close(actor_id="cashier-1", at=AT)


def test_unpaid_bill_cannot_close_and_invalid_history_is_rejected() -> None:
    bill = BillClosingAggregate.restore(bill_id="bill-1", customer_group_id="group-1", events=())
    with pytest.raises(BillClosingError, match="FULLY_PAID"):
        bill.close(actor_id="cashier", at=AT)
    with pytest.raises(BillClosingError, match="must follow confirmed Payment"):
        BillClosingAggregate.restore(
            bill_id="bill-1",
            customer_group_id="group-1",
            events=(BillFullyPaid("bill-1", "group-1", AT),),
        )


class Authority:
    def can_close_bill(self, **_: str) -> bool:
        return True


class Clock:
    def now(self) -> datetime:
        return AT


class Bills:
    def __init__(self) -> None:
        self.bill = paid()
        self.saved = False

    def load(self, **_: str):
        return self.bill

    def save(self, _: BillClosingAggregate) -> None:
        self.saved = True


class Receipts:
    def __init__(self) -> None:
        self.value = None

    def get(self, **_: str):
        return self.value

    def save(self, result) -> None:
        self.value = result


class Activity:
    def __init__(self) -> None:
        self.recorded = False

    def record(self, **_: object) -> None:
        self.recorded = True


class Unit:
    def __init__(self) -> None:
        self.bills, self.receipts, self.activity = Bills(), Receipts(), Activity()
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


def test_application_closes_idempotently_and_preserves_operational_state() -> None:
    units = Units()
    service = BillClosingService(authority=Authority(), clock=Clock(), units=units)
    command = CloseBillCommand("request-1", "cashier-1", "group-1")
    first = service.close_bill(command)
    second = service.close_bill(command)
    assert first == second
    assert first.status == "CLOSED"
    assert first.customer_group_status == "ACTIVE"
    assert first.service_location_status == "OCCUPIED"
    assert units.unit.bills.saved and units.unit.activity.recorded and units.unit.committed


def test_application_rejects_unpaid_bill() -> None:
    units = Units()
    units.unit.bills.bill = BillClosingAggregate.restore(
        bill_id="bill-1", customer_group_id="group-1", events=()
    )
    with pytest.raises(BillClosingApplicationError, match="FULLY_PAID"):
        BillClosingService(authority=Authority(), clock=Clock(), units=units).close_bill(
            CloseBillCommand("request-1", "cashier", "group-1")
        )
