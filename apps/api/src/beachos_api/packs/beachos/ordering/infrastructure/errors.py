"""Ordering Infrastructure failures."""


class OrderingInfrastructureError(RuntimeError):
    pass


class OrderingConcurrencyError(OrderingInfrastructureError):
    pass
