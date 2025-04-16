from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware import Middleware

from apps.http.routers import router
from apps.shared.boot import Boot
from src.shared.environ import env


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_middleware() -> list[Middleware]:
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]


def create_app() -> FastAPI:
    Boot()

    app_ = FastAPI(
        title="Markdown Notes",
        description="Markdown Notes API",
        version="1.0.0",
        middleware=init_middleware(),
    )
    init_routers(app_=app_)

    return app_
