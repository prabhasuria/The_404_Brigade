from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import hashlib
from datetime import datetime
from ..models.schemas import Campaign, CampaignStatus, VerificationApprovalRequest, VerificationAudit
from ..services.db_service import db

router = APIRouter(prefix="/api/verification", tags=["Verification"])

@router.get("/pending", response_model=List[Campaign])
def get_pending_campaigns():
    """
    Returns campaigns that require Human-in-the-loop review.
    """
    all_campaigns = db.get_campaigns()
    return [c for c in all_campaigns if c.status == CampaignStatus.PENDING_VERIFICATION or (c.verification and c.verification.human_status == "PENDING")]

@router.post("/review")
def review_campaign(req: VerificationApprovalRequest):
    """
    Human Reviewer Action:
    Reviews patient details, hospital estimates, and AI anomaly findings.
    Marks campaign as VERIFIED and ACTIVE, or FLAGGED / REJECTED.
    """
    campaign = db.get_campaign(req.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    audit = campaign.verification or db.get_audit_by_campaign(campaign.id)
    if not audit:
        audit = VerificationAudit(campaign_id=campaign.id)

    action_upper = req.action.upper()
    audit.human_status = action_upper
    audit.reviewer_notes = req.reviewer_notes
    audit.verified_by = req.reviewer_name

    if action_upper == "APPROVE":
        audit.verification_hash = hashlib.sha256(
            f"CAREPROOF-VERIFIED-{campaign.id}-{campaign.hospital_id}-{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:24].upper()
        campaign.status = CampaignStatus.ACTIVE
        msg = f"Campaign approved! CareProof Verification Hash issued: {audit.verification_hash}. Status is now ACTIVE."
    elif action_upper == "REJECT":
        campaign.status = CampaignStatus.REJECTED
        msg = "Campaign rejected by reviewer due to document discrepancies or unverified hospital claims."
    elif action_upper == "FLAG":
        msg = "Campaign flagged for additional clinical or billing documentation."
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Must be APPROVE, REJECT, or FLAG.")

    campaign.verification = audit
    db.save_audit(audit)
    db.save_campaign(campaign)

    return {
        "status": "success",
        "action": action_upper,
        "campaign_id": campaign.id,
        "campaign_status": campaign.status.value,
        "verification_hash": audit.verification_hash,
        "message": msg
    }

@router.get("/badge/{campaign_id}")
def get_verification_badge(campaign_id: str):
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    audit = campaign.verification
    return {
        "campaign_id": campaign.id,
        "patient_name": campaign.patient_name,
        "hospital_name": campaign.hospital_name,
        "is_verified": audit.human_status == "APPROVED" if audit else False,
        "trust_score": audit.gemini_trust_score if audit else 0,
        "verification_hash": audit.verification_hash if audit else None,
        "verified_by": audit.verified_by if audit else None,
        "escrow_destination": f"{campaign.hospital_name} Official Escrow Account",
        "overfunding_protection": "Active (Donation button auto-locks at target)"
    }
