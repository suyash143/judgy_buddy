#!/bin/bash

# Run Demographics Service

cd "$(dirname "$0")/../.."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

source .venv/bin/activate

echo "Starting Demographics Service on port 8004..."
python -m uvicorn services.demographics.app.main:app --host 0.0.0.0 --port 8004 --reload

