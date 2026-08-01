from typing import Final

from fastapi import FastAPI

from beachos_api.api import register_error_handlers, router

HEALTH_STATUS: Final = {"status": "ok"}


def create_app() -> FastAPI:
    application = FastAPI(
        title="BeachOS API",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    @application.get("/health")
    def health() -> dict[str, str]:
        return HEALTH_STATUS

    application.include_router(router)
    register_error_handlers(application)
    return application


app = create_app()
