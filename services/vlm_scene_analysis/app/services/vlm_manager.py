import logging
from typing import Optional, Tuple, Any
from pathlib import Path
import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
from services.vlm_scene_analysis.app.config import config


logger = logging.getLogger(__name__)


class VLMManager:
    """Manages VLM model loading and inference."""

    def __init__(self):
        self.model = None
        self.processor = None
        self.config_data = None
        self.models_loaded = False

    async def load_models(self):
        """Load VLM model."""
        try:
            logger.info(f"Loading VLM model: {config.model_name}")
            logger.info("This may take a few minutes on first run (downloading ~4GB)...")

            # Load model and processor
            self.model, self.processor = load(config.model_name)
            self.config_data = load_config(config.model_name)

            self.models_loaded = True
            logger.info(f"VLM model loaded successfully: {config.model_name}")

        except Exception as e:
            logger.error(f"Error loading VLM model: {e}")
            self.models_loaded = False
            raise

    async def unload_models(self):
        """Unload models to free memory."""
        logger.info("Unloading VLM models...")
        self.model = None
        self.processor = None
        self.config_data = None
        self.models_loaded = False
        logger.info("VLM models unloaded")

    async def analyze_image(
        self,
        image_path: str,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Analyze image using VLM.

        Args:
            image_path: Path to image file
            prompt: Text prompt for analysis
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text description
        """
        if not self.models_loaded:
            raise RuntimeError("VLM models not loaded")

        try:
            # Use config defaults if not specified
            max_tokens = max_tokens or config.max_tokens
            temperature = temperature or config.temperature

            # Generate analysis
            logger.info(f"Generating VLM analysis for image: {image_path}")
            logger.info(f"Prompt: {prompt[:100]}...")

            # Correct signature: generate(model, processor, prompt, image=None, ...)
            output = generate(
                self.model,
                self.processor,
                prompt,
                image=image_path,
                max_tokens=max_tokens,
                temperature=temperature,
                verbose=False
            )

            logger.info(f"VLM analysis generated: {len(output)} characters")
            return output

        except Exception as e:
            logger.error(f"Error during VLM inference: {e}")
            raise
