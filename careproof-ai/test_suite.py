import sys
from pathlib import Path

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    from app.services.db_service import db
    db._seed_default_data()
    db.save_all()

    client = TestClient(app)
    print("=" * 60)
    print(" 🧪 RUNNING CAREPROOF AI INTEGRATION TEST SUITE")
    print("=" * 60)

    # 1. Health check
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

    # 4. Simulate Normal Donation & Escrow Routing
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
    print("✅ 4. Donation simulated & routed to hospital escrow:")
    print(f"     Receipt Hash: {don_data['receipt_hash']}")
    print(f"     Settlement ID: {don_data['settlement_id']}")
    print(f"     Message: {don_data['message']}")

    # 5. Overfunding Protection Test
    # Rohan remaining was around 2450. Let's donate 3000 to trigger overfunding cap!
    overfund_res = client.post("/api/donations/simulate", json={
        "campaign_id": cmp_id,
        "amount": 5000.0,
        "donor_name": "Overfunding Test Donor",
        "donor_email": "test@google.com"
    })
    assert overfund_res.status_code == 200
    over_data = overfund_res.json()
    assert over_data["campaign_status"] == "TARGET_REACHED"
    print("✅ 5. Overfunding Protection successfully engaged:")
    print(f"     New Campaign Status: {over_data['campaign_status']}")
    print(f"     Disclosed Surplus Notice: {over_data['message']}")

    # 6. Verify subsequent donation is locked out
    blocked_res = client.post("/api/donations/simulate", json={
        "campaign_id": cmp_id,
        "amount": 50.0,
        "donor_name": "Late Donor"
    })
    assert blocked_res.status_code == 400
    print("✅ 6. Locked campaign successfully rejected excess donation:", blocked_res.json()["detail"])

    # 7. AI Verification Review (Admin Copilot)
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
    print("✅ 7. Human-in-the-loop audit approved & hash issued:", audit_data["verification_hash"])

    # 8. Gemini Multilingual Reel Generation
    reel_res = client.post("/api/ai/generate-reel", json={
        "campaign_id": cmp_id,
        "language": "hi",
        "social_platform": "Instagram"
    })
    assert reel_res.status_code == 200
    reel_data = reel_res.json()
    assert "scenes" in reel_data
    print(f"✅ 8. Gemini Reel Script generated ({reel_data['language']}): {reel_data['title']}")

    # 9. Gemini Transparent Captions
    captions_res = client.post("/api/ai/generate-captions", json={
        "campaign_id": cmp_id,
        "language": "en"
    })
    assert captions_res.status_code == 200
    caps = captions_res.json()["captions"]
    assert len(caps) >= 3
    print(f"✅ 9. Gemini Captions generated ({len(caps)} styles with CareProof hashes)")

    # 10. Gemini Draft Inconsistency Auditor
    fraud_draft_res = client.post("/api/ai/audit-draft", json={
        "campaign_id": cmp_id,
        "creator_draft_text": "Please send money to my personal UPI aarav@upi! We need $50,000 urgently within 2 hours!"
    })
    assert fraud_draft_res.status_code == 200
    fraud_audit = fraud_draft_res.json()
    assert fraud_audit["is_safe_to_publish"] is False
    print("✅ 10. Inconsistency detection flagged unsafe draft successfully:")
    for flag in fraud_audit["flags"]:
        print(f"     ⚠️ {flag}")

    # 11. Hospital Escrow Ledger
    hosp_res = client.get("/api/hospitals/hosp_apollo_01/escrow-ledger")
    assert hosp_res.status_code == 200
    hosp_data = hosp_res.json()
    assert hosp_data["verified_status"] == "ACTIVE_ESCROW_CONNECTED"
    print("✅ 11. Hospital escrow ledger verified:", hosp_data["hospital_name"])

    # 12. Frontend Pages Render Check
    pages = ["/", f"/campaign/{cmp_id}", "/creator-studio", "/verifier", "/hospital-escrow", "/create"]
    for p in pages:
        p_res = client.get(p)
        assert p_res.status_code == 200, f"Page {p} returned {p_res.status_code}"
    print(f"✅ 12. All {len(pages)} frontend HTML template pages rendered with 200 OK")

    print("=" * 60)
    print(" 🎉 ALL 12 INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
