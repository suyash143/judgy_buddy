from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from services.body_analysis.app.api import routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Body Analysis Service starting up...")
    yield
    logger.info("Body Analysis Service shutting down...")

app = FastAPI(
    title="Body Analysis Service",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(routes.router)

