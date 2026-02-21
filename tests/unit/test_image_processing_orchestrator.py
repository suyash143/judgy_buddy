import pytest
from unittest.mock import AsyncMock, patch
from services.image_processing_orchestrator.app.services.orchestrator import ImageProcessingOrchestrator


@pytest.fixture
def orchestrator():
    """Create an ImageProcessingOrchestrator instance."""
    return ImageProcessingOrchestrator()


@pytest.fixture
def sample_image_base64():
    """Create a sample base64 encoded image string."""
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


@pytest.mark.unit
@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator):
    """Test that orchestrator initializes correctly."""
    assert orchestrator.face_analysis_url is not None
    assert orchestrator.body_analysis_url is not None
    assert orchestrator.demographics_url is not None
    assert orchestrator.object_scene_url is not None
    assert orchestrator.quality_aesthetics_url is not None
    assert orchestrator.timeout is not None
    assert orchestrator.max_concurrent is not None


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
        assert "face_analysis" in health


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_image_success(orchestrator, sample_image_base64):
    """Test successful image processing."""
    with patch.object(orchestrator, "_call_face_analysis", new_callable=AsyncMock) as mock_face:
        # Mock successful face analysis response
        mock_face.return_value = {
            "face_count": 1,
            "gender": "male",
            "age": 25
        }
        
        result = await orchestrator.process_image(sample_image_base64, "test-request-id")
        
        assert "face_analysis" in result
        assert "processing_time_ms" in result
        assert result["face_analysis"]["face_count"] == 1
        assert result["processing_time_ms"] > 0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_image_service_failure(orchestrator, sample_image_base64):
    """Test image processing when a service fails."""
    with patch.object(orchestrator, "_call_face_analysis", new_callable=AsyncMock) as mock_face:
        # Mock service failure
        mock_face.return_value = None
        
        result = await orchestrator.process_image(sample_image_base64, "test-request-id")
        
        assert "face_analysis" in result
        assert result["face_analysis"] is None
        assert "processing_time_ms" in result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_call_service_success(orchestrator):
    """Test successful service call."""
    with patch("aiohttp.ClientSession") as mock_session:
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"result": "success"})
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        result = await orchestrator._call_service(
            url="http://test.com/api",
            payload={"test": "data"},
            service_name="test_service"
        )
        
        assert result == {"result": "success"}


@pytest.mark.unit
@pytest.mark.asyncio
async def test_call_service_timeout(orchestrator):
    """Test service call timeout."""
    with patch("aiohttp.ClientSession") as mock_session:
        # Mock timeout
        mock_session.return_value.__aenter__.return_value.post.side_effect = TimeoutError()
        
        result = await orchestrator._call_service(
            url="http://test.com/api",
            payload={"test": "data"},
            service_name="test_service"
        )
        
        assert result is None


@pytest.mark.unit
def test_sample_image_base64_fixture(sample_image_base64):
    """Test that sample image base64 fixture works."""
    assert isinstance(sample_image_base64, str)
    assert len(sample_image_base64) > 0

