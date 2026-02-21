# Microservice-Based Image Processing Application

## Project Overview
A microservice architecture application that acts as a **Witty AI Judge/Roaster**. Users upload images (selfies, group photos, etc.), and the system analyzes various characteristics (faces, body structure, dressing, objects, etc.) to generate humorous, witty, and roastful commentary.

**Project Type**: Personal Project
**Constraint**: Self-hosted only - No paid services, using open-source models and free tools
**Hardware**: MacBook M4 Pro (primary development and deployment)

---

## System Architecture

### Microservices

#### 1. **LLM Inferencer Service**
- **Purpose**: Generate witty sentences based on image features
- **Technology**: Python (FastAPI)
- **Model**: Self-hosted open-source LLM - LLaMA
- **API Endpoint**: Local REST API
- **Responsibilities**:
  - Expose inference endpoint
  - Process feature data and generate creative text
  - Handle LLM model loading and inference
- **Status**: 🔴 Not Started

#### 2. **Orchestrator Service**
- **Purpose**: Central coordinator for all client requests
- **Technology**: Python (FastAPI)
- **Responsibilities**:
  - Handle incoming client API calls
  - Process uploaded images
  - Store images (temporary storage)
  - Coordinate between image processing and LLM services
  - Return final response to client
- **Status**: 🔴 Not Started

#### 3. **Image Processing Orchestrator**
- **Purpose**: Coordinate parallel multi-model image analysis
- **Technology**: Python (FastAPI with async processing)
- **Responsibilities**:
  - Receive images from main orchestrator
  - Distribute image to multiple specialized models in parallel
  - Aggregate results from all models
  - Return comprehensive feature data
- **Status**: 🔴 Not Started

#### 4. **Image Processing Models** (Multiple Specialized Services)
- **Purpose**: Extract specific characteristics from images
- **Technology**: Python (FastAPI + PyTorch/ONNX)
- **Models & Characteristics**:

  **4a. Face Analysis Service**
  - Face detection & counting
  - Gender classification
  - Age estimation
  - Facial structure analysis
  - Emotion detection
  - Attractiveness/looks rating

  **4b. Body Analysis Service**
  - Body pose detection
  - Body type classification
  - Fashion/dressing analysis

  **4c. Demographics Service**
  - Race/ethnicity detection
  - Skin tone analysis

  **4d. Object & Scene Detection Service**
  - Object detection (items in image)
  - Scene classification (indoor/outdoor, location type)
  - Background analysis

  **4e. Quality & Aesthetics Service**
  - Image quality assessment
  - Composition analysis
  - Lighting evaluation
  - Overall aesthetic rating

- **Status**: 🔴 Not Started

#### 5. **Web Frontend**
- **Purpose**: User interface for image upload and roast display
- **Technology**: React (with Vite)
- **Features**:
  - Upload button for file selection
  - Camera button for direct photo capture
  - Display processing status with progress indicators
  - Show generated witty roast/commentary
  - Display extracted characteristics (optional debug view)
- **Status**: 🔴 Not Started

---

## Data Flow

```
User (Web Frontend)
    ↓ (Upload Image)
Main Orchestrator Service
    ↓ (Image Data)
Image Processing Orchestrator
    ↓ (Parallel Distribution)
    ├─→ Face Analysis Service ──────┐
    ├─→ Body Analysis Service ───────┤
    ├─→ Demographics Service ─────────┤ (Parallel Processing)
    ├─→ Object Detection Service ────┤
    └─→ Quality/Aesthetics Service ──┘
    ↓ (Aggregated Features)
Image Processing Orchestrator
    ↓ (Comprehensive Feature Data)
Main Orchestrator Service
    ↓ (Feature Data)
LLM Inferencer Service
    ↓ (Witty Roast/Commentary)
Main Orchestrator Service
    ↓ (Final Response)
User (Web Frontend)
```

---

## Technical Stack

### Confirmed Technologies
- **Backend Services**: Python 3.10+
- **API Framework**: FastAPI (async, high-performance)
- **Frontend**: React with Vite
- **LLM**: Self-hosted open-source model (LLaMA 2/3, Mistral, Phi-2, etc.)
- **Vision Models**: Self-hosted (CLIP, BLIP-2, or lightweight CNNs)
- **Image Processing**: OpenCV, Pillow (PIL)
- **ML Framework**: PyTorch or TensorFlow (for model inference)

### Technical Decisions (To Be Determined)

#### Infrastructure
- [ ] Containerization (Docker - recommended for isolation)
- [ ] Orchestration (Docker Compose for local development)
- [ ] Service discovery mechanism (direct HTTP calls vs service mesh)
- [ ] API Gateway (optional - nginx/traefik)

#### Storage
- [ ] Image storage solution (local filesystem recommended)
- [ ] Database for metadata (SQLite/PostgreSQL if needed)
- [ ] Caching strategy (Redis if needed, or in-memory)

