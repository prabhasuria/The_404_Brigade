import uvicorn
import os
import sys
from pathlib import Path

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

from app.config import settings

if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.PORT))
    host = os.environ.get("HOST", settings.HOST)
    print("=" * 65)
    print(" 🏥 CareProof AI — Transparent Social Media Fundraising")
    print(" Google H2S Hackathon Prototype | The 404 Brigade")
    print(f" Server running at: http://{host}:{port}")
    print(" Features Active: Gemini 2.0 AI, Direct Escrow, Overfunding Lock")
    print("=" * 65)
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
