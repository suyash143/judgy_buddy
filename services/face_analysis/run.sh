#!/bin/bash

# Run Face Analysis Service
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "../../.venv" ]; then
    source ../../.venv/bin/activate
fi

# Set PYTHONPATH to include project root
export PYTHONPATH="${PYTHONPATH}:$(cd ../.. && pwd)"

# Run the service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

