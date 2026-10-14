from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..models.schemas import ContentGenerationRequest
from ..services.db_service import db
from ..services.gemini_service import gemini_service

router = APIRouter(prefix="/api/ai", tags=["AI Engine"])

@router.post("/generate-reel")
def generate_reel_script(req: ContentGenerationRequest):
    campaign = db.get_campaign(req.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    result = gemini_service.generate_reel_script(
        campaign=campaign,
        language=req.language,
        platform=req.social_platform
    )
    return result

@router.post("/generate-captions")
def generate_captions(req: ContentGenerationRequest):
    campaign = db.get_campaign(req.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    captions = gemini_service.generate_social_captions(
        campaign=campaign,
        language=req.language,
        platform=req.social_platform
    )
    return {"captions": captions}

@router.post("/accessible-story")
def generate_accessible_story(req: ContentGenerationRequest):
    campaign = db.get_campaign(req.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    result = gemini_service.generate_accessible_story(
        campaign=campaign,
        language=req.language
    )
    return result

@router.post("/audit-draft")
def audit_creator_draft(req: ContentGenerationRequest):
    campaign = db.get_campaign(req.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if not req.creator_draft_text:
        raise HTTPException(status_code=400, detail="Creator draft text is required")

    result = gemini_service.audit_creator_draft(
        campaign=campaign,
        draft_text=req.creator_draft_text
    )
    return result
