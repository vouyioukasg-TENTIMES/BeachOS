"""HTTP delivery adapter for BeachOS backend capabilities."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from beachos_api.composition import (
    ConfigurationError,
    bar_service,
    billing_service,
    guest_arrival_service,
    kitchen_service,
    ordering_service,
    venue_opening_service,
)
from beachos_api.identity import DevelopmentIdentity, development_identity
from beachos_api.packs.beachos.bar.application import (
    AcknowledgeBarTicketCommand,
    AcknowledgeBarTicketResult,
    BarContextResult,
    BarService,
    BarTicketDTO,
    ProgressBarTicketCommand,
)
from beachos_api.packs.beachos.bar.application.exceptions import (
    BarAuthorizationDeniedError,
    BarBusinessRuleRejectedError,
    BarCommandValidationError,
    BarTicketNotFoundError,
)
from beachos_api.packs.beachos.bar.infrastructure.errors import (
    BarConcurrencyError,
    BarInfrastructureError,
)
from beachos_api.packs.beachos.billing.application import BillDTO as RunningBillDTO
from beachos_api.packs.beachos.billing.application import BillingService
from beachos_api.packs.beachos.guest_arrival.application import (
    GuestArrivalContextResult,
    GuestArrivalService,
    OpenCustomerGroupCommand,
    OpenCustomerGroupResult,
    ServiceLocationDTO,
)
from beachos_api.packs.beachos.guest_arrival.application.exceptions import (
    GuestArrivalAuthorizationError,
    GuestArrivalBusinessRuleError,
    GuestArrivalNotFoundError,
    GuestArrivalValidationError,
)
from beachos_api.packs.beachos.guest_arrival.infrastructure.errors import (
    GuestArrivalConcurrencyError,
    GuestArrivalInfrastructureError,
)
from beachos_api.packs.beachos.kitchen.application import (
    AcknowledgeKitchenTicketCommand,
    AcknowledgeKitchenTicketResult,
    KitchenContextResult,
    KitchenService,
    ProgressKitchenTicketCommand,
)
from beachos_api.packs.beachos.kitchen.application.dtos import KitchenTicketDTO
from beachos_api.packs.beachos.kitchen.application.exceptions import (
    KitchenAuthorizationDeniedError,
    KitchenBusinessRuleRejectedError,
    KitchenCommandValidationError,
    KitchenTicketNotFoundError,
)
from beachos_api.packs.beachos.kitchen.infrastructure.errors import (
    KitchenConcurrencyError,
    KitchenInfrastructureError,
)
from beachos_api.packs.beachos.ordering.application import (
    OrderingContextResult,
    OrderingService,
    SubmitOrderCommand,
    SubmitOrderItem,
    SubmitOrderResult,
)
from beachos_api.packs.beachos.ordering.application.dtos import BillDTO, OrderDTO
from beachos_api.packs.beachos.ordering.application.exceptions import (
    CustomerGroupNotFoundError,
    OrderingAuthorizationDeniedError,
    OrderingBusinessRuleRejectedError,
    OrderingCommandValidationError,
)
from beachos_api.packs.beachos.ordering.infrastructure.errors import (
    OrderingConcurrencyError,
    OrderingInfrastructureError,
)
from beachos_api.packs.beachos.venue_opening.application import (
    DeclareDepartmentReadinessCommand,
    DeclareDepartmentReadinessResult,
    DepartmentOwnerContextResult,
    OpenVenueCommand,
    VenueOpeningService,
)
from beachos_api.packs.beachos.venue_opening.application.dtos import (
    DepartmentReadinessDTO,
    OpeningReportDTO,
    OpenVenueResult,
    VenueContextResult,
)
from beachos_api.packs.beachos.venue_opening.application.exceptions import (
    AuthorizationDeniedError,
    BusinessRuleRejectedError,
    CommandValidationError,
    VenueContextMismatchError,
    VenueNotFoundError,
)
from beachos_api.packs.beachos.venue_opening.domain import ReadinessStatus
from beachos_api.packs.beachos.venue_opening.infrastructure.errors import (
    BusinessDatePolicyNotFoundError,
    InfrastructureError,
    OptimisticConcurrencyError,
)

router = APIRouter()


class OpenVenueRequest(BaseModel):
    """HTTP input for one Venue-opening intention."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    request_id: str = Field(min_length=1)
    venue_id: str = Field(min_length=1)


