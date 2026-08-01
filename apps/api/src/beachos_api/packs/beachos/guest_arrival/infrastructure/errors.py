"""Guest Arrival Infrastructure failures."""


class GuestArrivalInfrastructureError(RuntimeError):
    pass


class GuestArrivalConcurrencyError(GuestArrivalInfrastructureError):
    pass
