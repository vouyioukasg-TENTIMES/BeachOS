"""Infrastructure failure categories for Venue Opening."""


class InfrastructureError(RuntimeError):
    """Base class for expected Infrastructure adapter failures."""


class OptimisticConcurrencyError(InfrastructureError):
    """The stored aggregate changed after it was loaded."""


class AggregateNotLoadedError(InfrastructureError):
    """An existing aggregate was saved without first being loaded."""


class BusinessDatePolicyNotFoundError(InfrastructureError):
    """No approved Business Date policy exists for the Venue."""


class MigrationChecksumError(InfrastructureError):
    """An already-applied migration differs from the committed migration."""
