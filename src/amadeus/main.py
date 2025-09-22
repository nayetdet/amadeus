from fastapi import FastAPI
from src.amadeus.exceptions import register_exception_handlers
from src.amadeus.middlewares import register_middlewares
from src.amadeus.routes import register_routes

app = FastAPI(title="Amadeus")

register_middlewares(app)
register_exception_handlers(app)
register_routes(app)
