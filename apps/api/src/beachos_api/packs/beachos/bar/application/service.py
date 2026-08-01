"""Application orchestration for Bar Operations."""

from beachos_api.packs.beachos.bar.domain import BarError

from .commands import AcknowledgeBarTicketCommand, ProgressBarTicketCommand
from .dtos import AcknowledgeBarTicketResult, BarContextResult, BarTicketDTO
from .exceptions import (
    BarAuthorizationDeniedError,
    BarBusinessRuleRejectedError,
    BarTicketNotFoundError,
)
from .ports import BarCapabilityVerifier, BarUnitOfWorkFactory, Clock


class BarService:
    def __init__(
        self,
        *,
        capabilities: BarCapabilityVerifier,
        clock: Clock,
        unit_of_work_factory: BarUnitOfWorkFactory,
    ) -> None:
        self._capabilities = capabilities
        self._clock = clock
        self._unit_of_work_factory = unit_of_work_factory

    def get_context(self, *, venue_id: str) -> BarContextResult:
        with self._unit_of_work_factory.create() as uow:
            return BarContextResult(
                venue_id,
                tuple(
                    BarTicketDTO.from_domain(t)
                    for t in uow.tickets.list_for_venue(venue_id=venue_id)
                ),
            )

    def acknowledge(self, command: AcknowledgeBarTicketCommand) -> AcknowledgeBarTicketResult:
        with self._unit_of_work_factory.create() as uow:
            prior = uow.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.ticket.ticket_id != command.ticket_id:
                    raise BarBusinessRuleRejectedError(
                        "request id was already used for another Bar Ticket"
                    )
                return prior
            ticket = uow.tickets.get(ticket_id=command.ticket_id)
            if ticket is None:
                raise BarTicketNotFoundError("Bar Ticket was not found")
            if not self._capabilities.can_acknowledge_bar_ticket(
                actor_id=command.actor_id, venue_id=ticket.venue_id, ticket_id=ticket.ticket_id
            ):
                raise BarAuthorizationDeniedError(
                    "Staff Member lacks authority to acknowledge this Bar Ticket"
                )
            try:
                ticket.acknowledge(actor_id=command.actor_id, acknowledged_at=self._clock.now())
            except BarError as error:
                raise BarBusinessRuleRejectedError(str(error)) from error
            result = AcknowledgeBarTicketResult(
                command.request_id, BarTicketDTO.from_domain(ticket)
            )
            uow.tickets.save(ticket)
            uow.receipts.save(request_id=command.request_id, result=result)
            uow.commit()
            return result

    def progress(self, command: ProgressBarTicketCommand) -> AcknowledgeBarTicketResult:
        expected = {"MARK_READY": "READY", "COLLECT": "COLLECTED", "DELIVER": "DELIVERED"}[
            command.action
        ]
        with self._unit_of_work_factory.create() as uow:
            prior = uow.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.ticket.ticket_id != command.ticket_id or prior.ticket.status != expected:
                    raise BarBusinessRuleRejectedError(
                        "request id was already used for another Bar action"
                    )
                return prior
            ticket = uow.tickets.get(ticket_id=command.ticket_id)
            if ticket is None:
                raise BarTicketNotFoundError("Bar Ticket was not found")
            if command.action == "MARK_READY":
                allowed = self._capabilities.can_mark_bar_ticket_ready(
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
                raise BarAuthorizationDeniedError(
                    "Staff Member lacks authority for this Bar fulfilment action"
                )
            try:
                now = self._clock.now()
                if command.action == "MARK_READY":
                    ticket.mark_ready(actor_id=command.actor_id, confirmed_at=now)
                elif command.action == "COLLECT":
                    ticket.collect(actor_id=command.actor_id, collected_at=now)
                else:
                    ticket.deliver(actor_id=command.actor_id, delivered_at=now)
            except BarError as error:
                raise BarBusinessRuleRejectedError(str(error)) from error
            result = AcknowledgeBarTicketResult(
                command.request_id, BarTicketDTO.from_domain(ticket)
            )
            uow.tickets.save(ticket)
            uow.receipts.save(request_id=command.request_id, result=result)
            uow.commit()
            return result
