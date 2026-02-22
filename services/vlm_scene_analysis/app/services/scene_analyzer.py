import logging
import time
import tempfile
from pathlib import Path
from typing import Dict, Any
from libs.common.utils import base64_to_numpy
import cv2
from services.vlm_scene_analysis.app.services.vlm_manager import VLMManager


logger = logging.getLogger(__name__)


class SceneAnalyzer:
    """Analyzes scenes in images using VLM."""

    def __init__(self, vlm_manager: VLMManager):
        self.vlm_manager = vlm_manager

    async def analyze(self, image_base64: str, request_id: str) -> Dict[str, Any]:
        """
        Analyze scene in an image using VLM.

        Args:
            image_base64: Base64 encoded image
            request_id: Request ID for tracking

        Returns:
            Dictionary with scene analysis results
        """
        start_time = time.time()

        try:
            # Convert base64 to numpy array
            image = base64_to_numpy(image_base64)

            # Save image to temporary file for VLM processing
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                cv2.imwrite(tmp_path, image)

            try:
                # Create comprehensive prompt for scene analysis
                prompt = """Analyze this image in detail and provide:

1. **Objects**: List all visible objects with descriptions (furniture, electronics, decorations, etc.)
2. **Scene Type**: What kind of space is this? (living room, bedroom, office, outdoor, etc.)
3. **Atmosphere**: Describe the mood, lighting, and overall feel
4. **Colors & Materials**: Dominant colors, textures, and materials visible
5. **Spatial Layout**: How objects are arranged and positioned
6. **Quality Assessment**: Rate the aesthetic quality, composition, and cleanliness (1-10)
7. **Notable Details**: Any interesting, unusual, or noteworthy features

Be specific and detailed. Focus on what makes this image unique or roast-worthy."""

                # Generate VLM analysis
                analysis_text = await self.vlm_manager.analyze_image(
                    image_path=tmp_path,
                    prompt=prompt
                )

                processing_time_ms = (time.time() - start_time) * 1000

                return {
                    "scene_description": analysis_text,
                    "processing_time_ms": processing_time_ms
                }

            finally:
                # Clean up temporary file
                Path(tmp_path).unlink(missing_ok=True)

        except Exception as e:
            logger.error(f"Error analyzing scene: {e}")
            raise
