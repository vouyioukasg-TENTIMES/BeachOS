"""Guest Arrival Application orchestration."""

from beachos_api.packs.beachos.guest_arrival.application.commands import OpenCustomerGroupCommand
from beachos_api.packs.beachos.guest_arrival.application.dtos import (
    ActivityLogRecord,
    CustomerGroupDTO,
    GuestArrivalContextResult,
    OpenCustomerGroupResult,
    ServiceLocationDTO,
)
from beachos_api.packs.beachos.guest_arrival.application.exceptions import (
    GuestArrivalAuthorizationError,
    GuestArrivalBusinessRuleError,
    GuestArrivalNotFoundError,
)
from beachos_api.packs.beachos.guest_arrival.application.ports import (
    Clock,
    GuestArrivalAuthority,
    GuestArrivalUnitOfWorkFactory,
    IdentityGenerator,
    VenueOpeningReader,
)
from beachos_api.packs.beachos.guest_arrival.domain import GuestArrivalError, ServiceLocationType


class GuestArrivalService:
    def __init__(
        self,
        *,
        authority: GuestArrivalAuthority,
        clock: Clock,
        identities: IdentityGenerator,
        venue_opening: VenueOpeningReader,
        unit_of_work_factory: GuestArrivalUnitOfWorkFactory,
    ) -> None:
        self._authority = authority
        self._clock = clock
        self._identities = identities
        self._venue_opening = venue_opening
        self._unit_of_work_factory = unit_of_work_factory

    def get_context(self, *, actor_id: str, venue_id: str) -> GuestArrivalContextResult:
        if not self._authority.can_view_arrival(actor_id=actor_id, venue_id=venue_id):
            raise GuestArrivalAuthorizationError("Staff Member cannot view Guest Arrival")
        opening = self._venue_opening.current(venue_id=venue_id)
        if opening is None:
            raise GuestArrivalNotFoundError("Venue context was not found")
        venue_name, business_date, is_open = opening
        with self._unit_of_work_factory.create() as unit:
            locations = unit.locations.list_for_venue(venue_id=venue_id)
        return GuestArrivalContextResult(
            venue_id,
            venue_name,
            business_date,
            is_open,
            "CONFIRMED" if is_open else "INSUFFICIENT",
            tuple(ServiceLocationDTO.from_domain(item) for item in locations),
        )

    def identify(
        self, *, actor_id: str, venue_id: str, digital_identity: str
    ) -> ServiceLocationDTO:
        if not self._authority.can_view_arrival(actor_id=actor_id, venue_id=venue_id):
            raise GuestArrivalAuthorizationError("Staff Member cannot identify Service Locations")
        with self._unit_of_work_factory.create() as unit:
            location = unit.locations.get_by_digital_identity(
                venue_id=venue_id, digital_identity=digital_identity.strip()
            )
            if location is None:
                raise GuestArrivalNotFoundError("Service Location was not found")
            return ServiceLocationDTO.from_domain(location)

    def open_customer_group(self, command: OpenCustomerGroupCommand) -> OpenCustomerGroupResult:
        with self._unit_of_work_factory.create() as unit:
            prior = unit.receipts.get(request_id=command.request_id)
            if prior is not None:
                if prior.customer_group.service_location_id != command.service_location_id:
                    raise GuestArrivalBusinessRuleError(
                        "request id was already used for another Service Location"
                    )
                return prior
            location = unit.locations.get(service_location_id=command.service_location_id)
            if location is None or location.venue_id != command.venue_id:
                raise GuestArrivalNotFoundError("Service Location was not found")
            if not self._authority.can_open_customer_group(
                actor_id=command.actor_id, venue_id=command.venue_id
            ):
                raise GuestArrivalAuthorizationError("Staff Member cannot open a Customer Group")
            opening = self._venue_opening.current(venue_id=command.venue_id)
            venue_is_open = opening is not None and opening[2]
            is_beach = location.location_type is ServiceLocationType.BEACH_SUNBED
            moment = self._clock.now()
            try:
                group = location.open_customer_group(
                    customer_group_id=self._identities.new_id("customer-group"),
                    responsible_waiter_id=command.actor_id,
                    opened_by_id=command.actor_id,
                    opened_at=moment,
                    venue_is_open=venue_is_open,
                    waiter_is_eligible=self._authority.is_eligible_responsible_waiter(
                        actor_id=command.actor_id, venue_id=command.venue_id
                    ),
                    waiter_has_capability=True,
                    waiter_accepts_responsibility=command.waiter_accepts_responsibility,
                    physical_context_confirmed=command.physical_context_confirmed,
                    opening_charge_confirmed=command.opening_charge_confirmed,
                    obligation_id=self._identities.new_id("financial-obligation")
                    if is_beach
                    else None,
                    bill_id=self._identities.new_id("bill") if is_beach else None,
                    bill_line_id=self._identities.new_id("bill-line") if is_beach else None,
                )
            except GuestArrivalError as error:
                raise GuestArrivalBusinessRuleError(str(error)) from error
            result = OpenCustomerGroupResult(
                command.request_id,
                CustomerGroupDTO.from_domain(group),
                ServiceLocationDTO.from_domain(location),
            )
            unit.locations.save(location)
            unit.ordering.provision(location)
            unit.activity_log.record_customer_group_opened(
                ActivityLogRecord(
                    command.request_id,
                    command.actor_id,
                    command.venue_id,
                    location.service_location_id,
                    group.customer_group_id,
                    moment,
                )
            )
            unit.receipts.save(request_id=command.request_id, result=result)
            unit.commit()
            return result
