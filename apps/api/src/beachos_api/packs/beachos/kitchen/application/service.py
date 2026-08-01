"""Application orchestration for Kitchen Operations."""

from beachos_api.packs.beachos.kitchen.application.commands import (
    AcknowledgeKitchenTicketCommand,
    ProgressKitchenTicketCommand,
)
from beachos_api.packs.beachos.kitchen.application.dtos import (
    AcknowledgeKitchenTicketResult,
    KitchenContextResult,
    KitchenTicketDTO,
)
from beachos_api.packs.beachos.kitchen.application.exceptions import (
    KitchenAuthorizationDeniedError,
    KitchenBusinessRuleRejectedError,
    KitchenTicketNotFoundError,
)
from beachos_api.packs.beachos.kitchen.application.ports import (
    Clock,
    KitchenCapabilityVerifier,
    KitchenUnitOfWorkFactory,
)
from beachos_api.packs.beachos.kitchen.domain import KitchenError


class KitchenService:
    def __init__(
        self,
        *,
        capabilities: KitchenCapabilityVerifier,
        clock: Clock,
        unit_of_work_factory: KitchenUnitOfWorkFactory,
    ) -> None:
        self._capabilities = capabilities
        self._clock = clock
        self._unit_of_work_factory = unit_of_work_factory

    def get_context(self, *, venue_id: str) -> KitchenContextResult:
        with self._unit_of_work_factory.create() as unit_of_work:
            tickets = unit_of_work.tickets.list_for_venue(venue_id=venue_id)
            return KitchenContextResult(
                venue_id=venue_id,
                tickets=tuple(KitchenTicketDTO.from_domain(ticket) for ticket in tickets),
            )

    def acknowledge(
        self, command: AcknowledgeKitchenTicketCommand
    ) -> AcknowledgeKitchenTicketResult:
        with self._unit_of_work_factory.create() as unit_of_work:
            prior = unit_of_work.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.ticket.ticket_id != command.ticket_id:
                    raise KitchenBusinessRuleRejectedError(
                        "request id was already used for another Kitchen Ticket"
                    )
                return prior
            ticket = unit_of_work.tickets.get(ticket_id=command.ticket_id)
            if ticket is None:
                raise KitchenTicketNotFoundError("Kitchen Ticket was not found")
            if not self._capabilities.can_acknowledge_kitchen_ticket(
                actor_id=command.actor_id,
                venue_id=ticket.venue_id,
                ticket_id=ticket.ticket_id,
            ):
                raise KitchenAuthorizationDeniedError(
                    "Staff Member lacks authority to acknowledge this Kitchen Ticket"
                )
            try:
                ticket.acknowledge(
                    actor_id=command.actor_id,
                    acknowledged_at=self._clock.now(),
                )
            except KitchenError as error:
                raise KitchenBusinessRuleRejectedError(str(error)) from error
            result = AcknowledgeKitchenTicketResult(
                request_id=command.request_id,
                ticket=KitchenTicketDTO.from_domain(ticket),
            )
            unit_of_work.tickets.save(ticket)
            unit_of_work.receipts.save(request_id=command.request_id, result=result)
            unit_of_work.commit()
            return result

    def progress(self, command: ProgressKitchenTicketCommand) -> AcknowledgeKitchenTicketResult:
        expected = {"MARK_READY": "READY", "COLLECT": "COLLECTED", "DELIVER": "DELIVERED"}[
            command.action
        ]
        with self._unit_of_work_factory.create() as unit:
            prior = unit.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.ticket.ticket_id != command.ticket_id or prior.ticket.status != expected:
                    raise KitchenBusinessRuleRejectedError(
                        "request id was already used for another Kitchen action"
                    )
                return prior
            ticket = unit.tickets.get(ticket_id=command.ticket_id)
            if ticket is None:
                raise KitchenTicketNotFoundError("Kitchen Ticket was not found")
            if command.action == "MARK_READY":
                allowed = self._capabilities.can_mark_kitchen_ticket_ready(
                    actor_id=command.actor_id, venue_id=ticket.venue_id, ticket_id=ticket.ticket_id
                )
            elif command.action == "COLLECT":
                allowed = self._capabilities.can_collect_ticket(
                    actor_id=command.actor_id,
                    venue_id=ticket.venue_id,
                    responsible_service_staff_id=ticket.responsible_service_staff_id,
                )
            else:
                allowed = self._capabilities.can_deliver_ticket(
                    actor_id=command.actor_id,
                    venue_id=ticket.venue_id,
                    responsible_service_staff_id=ticket.responsible_service_staff_id,
                )
            if not allowed:
                raise KitchenAuthorizationDeniedError(
                    "Staff Member lacks authority for this Kitchen fulfilment action"
                )
            try:
                now = self._clock.now()
                if command.action == "MARK_READY":
                    ticket.mark_ready(actor_id=command.actor_id, confirmed_at=now)
                elif command.action == "COLLECT":
                    ticket.collect(actor_id=command.actor_id, collected_at=now)
                else:
                    ticket.deliver(actor_id=command.actor_id, delivered_at=now)
            except KitchenError as error:
                raise KitchenBusinessRuleRejectedError(str(error)) from error
            result = AcknowledgeKitchenTicketResult(
                command.request_id, KitchenTicketDTO.from_domain(ticket)
            )
            unit.tickets.save(ticket)
            unit.receipts.save(request_id=command.request_id, result=result)
            unit.commit()
            return result
