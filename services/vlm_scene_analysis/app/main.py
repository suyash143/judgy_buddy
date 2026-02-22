import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.vlm_scene_analysis.app.api.routes import router, set_vlm_manager
from services.vlm_scene_analysis.app.services.vlm_manager import VLMManager
from services.vlm_scene_analysis.app.config import config


logging.basicConfig(
    level=getattr(logging, config.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info(f"Starting {config.service_name} v{config.service_version}")
    logger.info(f"Device: {config.device}")
    logger.info(f"Model: {config.model_name}")
    logger.info(f"Model cache directory: {config.model_cache_dir}")

    # Initialize and load VLM model
    vlm_manager = VLMManager()
    set_vlm_manager(vlm_manager)

    try:
        await vlm_manager.load_models()
        logger.info("VLM model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading VLM model: {e}")
        logger.warning("Service starting with degraded status")

    yield

    # Shutdown
    logger.info(f"Shutting down {config.service_name}")
    await vlm_manager.unload_models()


app = FastAPI(
    title="I Judge - VLM Scene Analysis Service",
    description="Comprehensive scene understanding using LLaVA Vision-Language Model",
    version=config.service_version,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "status": "error",
            "error_code": "INTERNAL_ERROR"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "services.vlm_scene_analysis.app.main:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        log_level=config.log_level.lower()
    )
