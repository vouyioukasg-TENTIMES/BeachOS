"""Bar Infrastructure failures."""


class BarInfrastructureError(RuntimeError):
    pass


class BarConcurrencyError(BarInfrastructureError):
    pass
