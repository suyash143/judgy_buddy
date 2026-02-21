#!/usr/bin/env python3
"""Mock LLM Inferencer for testing Main Orchestrator."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Any
import uvicorn


app = FastAPI(title="Mock LLM Inferencer")


class LLMGenerateRequest(BaseModel):
    features: dict[str, Any]
    roast_level: str = "medium"


class LLMGenerateResponse(BaseModel):
    roast_text: str
    confidence: Optional[float] = None
    generation_time_ms: Optional[float] = None


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "mock-llm-inferencer"}


@app.post("/api/v1/generate", response_model=LLMGenerateResponse)
async def generate_roast(request: LLMGenerateRequest):
    """Mock LLM generation - returns witty roasts based on roast level."""
    
    roasts = {
        "mild": (
            "Well, well, well... looks like someone tried their best today! "
            "That casual outfit says 'I woke up like this' but your messy bedroom "
            "background says 'I actually woke up like this.' At least you're consistent! "
            "7.5/10 for authenticity, though. 😊"
        ),
        "medium": (
            "Oh honey, that bedroom background is working harder than your fashion sense! "
            "I see you went for the 'athletic casual' look - very brave considering that "
            "harsh lighting is exposing EVERYTHING. Your face says 'happy' but that "
            "messy room says 'gave up 3 weeks ago.' But hey, at least you're a solid 7.5 "
            "in the looks department, so you've got that going for you! 😏"
        ),
        "savage": (
            "YIKES. So you're telling me you're 28, scored a 7.5 in attractiveness, "
            "and THIS is the best photo you could produce?! That bedroom looks like a "
            "tornado had a fight with a laundry basket and lost. The harsh lighting is "
            "doing you NO favors - it's like you WANTED us to see every flaw. "
            "And that 'casual' outfit? More like 'I've given up on life' chic. "
            "At least your face is naturally happy, because that room sure isn't giving "
            "anyone joy. Clean your room, fix that lighting, and maybe - MAYBE - "
            "you'll crack an 8. But today? This ain't it, chief. 💀"
        )
    }
    
    roast_level = request.roast_level.lower()
    roast_text = roasts.get(roast_level, roasts["medium"])
    
    return LLMGenerateResponse(
        roast_text=roast_text,
        confidence=0.92,
        generation_time_ms=856.3
    )


if __name__ == "__main__":
    print("🤖 Starting Mock LLM Inferencer on port 8007...")
    uvicorn.run(app, host="0.0.0.0", port=8007)

