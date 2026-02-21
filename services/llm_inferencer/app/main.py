import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.llm_inferencer.app.api.routes import router, set_llm_manager
from services.llm_inferencer.app.services.llm_manager import LLMManager
from services.llm_inferencer.app.config import config


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
    logger.info(f"Model: {config.model_name}")
    logger.info(f"Max tokens: {config.max_tokens}")
    logger.info(f"Temperature: {config.temperature}")
    logger.info(f"Top-p: {config.top_p}")
    
    # Initialize and load LLM
    llm_manager = LLMManager()
    set_llm_manager(llm_manager)
    
    try:
        await llm_manager.load_model()
        logger.info("LLM model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading LLM model: {e}")
        logger.warning("Service starting in placeholder mode")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {config.service_name}")
    await llm_manager.unload_model()


app = FastAPI(
    title="Judgy Buddy - LLM Inferencer",
    description="Generates witty roasts from image features using LLaMA 3.2 3B Instruct",
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
        "services.llm_inferencer.app.main:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        log_level=config.log_level.lower()
    )

