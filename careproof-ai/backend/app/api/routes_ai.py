from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any, Optional
from ..models.schemas import ContentGenerationRequest
from ..services.db_service import db
from ..services.gemini_service import gemini_service
from ..config import settings

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

@router.post("/scan-social-story")
async def scan_social_story(
    story_image: Optional[UploadFile] = File(None),
    use_sample: bool = Form(False)
):
    """
    Multimodal Gemini Vision Endpoint:
    Scans a viral social media story or reel flyer (e.g. Instagram Reel, TikTok post),
    extracts patient condition, detects personal UPI payment redirection (e.g. limsontt1@fbl),
    flags missing hospitals and financial targets, and provides a CareProof Trust Diagnostic.
    """
    sample_path = settings.STATIC_DIR / "sample_docs" / "sample_viral_reel_elroy.jpg"
    
    if use_sample or not story_image:
        if not sample_path.exists():
            raise HTTPException(status_code=404, detail="Sample reel image not found")
        with open(sample_path, "rb") as f:
            image_bytes = f.read()
        mime_type = "image/jpeg"
        filename = "sample_viral_reel_elroy.jpg"
    else:
        image_bytes = await story_image.read()
        mime_type = story_image.content_type or "image/jpeg"
        filename = story_image.filename or "uploaded_story.jpg"

    diagnostic = gemini_service.scan_social_story_image(
        image_bytes=image_bytes,
        mime_type=mime_type,
        filename=filename
    )
    return diagnostic
