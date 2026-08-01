"""Application-level failure categories for Venue Opening."""


class ApplicationError(Exception):
    """Base class for expected Application Layer failures."""


class CommandValidationError(ApplicationError):
    """A Command is structurally incomplete or malformed."""


class AuthorizationDeniedError(ApplicationError):
    """The actor lacks an authority required to attempt the Command."""


class VenueNotFoundError(ApplicationError):
    """No Venue aggregate exists for the requested opening context."""


class VenueContextMismatchError(ApplicationError):
    """A repository returned a Venue outside the requested context."""


class BusinessRuleRejectedError(ApplicationError):
    """The Domain rejected the requested business action."""
