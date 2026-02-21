import logging
from typing import Optional
from services.llm_inferencer.app.config import config


logger = logging.getLogger(__name__)


class LLMManager:
    """Manages loading and inference for the LLM model."""
    
    def __init__(self):
        self.model_loaded = False
        self.model = None
        self.tokenizer = None
        
    async def load_model(self):
        """Load the LLM model."""
        try:
            logger.info(f"Loading LLM model: {config.model_name}")
            
            # Import mlx_lm here to avoid import errors if not installed
            try:
                from mlx_lm import load, generate
                self.generate_fn = generate
            except ImportError:
                logger.warning("mlx_lm not installed. Using placeholder mode.")
                self.model_loaded = True
                return
            
            # Load the model and tokenizer
            self.model, self.tokenizer = load(config.model_name)
            
            self.model_loaded = True
            logger.info(f"LLM model loaded successfully: {config.model_name}")
            
        except Exception as e:
            logger.error(f"Error loading LLM model: {e}")
            logger.warning("Running in placeholder mode")
            self.model_loaded = True  # Set to true to allow service to run
            raise
    
    async def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
        
        Returns:
            Generated text
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded")
        
        # Use config defaults if not specified
        max_tokens = max_tokens or config.max_tokens
        temperature = temperature or config.temperature
        top_p = top_p or config.top_p
        
        try:
            # If model is not actually loaded (placeholder mode), return mock response
            if self.model is None or self.tokenizer is None:
                logger.warning("Using placeholder generation")
                return self._placeholder_generate(prompt)
            
            # Generate using mlx_lm
            response = self.generate_fn(
                self.model,
                self.tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                temp=temperature,
                top_p=top_p,
                verbose=False
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            # Fallback to placeholder
            return self._placeholder_generate(prompt)
    
    def _placeholder_generate(self, prompt: str) -> str:
        """Placeholder generation for testing without actual model."""
        # Extract roast level from prompt if present
        if "savage" in prompt.lower():
            return (
                "Listen up, because I'm only saying this once: That outfit is a crime against fashion, "
                "your room looks like a tornado hit a thrift store, and honestly? Your face says 'confident' "
                "but everything else screams 'help me.' That 7.5 attractiveness score must've been graded "
                "on a VERY generous curve. But hey, at least you had the audacity to take this photo - "
                "that takes guts, or maybe just a complete lack of self-awareness. Either way, iconic. 💀"
            )
        elif "mild" in prompt.lower():
            return (
                "Well, well, well... looks like someone tried their best today! "
                "That casual outfit says 'I woke up like this' but your messy bedroom "
                "background says 'I actually woke up like this.' At least you're consistent! "
                "7.5/10 for authenticity, though. 😊"
            )
        else:  # medium
            return (
                "Oh honey, that bedroom background is working harder than your fashion sense! "
                "I see you went for the 'athletic casual' look - very brave considering that "
                "harsh lighting is exposing EVERYTHING. Your face says 'happy' but that "
                "messy room says 'gave up 3 weeks ago.' But hey, at least you're a solid 7.5 "
                "in the looks department, so you've got that going for you! 😏"
            )
    
    async def unload_model(self):
        """Unload the model to free memory."""
        logger.info("Unloading LLM model...")
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        logger.info("LLM model unloaded")

