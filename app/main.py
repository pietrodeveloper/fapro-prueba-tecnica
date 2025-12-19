"""
Application entrypoint for the UF FastAPI service.

Creates a `FastAPI` instance and includes the UF router from app.api.routers.router.
Exported symbol:
- `app`: FastAPI instance used by ASGI servers.

Example:
    uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI

from app.api.routers.router import router as uf_router

app = FastAPI()
app.include_router(uf_router)