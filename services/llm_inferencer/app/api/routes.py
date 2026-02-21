from fastapi import APIRouter, HTTPException, status
from services.llm_inferencer.app.models.schemas import (
    HealthResponse,
    ErrorResponse,
    LLMGenerateRequest,
    LLMGenerateResponse
)
from services.llm_inferencer.app.services.roast_generator import RoastGenerator
from services.llm_inferencer.app.services.llm_manager import LLMManager
from services.llm_inferencer.app.config import config


router = APIRouter()

# Global instances (will be initialized in lifespan)
llm_manager: LLMManager = None
roast_generator: RoastGenerator = None


def set_llm_manager(lm: LLMManager):
    """Set the LLM manager instance."""
    global llm_manager, roast_generator
    llm_manager = lm
    roast_generator = RoastGenerator(llm_manager)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    model_loaded = llm_manager.model_loaded if llm_manager else False
    
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        service=config.service_name,
        version=config.service_version,
        model_loaded=model_loaded
    )


@router.post(
    "/api/v1/generate",
    response_model=LLMGenerateResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def generate_roast(request: LLMGenerateRequest) -> LLMGenerateResponse:
    """
    Generate a witty roast from image features.
    
    Args:
        request: LLM generation request with features and roast level
    
    Returns:
        LLMGenerateResponse with generated roast text
    
    Raises:
        HTTPException: If generation fails
    """
    if not llm_manager or not llm_manager.model_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM model not loaded yet. Please wait for service to initialize."
        )
    
    # Validate roast level
    if request.roast_level not in ["mild", "medium", "savage"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid roast_level. Must be 'mild', 'medium', or 'savage'."
        )
    
    try:
        # Generate roast
        result = await roast_generator.generate_roast(
            features=request.features,
            roast_level=request.roast_level
        )
        
        return LLMGenerateResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Roast generation failed: {str(e)}"
        )

