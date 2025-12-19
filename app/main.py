from fastapi import FastAPI

from app.api.routers.router import router as uf_router

app = FastAPI()
app.include_router(uf_router)