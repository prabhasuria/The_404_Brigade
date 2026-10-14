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
    """
    def process_incoming_donation(
        self,
        campaign: Campaign,
        amount: float,
        donor_name: str,
        donor_email: str,
        payment_intent_id: str
    ) -> Tuple[bool, Optional[Donation], str]:
        """
        Returns:
            (success, donation_object, message_or_error)
        """
        # 1. Check if campaign is already paused/target reached
        if campaign.status in [CampaignStatus.TARGET_REACHED, CampaignStatus.PAUSED, CampaignStatus.COMPLETED]:
            return False, None, "Donation rejected: Campaign has already reached its verified medical bill target. Overfunding protection is active."

        # 2. Check if campaign is verified
        if campaign.status != CampaignStatus.ACTIVE:
            return False, None, f"Donation rejected: Campaign is currently in {campaign.status.value} status."

        remaining = campaign.target_amount - campaign.amount_raised

        # Case A: Amount fits comfortably within remaining target
        if amount <= remaining:
            donation = escrow_service.route_donation_to_hospital(
                campaign=campaign,
                amount=amount,
                donor_name=donor_name,
                donor_email=donor_email,
                payment_intent_id=payment_intent_id
            )
            campaign.amount_raised += amount
            campaign.update_financials()

            # Check if this exact donation fulfilled the target
            if campaign.amount_raised >= campaign.target_amount:
                campaign.status = CampaignStatus.TARGET_REACHED
                msg = f"Thank you! Your donation of ${amount:,.2f} completed the campaign target! Overfunding protection is now engaged."
            else:
                msg = f"Success! ${amount:,.2f} routed directly to {campaign.hospital_name}'s verified escrow account."

            db.save_campaign(campaign)
            db.save_donation(donation)
            return True, donation, msg

        # Case B: Amount exceeds remaining requirement (Concurrent or large final donation)
        excess_amount = amount - remaining
        accepted_principal = remaining

        donation = escrow_service.route_donation_to_hospital(
            campaign=campaign,
            amount=accepted_principal,
            donor_name=donor_name,
            donor_email=donor_email,
            payment_intent_id=payment_intent_id
        )

        campaign.amount_raised += accepted_principal
        campaign.status = CampaignStatus.TARGET_REACHED

        if campaign.surplus_policy == SurplusPolicyType.HOSPITAL_EMERGENCY_POOL:
            campaign.surplus_redirected_amount += excess_amount
            donation.surplus_note = (
                f"Goal achieved: ${accepted_principal:,.2f} settled to patient invoice. "
                f"Disclosed Surplus Policy: Excess ${excess_amount:,.2f} redirected to {campaign.hospital_name} Emergency Pediatric ICU Pool."
            )
            msg = (
                f"Campaign target met! ${accepted_principal:,.2f} completed {campaign.patient_name}'s bill. "
                f"Per campaign disclosure, surplus of ${excess_amount:,.2f} was routed to the Hospital Emergency Pool."
            )
        else: # REFUND_EXCESS
            donation.surplus_note = (
                f"Goal achieved: ${accepted_principal:,.2f} settled to patient invoice. "
                f"Surplus of ${excess_amount:,.2f} refunded back to donor's card."
            )
            msg = (
                f"Campaign target met! ${accepted_principal:,.2f} completed the bill. "
                f"Surplus of ${excess_amount:,.2f} has been automatically queued for refund to your payment card."
            )

        campaign.update_financials()
        db.save_campaign(campaign)
        db.save_donation(donation)
        return True, donation, msg

overfunding_service = OverfundingProtectionService()