#### Model Selection
- [ ] Specific LLM model (LLaMA 3.2 3B or Phi-3 recommended for M4 Pro)
- [ ] Model quantization strategy (4-bit GGUF for LLM, FP16 for vision models)
- [ ] Model optimization for Apple Silicon (MLX, Core ML conversion)

#### Deployment
- [ ] Local development setup
- [ ] Environment management (.venv, conda)
- [ ] Logging framework (Python logging, structlog)

---

## Development Phases

### Phase 1: Setup & Infrastructure
- [ ] Project structure setup
- [ ] Development environment configuration
- [ ] Service skeleton creation

### Phase 2: Core Services Development
- [ ] Image Processing Engine implementation
- [ ] LLM Inferencer Service implementation
- [ ] Orchestrator Service implementation
- [ ] Inter-service communication setup

### Phase 3: Frontend Development
- [ ] Web interface design
- [ ] Upload functionality
- [ ] Camera capture functionality
- [ ] Response display

### Phase 4: Integration & Testing
- [ ] End-to-end integration
- [ ] Testing (unit, integration, e2e)
- [ ] Performance optimization

### Phase 5: Deployment & Documentation
- [ ] Deployment setup
- [ ] Documentation
- [ ] Monitoring setup

---

## Next Steps
1. Discuss detailed requirements for each service
2. Finalize technology stack
3. Define API contracts between services
4. Set up project structure
5. Begin implementation

---

## Model Recommendations for Each Characteristic

### Face Analysis Service
| Characteristic | Suggested Models | Selected Model ✅ | Size | Notes |
|---------------|------------------|------------------|------|-------|
| **Face Detection** | RetinaFace, MTCNN, YuNet | **YuNet (OpenCV)** | ~300KB | Ultra-fast, built into OpenCV, excellent for M4 |
| **Gender Classification** | FairFace, UTKFace-trained | **FairFace** | ~100MB | Best accuracy, handles multiple attributes |
| **Age Estimation** | FairFace, DEX | **FairFace** | ~100MB | Same model as gender, efficient |
| **Facial Structure** | dlib 68-point, MediaPipe Face Mesh | **MediaPipe Face Mesh** | ~10MB | 478 landmarks, very detailed, optimized |
| **Emotion Detection** | FER2013, HSEmotion, DeepFace | **HSEmotion** | ~50MB | Better accuracy than FER2013, 8 emotions |
| **Attractiveness Rating** | SCUT-FBP, R2-ResNeXt | **SCUT-FBP5500** | ~100MB | Research-backed, Asian + Caucasian trained |

### Body Analysis Service
| Characteristic | Suggested Models | Selected Model ✅ | Size | Notes |
|---------------|------------------|------------------|------|-------|
| **Pose Detection** | MediaPipe Pose, OpenPose, MoveNet | **MediaPipe Pose** | ~30MB | 33 keypoints, real-time on M4, Google-maintained |
| **Body Type** | Custom classifier, BodyNet | **Custom CNN on Pose** | ~50MB | Build on MediaPipe keypoints + ratios |
| **Fashion/Dressing** | DeepFashion, Fashion++, ClothingNet | **DeepFashion2** | ~200MB | Multi-attribute clothing recognition |

### Demographics Service
| Characteristic | Suggested Models | Selected Model ✅ | Size | Notes |
|---------------|------------------|------------------|------|-------|
| **Race/Ethnicity** | FairFace, DeepFace | **FairFace** | ~100MB | 7 categories, same model as age/gender |
| **Skin Tone** | OpenCV LAB color, Monk Skin Tone Scale | **OpenCV LAB + ITA°** | N/A | Algorithm-based, Individual Typology Angle |

### Object & Scene Detection Service
| Characteristic | Suggested Models | Selected Model ✅ | Size | Notes |
|---------------|------------------|------------------|------|-------|
| **Object Detection** | YOLOv8-nano, YOLOv10-nano, YOLOv5s | **YOLOv8-nano** | ~6MB | 80 COCO classes, fastest, Ultralytics maintained |
| **Scene Classification** | Places365-ResNet18, MobileNetV3 | **Places365-ResNet18** | ~100MB | 365 scene categories, good accuracy |
| **Background Analysis** | U2-Net, MODNet, RVM | **MODNet** | ~25MB | Lighter than U2-Net, real-time capable |

### Quality & Aesthetics Service
| Characteristic | Suggested Models | Selected Model ✅ | Size | Notes |
|---------------|------------------|------------------|------|-------|
| **Image Quality** | BRISQUE, NIMA-Quality, MUSIQ | **BRISQUE (OpenCV)** | Built-in | No-reference, fast, no neural network needed |
| **Composition** | Rule of thirds, Golden ratio | **Rule-based Algorithm** | N/A | Detect faces/objects position, symmetry |
| **Aesthetic Rating** | NIMA-Aesthetic, AVA-MLSP | **NIMA-MobileNet** | ~17MB | Lightweight version, AVA dataset trained |
| **Lighting Quality** | Custom analysis | **OpenCV Histogram** | N/A | Brightness, contrast, exposure analysis |

