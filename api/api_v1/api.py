from fastapi import APIRouter

from api.api_v1.endpoints import (
    restaurant,
)

api_router = APIRouter()
api_router.include_router(
    restaurant.router,
    prefix="/restaurants",
    tags=["restaurants"],
)
