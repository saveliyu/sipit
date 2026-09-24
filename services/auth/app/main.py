from fastapi import FastAPI
from fastapi.requests import Request
from starlette.responses import JSONResponse

from app.api.routers import api_router
from app.core.exceptions import ApiException

app = FastAPI()
app.include_router(api_router)


@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    headers = None
    if exc.status_code == 401:
        headers = {"WWW-Authenticate": "Bearer"}

    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=headers
    )
