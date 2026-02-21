#!/bin/bash

# Run Quality & Aesthetics Service

cd "$(dirname "$0")/../.."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

source .venv/bin/activate

echo "Starting Quality & Aesthetics Service on port 8006..."
python -m uvicorn services.quality_aesthetics.app.main:app --host 0.0.0.0 --port 8006 --reload

