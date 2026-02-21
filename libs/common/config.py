from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class ServiceConfig(BaseSettings):
    """Base configuration for all services."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Service Info
    service_name: str = "judgy-buddy-service"
    service_version: str = "0.1.0"
    
    # Server Config
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 1
    
    # Logging
    log_level: str = "INFO"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Request Settings
    max_request_size: int = 10 * 1024 * 1024  # 10MB
    request_timeout: int = 30  # seconds
    
    # Model Settings
    model_cache_dir: str = "./model_cache"
    device: str = "cpu"  # cpu, cuda, mps (for Apple Silicon)


class MainOrchestratorConfig(ServiceConfig):
    """Configuration for Main Orchestrator service."""
    
    service_name: str = "main-orchestrator"
    port: int = 8000
    
    # Service URLs
    image_processing_orchestrator_url: str = "http://localhost:8001"
    llm_inferencer_url: str = "http://localhost:8007"
    
    # Storage
    upload_dir: str = "./uploads"
    temp_dir: str = "./temp"
    
    # Rate Limiting
    rate_limit_per_minute: int = 10


class ImageProcessingOrchestratorConfig(ServiceConfig):
    """Configuration for Image Processing Orchestrator service."""
    
    service_name: str = "image-processing-orchestrator"
    port: int = 8001
    
    # Service URLs
    face_analysis_url: str = "http://localhost:8002"
    body_analysis_url: str = "http://localhost:8003"
    demographics_url: str = "http://localhost:8004"
    object_scene_url: str = "http://localhost:8005"
    quality_aesthetics_url: str = "http://localhost:8006"
    
    # Parallel Processing
    max_concurrent_requests: int = 5
    service_timeout: int = 30


class FaceAnalysisConfig(ServiceConfig):
    """Configuration for Face Analysis service."""
    
    service_name: str = "face-analysis"
    port: int = 8002
    
    # Model paths
    yunet_model_path: Optional[str] = None
    fairface_model_path: Optional[str] = None
    mediapipe_model_path: Optional[str] = None
    hsemotion_model_path: Optional[str] = None
    attractiveness_model_path: Optional[str] = None


class BodyAnalysisConfig(ServiceConfig):
    """Configuration for Body Analysis service."""
    
    service_name: str = "body-analysis"
    port: int = 8003
    
    # Model paths
    mediapipe_pose_model_path: Optional[str] = None
    body_type_model_path: Optional[str] = None
    deepfashion_model_path: Optional[str] = None


class DemographicsConfig(ServiceConfig):
    """Configuration for Demographics service."""
    
    service_name: str = "demographics"
    port: int = 8004
    
    # Model paths
    fairface_model_path: Optional[str] = None


class ObjectSceneConfig(ServiceConfig):
    """Configuration for Object & Scene Detection service."""
    
    service_name: str = "object-scene-detection"
    port: int = 8005
    
    # Model paths
    yolov8_model_path: Optional[str] = None
    places365_model_path: Optional[str] = None
    modnet_model_path: Optional[str] = None


class QualityAestheticsConfig(ServiceConfig):
    """Configuration for Quality & Aesthetics service."""
    
    service_name: str = "quality-aesthetics"
    port: int = 8006
    
    # Model paths
    nima_model_path: Optional[str] = None


class LLMInferencerConfig(ServiceConfig):
    """Configuration for LLM Inferencer service."""
    
    service_name: str = "llm-inferencer"
    port: int = 8007
    
    # Model settings
    model_name: str = "mlx-community/Llama-3.2-3B-Instruct-4bit"
    model_path: Optional[str] = None
    max_tokens: int = 256
    temperature: float = 0.8
    top_p: float = 0.9
    
    # System prompt
    system_prompt: str = (
        "You are a witty AI judge that creates humorous, clever roasts based on image analysis. "
        "Be creative, funny, and entertaining while staying respectful. "
        "Use the provided image features to craft personalized roasts."
    )

