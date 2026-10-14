import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the careproof project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "CareProof AI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Transparent Social Media Fundraising with AI Verification, Escrow Routing & Overfunding Protection"
    
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Firebase / Firestore
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "careproof-ai-h2s")
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL", "")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY", "")
    
    # Payment Provider (Stripe / Razorpay)
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "sk_test_careproof_mock")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock")
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "rzp_test_mock")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "mock_secret")
    
    # Storage and paths
    DATA_DIR: Path = BASE_DIR / "data"
    STATIC_DIR: Path = Path(__file__).resolve().parent / "static"
    TEMPLATES_DIR: Path = Path(__file__).resolve().parent / "templates"
    
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
