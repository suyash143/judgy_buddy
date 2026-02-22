from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from services.demographics.app.api import routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Demographics Service starting up...")
    yield
    logger.info("Demographics Service shutting down...")

app = FastAPI(
    title="Demographics Service",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(routes.router)

