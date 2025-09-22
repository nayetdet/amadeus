from fastapi import APIRouter, FastAPI
from src.amadeus.routes import tts_route

def register_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/v1")
    router.include_router(tts_route.router, prefix="/tts", tags=["TTS"])
    app.include_router(router)
