#!/bin/bash

# Run Object & Scene Detection Service

cd "$(dirname "$0")/../.."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

source .venv/bin/activate

echo "Starting Object & Scene Detection Service on port 8005..."
python -m uvicorn services.object_scene_detection.app.main:app --host 0.0.0.0 --port 8005 --reload

