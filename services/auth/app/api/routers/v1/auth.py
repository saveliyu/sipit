from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.get("/health-check")
async def health_check():
    return {"status": "ok"}