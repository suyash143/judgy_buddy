# API Contracts - Judgy Buddy

This document defines all API endpoints and contracts between microservices.

## Service Ports

| Service | Port | Base URL |
|---------|------|----------|
| Main Orchestrator | 8000 | http://localhost:8000 |
| Image Processing Orchestrator | 8001 | http://localhost:8001 |
| Face Analysis | 8002 | http://localhost:8002 |
| Body Analysis | 8003 | http://localhost:8003 |
| Demographics | 8004 | http://localhost:8004 |
| Object & Scene Detection | 8005 | http://localhost:8005 |
| Quality & Aesthetics | 8006 | http://localhost:8006 |
| LLM Inferencer | 8007 | http://localhost:8007 |

---

## 1. Main Orchestrator API (Public-Facing)

### POST /api/v1/analyze
**Description**: Upload an image and get a witty roast

**Request**:
- Content-Type: `multipart/form-data`
- Body:
  - `image`: File (required) - Image file (JPEG, PNG)
  - `roast_level`: String (optional) - "mild", "medium", "savage" (default: "medium")

**Response**: `200 OK`
```json
{
  "request_id": "uuid-string",
  "roast": "Your witty roast text here...",
  "features": {
    "face_analysis": { ... },
    "body_analysis": { ... },
    "demographics": { ... },
    "object_scene": { ... },
    "quality_aesthetics": { ... }
  },
  "total_processing_time_ms": 5432.1,
  "status": "success"
}
```

**Error Response**: `400/500`
```json
{
  "detail": "Error message",
  "status": "error"
}
```

### GET /health
**Description**: Health check endpoint

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "service": "main_orchestrator",
  "version": "0.1.0"
}
```

---

## 2. Image Processing Orchestrator API (Internal)

### POST /api/v1/process
**Description**: Process image through all analysis models in parallel

**Request**:
- Content-Type: `application/json`
- Body:
```json
{
  "image_base64": "base64-encoded-image-string",
  "request_id": "uuid-string"
}
```

**Response**: `200 OK`
```json
{
  "face_analysis": { ... },
  "body_analysis": { ... },
  "demographics": { ... },
  "object_scene": { ... },
  "quality_aesthetics": { ... },
  "processing_time_ms": 3421.5
}
```

### GET /health
Health check endpoint (same format as above)

---

## 3. Face Analysis Service API (Internal)

### POST /api/v1/analyze
**Description**: Analyze faces in the image

**Request**:
```json
{
  "image_base64": "base64-encoded-image-string"
}
```

**Response**: `200 OK`
```json
{
  "face_count": 1,
  "faces": [
    {
      "bbox": [100, 150, 200, 250],
      "confidence": 0.98,
      "landmarks": [[x1, y1], [x2, y2], ...]
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
}
```

### GET /health
Health check endpoint

---

## 4. Body Analysis Service API (Internal)

### POST /api/v1/analyze
**Description**: Analyze body pose, type, and fashion

**Request**:
```json
{
  "image_base64": "base64-encoded-image-string"
}
```

**Response**: `200 OK`
```json
{
  "body_detected": true,
  "body_type": "athletic",
  "body_type_confidence": 0.85,
  "pose_keypoints": [[x1, y1, conf1], [x2, y2, conf2], ...],
  "fashion_items": ["t-shirt", "jeans", "sneakers"],
  "fashion_style": "casual",
  "dressing_score": 6.5
}
```

### GET /health
Health check endpoint

---

## 5. Demographics Service API (Internal)

### POST /api/v1/analyze
**Description**: Analyze demographics (race, skin tone)

**Request**:
```json
{
  "image_base64": "base64-encoded-image-string"
}
```

**Response**: `200 OK`
```json
{
  "skin_tone": "medium",
  "skin_tone_ita": 35.2,
  "ethnicity": "asian",
  "ethnicity_confidence": 0.89
}
```

### GET /health
Health check endpoint

---

## 6. Object & Scene Detection Service API (Internal)

### POST /api/v1/analyze
**Description**: Detect objects and classify scene

**Request**:
```json
{
  "image_base64": "base64-encoded-image-string"
}
```

**Response**: `200 OK`
```json
{
  "objects": [
    {
      "label": "person",
      "confidence": 0.95,
      "bbox": [50, 100, 300, 500]
    },
    {
      "label": "chair",
      "confidence": 0.82,
      "bbox": [400, 300, 150, 200]
    }
  ],
  "scene_type": "bedroom",
  "scene_confidence": 0.88,
  "background_type": "indoor",
  "background_quality": "messy"
}
```

### GET /health
Health check endpoint

---

## 7. Quality & Aesthetics Service API (Internal)

### POST /api/v1/analyze
**Description**: Evaluate image quality and aesthetics

**Request**:
```json
{
  "image_base64": "base64-encoded-image-string"
}
```

**Response**: `200 OK`
```json
{
  "image_quality_score": 72.5,
  "aesthetic_score": 6.8,
  "composition_score": 7.2,
  "lighting_quality": "harsh",
  "brightness": 145.3,
  "contrast": 68.9,
  "is_blurry": false,
  "has_filters": true
}
```

### GET /health
Health check endpoint

---

## 8. LLM Inferencer Service API (Internal)

### POST /api/v1/generate
**Description**: Generate witty roast from image features

**Request**:
```json
{
  "features": {
    "face_analysis": { ... },
    "body_analysis": { ... },
    "demographics": { ... },
    "object_scene": { ... },
    "quality_aesthetics": { ... }
  },
  "roast_level": "medium"
}
```

**Response**: `200 OK`
```json
{
  "roast_text": "Your generated witty roast here...",
  "confidence": 0.92,
  "generation_time_ms": 1234.5
}
```

### GET /health
Health check endpoint

---

## Data Flow Sequence

```
1. Client → Main Orchestrator: POST /api/v1/analyze (multipart/form-data)
2. Main Orchestrator → Image Processing Orchestrator: POST /api/v1/process (JSON with base64 image)
3. Image Processing Orchestrator → [Parallel Calls]:
   - Face Analysis: POST /api/v1/analyze
   - Body Analysis: POST /api/v1/analyze
   - Demographics: POST /api/v1/analyze
   - Object & Scene: POST /api/v1/analyze
   - Quality & Aesthetics: POST /api/v1/analyze
4. Image Processing Orchestrator ← [Aggregated Results]
5. Main Orchestrator ← Image Processing Orchestrator: Aggregated features
6. Main Orchestrator → LLM Inferencer: POST /api/v1/generate
7. Main Orchestrator ← LLM Inferencer: Roast text
8. Client ← Main Orchestrator: Final response with roast + features
```

---

## Error Handling

All services should return consistent error responses:

**4xx Client Errors**:
```json
{
  "detail": "Descriptive error message",
  "status": "error",
  "error_code": "INVALID_IMAGE_FORMAT"
}
```

**5xx Server Errors**:
```json
{
  "detail": "Internal server error message",
  "status": "error",
  "error_code": "MODEL_INFERENCE_FAILED"
}
```

---

## Common Headers

All requests between services should include:
- `X-Request-ID`: UUID for request tracing
- `Content-Type`: `application/json` (except main orchestrator upload endpoint)
- `User-Agent`: `judgy-buddy/{service-name}/0.1.0`

---

## Rate Limiting & Timeouts

- **Client → Main Orchestrator**: 10 requests/minute per IP
- **Inter-service timeouts**: 30 seconds
- **LLM generation timeout**: 60 seconds
- **Image processing timeout**: 45 seconds

