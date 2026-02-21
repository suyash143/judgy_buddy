# Main Orchestrator Service

The main entry point for the Judgy Buddy application. Handles client requests, coordinates with downstream services, and returns the final roast response.

## Responsibilities

- Accept image uploads from clients
- Validate and preprocess images
- Coordinate with Image Processing Orchestrator
- Coordinate with LLM Inferencer
- Return final roast response to client
- Health monitoring of downstream services

## API Endpoints

### POST /api/v1/analyze
Upload an image and get a witty roast.

**Request:**
- Content-Type: `multipart/form-data`
- `image`: Image file (JPEG, PNG, WEBP)
- `roast_level`: Optional, one of "mild", "medium", "savage" (default: "medium")

**Response:**
```json
{
  "request_id": "uuid",
  "roast": "Your witty roast here...",
  "features": { ... },
  "total_processing_time_ms": 5432.1,
  "status": "success"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "main-orchestrator",
  "version": "0.1.0"
}
```

## Running the Service

### Using the run script:
```bash
cd services/main_orchestrator
./run.sh
```

### Using uvicorn directly:
```bash
cd services/main_orchestrator
export PYTHONPATH="${PYTHONPATH}:$(cd ../.. && pwd)"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Using Python module:
```bash
cd judgy_buddy
python -m services.main_orchestrator.app.main
```

## Configuration

Configuration is managed through environment variables or `.env` file. See `.env.example` in the project root.

Key configuration options:
- `PORT`: Service port (default: 8000)
- `IMAGE_PROCESSING_ORCHESTRATOR_URL`: URL of image processing service
- `LLM_INFERENCER_URL`: URL of LLM service
- `MAX_REQUEST_SIZE`: Maximum image size in bytes
- `REQUEST_TIMEOUT`: Timeout for downstream service calls

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- FastAPI - Web framework
- aiohttp - Async HTTP client for service calls
- Pillow - Image processing
- pydantic - Data validation

## Testing

```bash
# Run unit tests
pytest tests/unit/test_main_orchestrator.py -v

# Run with coverage
pytest tests/unit/test_main_orchestrator.py --cov=services.main_orchestrator
```

## Development

The service follows this structure:
- `app/main.py` - FastAPI application setup
- `app/api/routes.py` - API endpoint definitions
- `app/services/orchestrator.py` - Business logic
- `app/models/schemas.py` - Request/response models
- `app/config.py` - Configuration

