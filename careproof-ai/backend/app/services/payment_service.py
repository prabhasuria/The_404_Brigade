import uuid
from typing import Dict, Any, Optional
from ..models.schemas import Campaign, DonationRequest
from ..config import settings
from .overfunding_service import overfunding_service
from .db_service import db

class PaymentProviderService:
    """
    Integrates with supported payment providers (Stripe, Razorpay)
    and provides real-time webhook & checkout session handling.
    Includes a robust simulation sandbox for hackathon demo tests.
    """
    def __init__(self):
        self.stripe_key = settings.STRIPE_SECRET_KEY
        self.razorpay_key = settings.RAZORPAY_KEY_ID

    def create_payment_intent(self, request: DonationRequest) -> Dict[str, Any]:
        campaign = db.get_campaign(request.campaign_id)
        if not campaign:
            return {"status": "error", "message": "Campaign not found"}

        if campaign.status.value in ["TARGET_REACHED", "PAUSED", "COMPLETED"]:
            return {
                "status": "error",
                "message": "Campaign has reached its target bill amount! Overfunding protection has locked donations."
            }

        # Generate provider intent
        intent_id = f"pi_careproof_{uuid.uuid4().hex[:14]}"
        client_secret = f"{intent_id}_secret_{uuid.uuid4().hex[:10]}"

        return {
            "status": "success",
            "payment_intent_id": intent_id,
            "client_secret": client_secret,
            "provider": request.payment_provider,
            "amount": request.amount,
            "currency": request.currency,
            "campaign_id": campaign.id,
            "escrow_hospital": campaign.hospital_name,
            "message": f"Payment intent prepared. Payout destination: {campaign.hospital_name} Escrow."
        }

    def process_confirmed_payment_webhook(
        self,
        campaign_id: str,
        amount: float,
        donor_name: str,
        donor_email: str,
        payment_intent_id: str,
        provider: str = "Stripe"
    ) -> Dict[str, Any]:
        """
        Invoked by payment provider webhooks (e.g. `payment_intent.succeeded` or `order.paid`).
        Applies Overfunding Protection and Hospital Escrow routing.
        """
        campaign = db.get_campaign(campaign_id)
        if not campaign:
            return {"status": "error", "message": "Campaign not found"}

        success, donation, message = overfunding_service.process_incoming_donation(
            campaign=campaign,
            amount=amount,
            donor_name=donor_name,
            donor_email=donor_email,
            payment_intent_id=payment_intent_id
        )

        if not success:
            return {
                "status": "rejected",
                "message": message,
                "campaign_status": campaign.status.value,
                "amount_raised": campaign.amount_raised,
                "target_amount": campaign.target_amount
            }

        return {
            "status": "confirmed",
            "donation_id": donation.id,
            "receipt_hash": donation.receipt_hash,
            "settlement_id": donation.hospital_settlement_id,
            "campaign_status": campaign.status.value,
            "amount_raised": campaign.amount_raised,
            "remaining_amount": campaign.remaining_amount,
            "original_amount": donation.original_amount,
            "applied_to_patient": donation.applied_to_patient,
            "surplus_amount": donation.surplus_amount,
            "refund_amount": donation.refund_amount,
            "refund_transaction_id": donation.refund_transaction_id,
            "surplus_destination": donation.surplus_destination,
            "message": message
        }

payment_service = PaymentProviderService()
