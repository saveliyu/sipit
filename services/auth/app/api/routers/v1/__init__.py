from fastapi import APIRouter

from app.api.routers.v1 import auth

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
