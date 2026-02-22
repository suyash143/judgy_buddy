import logging
import time
import cv2
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from libs.common.utils import base64_to_numpy
from services.face_analysis.app.services.model_manager import ModelManager


logger = logging.getLogger(__name__)


class FaceAnalyzer:
    """Analyzes faces in images using multiple models."""
    
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
    
    async def analyze(self, image_base64: str, request_id: str) -> Dict[str, Any]:
        """
        Analyze faces in an image.
        
        Args:
            image_base64: Base64 encoded image
            request_id: Request ID for tracking
        
        Returns:
            Dictionary with face analysis results
        """
        start_time = time.time()
        
        try:
            # Convert base64 to numpy array
            image = base64_to_numpy(image_base64)
            
            # 1. Detect faces
            faces = await self._detect_faces(image)
            
            if not faces or len(faces) == 0:
                return {
                    "face_count": 0,
                    "faces": [],
                    "processing_time_ms": (time.time() - start_time) * 1000
                }
            
            # Get the primary face (largest or first detected)
            primary_face = faces[0]
            face_crop = self._crop_face(image, primary_face["bbox"])

            # 2. Analyze gender and race with FairFace
            gender_race = await self._analyze_fairface(face_crop)
            
            # 3. Analyze facial structure with MediaPipe
            facial_structure = await self._analyze_facial_structure(face_crop)
            
            # 4. Detect emotion with HSEmotion
            emotion = await self._detect_emotion(face_crop)
            
            # 5. Score attractiveness
            attractiveness = await self._score_attractiveness(face_crop)
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            return {
                "face_count": len(faces),
                "faces": faces,
                **gender_race,
                **emotion,
                **attractiveness,
                **facial_structure,
                "processing_time_ms": processing_time_ms
            }
            
        except Exception as e:
            logger.error(f"Error analyzing face: {e}")
            raise
    
    async def _detect_faces(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect faces using YuNet."""
        try:
            if self.model_manager.yunet_detector is None:
                # Return mock data for testing
                logger.warning("YuNet not loaded, returning mock face detection")
                h, w = image.shape[:2]
                return [{
                    "bbox": [w * 0.25, h * 0.25, w * 0.5, h * 0.5],
                    "confidence": 0.95,
                    "landmarks": [[w * 0.35, h * 0.35], [w * 0.65, h * 0.35]]
                }]
            
            # Set input size based on image dimensions
            h, w = image.shape[:2]
            self.model_manager.yunet_detector.setInputSize((w, h))
            
            # Detect faces
            _, faces_data = self.model_manager.yunet_detector.detect(image)
            
            if faces_data is None:
                return []
            
            faces = []
            for face in faces_data:
                # YuNet returns: [x, y, w, h, x_re, y_re, x_le, y_le, x_n, y_n, x_rcm, y_rcm, x_lcm, y_lcm, conf]
                bbox = face[:4].tolist()
                confidence = float(face[14])
                landmarks = [
                    [float(face[4]), float(face[5])],   # right eye
                    [float(face[6]), float(face[7])],   # left eye
                    [float(face[8]), float(face[9])],   # nose
                    [float(face[10]), float(face[11])], # right mouth corner
                    [float(face[12]), float(face[13])]  # left mouth corner
                ]
                
                faces.append({
                    "bbox": bbox,
                    "confidence": confidence,
                    "landmarks": landmarks
                })
            
            return faces
            
        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return []
    
    def _crop_face(self, image: np.ndarray, bbox: List[float]) -> np.ndarray:
        """Crop face region from image."""
        x, y, w, h = [int(v) for v in bbox]
        # Add some padding
        padding = int(max(w, h) * 0.2)
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)
        
        return image[y1:y2, x1:x2]
    
    async def _analyze_fairface(self, face_crop: np.ndarray) -> Dict[str, Any]:
        """Analyze gender and race using FairFace."""
        # Placeholder implementation
        # TODO: Implement actual FairFace inference
        return {
            "gender": "male",
            "gender_confidence": 0.85,
            "race": "asian",
            "race_confidence": 0.80
        }
    
    async def _analyze_facial_structure(self, face_crop: np.ndarray) -> Dict[str, Any]:
        """Analyze facial structure using MediaPipe."""
        # Placeholder implementation
        # TODO: Implement actual MediaPipe analysis
        return {
            "facial_structure_score": 7.5
        }
    
    async def _detect_emotion(self, face_crop: np.ndarray) -> Dict[str, Any]:
        """Detect emotion using HSEmotion."""
        # Placeholder implementation
        # TODO: Implement actual HSEmotion inference
        return {
            "emotion": "happy",
            "emotion_confidence": 0.88
        }
    
    async def _score_attractiveness(self, face_crop: np.ndarray) -> Dict[str, Any]:
        """Score attractiveness using SCUT-FBP5500 model."""
        # Placeholder implementation
        # TODO: Implement actual attractiveness scoring
        return {
            "attractiveness_score": 7.2
        }

