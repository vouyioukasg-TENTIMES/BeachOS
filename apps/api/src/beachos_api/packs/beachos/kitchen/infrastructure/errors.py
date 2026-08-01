"""Kitchen Infrastructure failures."""


class KitchenInfrastructureError(RuntimeError):
    pass


class KitchenConcurrencyError(KitchenInfrastructureError):
    pass
