from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class CampaignStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    VERIFIED = "VERIFIED"
    ACTIVE = "ACTIVE"
    TARGET_REACHED = "TARGET_REACHED"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"

class SurplusPolicyType(str, Enum):
    HOSPITAL_EMERGENCY_POOL = "HOSPITAL_EMERGENCY_POOL"
    REFUND_EXCESS = "REFUND_EXCESS"

class DonationStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    PENDING = "PENDING"
    REFUNDED_OVERFUNDED = "REFUNDED_OVERFUNDED"
    SURPLUS_REDIRECTED = "SURPLUS_REDIRECTED"
    FAILED = "FAILED"

class Hospital(BaseModel):
    id: str = Field(default_factory=lambda: f"hosp_{uuid.uuid4().hex[:8]}")
    name: str
    registration_number: str
    country: str = "India"
    city: str
    accreditation: str = "NABH & JCI Certified"
    escrow_account_id: str
    bank_name: str
    verified: bool = True
    contact_email: str
    phone: str

class SupportingDocument(BaseModel):
    id: str = Field(default_factory=lambda: f"doc_{uuid.uuid4().hex[:6]}")
    doc_type: str  # hospital_estimate, identity_proof, doctor_certificate, admission_slip
    filename: str
    url: str
    uploaded_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    extracted_amount: Optional[float] = None
    extracted_hospital: Optional[str] = None
    extracted_diagnosis: Optional[str] = None
    extracted_doctor: Optional[str] = None

class VerificationAudit(BaseModel):
    id: str = Field(default_factory=lambda: f"audit_{uuid.uuid4().hex[:8]}")
    campaign_id: str
    gemini_trust_score: int = 85  # 0 to 100
    ai_status: str = "RECOMMENDED"  # RECOMMENDED, REQUIRES_MANUAL_REVIEW, HIGH_RISK
    human_status: str = "PENDING"  # PENDING, APPROVED, REJECTED, FLAGGED
    findings: List[str] = []
    discrepancy_detected: bool = False
    discrepancy_details: Optional[str] = None
    hospital_verified: bool = True
    beneficiary_verified: bool = True
    reviewer_notes: Optional[str] = None
    verified_by: Optional[str] = None
    verification_hash: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class Campaign(BaseModel):
    id: str = Field(default_factory=lambda: f"cmp_{uuid.uuid4().hex[:8]}")
    title: str
    story: str
    patient_name: str
    patient_age: int
    diagnosis: str
    doctor_name: str
    hospital_id: str
    hospital_name: str
    target_amount: float
    amount_raised: float = 0.0
    remaining_amount: float = 0.0
    currency: str = "USD"
    status: CampaignStatus = CampaignStatus.PENDING_VERIFICATION
    surplus_policy: SurplusPolicyType = SurplusPolicyType.HOSPITAL_EMERGENCY_POOL
    surplus_redirected_amount: float = 0.0
    documents: List[SupportingDocument] = []
    verification: Optional[VerificationAudit] = None
    creator_name: str
    creator_social_handle: str
    creator_social_platform: str = "Instagram"
    social_campaign_url: Optional[str] = None
    banner_image_url: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    def update_financials(self):
        self.remaining_amount = max(0.0, self.target_amount - self.amount_raised)
        if self.amount_raised >= self.target_amount and self.status == CampaignStatus.ACTIVE:
            self.status = CampaignStatus.TARGET_REACHED

class Donation(BaseModel):
    id: str = Field(default_factory=lambda: f"don_{uuid.uuid4().hex[:8]}")
    campaign_id: str
    donor_name: str
    donor_email: str
    amount: float
    currency: str = "USD"
    status: DonationStatus = DonationStatus.CONFIRMED
    hospital_settlement_id: str = Field(default_factory=lambda: f"hset_{uuid.uuid4().hex[:8]}")
    payment_intent_id: str = Field(default_factory=lambda: f"pi_{uuid.uuid4().hex[:12]}")
    payment_provider: str = "Stripe"
    receipt_hash: str = Field(default_factory=lambda: f"cp_rec_{uuid.uuid4().hex[:16]}")
    is_anonymous: bool = False
    surplus_note: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class DonationRequest(BaseModel):
    campaign_id: str
    donor_name: str = "Kind Supporter"
    donor_email: str = "donor@example.com"
    amount: float
    currency: str = "USD"
    is_anonymous: bool = False
    payment_provider: str = "Stripe"

class ContentGenerationRequest(BaseModel):
    campaign_id: str
    content_type: str = "REEL_SCRIPT"  # REEL_SCRIPT, CAPTION, ACCESSIBLE_STORY, DISCREPANCY_CHECK
    language: str = "en"  # en, hi, es, ta, bn, mr
    social_platform: str = "Instagram"
    creator_tone: str = "Empathetic & Transparent"
    creator_draft_text: Optional[str] = None

class VerificationApprovalRequest(BaseModel):
    campaign_id: str
    action: str  # APPROVE, REJECT, FLAG
    reviewer_name: str = "Google H2S Trust Officer"
    reviewer_notes: str = "Verified hospital letterhead with Apollo Hospital accounts desk."
