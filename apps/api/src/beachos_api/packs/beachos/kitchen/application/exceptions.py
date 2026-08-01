"""Kitchen Application failures."""


class KitchenCommandValidationError(ValueError):
    pass


class KitchenTicketNotFoundError(LookupError):
    pass


class KitchenAuthorizationDeniedError(PermissionError):
    pass


class KitchenBusinessRuleRejectedError(RuntimeError):
    pass
