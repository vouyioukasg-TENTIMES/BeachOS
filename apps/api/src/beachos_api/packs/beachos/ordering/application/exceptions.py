"""Ordering Application failures."""


class OrderingApplicationError(RuntimeError):
    pass


class OrderingCommandValidationError(OrderingApplicationError):
    pass


class OrderingAuthorizationDeniedError(OrderingApplicationError):
    pass


class OrderingBusinessRuleRejectedError(OrderingApplicationError):
    pass


class CustomerGroupNotFoundError(OrderingApplicationError):
    pass
