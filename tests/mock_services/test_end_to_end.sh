#!/bin/bash

# End-to-end test script for Main Orchestrator with mock services
echo "🧪 Testing Main Orchestrator End-to-End"
echo "========================================"
echo ""

# Check if Main Orchestrator is running
echo "1️⃣  Checking Main Orchestrator health..."
HEALTH=$(curl -s http://localhost:8000/health)
echo "Response: $HEALTH"
echo ""

# Check if mock services are running
echo "2️⃣  Checking Mock Image Processing Orchestrator..."
MOCK_IPO=$(curl -s http://localhost:8001/health)
echo "Response: $MOCK_IPO"
echo ""

echo "3️⃣  Checking Mock LLM Inferencer..."
MOCK_LLM=$(curl -s http://localhost:8007/health)
echo "Response: $MOCK_LLM"
echo ""

# Create a test image
echo "4️⃣  Creating test image..."
python3 << 'EOF'
from PIL import Image
import io

# Create a simple test image
img = Image.new('RGB', (400, 400), color='red')
img.save('/tmp/test_image.jpg', 'JPEG')
print("✅ Test image created: /tmp/test_image.jpg")
EOF
echo ""

# Test the analyze endpoint with mild roast
echo "5️⃣  Testing /api/v1/analyze endpoint (mild roast)..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analyze \
  -F "image=@/tmp/test_image.jpg" \
  -F "roast_level=mild")
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Test with medium roast
echo "6️⃣  Testing /api/v1/analyze endpoint (medium roast)..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analyze \
  -F "image=@/tmp/test_image.jpg" \
  -F "roast_level=medium")
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Test with savage roast
echo "7️⃣  Testing /api/v1/analyze endpoint (savage roast)..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analyze \
  -F "image=@/tmp/test_image.jpg" \
  -F "roast_level=savage")
echo "$RESPONSE" | python3 -m json.tool
echo ""

echo "✅ End-to-end testing complete!"
echo ""
echo "🎉 If you see roast responses above, the Main Orchestrator is working correctly!"

