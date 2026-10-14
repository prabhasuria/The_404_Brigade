from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from typing import List, Optional
from ..models.schemas import Campaign, CampaignStatus, SurplusPolicyType, SupportingDocument
from ..services.db_service import db
from ..services.gemini_service import gemini_service

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

@router.post("", response_model=Campaign)
def create_campaign(
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
    doc_amount_estimate: Optional[float] = Form(None)
):
    hospital = db.get_hospital(hospital_id)
    if not hospital:
        raise HTTPException(status_code=400, detail="Invalid hospital ID. Must be a verified partner hospital.")

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
        target_amount=target_amount,
        remaining_amount=target_amount,
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
                filename=f"quote_{hospital.id}_{patient_name.replace(' ', '_')}.pdf",
                url=f"/static/sample_docs/quote_{patient_name.replace(' ', '_')}.pdf",
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
