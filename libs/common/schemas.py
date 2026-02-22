from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    UNKNOWN = "unknown"


class Race(str, Enum):
    WHITE = "white"
    BLACK = "black"
    ASIAN = "asian"
    INDIAN = "indian"
    LATINO_HISPANIC = "latino_hispanic"
    MIDDLE_EASTERN = "middle_eastern"
    SOUTHEAST_ASIAN = "southeast_asian"
    UNKNOWN = "unknown"


class Emotion(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    FEARFUL = "fearful"
    DISGUSTED = "disgusted"
    NEUTRAL = "neutral"
    CONTEMPT = "contempt"


class BodyType(str, Enum):
    SLIM = "slim"
    ATHLETIC = "athletic"
    AVERAGE = "average"
    CURVY = "curvy"
    PLUS_SIZE = "plus_size"
    UNKNOWN = "unknown"


class FaceDetection(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    bbox: List[float] = Field(..., description="Bounding box [x, y, width, height]")
    confidence: float = Field(..., ge=0.0, le=1.0)
    landmarks: Optional[List[List[float]]] = Field(None, description="Facial landmarks coordinates")


class FaceAnalysisResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    face_count: int = Field(..., ge=0)
    faces: List[FaceDetection] = Field(default_factory=list)
    gender: Optional[Gender] = None
    gender_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    race: Optional[Race] = None
    race_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    emotion: Optional[Emotion] = None
    emotion_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    attractiveness_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    facial_structure_score: Optional[float] = Field(None, ge=0.0, le=10.0)


class BodyAnalysisResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    body_detected: bool
    body_type: Optional[BodyType] = None
    body_type_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    pose_keypoints: Optional[List[List[float]]] = Field(None, description="Body pose keypoints")
    fashion_items: List[str] = Field(default_factory=list, description="Detected clothing items")
    fashion_style: Optional[str] = None
    dressing_score: Optional[float] = Field(None, ge=0.0, le=10.0, description="Fashion rating")


class DemographicsResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    skin_tone: Optional[str] = Field(None, description="Skin tone category")
    skin_tone_ita: Optional[float] = Field(None, description="ITA degree value")
    ethnicity: Optional[Race] = None
    ethnicity_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class ObjectDetection(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: List[float] = Field(..., description="Bounding box [x, y, width, height]")


class ObjectSceneResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    objects: List[ObjectDetection] = Field(default_factory=list)
    scene_type: Optional[str] = Field(None, description="Scene classification")
    scene_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    background_type: Optional[str] = Field(None, description="Indoor/outdoor/etc")
    background_quality: Optional[str] = Field(None, description="Clean/messy/etc")


class QualityAestheticsResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    image_quality_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    aesthetic_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    composition_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    lighting_quality: Optional[str] = Field(None, description="Good/poor/harsh/etc")
    brightness: Optional[float] = Field(None, ge=0.0, le=255.0)
    contrast: Optional[float] = Field(None, ge=0.0, le=255.0)
    is_blurry: Optional[bool] = None
    has_filters: Optional[bool] = None


class VLMSceneAnalysisRequest(BaseModel):
    """Request for VLM scene analysis."""
    image_base64: str
    request_id: str


class VLMSceneAnalysisResponse(BaseModel):
    """Response from VLM scene analysis."""
    scene_description: str = Field(..., description="Comprehensive scene description from VLM")
    processing_time_ms: Optional[float] = None


class AggregatedImageFeatures(BaseModel):
    model_config = ConfigDict(frozen=True)

    face_analysis: Optional[FaceAnalysisResult] = None
    vlm_scene_analysis: Optional[str] = Field(None, description="VLM comprehensive scene description")
    # Deprecated fields (will be removed after VLM integration)
    body_analysis: Optional[BodyAnalysisResult] = None
    demographics: Optional[DemographicsResult] = None
    object_scene: Optional[ObjectSceneResult] = None
    quality_aesthetics: Optional[QualityAestheticsResult] = None
    processing_time_ms: Optional[float] = None


class RoastRequest(BaseModel):
    features: AggregatedImageFeatures
    roast_level: Optional[str] = Field("medium", description="mild/medium/savage")


class RoastResponse(BaseModel):
    roast_text: str
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    generation_time_ms: Optional[float] = None


class AnalyzeImageResponse(BaseModel):
    request_id: str
    roast: str
    features: Optional[AggregatedImageFeatures] = None
    total_processing_time_ms: float
    status: str = "success"

