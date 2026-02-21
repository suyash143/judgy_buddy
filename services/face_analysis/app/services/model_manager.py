import logging
import os
from pathlib import Path
from typing import Optional
import cv2
import numpy as np
import torch
import mediapipe as mp
from services.face_analysis.app.config import config


logger = logging.getLogger(__name__)


class ModelManager:
    """Manages loading and inference for all face analysis models."""
    
    def __init__(self):
        self.models_loaded = False
        self.device = self._get_device()
        
        # Model instances
        self.yunet_detector = None
        self.fairface_model = None
        self.mediapipe_face_mesh = None
        self.hsemotion_model = None
        self.attractiveness_model = None
        
        # Model paths
        self.model_cache_dir = Path(config.model_cache_dir)
        self.model_cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_device(self) -> str:
        """Determine the best available device."""
        if config.device == "mps" and torch.backends.mps.is_available():
            return "mps"
        elif config.device == "cuda" and torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"
    
    async def load_models(self):
        """Load all face analysis models."""
        try:
            logger.info("Loading face analysis models...")
            
            # 1. Load YuNet face detector
            await self._load_yunet()
            
            # 2. Load FairFace model (gender, age, race)
            await self._load_fairface()
            
            # 3. Load MediaPipe Face Mesh
            await self._load_mediapipe()
            
            # 4. Load HSEmotion model
            await self._load_hsemotion()
            
            # 5. Load attractiveness model
            await self._load_attractiveness_model()
            
            self.models_loaded = True
            logger.info(f"All models loaded successfully on device: {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.models_loaded = False
            raise
    
    async def _load_yunet(self):
        """Load YuNet face detection model."""
        try:
            # YuNet model from OpenCV
            model_path = self.model_cache_dir / "face_detection_yunet_2023mar.onnx"
            
            if not model_path.exists():
                logger.info("Downloading YuNet model...")
                # Download from OpenCV zoo
                url = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
                import urllib.request
                urllib.request.urlretrieve(url, model_path)
                logger.info("YuNet model downloaded")
            
            # Initialize YuNet detector
            self.yunet_detector = cv2.FaceDetectorYN.create(
                str(model_path),
                "",
                (320, 320),
                score_threshold=0.6,
                nms_threshold=0.3
            )
            logger.info("YuNet detector loaded")
            
        except Exception as e:
            logger.error(f"Error loading YuNet: {e}")
            # Create a dummy detector for testing
            self.yunet_detector = None
    
    async def _load_fairface(self):
        """Load FairFace model for gender, age, and race prediction."""
        try:
            # For now, we'll use a placeholder
            # In production, download from: https://github.com/dchen236/FairFace
            logger.info("FairFace model loading (placeholder)")
            self.fairface_model = None  # Will implement actual loading
            
        except Exception as e:
            logger.error(f"Error loading FairFace: {e}")
            self.fairface_model = None
    
    async def _load_mediapipe(self):
        """Load MediaPipe Face Mesh."""
        try:
            self.mediapipe_face_mesh = mp.solutions.face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5
            )
            logger.info("MediaPipe Face Mesh loaded")
            
        except Exception as e:
            logger.error(f"Error loading MediaPipe: {e}")
            self.mediapipe_face_mesh = None
    
    async def _load_hsemotion(self):
        """Load HSEmotion model for emotion detection."""
        try:
            # For now, placeholder
            # In production, use: https://github.com/HSE-asavchenko/face-emotion-recognition
            logger.info("HSEmotion model loading (placeholder)")
            self.hsemotion_model = None
            
        except Exception as e:
            logger.error(f"Error loading HSEmotion: {e}")
            self.hsemotion_model = None
    
    async def _load_attractiveness_model(self):
        """Load SCUT-FBP5500 attractiveness model."""
        try:
            # For now, placeholder
            # In production, use SCUT-FBP5500 dataset model
            logger.info("Attractiveness model loading (placeholder)")
            self.attractiveness_model = None
            
        except Exception as e:
            logger.error(f"Error loading attractiveness model: {e}")
            self.attractiveness_model = None
    
    async def unload_models(self):
        """Unload all models to free memory."""
        logger.info("Unloading face analysis models...")
        
        if self.mediapipe_face_mesh:
            self.mediapipe_face_mesh.close()
        
        self.yunet_detector = None
        self.fairface_model = None
        self.mediapipe_face_mesh = None
        self.hsemotion_model = None
        self.attractiveness_model = None
        
        self.models_loaded = False
        logger.info("Models unloaded")

