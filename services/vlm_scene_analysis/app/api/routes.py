import logging
from fastapi import APIRouter, HTTPException, status
from services.vlm_scene_analysis.app.models.schemas import (
    HealthResponse,
    ErrorResponse,
    VLMSceneAnalysisRequest,
    VLMSceneAnalysisResponse
)
from services.vlm_scene_analysis.app.services.scene_analyzer import SceneAnalyzer
from services.vlm_scene_analysis.app.services.vlm_manager import VLMManager
from services.vlm_scene_analysis.app.config import config


logger = logging.getLogger(__name__)

router = APIRouter()

# Global instances (will be initialized in lifespan)
vlm_manager: VLMManager = None
scene_analyzer: SceneAnalyzer = None


def set_vlm_manager(vm: VLMManager):
    """Set the VLM manager instance."""
    global vlm_manager, scene_analyzer
    vlm_manager = vm
    scene_analyzer = SceneAnalyzer(vlm_manager)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    models_loaded = vlm_manager.models_loaded if vlm_manager else False

    return HealthResponse(
        status="healthy" if models_loaded else "degraded",
        service=config.service_name,
        version=config.service_version,
        details={"models_loaded": models_loaded}
    )


@router.post(
    "/api/v1/analyze",
    response_model=VLMSceneAnalysisResponse,
    responses={
        500: {"model": ErrorResponse}
    }
)
async def analyze_scene(request: VLMSceneAnalysisRequest) -> VLMSceneAnalysisResponse:
    """
    Analyze scene in an image using VLM.

    Args:
        request: VLM scene analysis request with base64 image and request ID

    Returns:
        VLMSceneAnalysisResponse with comprehensive scene description

    Raises:
        HTTPException: If analysis fails
    """
    if not vlm_manager or not vlm_manager.models_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="VLM model not loaded yet. Please wait for service to initialize."
        )

    try:
        # Analyze scene
        results = await scene_analyzer.analyze(
            image_base64=request.image_base64,
            request_id=request.request_id
        )

        return VLMSceneAnalysisResponse(**results)

    except Exception as e:
        logger.error(f"Error in analyze_scene endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scene analysis failed: {str(e)}"
        )
