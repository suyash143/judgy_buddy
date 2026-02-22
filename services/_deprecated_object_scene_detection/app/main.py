from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from services.object_scene_detection.app.api import routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Object & Scene Detection Service starting up...")
    yield
    logger.info("Object & Scene Detection Service shutting down...")

app = FastAPI(
    title="Object & Scene Detection Service",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(routes.router)

