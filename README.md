# Judgy Buddy - We the Judger

A microservice-based application that analyzes uploaded images and generates witty, humorous roasts using AI.

## 🎯 Project Overview

Judgy Buddy is a personal project that combines computer vision and large language models to create an entertaining image analysis and roasting system. Upload a photo, and get roasted!

## 🏗️ Architecture

The application consists of 7 microservices:

1. **Main Orchestrator** - Handles client requests and coordinates services
2. **Image Processing Orchestrator** - Distributes images to specialized analyzers
3. **Face Analysis Service** - Detects faces, analyzes gender, age, emotions, attractiveness
4. **Body Analysis Service** - Analyzes body pose, type, and fashion
5. **Demographics Service** - Analyzes race/ethnicity and skin tone
6. **Object & Scene Detection** - Detects objects and classifies scenes
7. **Quality & Aesthetics Service** - Evaluates image quality and composition
8. **LLM Inferencer** - Generates witty roasts based on all extracted features

## 🚀 Tech Stack

- **Backend**: Python 3.10+, FastAPI
- **Frontend**: React + Vite
- **ML Models**: See [PROJECT_PLANNING.md](PROJECT_PLANNING.md) for detailed model list
- **LLM**: LLaMA 3.2 3B Instruct (via mlx-lm)
- **Deployment**: Docker + Docker Compose

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 18+ (for frontend)
- macOS with Apple Silicon (M-series) recommended
- 16GB+ RAM recommended

## 🛠️ Setup

### 1. Create Python Virtual Environment

```bash
cd judgy_buddy
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -e ".[dev]"
```

### 3. Download Models

(Instructions will be added as we implement each service)

### 4. Run Services

```bash
# Using Docker Compose (recommended)
docker-compose up

# Or run individual services
cd services/main_orchestrator
uvicorn app.main:app --reload --port 8000
```

## 📁 Project Structure

See [PROJECT_PLANNING.md](PROJECT_PLANNING.md) for complete architecture and planning details.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## 📝 Development Guidelines

- Follow PEP 8 style guide
- Use type hints for all functions
- Write tests for all new features
- Run `mypy` and `ruff` before committing
- Keep services modular and independent

## 🤝 Contributing

This is a personal project, but suggestions and ideas are welcome!

## 📄 License

MIT License - Feel free to use for learning purposes

## ⚠️ Disclaimer

This application is for entertainment purposes only. The "roasts" are AI-generated and should not be taken seriously.

