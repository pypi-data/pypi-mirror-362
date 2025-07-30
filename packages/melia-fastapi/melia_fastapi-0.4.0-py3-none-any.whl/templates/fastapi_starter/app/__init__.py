from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import Settings
from app.core.database import Base, engine
from app.models import whale, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.api.title,
        description=settings.api.description,
        version=settings.api.version,
        redoc_url=None,
        openapi_tags=[
            {
                "name": "{{project_name}}",
                "description": """{{description}}""",
            }
        ],
        root_path=settings.api.root_path,
        lifespan=lifespan,
    )
    #app.include_router(monitoring_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=settings.api.cors_origin,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
