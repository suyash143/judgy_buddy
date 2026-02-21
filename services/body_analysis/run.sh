#!/bin/bash

# Run Body Analysis Service

cd "$(dirname "$0")/../.."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

source .venv/bin/activate

echo "Starting Body Analysis Service on port 8003..."
python -m uvicorn services.body_analysis.app.main:app --host 0.0.0.0 --port 8003 --reload

