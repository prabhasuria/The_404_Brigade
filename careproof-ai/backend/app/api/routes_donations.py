from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.schemas import Donation, DonationRequest
from ..services.db_service import db
from ..services.payment_service import payment_service

router = APIRouter(prefix="/api/donations", tags=["Donations"])

@router.get("/{campaign_id}", response_model=List[Donation])
def get_campaign_donations(campaign_id: str):
    return db.get_donations_for_campaign(campaign_id)

@router.post("/intent")
def create_payment_intent(req: DonationRequest):
    result = payment_service.create_payment_intent(req)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@router.post("/simulate")
def simulate_donation(req: DonationRequest):
    """
    Simulates an instant verified payment for demo and testing.
    Routes funds directly to hospital escrow, invokes overfunding check,
    and updates campaign real-time ledger.
    """
    result = payment_service.process_confirmed_payment_webhook(
        campaign_id=req.campaign_id,
        amount=req.amount,
        donor_name=req.donor_name,
        donor_email=req.donor_email,
        payment_intent_id=f"sim_pi_{req.amount}",
        provider=req.payment_provider
    )
    if result.get("status") == "rejected":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@router.post("/webhook")
def receive_payment_webhook(payload: Dict[str, Any]):
    """
    Payment webhook receiver for Stripe / Razorpay callbacks.
    """
    campaign_id = payload.get("campaign_id")
    amount = float(payload.get("amount", 0.0))
    donor_name = payload.get("donor_name", "Anonymous Donor")
    donor_email = payload.get("donor_email", "support@careproof.ai")
    intent_id = payload.get("payment_intent_id", "pi_webhook")

    if not campaign_id or amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid webhook payload")

    result = payment_service.process_confirmed_payment_webhook(
        campaign_id=campaign_id,
        amount=amount,
        donor_name=donor_name,
        donor_email=donor_email,
        payment_intent_id=intent_id
    )
    return result
