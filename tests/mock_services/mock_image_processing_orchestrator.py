#!/usr/bin/env python3
"""Mock Image Processing Orchestrator for testing Main Orchestrator."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI(title="Mock Image Processing Orchestrator")


class ImageProcessRequest(BaseModel):
    image_base64: str
    request_id: str


class ImageProcessResponse(BaseModel):
    face_analysis: dict
    body_analysis: dict
    demographics: dict
    object_scene: dict
    quality_aesthetics: dict
    processing_time_ms: float


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "mock-image-processing-orchestrator"}


@app.post("/api/v1/process", response_model=ImageProcessResponse)
async def process_image(request: ImageProcessRequest):
    """Mock image processing - returns fake but valid data."""
    return ImageProcessResponse(
        face_analysis={
            "face_count": 1,
            "faces": [
                {
                    "bbox": [100.0, 150.0, 200.0, 250.0],
                    "confidence": 0.98,
                    "landmarks": [[120.0, 170.0], [180.0, 170.0]]
                }
            ],
            "gender": "male",
            "gender_confidence": 0.92,
            "age": 28,
            "age_range": [25, 32],
            "race": "asian",
            "race_confidence": 0.87,
            "emotion": "happy",
            "emotion_confidence": 0.91,
            "attractiveness_score": 7.5,
            "facial_structure_score": 8.2
        },
        body_analysis={
            "body_detected": True,
            "body_type": "athletic",
            "body_type_confidence": 0.85,
            "pose_keypoints": [[100.0, 200.0, 0.9], [150.0, 250.0, 0.88]],
            "fashion_items": ["t-shirt", "jeans"],
            "fashion_style": "casual",
            "dressing_score": 6.5
        },
        demographics={
            "skin_tone": "medium",
            "skin_tone_ita": 35.2,
            "ethnicity": "asian",
            "ethnicity_confidence": 0.89
        },
        object_scene={
            "objects": [
                {
                    "label": "person",
                    "confidence": 0.95,
                    "bbox": [50.0, 100.0, 300.0, 500.0]
                },
                {
                    "label": "chair",
                    "confidence": 0.82,
                    "bbox": [400.0, 300.0, 150.0, 200.0]
                }
            ],
            "scene_type": "bedroom",
            "scene_confidence": 0.88,
            "background_type": "indoor",
            "background_quality": "messy"
        },
        quality_aesthetics={
            "image_quality_score": 72.5,
            "aesthetic_score": 6.8,
            "composition_score": 7.2,
            "lighting_quality": "harsh",
            "brightness": 145.3,
            "contrast": 68.9,
            "is_blurry": False,
            "has_filters": True
        },
        processing_time_ms=1234.5
    )


if __name__ == "__main__":
    print("🎭 Starting Mock Image Processing Orchestrator on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)

