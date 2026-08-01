"""Application orchestration for Ordering."""

from beachos_api.packs.beachos.ordering.application.commands import SubmitOrderCommand
from beachos_api.packs.beachos.ordering.application.dtos import (
    BillDTO,
    OrderDTO,
    OrderingContextResult,
    SubmitOrderResult,
    TicketDTO,
)
from beachos_api.packs.beachos.ordering.application.exceptions import (
    CustomerGroupNotFoundError,
    OrderingAuthorizationDeniedError,
    OrderingBusinessRuleRejectedError,
)
from beachos_api.packs.beachos.ordering.application.ports import (
    Clock,
    IdentityGenerator,
    OrderingCapabilityVerifier,
    OrderingUnitOfWorkFactory,
)
from beachos_api.packs.beachos.ordering.domain import (
    Destination,
    DraftOrderItem,
    OrderingError,
)


class OrderingService:
    def __init__(
        self,
        *,
        capabilities: OrderingCapabilityVerifier,
        clock: Clock,
        identities: IdentityGenerator,
        unit_of_work_factory: OrderingUnitOfWorkFactory,
    ) -> None:
        self._capabilities = capabilities
        self._clock = clock
        self._identities = identities
        self._unit_of_work_factory = unit_of_work_factory

    def get_context(self, *, customer_group_id: str) -> OrderingContextResult:
        with self._unit_of_work_factory.create() as unit_of_work:
            group = unit_of_work.customer_groups.get(customer_group_id=customer_group_id)
            if group is None:
                raise CustomerGroupNotFoundError("Customer Group was not found")
            menu_items = unit_of_work.menus.available_for_venue(venue_id=group.venue_id)
            return OrderingContextResult.from_domain(group, menu_items)

    def submit_order(self, command: SubmitOrderCommand) -> SubmitOrderResult:
        with self._unit_of_work_factory.create() as unit_of_work:
            prior = unit_of_work.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.order.customer_group_id != command.customer_group_id:
                    raise OrderingBusinessRuleRejectedError(
                        "request id was already used for another Customer Group"
                    )
                return prior

            group = unit_of_work.customer_groups.get(customer_group_id=command.customer_group_id)
            if group is None:
                raise CustomerGroupNotFoundError("Customer Group was not found")
            if not self._capabilities.can_submit_order(
                actor_id=command.actor_id,
                venue_id=group.venue_id,
                customer_group_id=group.customer_group_id,
            ):
                raise OrderingAuthorizationDeniedError(
                    "Staff Member lacks authority to submit this Order"
                )

            menu = {
                item.menu_item_id: item
                for item in unit_of_work.menus.available_for_venue(venue_id=group.venue_id)
            }
            draft_items: list[DraftOrderItem] = []
            for command_item in command.items:
                menu_item = menu.get(command_item.menu_item_id)
                if menu_item is None:
                    raise OrderingBusinessRuleRejectedError(
                        f"Menu Item {command_item.menu_item_id} is not currently available"
                    )
                try:
                    draft_items.append(
                        DraftOrderItem(
                            order_item_id=self._identities.new_id("order-item"),
                            menu_item=menu_item,
                            quantity=command_item.quantity,
                            note=command_item.note,
                        )
                    )
                except OrderingError as error:
                    raise OrderingBusinessRuleRejectedError(str(error)) from error

            has_kitchen = any(
                item.menu_item.destination is Destination.KITCHEN for item in draft_items
            )
            has_bar = any(item.menu_item.destination is Destination.BAR for item in draft_items)
            positive_count = sum(item.menu_item.price.amount > 0 for item in draft_items)
            previous_kitchen_count = len(group.kitchen_tickets)
            previous_bar_count = len(group.bar_tickets)
            try:
                order = group.submit_order(
                    order_id=self._identities.new_id("order"),
                    submitted_by_id=command.actor_id,
                    submitted_at=self._clock.now(),
                    draft_items=tuple(draft_items),
                    kitchen_ticket_id=(
                        self._identities.new_id("kitchen-ticket") if has_kitchen else None
                    ),
                    bar_ticket_id=self._identities.new_id("bar-ticket") if has_bar else None,
                    bill_id=(
                        group.bill.bill_id
                        if group.bill
                        else self._identities.new_id("bill")
                        if positive_count
                        else ""
                    ),
                    obligation_ids=tuple(
                        self._identities.new_id("financial-obligation")
                        for _ in range(positive_count)
                    ),
                    bill_line_ids=tuple(
                        self._identities.new_id("bill-line") for _ in range(positive_count)
                    ),
                )
            except OrderingError as error:
                raise OrderingBusinessRuleRejectedError(str(error)) from error

            tickets = tuple(
                TicketDTO.from_kitchen(ticket)
                for ticket in group.kitchen_tickets[previous_kitchen_count:]
            ) + tuple(
                TicketDTO.from_bar(ticket) for ticket in group.bar_tickets[previous_bar_count:]
            )
            result = SubmitOrderResult(
                request_id=command.request_id,
                order=OrderDTO.from_domain(order),
                tickets=tickets,
                bill=BillDTO.from_domain(group.bill) if group.bill else None,
            )
            unit_of_work.customer_groups.save(group)
            unit_of_work.receipts.save(request_id=command.request_id, result=result)
            unit_of_work.commit()
            return result
