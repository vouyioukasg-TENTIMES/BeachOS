from datetime import UTC, datetime

import pytest

from beachos_api.packs.beachos.customer_completion.application import (
    CompleteCustomerGroupCommand,
    CustomerGroupCompletionService,
)
from beachos_api.packs.beachos.customer_completion.application.service import (
    CompletionApplicationError,
    CompletionAuthorizationError,
    CompletionNotFoundError,
)
from beachos_api.packs.beachos.customer_completion.domain import (
    CustomerGroupCompleted,
    CustomerGroupCompletion,
    CustomerGroupCompletionError,
)

AT = datetime(2026, 8, 1, 18, 10, tzinfo=UTC)


def test_active_group_with_closed_bill_completes_once() -> None:
    group = CustomerGroupCompletion.restore(
        customer_group_id="group-1", status="ACTIVE", bill_status="CLOSED", events=()
    )
    event = group.complete(actor_id="staff-1", at=AT)
    assert event == CustomerGroupCompleted("group-1", "staff-1", AT)
    assert group.status == "COMPLETED"
    assert group.pull_events() == (event,)
    with pytest.raises(CustomerGroupCompletionError, match="ACTIVE"):
        group.complete(actor_id="staff-1", at=AT)


def test_no_bill_group_can_complete_but_open_or_paid_bill_cannot() -> None:
    no_bill = CustomerGroupCompletion.restore(
        customer_group_id="group-1", status="ACTIVE", bill_status=None, events=()
    )
    assert no_bill.complete(actor_id="staff", at=AT)
    for status in ("OPEN", "FULLY_PAID"):
        with pytest.raises(CustomerGroupCompletionError, match="must already be CLOSED"):
            CustomerGroupCompletion.restore(
                customer_group_id="group-2", status="ACTIVE", bill_status=status, events=()
            ).complete(actor_id="staff", at=AT)


def test_restoration_preserves_immutable_completion_without_new_events() -> None:
    event = CustomerGroupCompleted("group-1", "staff-1", AT)
    group = CustomerGroupCompletion.restore(
        customer_group_id="group-1",
        status="COMPLETED",
        bill_status="CLOSED",
        events=(event,),
    )
    assert group.completed == event
    assert group.version == 1
    assert group.pull_events() == ()


@pytest.mark.parametrize(
    ("customer_group_id", "status", "bill_status", "message"),
    [
        (" ", "ACTIVE", None, "identity"),
        ("group-1", "UNKNOWN", None, "status"),
        ("group-1", "ACTIVE", "PAID", "Bill status"),
    ],
)
def test_invalid_structural_state_is_rejected(
    customer_group_id: str, status: str, bill_status: str | None, message: str
) -> None:
    with pytest.raises(CustomerGroupCompletionError, match=message):
        CustomerGroupCompletion.restore(
            customer_group_id=customer_group_id,
            status=status,
            bill_status=bill_status,
            events=(),
        )


def test_invalid_completion_history_and_inputs_are_rejected() -> None:
    with pytest.raises(CustomerGroupCompletionError, match="immutable event"):
        CustomerGroupCompletion.restore(
            customer_group_id="group-1", status="COMPLETED", bill_status=None, events=()
        )
    with pytest.raises(CustomerGroupCompletionError, match="another Customer Group"):
        CustomerGroupCompletion.restore(
            customer_group_id="group-1",
            status="COMPLETED",
            bill_status=None,
            events=(CustomerGroupCompleted("group-2", "staff", AT),),
        )
    with pytest.raises(CustomerGroupCompletionError, match="Active state"):
        CustomerGroupCompletion.restore(
            customer_group_id="group-1",
            status="ACTIVE",
            bill_status=None,
            events=(CustomerGroupCompleted("group-1", "staff", AT),),
        )
    group = CustomerGroupCompletion.restore(
        customer_group_id="group-1", status="ACTIVE", bill_status=None, events=()
    )
    with pytest.raises(CustomerGroupCompletionError, match="identity"):
        group.complete(actor_id=" ", at=AT)
    with pytest.raises(CustomerGroupCompletionError, match="timezone"):
        group.complete(actor_id="staff", at=datetime(2026, 8, 1, 18, 10))


class Authority:
    allowed = True

    def can_complete_customer_group(self, **_: str) -> bool:
        return self.allowed


class Clock:
    def now(self) -> datetime:
        return AT


class Groups:
    def __init__(self) -> None:
        self.group = CustomerGroupCompletion.restore(
            customer_group_id="group-1", status="ACTIVE", bill_status="CLOSED", events=()
        )
        self.saved = False

    def load(self, **_: str):
        return self.group

    def save(self, _: CustomerGroupCompletion) -> None:
        self.saved = True


class Receipts:
    def __init__(self) -> None:
        self.value = None

    def get(self, **_: str):
        return self.value

    def save(self, value) -> None:
        self.value = value


class Activity:
    def __init__(self) -> None:
        self.recorded = False

    def record(self, **_: object) -> None:
        self.recorded = True


class Unit:
    def __init__(self) -> None:
        self.groups, self.receipts, self.activity = Groups(), Receipts(), Activity()
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


def test_application_exposes_context_and_completes_idempotently() -> None:
    units = Units()
    service = CustomerGroupCompletionService(authority=Authority(), clock=Clock(), units=units)
    context = service.get_context(customer_group_id="group-1")
    assert context.can_complete and context.service_location_status == "OCCUPIED"
    command = CompleteCustomerGroupCommand("request-1", "staff-1", "group-1")
    first = service.complete(command)
    second = service.complete(command)
    assert first == second
    assert not first.service_location_released
    assert units.unit.groups.saved and units.unit.activity.recorded and units.unit.committed


def test_application_rejects_group_with_unclosed_bill() -> None:
    units = Units()
    units.unit.groups.group = CustomerGroupCompletion.restore(
        customer_group_id="group-1", status="ACTIVE", bill_status="FULLY_PAID", events=()
    )
    with pytest.raises(CompletionApplicationError, match="must already be CLOSED"):
        CustomerGroupCompletionService(authority=Authority(), clock=Clock(), units=units).complete(
            CompleteCustomerGroupCommand("request-1", "staff", "group-1")
        )


def test_application_validates_authority_identity_and_missing_groups() -> None:
    units = Units()
    service = CustomerGroupCompletionService(authority=Authority(), clock=Clock(), units=units)
    with pytest.raises(CompletionApplicationError, match="required"):
        service.complete(CompleteCustomerGroupCommand("", "staff", "group-1"))

    denied = Authority()
    denied.allowed = False
    with pytest.raises(CompletionAuthorizationError, match="capability"):
        CustomerGroupCompletionService(authority=denied, clock=Clock(), units=units).complete(
            CompleteCustomerGroupCommand("request", "staff", "group-1")
        )

    units.unit.groups.group = None
    with pytest.raises(CompletionNotFoundError, match="not found"):
        service.get_context(customer_group_id="missing")
    with pytest.raises(CompletionNotFoundError, match="not found"):
        service.complete(CompleteCustomerGroupCommand("request", "staff", "missing"))


def test_idempotency_identity_cannot_be_reused_for_another_group() -> None:
    units = Units()
    service = CustomerGroupCompletionService(authority=Authority(), clock=Clock(), units=units)
    service.complete(CompleteCustomerGroupCommand("request", "staff", "group-1"))
    with pytest.raises(CompletionApplicationError, match="another group"):
        service.complete(CompleteCustomerGroupCommand("request", "staff", "group-2"))
