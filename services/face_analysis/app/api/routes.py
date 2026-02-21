from fastapi import APIRouter, HTTPException, status
from services.face_analysis.app.models.schemas import (
    HealthResponse,
    ErrorResponse,
    FaceAnalysisRequest,
    FaceAnalysisResponse
)
from services.face_analysis.app.services.face_analyzer import FaceAnalyzer
from services.face_analysis.app.services.model_manager import ModelManager
from services.face_analysis.app.config import config


router = APIRouter()

# Global instances (will be initialized in lifespan)
model_manager: ModelManager = None
face_analyzer: FaceAnalyzer = None


def set_model_manager(mm: ModelManager):
    """Set the model manager instance."""
    global model_manager, face_analyzer
    model_manager = mm
    face_analyzer = FaceAnalyzer(model_manager)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    models_loaded = model_manager.models_loaded if model_manager else False
    
    return HealthResponse(
        status="healthy" if models_loaded else "degraded",
        service=config.service_name,
        version=config.service_version,
        models_loaded=models_loaded
    )


@router.post(
    "/api/v1/analyze",
    response_model=FaceAnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_face(request: FaceAnalysisRequest) -> FaceAnalysisResponse:
    """
    Analyze faces in an image.
    
    Args:
        request: Face analysis request with base64 image and request ID
    
    Returns:
        FaceAnalysisResponse with detected faces and analysis results
    
    Raises:
        HTTPException: If analysis fails
    """
    if not model_manager or not model_manager.models_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Models not loaded yet. Please wait for service to initialize."
        )
    
    try:
        # Analyze faces
        results = await face_analyzer.analyze(
            image_base64=request.image_base64,
            request_id=request.request_id
        )
        
        return FaceAnalysisResponse(**results)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face analysis failed: {str(e)}"
        )

