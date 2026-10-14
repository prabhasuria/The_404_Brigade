from .routes_campaigns import router as campaigns_router
from .routes_donations import router as donations_router
from .routes_verification import router as verification_router
from .routes_ai import router as ai_router
from .routes_hospitals import router as hospitals_router

__all__ = [
    "campaigns_router",
    "donations_router",
    "verification_router",
    "ai_router",
    "hospitals_router"
]
