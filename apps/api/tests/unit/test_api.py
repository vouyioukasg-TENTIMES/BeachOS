"""Delivery composition and error-translation tests."""

from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from beachos_api.composition import venue_opening_service
from beachos_api.identity import FakeIdentityProvider, FakeVenueOpeningAuthority
from beachos_api.main import create_app
from beachos_api.packs.beachos.venue_opening.application.commands import OpenVenueCommand
from beachos_api.packs.beachos.venue_opening.application.dtos import OpenVenueResult
from beachos_api.packs.beachos.venue_opening.application.exceptions import (
    AuthorizationDeniedError,
    CommandValidationError,
    VenueContextMismatchError,
    VenueNotFoundError,
)
from beachos_api.packs.beachos.venue_opening.infrastructure.errors import (
    BusinessDatePolicyNotFoundError,
    InfrastructureError,
)


class FailingService:
    def __init__(self, error: Exception) -> None:
        self._error = error

    def open_venue(self, command: OpenVenueCommand) -> OpenVenueResult:
        del command
        raise self._error


@pytest.mark.parametrize(
    ("error_factory", "status", "code"),
    [
        (lambda: CommandValidationError("invalid"), 422, "invalid_command"),
        (lambda: AuthorizationDeniedError("denied"), 403, "forbidden"),
        (lambda: VenueNotFoundError("missing"), 404, "venue_opening_context_not_found"),
        (lambda: VenueContextMismatchError("changed"), 409, "venue_context_conflict"),
        (
            lambda: BusinessDatePolicyNotFoundError("missing"),
            503,
            "business_date_unavailable",
        ),
        (lambda: InfrastructureError("database detail"), 503, "service_unavailable"),
    ],
)
def test_expected_failures_have_stable_http_mappings(
    error_factory: Callable[[], Exception],
    status: int,
    code: str,
) -> None:
    application = create_app()
    application.dependency_overrides[venue_opening_service] = lambda: FailingService(
        error_factory()
    )

    response = TestClient(application).post(
        "/venue/open",
        json={"request_id": "request-1", "venue_id": "venue-1"},
    )

    assert response.status_code == status
    assert response.json()["error"]["code"] == code
    assert "database detail" not in response.text


def test_missing_database_configuration_is_service_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("BEACHOS_DATABASE_URL", raising=False)

    response = TestClient(create_app()).post(
        "/venue/open",
        json={"request_id": "request-1", "venue_id": "venue-1"},
    )

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "service_unavailable"


def test_composition_builds_service_when_database_is_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BEACHOS_DATABASE_URL", "postgresql://example.invalid/beachos")

    service = venue_opening_service()

    assert service.__class__.__name__ == "VenueOpeningService"


def test_fake_identity_separates_host_and_department_owner_authority() -> None:
    identities = FakeIdentityProvider()
    authority = FakeVenueOpeningAuthority(identities)

    assert authority.can_declare_department_readiness(
        actor_id="staff-kitchen",
        venue_id="venue-1",
        department_id="kitchen",
    )
    assert not authority.can_declare_department_readiness(
        actor_id="development-host",
        venue_id="venue-1",
        department_id="kitchen",
    )
    assert authority.can_open_venue(actor_id="development-host", venue_id="venue-1")
    assert not authority.can_open_venue(actor_id="another-host", venue_id="venue-1")
    assert authority.is_responsible_host(actor_id="development-host", venue_id="venue-1")
    assert identities.identity_for(" ").actor_id == "development-host"
    assert identities.identity_for(" staff-bar ").actor_id == "staff-bar"
