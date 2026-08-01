from datetime import UTC, datetime
from decimal import Decimal

import pytest

from beachos_api.packs.beachos.billing.application import BillingService
from beachos_api.packs.beachos.billing.domain import Bill, BillCreated, BillingError, BillLineAdded

AT = datetime(2026, 8, 1, 10, tzinfo=UTC)


def history() -> tuple[BillCreated | BillLineAdded, ...]:
    return (
        BillCreated("bill-1", "group-1", "EUR", AT),
        BillLineAdded(
            "bill-1",
            "line-1",
            "Sunbed",
            Decimal("1"),
            Decimal("20"),
            Decimal("20"),
            "EUR",
            "BEACH_SUNBED",
            AT,
        ),
        BillLineAdded(
            "bill-1",
            "line-2",
            "Coffee",
            Decimal("2"),
            Decimal("4"),
            Decimal("8"),
            "EUR",
            "ORDER_ITEM",
            AT,
        ),
    )


def test_bill_restores_an_explainable_running_total_from_events() -> None:
    bill = Bill.restore(history())
    assert bill.bill_id == "bill-1"
    assert bill.customer_group_id == "group-1"
    assert bill.total == Decimal("28")
    assert bill.version == 3
    assert [line.source for line in bill.lines] == ["BEACH_SUNBED", "ORDER_ITEM"]


@pytest.mark.parametrize(
    "events",
    [
        (),
        (BillLineAdded("bill-1", "line", "x", Decimal(1), Decimal(1), Decimal(1), "EUR", "x", AT),),
        (BillCreated("bill-1", "group", "EUR", AT), BillCreated("bill-2", "group", "EUR", AT)),
    ],
)
def test_bill_rejects_impossible_history(events: tuple[object, ...]) -> None:
    with pytest.raises(BillingError):
        Bill.restore(events)  # type: ignore[arg-type]


class Reader:
    def __init__(self, bill: Bill | None) -> None:
        self.bill = bill

    def get(self, *, customer_group_id: str) -> Bill | None:
        assert customer_group_id == "group-1"
        return self.bill


def test_service_returns_bill_or_explicit_no_bill() -> None:
    result = BillingService(Reader(Bill.restore(history()))).get_bill(customer_group_id="group-1")
    assert result is not None
    assert result.balance == Decimal("28")
    assert result.status == "OPEN"
    assert BillingService(Reader(None)).get_bill(customer_group_id="group-1") is None
