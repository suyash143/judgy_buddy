from fastapi import APIRouter, HTTPException, status
from services.image_processing_orchestrator.app.models.schemas import (
    HealthResponse,
    ErrorResponse,
    ImageProcessRequest,
    ImageProcessResponse
)
from services.image_processing_orchestrator.app.services.orchestrator import ImageProcessingOrchestrator
from services.image_processing_orchestrator.app.config import config


router = APIRouter()
orchestrator = ImageProcessingOrchestrator()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    downstream_health = await orchestrator.health_check()
    
    # Service is healthy if all downstream services are healthy
    all_healthy = all(downstream_health.values()) if downstream_health else False
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        service=config.service_name,
        version=config.service_version
    )


@router.post(
    "/api/v1/process",
    response_model=ImageProcessResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def process_image(request: ImageProcessRequest) -> ImageProcessResponse:
    """
    Process an image by calling all vision model services in parallel.
    
    Args:
        request: Image processing request with base64 image and request ID
    
    Returns:
        ImageProcessResponse with aggregated results from all services
    
    Raises:
        HTTPException: If processing fails
    """
    try:
        # Process image through all services
        results = await orchestrator.process_image(
            image_base64=request.image_base64,
            request_id=request.request_id
        )
        
        return ImageProcessResponse(**results)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image processing failed: {str(e)}"
        )

