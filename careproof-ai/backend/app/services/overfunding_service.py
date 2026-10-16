import threading
import uuid
from typing import Tuple, Dict, Any, Optional
from ..models.schemas import Campaign, CampaignStatus, SurplusPolicyType, Donation, DonationStatus
from .db_service import db
from .escrow_service import escrow_service

class OverfundingProtectionService:
    """
    Overfunding Protection:
    Ensures that social media campaigns do not raise excess unaccountable capital beyond
    the verified hospital bill. Automatically pauses donations when the target is reached,
    reconciles pending concurrent transactions, and applies the disclosed surplus/refund policy.
    Thread-safe implementation with atomic mutex locks to prevent race conditions during viral surges.
    """
    def __init__(self):
        self._lock = threading.Lock()

    def process_incoming_donation(
        self,
        campaign: Campaign,
        amount: float,
        donor_name: str,
        donor_email: str,
        payment_intent_id: str
    ) -> Tuple[bool, Optional[Donation], str]:
        """
        Thread-safe donation settlement and overfunding reconciliation.
        Returns:
            (success, donation_object, message_or_error)
        """
        with self._lock:
            # Re-fetch freshest state from database inside lock to prevent race conditions
            current_campaign = db.get_campaign(campaign.id)
            if not current_campaign:
                return False, None, "Donation rejected: Campaign not found."

            # 1. Validation on donation amount
            amount = round(float(amount), 2)
            if amount <= 0:
                return False, None, "Donation rejected: Amount must be greater than zero."

            # 2. Check if already paused/target reached or completed
            if current_campaign.amount_raised >= current_campaign.target_amount or current_campaign.status in [
                CampaignStatus.TARGET_REACHED,
                CampaignStatus.PAUSED,
                CampaignStatus.COMPLETED
            ]:
                return False, None, "Donation rejected: Campaign has already reached its verified medical bill target. Overfunding protection is active."

            # 3. Check if campaign is verified & active
            if current_campaign.status != CampaignStatus.ACTIVE:
                return False, None, f"Donation rejected: Campaign is currently in {current_campaign.status.value} status."

            remaining = round(current_campaign.target_amount - current_campaign.amount_raised, 2)

            # Case A: Amount fits within remaining target
            if amount <= remaining:
                donation = escrow_service.route_donation_to_hospital(
                    campaign=current_campaign,
                    amount=amount,
                    donor_name=donor_name,
                    donor_email=donor_email,
                    payment_intent_id=payment_intent_id
                )
                donation.original_amount = amount
                donation.applied_to_patient = amount
                donation.surplus_amount = 0.0
                donation.refund_amount = 0.0

                current_campaign.amount_raised = round(current_campaign.amount_raised + amount, 2)
                current_campaign.update_financials()

                # Check if this exact donation fulfilled the target
                if current_campaign.amount_raised >= current_campaign.target_amount:
                    current_campaign.status = CampaignStatus.TARGET_REACHED
                    msg = f"Thank you! Your donation of ${amount:,.2f} completed the campaign target! Overfunding protection is now engaged."
                else:
                    msg = f"Success! ${amount:,.2f} routed directly to {current_campaign.hospital_name}'s verified escrow account."

                db.save_campaign(current_campaign)
                db.save_donation(donation)
                return True, donation, msg

            # Case B: Amount exceeds remaining requirement (Concurrent or large final donation)
            excess_amount = round(amount - remaining, 2)
            accepted_principal = remaining

            donation = escrow_service.route_donation_to_hospital(
                campaign=current_campaign,
                amount=accepted_principal,
                donor_name=donor_name,
                donor_email=donor_email,
                payment_intent_id=payment_intent_id
            )
            donation.original_amount = amount
            donation.applied_to_patient = accepted_principal
            donation.surplus_amount = excess_amount

            current_campaign.amount_raised = round(current_campaign.amount_raised + accepted_principal, 2)
            current_campaign.status = CampaignStatus.TARGET_REACHED

            if current_campaign.surplus_policy == SurplusPolicyType.HOSPITAL_EMERGENCY_POOL:
                current_campaign.surplus_redirected_amount = round(current_campaign.surplus_redirected_amount + excess_amount, 2)
                donation.surplus_destination = f"{current_campaign.hospital_name} Emergency Pediatric ICU Pool"
                donation.surplus_note = (
                    f"Goal achieved: ${accepted_principal:,.2f} settled to patient invoice. "
                    f"Disclosed Surplus Policy: Excess ${excess_amount:,.2f} redirected to {current_campaign.hospital_name} Emergency Pediatric ICU Pool."
                )
                msg = (
                    f"Campaign target met! ${accepted_principal:,.2f} completed {current_campaign.patient_name}'s bill. "
                    f"Per campaign disclosure, surplus of ${excess_amount:,.2f} was routed to the Hospital Emergency Pool."
                )
            else: # REFUND_EXCESS
                refund_id = f"REF-{uuid.uuid4().hex[:10].upper()}"
                donation.refund_amount = excess_amount
                donation.refund_transaction_id = refund_id
                donation.surplus_note = (
                    f"Goal achieved: ${accepted_principal:,.2f} settled to patient invoice. "
                    f"Surplus of ${excess_amount:,.2f} refunded back to donor's card (Ref: {refund_id})."
                )
                msg = (
                    f"Campaign target met! ${accepted_principal:,.2f} completed the bill. "
                    f"Surplus of ${excess_amount:,.2f} has been automatically queued for refund to your payment card."
                )

            current_campaign.update_financials()
            db.save_campaign(current_campaign)
            db.save_donation(donation)
            return True, donation, msg

overfunding_service = OverfundingProtectionService()
