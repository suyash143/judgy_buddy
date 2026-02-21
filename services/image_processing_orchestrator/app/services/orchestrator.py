import asyncio
import logging
import time
from typing import Optional, Dict, Any
import aiohttp
from services.image_processing_orchestrator.app.config import config


logger = logging.getLogger(__name__)


class ImageProcessingOrchestrator:
    """Orchestrates parallel calls to all vision model services."""
    
    def __init__(self):
        self.face_analysis_url = config.face_analysis_url
        self.body_analysis_url = config.body_analysis_url
        self.demographics_url = config.demographics_url
        self.object_scene_url = config.object_scene_url
        self.quality_aesthetics_url = config.quality_aesthetics_url
        self.timeout = config.service_timeout
        self.max_concurrent = config.max_concurrent_requests
    
    async def process_image(self, image_base64: str, request_id: str) -> Dict[str, Any]:
        """
        Process image by calling all vision services in parallel.
        
        Args:
            image_base64: Base64 encoded image
            request_id: Request ID for tracking
        
        Returns:
            Dictionary with aggregated results from all services
        """
        start_time = time.time()
        
        # Create tasks for all services
        tasks = {
            "face_analysis": self._call_face_analysis(image_base64, request_id),
            "body_analysis": self._call_body_analysis(image_base64, request_id),
            "demographics": self._call_demographics(image_base64, request_id),
            "object_scene": self._call_object_scene(image_base64, request_id),
            "quality_aesthetics": self._call_quality_aesthetics(image_base64, request_id),
        }
        
        # Execute all tasks in parallel with semaphore for rate limiting
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def limited_task(name: str, coro):
            async with semaphore:
                try:
                    return name, await coro
                except Exception as e:
                    logger.error(f"Error calling {name}: {e}")
                    return name, None
        
        results = await asyncio.gather(
            *[limited_task(name, task) for name, task in tasks.items()],
            return_exceptions=True
        )
        
        # Aggregate results
        aggregated = {}
        for result in results:
            if isinstance(result, tuple):
                name, data = result
                aggregated[name] = data
            else:
                logger.error(f"Unexpected result type: {type(result)}")
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        return {
            **aggregated,
            "processing_time_ms": processing_time_ms
        }
    
    async def _call_face_analysis(self, image_base64: str, request_id: str) -> Optional[Dict[str, Any]]:
        """Call Face Analysis service."""
        return await self._call_service(
            url=f"{self.face_analysis_url}/api/v1/analyze",
            payload={"image_base64": image_base64, "request_id": request_id},
            service_name="face_analysis"
        )
    
    async def _call_body_analysis(self, image_base64: str, request_id: str) -> Optional[Dict[str, Any]]:
        """Call Body Analysis service."""
        return await self._call_service(
            url=f"{self.body_analysis_url}/analyze",
            payload={"image_base64": image_base64, "request_id": request_id},
            service_name="body_analysis"
        )

    async def _call_demographics(self, image_base64: str, request_id: str) -> Optional[Dict[str, Any]]:
        """Call Demographics service."""
        return await self._call_service(
            url=f"{self.demographics_url}/analyze",
            payload={"image_base64": image_base64, "request_id": request_id},
            service_name="demographics"
        )

    async def _call_object_scene(self, image_base64: str, request_id: str) -> Optional[Dict[str, Any]]:
        """Call Object & Scene Detection service."""
        return await self._call_service(
            url=f"{self.object_scene_url}/analyze",
            payload={"image_base64": image_base64, "request_id": request_id},
            service_name="object_scene"
        )

    async def _call_quality_aesthetics(self, image_base64: str, request_id: str) -> Optional[Dict[str, Any]]:
        """Call Quality & Aesthetics service."""
        return await self._call_service(
            url=f"{self.quality_aesthetics_url}/analyze",
            payload={"image_base64": image_base64, "request_id": request_id},
            service_name="quality_aesthetics"
        )
    
    async def _call_service(self, url: str, payload: Dict[str, Any], service_name: str) -> Optional[Dict[str, Any]]:
        """
        Generic method to call a service.
        
        Args:
            url: Service endpoint URL
            payload: Request payload
            service_name: Name of the service for logging
        
        Returns:
            Response data or None if failed
        """
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"{service_name} completed successfully")
                        return data
                    else:
                        logger.error(f"{service_name} returned status {response.status}")
                        return None
        except asyncio.TimeoutError:
            logger.error(f"{service_name} timed out after {self.timeout}s")
            return None
        except Exception as e:
            logger.error(f"Error calling {service_name}: {e}")
            return None
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all downstream services."""
        services = {
            "face_analysis": f"{self.face_analysis_url}/health",
            "body_analysis": f"{self.body_analysis_url}/health",
            "demographics": f"{self.demographics_url}/health",
            "object_scene": f"{self.object_scene_url}/health",
            "quality_aesthetics": f"{self.quality_aesthetics_url}/health",
        }
        
        health_status = {}
        
        async with aiohttp.ClientSession() as session:
            for service_name, url in services.items():
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        health_status[service_name] = response.status == 200
                except Exception:
                    health_status[service_name] = False
        
        return health_status

