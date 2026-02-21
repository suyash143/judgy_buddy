import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from PIL import Image
from services.main_orchestrator.app.services.orchestrator import OrchestratorService
from libs.common.schemas import (
    AggregatedImageFeatures,
    FaceAnalysisResult,
    AnalyzeImageResponse
)


@pytest.fixture
def orchestrator():
    """Create an OrchestratorService instance."""
    return OrchestratorService()


@pytest.fixture
def sample_image():
    """Create a sample PIL Image."""
    return Image.new("RGB", (100, 100), color="red")


@pytest.fixture
def sample_features():
    """Create sample aggregated features."""
    return AggregatedImageFeatures(
        face_analysis=FaceAnalysisResult(
            face_count=1,
            faces=[],
            gender="male",
            gender_confidence=0.9,
            age=25,
            age_range=(20, 30),
            race="asian",
            race_confidence=0.85,
            emotion="happy",
            emotion_confidence=0.88,
            attractiveness_score=7.5,
            facial_structure_score=8.0
        ),
        processing_time_ms=1000.0
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator):
    """Test that orchestrator initializes correctly."""
    assert orchestrator.image_processing_url is not None
    assert orchestrator.llm_url is not None
    assert orchestrator.timeout is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_health_check(orchestrator):
    """Test health check functionality."""
    with patch("aiohttp.ClientSession") as mock_session:
        # Mock successful health checks
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        
        health = await orchestrator.health_check()
        
        assert isinstance(health, dict)
        assert "image_processing_orchestrator" in health
        assert "llm_inferencer" in health


@pytest.mark.unit
def test_sample_image_fixture(sample_image):
    """Test that sample image fixture works."""
    assert isinstance(sample_image, Image.Image)
    assert sample_image.size == (100, 100)
    assert sample_image.mode == "RGB"


@pytest.mark.unit
def test_sample_features_fixture(sample_features):
    """Test that sample features fixture works."""
    assert isinstance(sample_features, AggregatedImageFeatures)
    assert sample_features.face_analysis is not None
    assert sample_features.face_analysis.face_count == 1

