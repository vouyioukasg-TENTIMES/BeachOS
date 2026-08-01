"""Guest Arrival Application failures."""


class GuestArrivalApplicationError(Exception):
    pass


class GuestArrivalValidationError(GuestArrivalApplicationError):
    pass


class GuestArrivalAuthorizationError(GuestArrivalApplicationError):
    pass


class GuestArrivalNotFoundError(GuestArrivalApplicationError):
    pass


class GuestArrivalBusinessRuleError(GuestArrivalApplicationError):
    pass
