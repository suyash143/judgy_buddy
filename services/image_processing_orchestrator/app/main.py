import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.image_processing_orchestrator.app.api.routes import router
from services.image_processing_orchestrator.app.config import config


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
    logger.info(f"Face Analysis URL: {config.face_analysis_url}")
    logger.info(f"Body Analysis URL: {config.body_analysis_url}")
    logger.info(f"Demographics URL: {config.demographics_url}")
    logger.info(f"Object/Scene URL: {config.object_scene_url}")
    logger.info(f"Quality/Aesthetics URL: {config.quality_aesthetics_url}")
    logger.info(f"Max concurrent requests: {config.max_concurrent_requests}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {config.service_name}")


app = FastAPI(
    title="Judgy Buddy - Image Processing Orchestrator",
    description="Orchestrates parallel calls to vision model services and aggregates results",
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
        "services.image_processing_orchestrator.app.main:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        log_level=config.log_level.lower()
    )

