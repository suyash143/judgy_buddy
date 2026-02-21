import time
import aiohttp
from typing import Optional
from PIL import Image
from libs.common.utils import generate_request_id, image_to_base64
from libs.common.schemas import AggregatedImageFeatures, AnalyzeImageResponse
from services.main_orchestrator.app.models.schemas import (
    ImageProcessRequest,
    ImageProcessResponse,
    LLMGenerateRequest,
    LLMGenerateResponse,
)
from services.main_orchestrator.app.config import config


class OrchestratorService:
    """Main orchestrator service that coordinates image processing and LLM generation."""
    
    def __init__(self) -> None:
        self.image_processing_url = config.image_processing_orchestrator_url
        self.llm_url = config.llm_inferencer_url
        self.timeout = aiohttp.ClientTimeout(total=config.request_timeout)
    
    async def process_image(
        self, 
        image: Image.Image, 
        roast_level: str = "medium"
    ) -> AnalyzeImageResponse:
        """
        Process an image through the entire pipeline.
        
        Args:
            image: PIL Image object
            roast_level: Roast intensity level (mild/medium/savage)
        
        Returns:
            AnalyzeImageResponse with roast and features
        """
        start_time = time.time()
        request_id = generate_request_id()
        
        # Convert image to base64
        image_base64 = image_to_base64(image)
        
        # Step 1: Send to Image Processing Orchestrator
        features = await self._call_image_processing(image_base64, request_id)
        
        # Step 2: Send features to LLM for roast generation
        roast_response = await self._call_llm_generator(features, roast_level)
        
        # Calculate total processing time
        total_time_ms = (time.time() - start_time) * 1000
        
        # Build final response
        return AnalyzeImageResponse(
            request_id=request_id,
            roast=roast_response.roast_text,
            features=features,
            total_processing_time_ms=total_time_ms,
            status="success"
        )
    
    async def _call_image_processing(
        self, 
        image_base64: str, 
        request_id: str
    ) -> AggregatedImageFeatures:
        """Call Image Processing Orchestrator service."""
        url = f"{self.image_processing_url}/api/v1/process"
        
        request_data = ImageProcessRequest(
            image_base64=image_base64,
            request_id=request_id
        )
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                url,
                json=request_data.model_dump(),
                headers={
                    "Content-Type": "application/json",
                    "X-Request-ID": request_id,
                    "User-Agent": f"judgy-buddy/main-orchestrator/{config.service_version}"
                }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                # Convert response to AggregatedImageFeatures
                return AggregatedImageFeatures(**data)
    
    async def _call_llm_generator(
        self, 
        features: AggregatedImageFeatures, 
        roast_level: str
    ) -> LLMGenerateResponse:
        """Call LLM Inferencer service."""
        url = f"{self.llm_url}/api/v1/generate"
        
        request_data = LLMGenerateRequest(
            features=features,
            roast_level=roast_level
        )
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                url,
                json=request_data.model_dump(),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": f"judgy-buddy/main-orchestrator/{config.service_version}"
                }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return LLMGenerateResponse(**data)
    
    async def health_check(self) -> dict[str, bool]:
        """Check health of downstream services."""
        health_status = {
            "image_processing_orchestrator": False,
            "llm_inferencer": False
        }
        
        # Check Image Processing Orchestrator
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(f"{self.image_processing_url}/health") as response:
                    health_status["image_processing_orchestrator"] = response.status == 200
        except Exception:
            pass
        
        # Check LLM Inferencer
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(f"{self.llm_url}/health") as response:
                    health_status["llm_inferencer"] = response.status == 200
        except Exception:
            pass
        
        return health_status

