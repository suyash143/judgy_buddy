from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from services.quality_aesthetics.app.api import routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Quality & Aesthetics Service starting up...")
    yield
    logger.info("Quality & Aesthetics Service shutting down...")

app = FastAPI(
    title="Quality & Aesthetics Service",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(routes.router)

