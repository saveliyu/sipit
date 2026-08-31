from fastapi import APIRouter

from app.api.routers import v1

api_router = APIRouter()
api_router.include_router(
    v1.router,
)