### LLM Inferencer Service
| Model | Size (Quantized) | Selected Model ✅ | Inference Library | Notes |
|-------|------------------|------------------|-------------------|-------|
| **LLaMA 3.2 3B Instruct** | ~2GB (4-bit) | ✅ **PRIMARY** | **mlx-lm** | Best for M4 Pro, creative, Apple Silicon optimized |
| **Phi-3.5 Mini (3.8B)** | ~2.3GB (4-bit) | **BACKUP** | mlx-lm / llama.cpp | Microsoft's model, excellent reasoning |
| **Qwen2.5 3B Instruct** | ~2GB (4-bit) | **ALTERNATIVE** | mlx-lm | Alibaba's model, multilingual, creative |
| **Mistral 7B Instruct** | ~4GB (4-bit) | Future upgrade | mlx-lm | More capable but slower |
| **Gemma 2B** | ~1.5GB (4-bit) | Too small | mlx-lm | Lightweight but less creative |

**Selected**: **LLaMA 3.2 3B Instruct** with **mlx-lm** (Apple's MLX framework for M-series chips)
- Optimized for Apple Silicon with unified memory
- Fast inference (~20-30 tokens/sec on M4 Pro)
- Excellent at creative, witty text generation
- 4-bit quantization keeps memory under 2GB

---

## Additional Characteristics to Extract for Better Roasts

### Environmental Context
- **Lighting quality** (harsh, flattering, poor)
- **Photo setting** (bathroom mirror, gym, car, bedroom)
- **Time of day** (if EXIF data available)
- **Photo angle** (high angle, low angle, straight-on)

### Photo Quality Indicators
- **Blur/sharpness**
- **Filters applied** (over-saturated, heavy filters)
- **Selfie vs. professional photo**
- **Mirror selfie detection**

### Behavioral/Contextual Cues
- **Facial expression** (duck face, serious, smiling)
- **Hand gestures** (peace sign, pointing, etc.)
- **Group dynamics** (who's in center, who's cut off)
- **Props/accessories** (sunglasses, hats, phones)

### Composition Issues
- **Cropping problems** (heads cut off, too much empty space)
- **Background distractions** (messy room, toilet visible)
- **Photo orientation** (tilted, upside down)

---

---

## 📦 Finalized Model Stack Summary

### Core Models Selected
1. **YuNet** - Face Detection (300KB)
2. **FairFace** - Gender, Age, Race/Ethnicity (100MB) - *Single model for 3 tasks!*
3. **MediaPipe Face Mesh** - Facial Structure (10MB, 478 landmarks)
4. **HSEmotion** - Emotion Detection (50MB, 8 emotions)
5. **SCUT-FBP5500** - Attractiveness Rating (100MB)
6. **MediaPipe Pose** - Body Pose Detection (30MB, 33 keypoints)
7. **Custom CNN** - Body Type Classification (50MB, built on pose data)
8. **DeepFashion2** - Fashion/Dressing Analysis (200MB)
9. **OpenCV LAB + ITA°** - Skin Tone Analysis (algorithm-based)
10. **YOLOv8-nano** - Object Detection (6MB, 80 classes)
11. **Places365-ResNet18** - Scene Classification (100MB, 365 scenes)
12. **MODNet** - Background Segmentation (25MB)
13. **BRISQUE** - Image Quality (OpenCV built-in)
14. **NIMA-MobileNet** - Aesthetic Rating (17MB)
15. **Rule-based Algorithms** - Composition & Lighting (no model)
16. **LLaMA 3.2 3B Instruct** - Witty Roast Generation (2GB quantized, via mlx-lm)

### Total Model Size
- **Vision Models**: ~688MB (excluding algorithms)
- **LLM**: ~2GB (4-bit quantized)
- **Total**: ~2.7GB (easily fits in M4 Pro memory)

### Key Libraries & Frameworks
- **mlx-lm** - LLM inference on Apple Silicon
- **OpenCV** - Image processing, YuNet, BRISQUE
- **MediaPipe** - Face mesh, pose detection
- **Ultralytics** - YOLOv8
- **PyTorch** - Model inference for custom models
- **FastAPI** - All service APIs
- **aiohttp** - Async HTTP for inter-service communication

---

## Notes
- All services will run locally on MacBook M4 Pro
- Focus on modularity and scalability
- Each service should be independently deployable
- API contracts need to be well-defined before implementation
- Models should be optimized for Apple Silicon (use MLX, ONNX, or Core ML where possible)
- Parallel processing is key for acceptable response times (~5-15 seconds target)
- Consider model caching and warm-up strategies
- FairFace efficiency: Single model handles gender, age, AND race detection!

