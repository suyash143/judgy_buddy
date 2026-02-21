#!/bin/bash

# Start all services for I Judge application

echo "Starting all I Judge services..."
echo "================================"

# Activate virtual environment
source .venv/bin/activate

# Start services in background
echo "Starting Main Orchestrator (port 8000)..."
python -m uvicorn services.main_orchestrator.app.main:app --host 0.0.0.0 --port 8000 &
MAIN_PID=$!

echo "Starting Image Processing Orchestrator (port 8001)..."
python -m uvicorn services.image_processing_orchestrator.app.main:app --host 0.0.0.0 --port 8001 &
IMG_PROC_PID=$!

echo "Starting Face Analysis (port 8002)..."
python -m uvicorn services.face_analysis.app.main:app --host 0.0.0.0 --port 8002 &
FACE_PID=$!

echo "Starting Body Analysis (port 8003)..."
python -m uvicorn services.body_analysis.app.main:app --host 0.0.0.0 --port 8003 &
BODY_PID=$!

echo "Starting Demographics (port 8004)..."
python -m uvicorn services.demographics.app.main:app --host 0.0.0.0 --port 8004 &
DEMO_PID=$!

echo "Starting Object & Scene Detection (port 8005)..."
python -m uvicorn services.object_scene_detection.app.main:app --host 0.0.0.0 --port 8005 &
OBJ_PID=$!

echo "Starting Quality & Aesthetics (port 8006)..."
python -m uvicorn services.quality_aesthetics.app.main:app --host 0.0.0.0 --port 8006 &
QUAL_PID=$!

echo "Starting LLM Inferencer (port 8007)..."
python -m uvicorn services.llm_inferencer.app.main:app --host 0.0.0.0 --port 8007 &
LLM_PID=$!

echo ""
echo "All services started!"
echo "================================"
echo "Main Orchestrator:        http://localhost:8000"
echo "Image Proc Orchestrator:  http://localhost:8001"
echo "Face Analysis:            http://localhost:8002"
echo "Body Analysis:            http://localhost:8003"
echo "Demographics:             http://localhost:8004"
echo "Object & Scene:           http://localhost:8005"
echo "Quality & Aesthetics:     http://localhost:8006"
echo "LLM Inferencer:           http://localhost:8007"
echo ""
echo "Frontend: cd frontend && npm run dev"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "echo 'Stopping all services...'; kill $MAIN_PID $IMG_PROC_PID $FACE_PID $BODY_PID $DEMO_PID $OBJ_PID $QUAL_PID $LLM_PID 2>/dev/null; exit" INT

wait

