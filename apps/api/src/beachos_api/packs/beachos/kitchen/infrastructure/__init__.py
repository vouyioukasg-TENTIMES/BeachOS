"""Public Kitchen Operations Infrastructure."""

from beachos_api.packs.beachos.kitchen.infrastructure.persistence.unit_of_work import (
    PostgresKitchenUnitOfWorkFactory,
)

__all__ = ["PostgresKitchenUnitOfWorkFactory"]
