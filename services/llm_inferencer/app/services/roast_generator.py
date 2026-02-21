import logging
import time
from typing import Dict, Any
from libs.common.schemas import AggregatedImageFeatures
from services.llm_inferencer.app.services.llm_manager import LLMManager
from services.llm_inferencer.app.config import config


logger = logging.getLogger(__name__)


class RoastGenerator:
    """Generates witty roasts from image features using LLM."""
    
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager
    
    async def generate_roast(
        self,
        features: AggregatedImageFeatures,
        roast_level: str
    ) -> Dict[str, Any]:
        """
        Generate a witty roast from image features.
        
        Args:
            features: Aggregated image features
            roast_level: Roast intensity (mild/medium/savage)
        
        Returns:
            Dictionary with roast_text, confidence, and generation_time_ms
        """
        start_time = time.time()
        
        try:
            # Build the prompt
            prompt = self._build_prompt(features, roast_level)
            
            # Generate roast
            roast_text = await self.llm_manager.generate(prompt)
            
            # Calculate generation time
            generation_time_ms = (time.time() - start_time) * 1000
            
            return {
                "roast_text": roast_text.strip(),
                "confidence": 0.92,  # Placeholder confidence
                "generation_time_ms": generation_time_ms
            }
            
        except Exception as e:
            logger.error(f"Error generating roast: {e}")
            raise
    
    def _build_prompt(
        self,
        features: AggregatedImageFeatures,
        roast_level: str
    ) -> str:
        """
        Build a prompt for the LLM based on image features.
        
        Args:
            features: Aggregated image features
            roast_level: Roast intensity
        
        Returns:
            Formatted prompt string
        """
        # Extract key features
        feature_summary = self._summarize_features(features)
        
        # Define roast level instructions
        roast_instructions = {
            "mild": "Be gentle and playful. Keep it light-hearted and friendly.",
            "medium": "Be witty and clever. Roast them but keep it fun.",
            "savage": "Go all out! Be brutally honest and hilariously savage."
        }
        
        instruction = roast_instructions.get(roast_level, roast_instructions["medium"])
        
        # Build the prompt
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{config.system_prompt}

Roast Level: {roast_level.upper()}
Instructions: {instruction}
<|eot_id|><|start_header_id|>user<|end_header_id|>

Analyze this person's image and create a witty roast based on these features:

{feature_summary}

Generate a creative, humorous roast (2-4 sentences). Be specific and reference the actual features detected.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
        
        return prompt
    
    def _summarize_features(self, features: AggregatedImageFeatures) -> str:
        """Summarize features into a readable format for the prompt."""
        summary_parts = []
        
        # Face analysis
        if features.face_analysis:
            face = features.face_analysis
            face_info = []
            if face.face_count is not None:
                face_info.append(f"Faces detected: {face.face_count}")
            if face.gender:
                face_info.append(f"Gender: {face.gender}")
            if face.age:
                face_info.append(f"Age: ~{face.age}")
            if face.emotion:
                face_info.append(f"Emotion: {face.emotion}")
            if face.attractiveness_score:
                face_info.append(f"Attractiveness: {face.attractiveness_score}/10")
            
            if face_info:
                summary_parts.append("Face: " + ", ".join(face_info))
        
        # Body analysis
        if features.body_analysis:
            body = features.body_analysis
            body_info = []
            if body.body_type:
                body_info.append(f"Body type: {body.body_type}")
            if body.fashion_items:
                body_info.append(f"Wearing: {', '.join(body.fashion_items)}")
            if body.dressing_score:
                body_info.append(f"Fashion score: {body.dressing_score}/10")
            
            if body_info:
                summary_parts.append("Body: " + ", ".join(body_info))
        
        # Object/Scene
        if features.object_scene:
            scene = features.object_scene
            scene_info = []
            if scene.scene_type:
                scene_info.append(f"Scene: {scene.scene_type}")
            if scene.objects:
                scene_info.append(f"Objects: {', '.join(scene.objects[:5])}")
            
            if scene_info:
                summary_parts.append("Scene: " + ", ".join(scene_info))
        
        # Quality/Aesthetics
        if features.quality_aesthetics:
            quality = features.quality_aesthetics
            quality_info = []
            if quality.lighting_quality:
                quality_info.append(f"Lighting: {quality.lighting_quality}")
            if quality.is_blurry is not None:
                quality_info.append(f"Blurry: {quality.is_blurry}")
            if quality.aesthetic_score:
                quality_info.append(f"Aesthetic score: {quality.aesthetic_score}/10")
            
            if quality_info:
                summary_parts.append("Quality: " + ", ".join(quality_info))
        
        if not summary_parts:
            return "No specific features detected. Generate a generic roast."
        
        return "\n".join(f"- {part}" for part in summary_parts)

