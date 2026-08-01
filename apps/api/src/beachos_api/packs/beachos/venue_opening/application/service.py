"""Application orchestration for approved Venue Opening Commands."""

from beachos_api.packs.beachos.venue_opening.application.commands import (
    DeclareDepartmentReadinessCommand,
    OpenVenueCommand,
)
from beachos_api.packs.beachos.venue_opening.application.dtos import (
    ActivityLogRecord,
    DeclareDepartmentReadinessResult,
    DepartmentOwnerContextResult,
    DepartmentReadinessDTO,
    OpeningReportDTO,
    OpenVenueResult,
    VenueContextResult,
)
from beachos_api.packs.beachos.venue_opening.application.exceptions import (
    AuthorizationDeniedError,
    BusinessRuleRejectedError,
    VenueContextMismatchError,
    VenueNotFoundError,
)
from beachos_api.packs.beachos.venue_opening.application.ports import (
    BusinessDateProvider,
    CapabilityVerifier,
    Clock,
    HostResponsibilityVerifier,
    VenueOpeningUnitOfWork,
    VenueOpeningUnitOfWorkFactory,
)
from beachos_api.packs.beachos.venue_opening.domain import (
    BusinessDate,
    Venue,
    VenueOpeningError,
    VenueOpeningPolicy,
)


class VenueOpeningService:
    """Coordinates Venue Opening without deciding business rules."""

    def __init__(
        self,
        *,
        capabilities: CapabilityVerifier,
        host_responsibilities: HostResponsibilityVerifier,
        business_dates: BusinessDateProvider,
        clock: Clock,
        unit_of_work_factory: VenueOpeningUnitOfWorkFactory,
        policy: VenueOpeningPolicy,
    ) -> None:
        self._capabilities = capabilities
        self._host_responsibilities = host_responsibilities
        self._business_dates = business_dates
        self._clock = clock
        self._unit_of_work_factory = unit_of_work_factory
        self._policy = policy

    def declare_department_readiness(
        self,
        command: DeclareDepartmentReadinessCommand,
    ) -> DeclareDepartmentReadinessResult:
        business_date = self._business_dates.current_for(venue_id=command.venue_id)
        if not self._capabilities.can_declare_department_readiness(
            actor_id=command.actor_id,
            venue_id=command.venue_id,
            department_id=command.department_id,
        ):
            raise AuthorizationDeniedError("actor lacks authority to declare department readiness")

        with self._unit_of_work_factory.create() as unit_of_work:
            venue = self._load_venue(
                unit_of_work=unit_of_work,
                venue_id=command.venue_id,
                business_date=business_date,
            )
            try:
                declaration = venue.declare_department_readiness(
                    department_id=command.department_id,
                    declared_by_id=command.actor_id,
                    status=command.status,
                    declared_at=self._clock.now(),
                    reason=command.reason,
                    comment=command.comment,
                )
            except VenueOpeningError as error:
                raise BusinessRuleRejectedError(str(error)) from error

            unit_of_work.venues.save(venue)
            unit_of_work.commit()

        return DeclareDepartmentReadinessResult(
            request_id=command.request_id,
            venue_id=venue.venue_id,
            business_date=venue.business_date.value,
            declaration=DepartmentReadinessDTO.from_domain(declaration),
        )

    def open_venue(self, command: OpenVenueCommand) -> OpenVenueResult:
        business_date = self._business_dates.current_for(venue_id=command.venue_id)
        has_capability = self._capabilities.can_open_venue(
            actor_id=command.actor_id,
            venue_id=command.venue_id,
        )
        if not has_capability:
            raise AuthorizationDeniedError("actor lacks authority to open the Venue")

        host_is_responsible = self._host_responsibilities.is_responsible_host(
            actor_id=command.actor_id,
            venue_id=command.venue_id,
        )

        with self._unit_of_work_factory.create() as unit_of_work:
            venue = self._load_venue(
                unit_of_work=unit_of_work,
                venue_id=command.venue_id,
                business_date=business_date,
            )
            opened_at = self._clock.now()
            try:
                report = venue.open_for_business_date(
                    host_id=command.actor_id,
                    host_is_responsible=host_is_responsible,
                    host_has_required_capability=has_capability,
                    opened_at=opened_at,
                    policy=self._policy,
                )
            except VenueOpeningError as error:
                raise BusinessRuleRejectedError(str(error)) from error

            unit_of_work.venues.save(venue)
            unit_of_work.activity_log.record_venue_opened(
                ActivityLogRecord(
                    request_id=command.request_id,
                    actor_id=command.actor_id,
                    venue_id=venue.venue_id,
                    business_date=venue.business_date.value,
                    occurred_at=opened_at,
                )
            )
            unit_of_work.commit()

        return OpenVenueResult(
            request_id=command.request_id,
            report=OpeningReportDTO.from_domain(report),
        )

    def get_context(self, *, venue_id: str) -> VenueContextResult:
        """Return authoritative current context without mutating the aggregate."""

        business_date = self._business_dates.current_for(venue_id=venue_id)
        with self._unit_of_work_factory.create() as unit_of_work:
            venue = self._load_venue(
                unit_of_work=unit_of_work,
                venue_id=venue_id,
                business_date=business_date,
            )
            return VenueContextResult.from_domain(venue)

    def get_department_owner_context(
        self,
        *,
        actor_id: str,
        venue_id: str,
    ) -> DepartmentOwnerContextResult:
        """Return only the opening departments assigned to the current actor."""

        business_date = self._business_dates.current_for(venue_id=venue_id)
        with self._unit_of_work_factory.create() as unit_of_work:
            venue = self._load_venue(
                unit_of_work=unit_of_work,
                venue_id=venue_id,
                business_date=business_date,
            )
            result = DepartmentOwnerContextResult.from_domain(venue, actor_id=actor_id)
            if not result.departments or any(
                not self._capabilities.can_declare_department_readiness(
                    actor_id=actor_id,
                    venue_id=venue_id,
                    department_id=department.department_id,
                )
                for department in result.departments
            ):
                raise AuthorizationDeniedError(
                    "actor is not a configured department owner for this Venue"
                )
            return result

    @staticmethod
    def _load_venue(
        *,
        unit_of_work: VenueOpeningUnitOfWork,
        venue_id: str,
        business_date: BusinessDate,
    ) -> Venue:
        venue = unit_of_work.venues.get(
            venue_id=venue_id,
            business_date=business_date,
        )
        if venue is None:
            raise VenueNotFoundError("Venue opening context was not found")
        if venue.venue_id != venue_id or venue.business_date != business_date:
            raise VenueContextMismatchError(
                "repository returned a Venue outside the requested opening context"
            )
        return venue
