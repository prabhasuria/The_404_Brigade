import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .services.db_service import db
from .api import (
    campaigns_router,
    donations_router,
    verification_router,
    ai_router,
    hospitals_router
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# Mount API Routers
app.include_router(campaigns_router)
app.include_router(donations_router)
app.include_router(verification_router)
app.include_router(ai_router)
app.include_router(hospitals_router)

# Health Check for Google Cloud Run
@app.get("/healthz")
def health_check():
    return {
        "status": "healthy",
        "service": "CareProof AI",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Frontend Web Page Routes
@app.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    campaigns = db.get_campaigns()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"campaigns": campaigns}
    )

@app.get("/campaign/{campaign_id}", response_class=HTMLResponse)
def campaign_detail_page(request: Request, campaign_id: str):
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    donations = db.get_donations_for_campaign(campaign_id)
    return templates.TemplateResponse(
        request=request,
        name="campaign_detail.html",
        context={"campaign": campaign, "donations": donations}
    )

@app.get("/creator-studio", response_class=HTMLResponse)
def creator_studio_page(request: Request, campaign_id: str = None):
    campaigns = db.get_campaigns()
    selected = db.get_campaign(campaign_id) if campaign_id else (campaigns[0] if campaigns else None)
    return templates.TemplateResponse(
        request=request,
        name="creator_studio.html",
        context={"campaigns": campaigns, "selected_campaign": selected}
    )

@app.get("/verifier", response_class=HTMLResponse)
def verifier_page(request: Request):
    pending = [c for c in db.get_campaigns() if c.status.value in ["PENDING_VERIFICATION", "DRAFT"] or (c.verification and c.verification.human_status == "PENDING")]
    return templates.TemplateResponse(
        request=request,
        name="admin_verifier.html",
        context={"pending_campaigns": pending}
    )

@app.get("/hospital-escrow", response_class=HTMLResponse)
def hospital_escrow_page(request: Request):
    hospitals = db.get_hospitals()
    return templates.TemplateResponse(
        request=request,
        name="hospital_portal.html",
        context={"hospitals": hospitals}
    )

@app.get("/create", response_class=HTMLResponse)
def create_campaign_page(request: Request):
    hospitals = db.get_hospitals()
    return templates.TemplateResponse(
        request=request,
        name="create_campaign.html",
        context={"hospitals": hospitals}
    )
