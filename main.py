from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from core.config import settings
from core.utils import populate_database_with_restaurants
from database_app.database import SessionLocal


@asynccontextmanager
async def lifespan(application: FastAPI):
    db = SessionLocal()
    try:
        populate_database_with_restaurants(db=db)
        yield
    finally:
        db.close()

app = FastAPI(lifespan=lifespan)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
