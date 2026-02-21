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
| Characteristic | Recommended Model | Size | Notes |
|---------------|-------------------|------|-------|
| **Face Detection** | RetinaFace or MTCNN | ~5-10MB | Fast, accurate, works well on M-series |
| **Gender Classification** | FairFace or UTKFace-trained model | ~100MB | Good accuracy, lightweight |
| **Age Estimation** | FairFace or DEX (Deep EXpectation) | ~100MB | Reasonable accuracy |
| **Facial Structure** | Face landmarks (dlib or MediaPipe) | ~10MB | 68-point or 478-point landmarks |
| **Emotion Detection** | FER2013-trained model or HSEmotion | ~50MB | 7 basic emotions |
| **Attractiveness Rating** | Custom CNN or pre-trained beauty predictor | ~100MB | Subjective, use with caution |

### Body Analysis Service
| Characteristic | Recommended Model | Size | Notes |
|---------------|-------------------|------|-------|
| **Pose Detection** | MediaPipe Pose or OpenPose | ~30MB | Real-time capable on M4 |
| **Body Type** | Custom classifier on pose keypoints | ~50MB | Can build on pose data |
| **Fashion/Dressing** | Fashion-MNIST or DeepFashion model | ~200MB | Clothing classification |

### Demographics Service
| Characteristic | Recommended Model | Size | Notes |
|---------------|-------------------|------|-------|
| **Race/Ethnicity** | FairFace | ~100MB | Handles 7 race categories |
| **Skin Tone** | Color analysis (OpenCV-based) | N/A | Algorithm-based, no model needed |

### Object & Scene Detection Service
| Characteristic | Recommended Model | Size | Notes |
|---------------|-------------------|------|-------|
| **Object Detection** | YOLOv8-nano or YOLOv5s | ~6-15MB | Fast, 80 object classes |
| **Scene Classification** | Places365-CNN (ResNet18) | ~100MB | 365 scene categories |
| **Background Analysis** | U2-Net (background segmentation) | ~176MB | Separate foreground/background |

### Quality & Aesthetics Service
| Characteristic | Recommended Model | Size | Notes |
|---------------|-------------------|------|-------|
| **Image Quality** | BRISQUE or NIMA | ~50MB | No-reference quality assessment |
| **Composition** | Rule-based (rule of thirds, etc.) | N/A | Algorithm-based |
| **Aesthetic Rating** | NIMA (Neural Image Assessment) | ~100MB | Trained on AVA dataset |

### LLM Inferencer Service
| Model | Size (Quantized) | Notes |
|-------|------------------|-------|
| **LLaMA 3.2 3B** | ~2GB (4-bit) | Best balance for M4 Pro, good at creative text |
| **Phi-3 Mini (3.8B)** | ~2.3GB (4-bit) | Microsoft's efficient model, good reasoning |
| **Mistral 7B** | ~4GB (4-bit) | More capable but slower on M4 |
| **Gemma 2B** | ~1.5GB (4-bit) | Lightweight, Google's model |

**Recommendation**: Start with **LLaMA 3.2 3B** or **Phi-3 Mini** using `llama.cpp` or `mlx-lm` for Apple Silicon optimization.

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

## Notes
- All services will run locally on MacBook M4 Pro
- Focus on modularity and scalability
- Each service should be independently deployable
- API contracts need to be well-defined before implementation
- Models should be optimized for Apple Silicon (use MLX, ONNX, or Core ML where possible)
- Parallel processing is key for acceptable response times
- Consider model caching and warm-up strategies

