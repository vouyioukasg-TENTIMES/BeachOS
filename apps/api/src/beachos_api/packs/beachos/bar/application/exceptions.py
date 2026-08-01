"""Bar Application failures."""


class BarApplicationError(RuntimeError):
    pass


class BarAuthorizationDeniedError(BarApplicationError):
    pass


class BarBusinessRuleRejectedError(BarApplicationError):
    pass


class BarCommandValidationError(BarApplicationError):
    pass


class BarTicketNotFoundError(BarApplicationError):
    pass
