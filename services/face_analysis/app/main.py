import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.face_analysis.app.api.routes import router, set_model_manager
from services.face_analysis.app.services.model_manager import ModelManager
from services.face_analysis.app.config import config


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
    logger.info(f"Model cache directory: {config.model_cache_dir}")
    
    # Initialize and load models
    model_manager = ModelManager()
    set_model_manager(model_manager)
    
    try:
        await model_manager.load_models()
        logger.info("All models loaded successfully")
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        logger.warning("Service starting with degraded status")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {config.service_name}")
    await model_manager.unload_models()


app = FastAPI(
    title="Judgy Buddy - Face Analysis Service",
    description="Face detection and analysis using YuNet, FairFace, MediaPipe, HSEmotion, and attractiveness models",
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
        "services.face_analysis.app.main:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        log_level=config.log_level.lower()
    )

