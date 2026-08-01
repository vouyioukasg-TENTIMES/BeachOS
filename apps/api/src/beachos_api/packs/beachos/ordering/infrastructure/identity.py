"""Infrastructure identity generation."""

from uuid import uuid4


class UUIDIdentityGenerator:
    def new_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid4()}"
