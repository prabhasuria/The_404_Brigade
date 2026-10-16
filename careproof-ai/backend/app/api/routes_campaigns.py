import re
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from typing import List, Optional, Dict, Any
from pathlib import Path
from ..models.schemas import Campaign, CampaignStatus, SurplusPolicyType, SupportingDocument
from ..services.db_service import db
from ..services.gemini_service import gemini_service
from ..config import settings

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])

@router.get("", response_model=List[Campaign])
def list_campaigns(status: Optional[CampaignStatus] = None):
    return db.get_campaigns(status=status)

@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: str):
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.get("/{campaign_id}/live-status")
def get_campaign_live_status(campaign_id: str) -> Dict[str, Any]:
    """
    Real-Time Tracking Endpoint:
    Returns the real-time financial status, overfunding lock state,
    and recent verified ledger settlements for multi-client synchronization.
    """
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    donations = db.get_donations_for_campaign(campaign_id)
    recent = []
    for d in reversed(donations[-8:]):
        recent.append({
            "donor_name": d.donor_name,
            "amount": d.amount,
            "receipt_hash": d.receipt_hash,
            "status": d.status.value,
            "created_at": d.created_at
        })

    pct = round((campaign.amount_raised / campaign.target_amount * 100), 1) if campaign.target_amount > 0 else 0.0

    return {
        "campaign_id": campaign.id,
        "status": campaign.status.value,
        "amount_raised": campaign.amount_raised,
        "remaining_amount": campaign.remaining_amount,
        "target_amount": campaign.target_amount,
        "currency": campaign.currency,
        "pct_achieved": min(pct, 100.0),
        "is_overfunded": campaign.status == CampaignStatus.TARGET_REACHED or campaign.amount_raised >= campaign.target_amount,
        "donations_count": len(donations),
        "recent_donations": recent
    }

@router.post("", response_model=Campaign)
async def create_campaign(
    title: str = Form(...),
    story: str = Form(...),
    patient_name: str = Form(...),
    patient_age: int = Form(...),
    diagnosis: str = Form(...),
    doctor_name: str = Form(...),
    hospital_id: str = Form(...),
    target_amount: float = Form(...),
    currency: str = Form("USD"),
    surplus_policy: SurplusPolicyType = Form(SurplusPolicyType.HOSPITAL_EMERGENCY_POOL),
    creator_name: str = Form(...),
    creator_social_handle: str = Form(...),
    creator_social_platform: str = Form("Instagram"),
    social_campaign_url: Optional[str] = Form(None),
    banner_image_url: Optional[str] = Form(None),
    doc_amount_estimate: Optional[float] = Form(None),
    estimate_doc: Optional[UploadFile] = File(None)
):
    hospital = db.get_hospital(hospital_id)
    if not hospital:
        raise HTTPException(status_code=400, detail="Invalid hospital ID. Must be a verified partner hospital.")

    # Validate target amount
    if target_amount <= 0:
        raise HTTPException(status_code=400, detail="Target amount must be greater than zero.")

    # Handle document upload if provided
    doc_filename = f"quote_{hospital.id}_{re.sub(r'[^a-zA-Z0-9_]', '', patient_name.replace(' ', '_'))}.pdf"
    doc_url = f"/static/sample_docs/{doc_filename}"

    if estimate_doc and estimate_doc.filename:
        safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '', estimate_doc.filename)
        doc_filename = f"uploaded_{hospital.id}_{safe_name}"
        dest = settings.STATIC_DIR / "sample_docs" / doc_filename
        dest.parent.mkdir(parents=True, exist_ok=True)
        content = await estimate_doc.read()
        with open(dest, "wb") as f:
            f.write(content)
        doc_url = f"/static/sample_docs/{doc_filename}"

    # Create campaign
    campaign = Campaign(
        title=title,
        story=story,
        patient_name=patient_name,
        patient_age=patient_age,
        diagnosis=diagnosis,
        doctor_name=doctor_name,
        hospital_id=hospital.id,
        hospital_name=hospital.name,
        target_amount=round(target_amount, 2),
        remaining_amount=round(target_amount, 2),
        currency=currency,
        status=CampaignStatus.PENDING_VERIFICATION,
        surplus_policy=surplus_policy,
        creator_name=creator_name,
        creator_social_handle=creator_social_handle,
        creator_social_platform=creator_social_platform,
        social_campaign_url=social_campaign_url,
        banner_image_url=banner_image_url or "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80",
        documents=[
            SupportingDocument(
                doc_type="hospital_estimate",
                filename=doc_filename,
                url=doc_url,
                extracted_amount=doc_amount_estimate or target_amount,
                extracted_hospital=hospital.name,
                extracted_diagnosis=diagnosis,
                extracted_doctor=doctor_name
            )
        ]
    )

    # Run initial Gemini Verification Analysis
    audit_dict = gemini_service.verify_campaign_documents(
        campaign=campaign,
        hospital=hospital,
        extracted_doc_amount=doc_amount_estimate
    )

    from ..models.schemas import VerificationAudit
    audit = VerificationAudit(
        campaign_id=campaign.id,
        gemini_trust_score=audit_dict.get("trust_score", 85),
        ai_status=audit_dict.get("ai_status", "RECOMMENDED"),
        human_status="PENDING",
        findings=audit_dict.get("findings", []),
        discrepancy_detected=audit_dict.get("discrepancy_detected", False),
        discrepancy_details=audit_dict.get("discrepancy_details"),
        hospital_verified=True,
        beneficiary_verified=True
    )
    campaign.verification = audit
    db.save_audit(audit)
    db.save_campaign(campaign)
    return campaign
