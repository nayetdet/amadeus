from fastapi import FastAPI
from src.amadeus.middlewares.cors_middleware import register_cors_middleware

def register_middlewares(app: FastAPI) -> None:
    register_cors_middleware(app)
