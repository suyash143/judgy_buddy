import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Configuration for VLM Scene Analysis Service."""

    # Service info
    service_name: str = "vlm_scene_analysis"
    service_version: str = "0.1.0"

    # Server config
    host: str = "0.0.0.0"
    port: int = 8008
    reload: bool = True
    log_level: str = "INFO"

    # CORS
    cors_origins: list[str] = ["*"]

    # Model config
    model_name: str = "mlx-community/llava-v1.6-mistral-7b-4bit"
    model_cache_dir: Path = Path(__file__).parent.parent / "model_cache"

    # Device config (MLX automatically uses Apple Silicon)
    device: str = "mps"  # Metal Performance Shaders

    # Generation config
    max_tokens: int = 500
    temperature: float = 0.7
    top_p: float = 0.9

    class Config:
        env_prefix = "VLM_"
        case_sensitive = False


config = Config()

# Create model cache directory if it doesn't exist
config.model_cache_dir.mkdir(parents=True, exist_ok=True)
