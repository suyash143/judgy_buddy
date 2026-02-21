import io
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from PIL import Image
from libs.common.utils import validate_image_format, resize_image_if_needed
from libs.common.schemas import AnalyzeImageResponse
from services.main_orchestrator.app.models.schemas import HealthResponse, ErrorResponse
from services.main_orchestrator.app.services.orchestrator import OrchestratorService
from services.main_orchestrator.app.config import config


router = APIRouter()
orchestrator = OrchestratorService()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    downstream_health = await orchestrator.health_check()
    
    # Service is healthy if all downstream services are healthy
    all_healthy = all(downstream_health.values())
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        service=config.service_name,
        version=config.service_version
    )


@router.post(
    "/api/v1/analyze",
    response_model=AnalyzeImageResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_image(
    image: UploadFile = File(..., description="Image file to analyze"),
    roast_level: str = Form("medium", description="Roast level: mild, medium, or savage")
) -> AnalyzeImageResponse:
    """
    Analyze an uploaded image and generate a witty roast.
    
    Args:
        image: Uploaded image file (JPEG, PNG, WEBP)
        roast_level: Intensity of the roast (mild/medium/savage)
    
    Returns:
        AnalyzeImageResponse with roast text and extracted features
    
    Raises:
        HTTPException: If image is invalid or processing fails
    """
    # Validate roast level
    if roast_level not in ["mild", "medium", "savage"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid roast_level. Must be 'mild', 'medium', or 'savage'."
        )
    
    # Read and validate image
    try:
        image_bytes = await image.read()
        
        # Check file size
        if len(image_bytes) > config.max_request_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image too large. Maximum size is {config.max_request_size / (1024*1024)}MB"
            )
        
        # Open image with PIL
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Validate format
        if not validate_image_format(pil_image):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image format: {pil_image.format}. Supported: JPEG, PNG, WEBP"
            )
        
        # Convert to RGB if needed (handle RGBA, grayscale, etc.)
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        
        # Resize if too large
        pil_image = resize_image_if_needed(pil_image)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process image: {str(e)}"
        )
    
    # Process image through the pipeline
    try:
        result = await orchestrator.process_image(pil_image, roast_level)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image processing failed: {str(e)}"
        )