class DeclareDepartmentReadinessRequest(BaseModel):
    """HTTP input for one department owner's readiness declaration."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    request_id: str = Field(min_length=1)
    venue_id: str = Field(min_length=1)
    status: ReadinessStatus
    reason: str | None = None
    comment: str | None = None


class OpenCustomerGroupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    request_id: str = Field(min_length=1)
    venue_id: str = Field(min_length=1)
    service_location_id: str = Field(min_length=1)
    physical_context_confirmed: bool
    waiter_accepts_responsibility: bool
    opening_charge_confirmed: bool = False


class ServiceLocationResponse(BaseModel):
    service_location_id: str
    visible_name: str
    digital_identity: str
    location_type: str
    status: str
    active_customer_group_id: str | None
    opening_charge: Decimal | None
    currency: str | None
    charge_description: str | None

    @classmethod
    def from_application(cls, value: ServiceLocationDTO) -> ServiceLocationResponse:
        return cls(
            service_location_id=value.service_location_id,
            visible_name=value.visible_name,
            digital_identity=value.digital_identity,
            location_type=value.location_type,
            status=value.status,
            active_customer_group_id=value.active_customer_group_id,
            opening_charge=value.opening_charge,
            currency=value.currency,
            charge_description=value.charge_description,
        )


class GuestArrivalContextResponse(BaseModel):
    venue_id: str
    venue_name: str
    business_date: str
    venue_open: bool
    operational_confidence: str
    locations: list[ServiceLocationResponse]

    @classmethod
    def from_application(cls, value: GuestArrivalContextResult) -> GuestArrivalContextResponse:
        return cls(
            venue_id=value.venue_id,
            venue_name=value.venue_name,
            business_date=value.business_date,
            venue_open=value.venue_open,
            operational_confidence=value.operational_confidence,
            locations=[ServiceLocationResponse.from_application(item) for item in value.locations],
        )


class CustomerGroupResponse(BaseModel):
    customer_group_id: str
    venue_id: str
    service_location_id: str
    responsible_waiter_id: str
    opened_at: datetime
    bill_id: str | None
    opening_obligation: Decimal | None
    currency: str | None


class OpenCustomerGroupResponse(BaseModel):
    request_id: str
    customer_group: CustomerGroupResponse
    service_location: ServiceLocationResponse

    @classmethod
    def from_application(cls, value: OpenCustomerGroupResult) -> OpenCustomerGroupResponse:
        group = value.customer_group
        return cls(
            request_id=value.request_id,
            customer_group=CustomerGroupResponse(
                customer_group_id=group.customer_group_id,
                venue_id=group.venue_id,
                service_location_id=group.service_location_id,
                responsible_waiter_id=group.responsible_waiter_id,
                opened_at=group.opened_at,
                bill_id=group.bill_id,
                opening_obligation=group.opening_obligation,
                currency=group.currency,
            ),
            service_location=ServiceLocationResponse.from_application(value.service_location),
        )


class ReadinessResponse(BaseModel):
    department_id: str
    responsible_person_id: str
    declared_by_id: str
    status: str
    declared_at: datetime
    reason: str | None
    comment: str | None

    @classmethod
    def from_application(cls, value: DepartmentReadinessDTO) -> ReadinessResponse:
        return cls(
            department_id=value.department_id,
            responsible_person_id=value.responsible_person_id,
            declared_by_id=value.declared_by_id,
            status=value.status,
            declared_at=value.declared_at.astimezone(UTC),
            reason=value.reason,
            comment=value.comment,
        )


class OpeningReportResponse(BaseModel):
    venue_id: str
    business_date: date
    opened_at: datetime
    host_id: str
    department_readiness: list[ReadinessResponse]
    declaration_history: list[ReadinessResponse]
    delays: list[ReadinessResponse]
    blocking_issues: list[ReadinessResponse]

    @classmethod
    def from_application(cls, report: OpeningReportDTO) -> OpeningReportResponse:
        return cls(
            venue_id=report.venue_id,
            business_date=report.business_date,
            opened_at=report.opened_at.astimezone(UTC),
            host_id=report.host_id,
            department_readiness=[
                ReadinessResponse.from_application(item) for item in report.department_readiness
            ],
            declaration_history=[
                ReadinessResponse.from_application(item) for item in report.declaration_history
            ],
            delays=[ReadinessResponse.from_application(item) for item in report.delays],
            blocking_issues=[
                ReadinessResponse.from_application(item) for item in report.blocking_issues
            ],
        )


class OpenVenueResponse(BaseModel):
    request_id: str
    report: OpeningReportResponse

    @classmethod
    def from_application(cls, result: OpenVenueResult) -> OpenVenueResponse:
        return cls(
            request_id=result.request_id,
            report=OpeningReportResponse.from_application(result.report),
        )


class DepartmentContextResponse(BaseModel):
    department_id: str
    name: str
    responsible_person_id: str
    current_readiness: ReadinessResponse | None


class DepartmentOwnerContextResponse(BaseModel):
    venue_id: str
    venue_name: str
    business_date: date
    opening_status: str
    departments: list[DepartmentContextResponse]
    declaration_history: list[ReadinessResponse]

    @classmethod
    def from_application(
        cls, result: DepartmentOwnerContextResult
    ) -> DepartmentOwnerContextResponse:
        return cls(
            venue_id=result.venue_id,
            venue_name=result.venue_name,
            business_date=result.business_date,
            opening_status=result.opening_status,
            departments=[
                DepartmentContextResponse(
                    department_id=department.department_id,
                    name=department.name,
                    responsible_person_id=department.responsible_person_id,
                    current_readiness=(
                        ReadinessResponse.from_application(department.current_readiness)
                        if department.current_readiness is not None
                        else None
                    ),
                )
                for department in result.departments
            ],
            declaration_history=[
                ReadinessResponse.from_application(declaration)
                for declaration in result.declaration_history
            ],
        )


class DeclareDepartmentReadinessResponse(BaseModel):
    request_id: str
    venue_id: str
    business_date: date
    declaration: ReadinessResponse

    @classmethod
    def from_application(
        cls, result: DeclareDepartmentReadinessResult
    ) -> DeclareDepartmentReadinessResponse:
        return cls(
            request_id=result.request_id,
            venue_id=result.venue_id,
            business_date=result.business_date,
            declaration=ReadinessResponse.from_application(result.declaration),
        )


class AttentionItemResponse(BaseModel):
    code: str
    importance: str
    message: str
    department_id: str | None


class VenueContextResponse(BaseModel):
    venue_id: str
    venue_name: str
    business_date: date
    opening_status: str
    opening_report: OpeningReportResponse | None
    department_readiness: list[DepartmentContextResponse]
    outstanding_departments: list[str]
    attention_queue: list[AttentionItemResponse]

    @classmethod
    def from_application(cls, result: VenueContextResult) -> VenueContextResponse:
        return cls(
            venue_id=result.venue_id,
            venue_name=result.venue_name,
            business_date=result.business_date,
            opening_status=result.opening_status,
            opening_report=(
                OpeningReportResponse.from_application(result.opening_report)
                if result.opening_report is not None
                else None
            ),
            department_readiness=[
                DepartmentContextResponse(
                    department_id=department.department_id,
                    name=department.name,
                    responsible_person_id=department.responsible_person_id,
                    current_readiness=(
                        ReadinessResponse.from_application(department.current_readiness)
                        if department.current_readiness is not None
                        else None
                    ),
                )
                for department in result.departments
            ],
            outstanding_departments=list(result.outstanding_department_ids),
            attention_queue=[
                AttentionItemResponse(
                    code=item.code,
                    importance=item.importance,
                    message=item.message,
                    department_id=item.department_id,
                )
                for item in result.attention_queue
            ],
        )


Service = Annotated[VenueOpeningService, Depends(venue_opening_service)]
Identity = Annotated[DevelopmentIdentity, Depends(development_identity)]
VenueId = Annotated[str, Query(min_length=1)]
OrderingServiceDependency = Annotated[OrderingService, Depends(ordering_service)]
BillingServiceDependency = Annotated[BillingService, Depends(billing_service)]
GuestArrivalServiceDependency = Annotated[GuestArrivalService, Depends(guest_arrival_service)]
CustomerGroupId = Annotated[str, Query(min_length=1)]


def department_development_identity(
    actor_id: Annotated[str, Header(alias="X-BeachOS-Development-Actor", min_length=1)],
) -> DevelopmentIdentity:
    """Select a temporary department-owner identity until authentication exists."""

    from beachos_api.identity import FakeIdentityProvider

    return FakeIdentityProvider().identity_for(actor_id)


DepartmentIdentity = Annotated[DevelopmentIdentity, Depends(department_development_identity)]


@router.get("/guest-arrival/context", response_model=GuestArrivalContextResponse)
def guest_arrival_context(
    venue_id: VenueId, service: GuestArrivalServiceDependency, identity: Identity
) -> GuestArrivalContextResponse:
    return GuestArrivalContextResponse.from_application(
        service.get_context(actor_id=identity.actor_id, venue_id=venue_id)
    )


@router.get("/guest-arrival/service-locations/identify", response_model=ServiceLocationResponse)
def identify_service_location(
    venue_id: VenueId,
    digital_identity: Annotated[str, Query(min_length=1)],
    service: GuestArrivalServiceDependency,
    identity: Identity,
) -> ServiceLocationResponse:
    return ServiceLocationResponse.from_application(
        service.identify(
            actor_id=identity.actor_id, venue_id=venue_id, digital_identity=digital_identity
        )
    )


@router.post("/guest-arrival/customer-groups/open", response_model=OpenCustomerGroupResponse)
def open_customer_group(
    payload: OpenCustomerGroupRequest,
    service: GuestArrivalServiceDependency,
    identity: DepartmentIdentity,
) -> OpenCustomerGroupResponse:
    return OpenCustomerGroupResponse.from_application(
        service.open_customer_group(
            OpenCustomerGroupCommand(
                payload.request_id,
                identity.actor_id,
                payload.venue_id,
                payload.service_location_id,
                payload.physical_context_confirmed,
                payload.waiter_accepts_responsibility,
                payload.opening_charge_confirmed,
            )
        )
    )


KitchenServiceDependency = Annotated[KitchenService, Depends(kitchen_service)]
BarServiceDependency = Annotated[BarService, Depends(bar_service)]


class SubmitOrderItemRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    menu_item_id: str = Field(min_length=1)
    quantity: Decimal
    note: str | None = None


class AcknowledgeKitchenTicketRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    request_id: str = Field(min_length=1)


class AcknowledgeBarTicketRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    request_id: str = Field(min_length=1)


class BarTicketResponse(BaseModel):
    ticket_id: str
    order_id: str
    customer_group_id: str
    venue_id: str
    submission_service_location_id: str
    current_service_location_id: str
    responsible_service_staff_id: str
    submitted_at: datetime
    items: list[dict[str, object]]
    status: str
    acknowledged_by_id: str | None
    acknowledged_at: datetime | None
    ready_by_id: str | None
    ready_at: datetime | None
    collected_by_id: str | None
    collected_at: datetime | None
    delivered_by_id: str | None
    delivered_at: datetime | None
    current_responsibility: str
    current_responsible_person_id: str
    next_action: str

    @classmethod
    def from_application(cls, ticket: BarTicketDTO) -> BarTicketResponse:
        return cls(
            ticket_id=ticket.ticket_id,
            order_id=ticket.order_id,
            customer_group_id=ticket.customer_group_id,
            venue_id=ticket.venue_id,
            submission_service_location_id=ticket.submission_service_location_id,
            current_service_location_id=ticket.current_service_location_id,
            responsible_service_staff_id=ticket.responsible_service_staff_id,
            submitted_at=ticket.submitted_at,
            items=[
                {
                    "order_item_id": i.order_item_id,
                    "name": i.name,
                    "quantity": i.quantity,
                    "note": i.note,
                }
                for i in ticket.items
            ],
            status=ticket.status,
            acknowledged_by_id=ticket.acknowledged_by_id,
            acknowledged_at=ticket.acknowledged_at,
            ready_by_id=ticket.ready_by_id,
            ready_at=ticket.ready_at,
            collected_by_id=ticket.collected_by_id,
            collected_at=ticket.collected_at,
            delivered_by_id=ticket.delivered_by_id,
            delivered_at=ticket.delivered_at,
            current_responsibility=ticket.current_responsibility,
            current_responsible_person_id=ticket.current_responsible_person_id,
            next_action=ticket.next_action,
        )


class BarContextResponse(BaseModel):
    venue_id: str
    awaiting_acknowledgement_count: int
    tickets: list[BarTicketResponse]

    @classmethod
    def from_application(cls, result: BarContextResult) -> BarContextResponse:
        return cls(
            venue_id=result.venue_id,
            awaiting_acknowledgement_count=result.awaiting_acknowledgement_count,
            tickets=[BarTicketResponse.from_application(t) for t in result.tickets],
        )


class AcknowledgeBarTicketResponse(BaseModel):
    request_id: str
    ticket: BarTicketResponse

    @classmethod
    def from_application(cls, result: AcknowledgeBarTicketResult) -> AcknowledgeBarTicketResponse:
        return cls(
            request_id=result.request_id, ticket=BarTicketResponse.from_application(result.ticket)
        )


class KitchenTicketResponse(BaseModel):
    ticket_id: str
    order_id: str
    customer_group_id: str
    venue_id: str
    submission_service_location_id: str
    current_service_location_id: str
    responsible_service_staff_id: str
    submitted_at: datetime
    items: list[dict[str, object]]
    status: str
    acknowledged_by_id: str | None
    acknowledged_at: datetime | None
    ready_by_id: str | None
    ready_at: datetime | None
    collected_by_id: str | None
    collected_at: datetime | None
    delivered_by_id: str | None
    delivered_at: datetime | None
    current_responsibility: str
    current_responsible_person_id: str
    next_action: str

    @classmethod
    def from_application(cls, ticket: KitchenTicketDTO) -> KitchenTicketResponse:
        return cls(
            ticket_id=ticket.ticket_id,
            order_id=ticket.order_id,
            customer_group_id=ticket.customer_group_id,
            venue_id=ticket.venue_id,
            submission_service_location_id=ticket.submission_service_location_id,
            current_service_location_id=ticket.current_service_location_id,
            responsible_service_staff_id=ticket.responsible_service_staff_id,
            submitted_at=ticket.submitted_at,
            items=[
                {
                    "order_item_id": item.order_item_id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "note": item.note,
                }
                for item in ticket.items
            ],
            status=ticket.status,
            acknowledged_by_id=ticket.acknowledged_by_id,
            acknowledged_at=ticket.acknowledged_at,
            ready_by_id=ticket.ready_by_id,
            ready_at=ticket.ready_at,
            collected_by_id=ticket.collected_by_id,
            collected_at=ticket.collected_at,
            delivered_by_id=ticket.delivered_by_id,
            delivered_at=ticket.delivered_at,
            current_responsibility=ticket.current_responsibility,
            current_responsible_person_id=ticket.current_responsible_person_id,
            next_action=ticket.next_action,
        )


class KitchenContextResponse(BaseModel):
    venue_id: str
    awaiting_acknowledgement_count: int
    tickets: list[KitchenTicketResponse]

    @classmethod
    def from_application(cls, result: KitchenContextResult) -> KitchenContextResponse:
        return cls(
            venue_id=result.venue_id,
            awaiting_acknowledgement_count=result.awaiting_acknowledgement_count,
            tickets=[KitchenTicketResponse.from_application(ticket) for ticket in result.tickets],
        )


class AcknowledgeKitchenTicketResponse(BaseModel):
    request_id: str
    ticket: KitchenTicketResponse

    @classmethod
    def from_application(
        cls, result: AcknowledgeKitchenTicketResult
    ) -> AcknowledgeKitchenTicketResponse:
        return cls(
            request_id=result.request_id,
            ticket=KitchenTicketResponse.from_application(result.ticket),
        )


class SubmitOrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    request_id: str = Field(min_length=1)
    customer_group_id: str = Field(min_length=1)
    items: list[SubmitOrderItemRequest] = Field(min_length=1)


class OrderingContextResponse(BaseModel):
    customer_group_id: str
    venue_id: str
    service_location_id: str
    responsible_waiter_id: str
    status: str
    orders: list[dict[str, object]]
    bill: dict[str, object] | None
    menu_items: list[dict[str, object]]

    @classmethod
    def from_application(cls, result: OrderingContextResult) -> OrderingContextResponse:
        return cls(
            customer_group_id=result.customer_group_id,
            venue_id=result.venue_id,
            service_location_id=result.service_location_id,
            responsible_waiter_id=result.responsible_waiter_id,
            status=result.status,
            orders=[_order_data(order) for order in result.orders],
            bill=_bill_data(result.bill),
            menu_items=[
                {
                    "menu_item_id": item.menu_item_id,
                    "name": item.name,
                    "category_name": item.category_name,
                    "unit_price": item.unit_price,
                    "currency": item.currency,
                    "destination": item.destination,
                }
                for item in result.menu_items
            ],
        )


class SubmitOrderResponse(BaseModel):
    request_id: str
    order: dict[str, object]
    tickets: list[dict[str, object]]
    bill: dict[str, object] | None

    @classmethod
    def from_application(cls, result: SubmitOrderResult) -> SubmitOrderResponse:
        return cls(
            request_id=result.request_id,
            order=_order_data(result.order),
            tickets=[
                {
                    "ticket_id": ticket.ticket_id,
                    "destination": ticket.destination,
                    "item_ids": list(ticket.item_ids),
                }
                for ticket in result.tickets
            ],
            bill=_bill_data(result.bill),
        )


def _order_data(order: OrderDTO) -> dict[str, object]:
    return {
        "order_id": order.order_id,
        "customer_group_id": order.customer_group_id,
        "submitted_at": order.submitted_at,
        "submitted_by_id": order.submitted_by_id,
        "service_location_id": order.service_location_id,
        "responsible_waiter_id": order.responsible_waiter_id,
        "items": [
            {
                "order_item_id": item.order_item_id,
                "menu_item_id": item.menu_item_id,
                "name": item.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "amount": item.amount,
                "currency": item.currency,
                "destination": item.destination,
                "note": item.note,
            }
            for item in order.items
        ],
    }


def _bill_data(bill: BillDTO | None) -> dict[str, object] | None:
    if bill is None:
        return None
    return {
        "bill_id": bill.bill_id,
        "currency": bill.currency,
        "total": bill.total,
        "line_count": bill.line_count,
    }


@router.get("/venue/context", response_model=VenueContextResponse)
def venue_context(
    venue_id: VenueId,
    service: Service,
    identity: Identity,
) -> VenueContextResponse:
    del identity
    return VenueContextResponse.from_application(service.get_context(venue_id=venue_id))


@router.post("/venue/open", response_model=OpenVenueResponse)
def open_venue(
    payload: OpenVenueRequest,
    service: Service,
    identity: Identity,
) -> OpenVenueResponse:
    result = service.open_venue(
        OpenVenueCommand(
            request_id=payload.request_id,
            actor_id=identity.host_id,
            venue_id=payload.venue_id,
        )
    )
    return OpenVenueResponse.from_application(result)


@router.get(
    "/venue/department-readiness/context",
    response_model=DepartmentOwnerContextResponse,
)
def department_readiness_context(
    venue_id: VenueId,
    service: Service,
    identity: DepartmentIdentity,
) -> DepartmentOwnerContextResponse:
    return DepartmentOwnerContextResponse.from_application(
        service.get_department_owner_context(
            actor_id=identity.actor_id,
            venue_id=venue_id,
        )
    )


@router.post(
    "/venue/departments/{department_id}/readiness",
    response_model=DeclareDepartmentReadinessResponse,
)
def declare_department_readiness(
    department_id: str,
    payload: DeclareDepartmentReadinessRequest,
    service: Service,
    identity: DepartmentIdentity,
) -> DeclareDepartmentReadinessResponse:
    return DeclareDepartmentReadinessResponse.from_application(
        service.declare_department_readiness(
            DeclareDepartmentReadinessCommand(
                request_id=payload.request_id,
                actor_id=identity.actor_id,
                venue_id=payload.venue_id,
                department_id=department_id,
                status=payload.status,
                reason=payload.reason,
                comment=payload.comment,
            )
        )
    )


@router.get("/ordering/context", response_model=OrderingContextResponse)
def ordering_context(
    customer_group_id: CustomerGroupId,
    service: OrderingServiceDependency,
    identity: Identity,
) -> OrderingContextResponse:
    del identity
    return OrderingContextResponse.from_application(
        service.get_context(customer_group_id=customer_group_id)
    )


class RunningBillLineResponse(BaseModel):
    bill_line_id: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    currency: str
    source: str
    occurred_at: datetime


class RunningBillResponse(BaseModel):
    bill_id: str
    customer_group_id: str
    currency: str
    total: Decimal
    balance: Decimal
    status: str
    lines: tuple[RunningBillLineResponse, ...]
    version: int

    @classmethod
    def from_application(cls, bill: RunningBillDTO) -> RunningBillResponse:
        return cls(
            bill_id=bill.bill_id,
            customer_group_id=bill.customer_group_id,
            currency=bill.currency,
            total=bill.total,
            balance=bill.balance,
            status=bill.status,
            lines=tuple(
                RunningBillLineResponse(
                    bill_line_id=line.bill_line_id,
                    description=line.description,
                    quantity=line.quantity,
                    unit_price=line.unit_price,
                    amount=line.amount,
                    currency=line.currency,
                    source=line.source,
                    occurred_at=line.occurred_at,
                )
                for line in bill.lines
            ),
            version=bill.version,
        )


@router.get(
    "/billing/customer-groups/{customer_group_id}", response_model=RunningBillResponse | None
)
def running_bill(
    customer_group_id: str,
    service: BillingServiceDependency,
    identity: Identity,
) -> RunningBillResponse | None:
    del identity
    bill = service.get_bill(customer_group_id=customer_group_id)
    return RunningBillResponse.from_application(bill) if bill else None


@router.post("/orders", response_model=SubmitOrderResponse)
def submit_order(
    payload: SubmitOrderRequest,
    service: OrderingServiceDependency,
    identity: Identity,
) -> SubmitOrderResponse:
    result = service.submit_order(
        SubmitOrderCommand(
            request_id=payload.request_id,
            actor_id=identity.host_id,
            customer_group_id=payload.customer_group_id,
            items=tuple(
                SubmitOrderItem(item.menu_item_id, item.quantity, item.note)
                for item in payload.items
            ),
        )
    )
    return SubmitOrderResponse.from_application(result)


@router.get("/kitchen/context", response_model=KitchenContextResponse)
def kitchen_context(
    venue_id: VenueId,
    service: KitchenServiceDependency,
    identity: Identity,
) -> KitchenContextResponse:
    del identity
    return KitchenContextResponse.from_application(service.get_context(venue_id=venue_id))


@router.post(
    "/kitchen/tickets/{ticket_id}/acknowledge",
    response_model=AcknowledgeKitchenTicketResponse,
)
def acknowledge_kitchen_ticket(
    ticket_id: str,
    payload: AcknowledgeKitchenTicketRequest,
    service: KitchenServiceDependency,
    identity: Identity,
) -> AcknowledgeKitchenTicketResponse:
    return AcknowledgeKitchenTicketResponse.from_application(
        service.acknowledge(
            AcknowledgeKitchenTicketCommand(
                request_id=payload.request_id,
                actor_id=identity.host_id,
                ticket_id=ticket_id,
            )
        )
    )


@router.post(
    "/kitchen/tickets/{ticket_id}/{action}", response_model=AcknowledgeKitchenTicketResponse
)
def progress_kitchen_ticket(
    ticket_id: str,
    action: str,
    payload: AcknowledgeKitchenTicketRequest,
    service: KitchenServiceDependency,
    identity: Identity,
) -> AcknowledgeKitchenTicketResponse:
    return AcknowledgeKitchenTicketResponse.from_application(
        service.progress(
            ProgressKitchenTicketCommand(payload.request_id, identity.actor_id, ticket_id, action)
        )
    )


@router.get("/bar/context", response_model=BarContextResponse)
def bar_context(
    venue_id: VenueId, service: BarServiceDependency, identity: Identity
) -> BarContextResponse:
    del identity
    return BarContextResponse.from_application(service.get_context(venue_id=venue_id))


@router.post("/bar/tickets/{ticket_id}/acknowledge", response_model=AcknowledgeBarTicketResponse)
def acknowledge_bar_ticket(
    ticket_id: str,
    payload: AcknowledgeBarTicketRequest,
    service: BarServiceDependency,
    identity: Identity,
) -> AcknowledgeBarTicketResponse:
    return AcknowledgeBarTicketResponse.from_application(
        service.acknowledge(
            AcknowledgeBarTicketCommand(payload.request_id, identity.actor_id, ticket_id)
        )
    )


@router.post("/bar/tickets/{ticket_id}/{action}", response_model=AcknowledgeBarTicketResponse)
def progress_bar_ticket(
    ticket_id: str,
    action: str,
    payload: AcknowledgeBarTicketRequest,
    service: BarServiceDependency,
    identity: Identity,
) -> AcknowledgeBarTicketResponse:
    return AcknowledgeBarTicketResponse.from_application(
        service.progress(
            ProgressBarTicketCommand(payload.request_id, identity.actor_id, ticket_id, action)
        )
    )


def _error(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


def register_error_handlers(app: FastAPI) -> None:
    """Map expected layer failures without leaking internal details."""

    @app.exception_handler(CommandValidationError)
    def command_validation(_: Request, error: CommandValidationError) -> JSONResponse:
        return _error(422, "invalid_command", str(error))

    @app.exception_handler(GuestArrivalValidationError)
    def guest_arrival_validation(_: Request, error: GuestArrivalValidationError) -> JSONResponse:
        return _error(422, "invalid_guest_arrival_command", str(error))

    @app.exception_handler(GuestArrivalAuthorizationError)
    def guest_arrival_denied(_: Request, error: GuestArrivalAuthorizationError) -> JSONResponse:
        return _error(403, "guest_arrival_forbidden", str(error))

    @app.exception_handler(GuestArrivalNotFoundError)
    def guest_arrival_not_found(_: Request, error: GuestArrivalNotFoundError) -> JSONResponse:
        return _error(404, "guest_arrival_context_not_found", str(error))

    @app.exception_handler(GuestArrivalBusinessRuleError)
    def guest_arrival_rejected(_: Request, error: GuestArrivalBusinessRuleError) -> JSONResponse:
        return _error(409, "guest_arrival_rejected", str(error))

    @app.exception_handler(GuestArrivalConcurrencyError)
    def guest_arrival_conflict(_: Request, __: GuestArrivalConcurrencyError) -> JSONResponse:
        return _error(
            409,
            "guest_arrival_conflict",
            "The Service Location changed. Review its current state before continuing.",
        )

    @app.exception_handler(GuestArrivalInfrastructureError)
    def guest_arrival_unavailable(_: Request, __: GuestArrivalInfrastructureError) -> JSONResponse:
        return _error(503, "guest_arrival_unavailable", "Guest Arrival is temporarily unavailable.")

    @app.exception_handler(AuthorizationDeniedError)
    def authorization_denied(_: Request, error: AuthorizationDeniedError) -> JSONResponse:
        return _error(403, "forbidden", str(error))

    @app.exception_handler(VenueNotFoundError)
    def venue_not_found(_: Request, error: VenueNotFoundError) -> JSONResponse:
        return _error(404, "venue_opening_context_not_found", str(error))

    @app.exception_handler(VenueContextMismatchError)
    def context_mismatch(_: Request, __: VenueContextMismatchError) -> JSONResponse:
        return _error(409, "venue_context_conflict", "The Venue context changed.")

    @app.exception_handler(BusinessRuleRejectedError)
    def business_rejected(_: Request, error: BusinessRuleRejectedError) -> JSONResponse:
        return _error(409, "business_rule_rejected", str(error))

    @app.exception_handler(OptimisticConcurrencyError)
    def concurrency_conflict(_: Request, __: OptimisticConcurrencyError) -> JSONResponse:
        return _error(
            409,
            "optimistic_concurrency_conflict",
            "The Venue changed. Review the current opening state and try again.",
        )

    @app.exception_handler(BusinessDatePolicyNotFoundError)
    def business_date_unavailable(
        _: Request,
        __: BusinessDatePolicyNotFoundError,
    ) -> JSONResponse:
        return _error(
            503,
            "business_date_unavailable",
            "The current Business Date cannot be confirmed.",
        )

    @app.exception_handler(ConfigurationError)
    @app.exception_handler(InfrastructureError)
    def service_unavailable(_: Request, __: Exception) -> JSONResponse:
        return _error(503, "service_unavailable", "Venue Opening is temporarily unavailable.")

    @app.exception_handler(OrderingCommandValidationError)
    def ordering_validation(_: Request, error: OrderingCommandValidationError) -> JSONResponse:
        return _error(422, "invalid_order", str(error))

    @app.exception_handler(OrderingAuthorizationDeniedError)
    def ordering_denied(_: Request, error: OrderingAuthorizationDeniedError) -> JSONResponse:
        return _error(403, "ordering_forbidden", str(error))

    @app.exception_handler(CustomerGroupNotFoundError)
    def customer_group_not_found(_: Request, error: CustomerGroupNotFoundError) -> JSONResponse:
        return _error(404, "customer_group_not_found", str(error))

    @app.exception_handler(OrderingBusinessRuleRejectedError)
    def ordering_rejected(_: Request, error: OrderingBusinessRuleRejectedError) -> JSONResponse:
        return _error(409, "order_rejected", str(error))

    @app.exception_handler(OrderingConcurrencyError)
    def ordering_conflict(_: Request, __: OrderingConcurrencyError) -> JSONResponse:
        return _error(
            409,
            "ordering_concurrency_conflict",
            "The Customer Group changed. Review the current Order state.",
        )

    @app.exception_handler(OrderingInfrastructureError)
    def ordering_unavailable(_: Request, __: OrderingInfrastructureError) -> JSONResponse:
        return _error(503, "ordering_unavailable", "Ordering is temporarily unavailable.")

    @app.exception_handler(KitchenCommandValidationError)
    def kitchen_validation(_: Request, error: KitchenCommandValidationError) -> JSONResponse:
        return _error(422, "invalid_kitchen_command", str(error))

    @app.exception_handler(KitchenAuthorizationDeniedError)
    def kitchen_denied(_: Request, error: KitchenAuthorizationDeniedError) -> JSONResponse:
        return _error(403, "kitchen_forbidden", str(error))

    @app.exception_handler(KitchenTicketNotFoundError)
    def kitchen_ticket_missing(_: Request, error: KitchenTicketNotFoundError) -> JSONResponse:
        return _error(404, "kitchen_ticket_not_found", str(error))

    @app.exception_handler(KitchenBusinessRuleRejectedError)
    def kitchen_rejected(_: Request, error: KitchenBusinessRuleRejectedError) -> JSONResponse:
        return _error(409, "kitchen_action_rejected", str(error))

    @app.exception_handler(KitchenConcurrencyError)
    def kitchen_conflict(_: Request, __: KitchenConcurrencyError) -> JSONResponse:
        return _error(
            409,
            "kitchen_concurrency_conflict",
            "The Kitchen Ticket changed. Review its current acknowledgement.",
        )

    @app.exception_handler(KitchenInfrastructureError)
    def kitchen_unavailable(_: Request, __: KitchenInfrastructureError) -> JSONResponse:
        return _error(
            503,
            "kitchen_unavailable",
            "Kitchen Operations is temporarily unavailable.",
        )

    @app.exception_handler(BarCommandValidationError)
    def bar_validation(_: Request, error: BarCommandValidationError) -> JSONResponse:
        return _error(422, "invalid_bar_command", str(error))

    @app.exception_handler(BarAuthorizationDeniedError)
    def bar_denied(_: Request, error: BarAuthorizationDeniedError) -> JSONResponse:
        return _error(403, "bar_forbidden", str(error))

    @app.exception_handler(BarTicketNotFoundError)
    def bar_missing(_: Request, error: BarTicketNotFoundError) -> JSONResponse:
        return _error(404, "bar_ticket_not_found", str(error))

    @app.exception_handler(BarBusinessRuleRejectedError)
    def bar_rejected(_: Request, error: BarBusinessRuleRejectedError) -> JSONResponse:
        return _error(409, "bar_action_rejected", str(error))

    @app.exception_handler(BarConcurrencyError)
    def bar_conflict(_: Request, __: BarConcurrencyError) -> JSONResponse:
        return _error(
            409,
            "bar_concurrency_conflict",
            "The Bar Ticket changed. Review its current acknowledgement.",
        )

    @app.exception_handler(BarInfrastructureError)
    def bar_unavailable(_: Request, __: BarInfrastructureError) -> JSONResponse:
        return _error(503, "bar_unavailable", "Bar Operations is temporarily unavailable.")
