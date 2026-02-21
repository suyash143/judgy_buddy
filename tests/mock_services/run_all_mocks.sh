#!/bin/bash

# Run all mock services for testing
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "../../.venv" ]; then
    source ../../.venv/bin/activate
fi

echo "🎭 Starting Mock Services..."
echo ""

# Start mock services in background
echo "Starting Mock Image Processing Orchestrator on port 8001..."
python mock_image_processing_orchestrator.py &
MOCK_IPO_PID=$!

sleep 2

echo "Starting Mock LLM Inferencer on port 8007..."
python mock_llm_inferencer.py &
MOCK_LLM_PID=$!

sleep 2

echo ""
echo "✅ Mock services started!"
echo "   - Image Processing Orchestrator: http://localhost:8001"
echo "   - LLM Inferencer: http://localhost:8007"
echo ""
echo "PIDs: IPO=$MOCK_IPO_PID, LLM=$MOCK_LLM_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping mock services...'; kill $MOCK_IPO_PID $MOCK_LLM_PID 2>/dev/null; exit 0" INT

wait

