from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
import logging
import time

logger = logging.getLogger(__name__)
router = APIRouter()

class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    image_base64: str
    request_id: str

class DemographicsResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    race: str | None = None
    ethnicity: str | None = None
    skin_tone: str | None = None
    skin_tone_ita: float | None = None
    processing_time_ms: float

@router.post("/analyze", response_model=DemographicsResult)
async def analyze_demographics(request: AnalyzeRequest):
    start_time = time.time()
    logger.info(f"Analyzing demographics for request {request.request_id}")
    
    try:
        # Placeholder implementation - returns mock data
        result = DemographicsResult(
            race="asian",
            ethnicity="asian",
            skin_tone="medium",
            skin_tone_ita=45.0,
            processing_time_ms=(time.time() - start_time) * 1000
        )
        
        logger.info(f"Demographics analysis complete for request {request.request_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing demographics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "demographics",
        "version": "0.1.0"
    }

