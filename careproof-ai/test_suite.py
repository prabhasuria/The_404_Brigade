import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    from app.services.db_service import db
    db._seed_default_data()
    db.save_all()

    client = TestClient(app)
    print("=" * 65)
    print(" 🧪 RUNNING CAREPROOF AI INTEGRATION & SECURITY TEST SUITE")
    print("=" * 65)

    # 1. Health check probe
    res = client.get("/healthz")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("✅ 1. Health check probe passed:", res.json())

    # 2. Campaigns API
    res = client.get("/api/campaigns")
    assert res.status_code == 200
    campaigns = res.json()
    assert len(campaigns) >= 3
    print(f"✅ 2. Campaigns listed ({len(campaigns)} seeded campaigns found)")

    # 3. Campaign Detail
    cmp_id = "cmp_rohan_heart"
    res = client.get(f"/api/campaigns/{cmp_id}")
    assert res.status_code == 200
    rohan = res.json()
    assert rohan["patient_name"] == "Rohan Verma"
    assert rohan["hospital_id"] == "hosp_apollo_01"
    print(f"✅ 3. Campaign detail retrieved: {rohan['title']} (Target: ${rohan['target_amount']:,.0f})")

    # 4. Security Test: Negative and Zero Donation Rejection
    neg_res = client.post("/api/donations/simulate", json={
        "campaign_id": cmp_id,
        "amount": -250.0,
        "donor_name": "Attacker"
    })
    assert neg_res.status_code == 422 or neg_res.status_code == 400
    zero_res = client.post("/api/donations/simulate", json={
        "campaign_id": cmp_id,
        "amount": 0.0,
        "donor_name": "Zero Attacker"
    })
    assert zero_res.status_code == 422 or zero_res.status_code == 400
    print("✅ 4. Security Guard: Negative and zero donations strictly blocked with HTTP 400/422")

    # 5. Security Test: Donation Guard on Pending Campaign
    pending_res = client.post("/api/donations/simulate", json={
        "campaign_id": "cmp_vikram_spine",
        "amount": 100.0,
        "donor_name": "Premature Donor"
    })
    assert pending_res.status_code == 400
    print("✅ 5. Security Guard: Donations blocked on unverified campaign (PENDING_VERIFICATION)")

    # 6. Simulate Normal Donation & Escrow Routing
    donate_res = client.post("/api/donations/simulate", json={
        "campaign_id": cmp_id,
        "amount": 100.0,
        "donor_name": "Hackathon Judge",
        "donor_email": "judge@google.com",
        "currency": "USD"
    })
    assert donate_res.status_code == 200, f"Donation failed: {donate_res.text}"
    don_data = donate_res.json()
    assert don_data["status"] == "confirmed"
    assert "CP-REC-" in don_data["receipt_hash"]
    print("✅ 6. Donation simulated & routed to hospital escrow:")
    print(f"     Receipt Hash: {don_data['receipt_hash']}")
    print(f"     Settlement ID: {don_data['settlement_id']}")
    print(f"     Message: {don_data['message']}")

    # 7. Real-Time Tracking Status Endpoint
    status_res = client.get(f"/api/campaigns/{cmp_id}/live-status")
    assert status_res.status_code == 200
    live_stat = status_res.json()
    assert live_stat["amount_raised"] == 19550.0
    assert live_stat["remaining_amount"] == 2450.0
    assert len(live_stat["recent_donations"]) >= 1
    print(f"✅ 7. Real-Time Live Status stream synchronized: ${live_stat['amount_raised']:,.0f} raised ({live_stat['pct_achieved']}%)")

    # 8. Overfunding Protection & Disclosed Surplus Policy Test
    # Rohan remaining is 2450. Let's donate 5000 to trigger overfunding cap!
    overfund_res = client.post("/api/donations/simulate", json={
        "campaign_id": cmp_id,
        "amount": 5000.0,
        "donor_name": "Overfunding Test Donor",
        "donor_email": "test@google.com"
    })
    assert overfund_res.status_code == 200
    over_data = overfund_res.json()
    assert over_data["campaign_status"] == "TARGET_REACHED"
    assert over_data["applied_to_patient"] == 2450.0
    assert over_data["surplus_amount"] == 2550.0
    print("✅ 8. Overfunding Protection successfully engaged:")
    print(f"     New Status: {over_data['campaign_status']}")
    print(f"     Principal Applied: ${over_data['applied_to_patient']:,.2f}")
    print(f"     Surplus Allocated: ${over_data['surplus_amount']:,.2f}")
    print(f"     Surplus Destination: {over_data.get('surplus_destination')}")

    # 9. Verify subsequent donation is locked out
    blocked_res = client.post("/api/donations/simulate", json={
        "campaign_id": cmp_id,
        "amount": 50.0,
        "donor_name": "Late Donor"
    })
    assert blocked_res.status_code == 400
    print("✅ 9. Locked campaign successfully rejected subsequent donation:", blocked_res.json()["detail"])

    # 10. Concurrency & Race Condition Mutex Test
    # Create fresh campaign to test concurrent donation barrage
    from app.models.schemas import Campaign, CampaignStatus, SurplusPolicyType
    c_test = Campaign(
        id="cmp_concurrency_test",
        title="Concurrency Test Campaign",
        story="Testing high-velocity concurrent donations during viral traffic spikes",
        patient_name="Baby Zara",
        patient_age=2,
        diagnosis="Biliary Atresia",
        doctor_name="Dr. Test Surgeon",
        hospital_id="hosp_apollo_01",
        hospital_name="Apollo Hospitals Bannerghatta",
        target_amount=1000.0,
        amount_raised=500.0,
        remaining_amount=500.0,
        currency="USD",
        status=CampaignStatus.ACTIVE,
        surplus_policy=SurplusPolicyType.HOSPITAL_EMERGENCY_POOL,
        creator_name="Test Creator",
        creator_social_handle="@test"
    )
    db.save_campaign(c_test)

    def send_concurrent_donation(idx):
        return client.post("/api/donations/simulate", json={
            "campaign_id": "cmp_concurrency_test",
            "amount": 200.0,
            "donor_name": f"Concurrent Donor #{idx}"
        })

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(send_concurrent_donation, i) for i in range(10)]
        results = [f.result() for f in futures]

    fresh_test = db.get_campaign("cmp_concurrency_test")
    # Amount raised must NEVER exceed target_amount (1000.0) regardless of concurrent burst
    assert fresh_test.amount_raised == 1000.0
    assert fresh_test.status == CampaignStatus.TARGET_REACHED
    print(f"✅ 10. Concurrency Thread-Safety: 10 concurrent requests handled atomically. Final raised = ${fresh_test.amount_raised:,.0f} (Target Cap Respected 100%!)")

    # 11. AI Verification Review (Admin Copilot)
    audit_res = client.post("/api/verification/review", json={
        "campaign_id": "cmp_vikram_spine",
        "action": "APPROVE",
        "reviewer_name": "Chief Medical Auditor",
        "reviewer_notes": "Hospital confirmed revised invoice with surgical package."
    })
    assert audit_res.status_code == 200
    audit_data = audit_res.json()
    assert audit_data["action"] == "APPROVE"
    assert audit_data["verification_hash"] is not None
    print("✅ 11. Human-in-the-loop audit approved & verification hash issued:", audit_data["verification_hash"])

    # 12. Gemini Multilingual Reel Generation
    reel_res = client.post("/api/ai/generate-reel", json={
        "campaign_id": cmp_id,
        "language": "hi",
        "social_platform": "Instagram"
    })
    assert reel_res.status_code == 200
    reel_data = reel_res.json()
    assert "scenes" in reel_data
    print(f"✅ 12. Gemini Reel Script generated ({reel_data['language']}): {reel_data['title']}")

    # 13. Gemini Transparent Captions
    captions_res = client.post("/api/ai/generate-captions", json={
        "campaign_id": cmp_id,
        "language": "en"
    })
    assert captions_res.status_code == 200
    caps = captions_res.json()["captions"]
    assert len(caps) >= 3
    print(f"✅ 13. Gemini Captions generated ({len(caps)} styles with CareProof hashes)")

    # 14. Gemini Draft Inconsistency Auditor
    fraud_draft_res = client.post("/api/ai/audit-draft", json={
        "campaign_id": cmp_id,
        "creator_draft_text": "Please send money to my personal UPI aarav@upi! We need $50,000 urgently within 2 hours!"
    })
    assert fraud_draft_res.status_code == 200
    fraud_audit = fraud_draft_res.json()
    assert fraud_audit["is_safe_to_publish"] is False
    print("✅ 14. Inconsistency detection flagged unsafe draft successfully:")
    for flag in fraud_audit["flags"]:
        print(f"     ⚠️ {flag}")

    # 15. Hospital Escrow Ledger & Live Settlements List
    hosp_res = client.get("/api/hospitals/hosp_apollo_01/escrow-ledger")
    assert hosp_res.status_code == 200
    hosp_data = hosp_res.json()
    assert hosp_data["verified_status"] == "ACTIVE_ESCROW_CONNECTED"
    assert "settlements" in hosp_data
    assert len(hosp_data["settlements"]) >= 1
    print(f"✅ 15. Hospital escrow ledger verified with {len(hosp_data['settlements'])} live direct settlements")

    # 16. Frontend Pages Render Check
    pages = ["/", f"/campaign/{cmp_id}", "/creator-studio", "/verifier", "/hospital-escrow", "/create"]
    for p in pages:
        p_res = client.get(p)
        assert p_res.status_code == 200, f"Page {p} returned {p_res.status_code}"
    print(f"✅ 16. All {len(pages)} frontend HTML template pages rendered with 200 OK")

    print("=" * 65)
    print(" 🎉 ALL 16 INTEGRATION & SECURITY TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
