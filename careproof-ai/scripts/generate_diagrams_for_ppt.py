#!/usr/bin/env python3
"""
Generate crisp, dark-themed diagrams for the official Google Cloud H2S PPT slides:
1. Process Flow Diagram
2. System Architecture Diagram
"""

import os
from PIL import Image, ImageDraw, ImageFont

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
os.makedirs(DOCS_DIR, exist_ok=True)

FLOW_PATH = os.path.join(DOCS_DIR, "process_flow_diagram.png")
ARCH_PATH = os.path.join(DOCS_DIR, "architecture_diagram.png")

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

# Colors
BG = (10, 25, 47)
CARD = (23, 42, 69)
CYAN = (100, 255, 218)
TEAL = (13, 148, 136)
WHITE = (240, 246, 252)
MUTED = (136, 146, 176)
AMBER = (245, 158, 11)
GREEN = (34, 197, 94)
RED = (239, 68, 68)

def create_process_flow_diagram():
    W, H = 1600, 850
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((60, 40), "CAREPROOF AI — END-TO-END PROCESS FLOW", font=get_font(28, bold=True), fill=CYAN)
    draw.text((60, 80), "Bridging Viral Social Media Campaigns with Verified Hospital Escrow & Thread-Safe Overfunding Caps", font=get_font(18), fill=MUTED)

    steps = [
        ("1. INGESTION", "Creator uploads hospital estimate & clinical quote", CYAN, "Bill PDF / Scan"),
        ("2. GEMINI AI OCR", "Gemini 2.0 Flash extracts line items & flags discrepancies", TEAL, "Trust Score 0-100"),
        ("3. MEDICAL AUDIT", "Human Verifier reviews and issues SHA-256 certificate", GREEN, "Signed Hash"),
        ("4. CREATOR STUDIO", "Gemini synthesizes 9:16 multilingual Reel & caption", CYAN, "Hindi/Spanish/Tamil"),
        ("5. SOCIAL DONATION", "Donors view verified Reel & click verified bio-link", WHITE, "Direct Webhook"),
        ("6. MUTEX OVERFUNDING", "Thread-safe lock checks target; flips to TARGET_REACHED", AMBER, "Atomic Lock"),
        ("7. HOSPITAL ESCROW", "100% of bill settled directly to hospital account (0% creator)", GREEN, "Apollo / Fortis"),
        ("8. SURPLUS POOL", "Overflow funds redirected to Pediatric Emergency Pool", AMBER, "Disclosed Policy")
    ]

    # Two rows of 4 cards
    card_w, card_h = 340, 280
    gap_x, gap_y = 35, 45
    start_x, start_y = 60, 140

    for idx, (title, desc, col, tag) in enumerate(steps):
        row = idx // 4
        col_idx = idx % 4
        cx = start_x + col_idx * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        # Card
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=12, fill=CARD, outline=col, width=2)
        
        # Step Tag
        draw.rounded_rectangle([cx + 15, cy + 18, cx + card_w - 15, cy + 50], radius=6, fill=(18, 35, 60), outline=col, width=1)
        draw.text((cx + 25, cy + 24), title, font=get_font(15, bold=True), fill=col)

        # Description
        words = desc.split()
        l1 = " ".join(words[:6])
        l2 = " ".join(words[6:12])
        l3 = " ".join(words[12:])
        draw.text((cx + 20, cy + 75), l1, font=get_font(15), fill=WHITE)
        if l2: draw.text((cx + 20, cy + 105), l2, font=get_font(15), fill=WHITE)
        if l3: draw.text((cx + 20, cy + 135), l3, font=get_font(15), fill=WHITE)

        # Bottom Tag Badge
        draw.rounded_rectangle([cx + 20, cy + 220, cx + card_w - 20, cy + 255], radius=6, fill=(12, 22, 40))
        draw.text((cx + 35, cy + 228), f"Output: {tag}", font=get_font(13, bold=True), fill=CYAN)

        # Draw connecting arrow to next step if in same row
        if col_idx < 3:
            ax = cx + card_w + 5
            ay = cy + card_h // 2
            draw.line([(ax, ay), (ax + 25, ay)], fill=CYAN, width=3)
            # Arrow head
            draw.polygon([(ax + 25, ay), (ax + 15, ay - 6), (ax + 15, ay + 6)], fill=CYAN)

    img.save(FLOW_PATH)
    print(f"✅ Generated Process Flow: {FLOW_PATH}")

def create_architecture_diagram():
    W, H = 1600, 850
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((60, 40), "CAREPROOF AI — 5-TIER SYSTEM ARCHITECTURE", font=get_font(28, bold=True), fill=CYAN)
    draw.text((60, 80), "Production-Grade Serverless Microservices Deployed on Google Cloud Run", font=get_font(18), fill=MUTED)

    tiers = [
        ("TIER 1: CLIENT & SOCIAL LAYER", [
            ("Donor Web & Mobile UI", "Tailwind Glassmorphic Live SSE Polling"),
            ("Creator Studio", "Interactive 9:16 Smartphone Simulator"),
            ("Verifier Copilot", "Human-in-the-Loop Audit Dashboard"),
            ("Hospital Billing Portal", "Live Inward Escrow Settlement Ledger")
        ], CYAN),
        ("TIER 2: API GATEWAY & ROUTING", [
            ("FastAPI Asynchronous Router", "High-Throughput Non-Blocking Endpoints"),
            ("Pydantic Guard Validation", "Strict gt=0 & State Verification Guards"),
            ("Cryptographic Signer", "SHA-256 Tamper-Evident Receipt Hashes")
        ], TEAL),
        ("TIER 3: GOOGLE GEMINI CORE", [
            ("Gemini 2.0 Flash Vision", "Multimodal Flyer OCR & Forensic Audit"),
            ("Gemini 1.5 Pro Language", "Multilingual 9:16 Scripts in 6 Languages"),
            ("Post Discrepancy Auditor", "Zero-Tolerance Unverified Link Detection"),
            ("Accessible Story Engine", "Plain-Language 6th Grade Translation")
        ], WHITE),
        ("TIER 4: ESCROW & MUTEX LOCK", [
            ("Thread-Safe Mutex Lock", "Atomic threading.Lock() Concurrency Engine"),
            ("Overfunding Guard", "Instant Lockdown at 100% Target Met"),
            ("Surplus Split Controller", "Redirects Overflow to Pediatric Pool"),
            ("Direct Escrow Router", "0.00% Influencer Intermediation (Blocked)")
        ], AMBER),
        ("TIER 5: GOOGLE CLOUD INFRA", [
            ("Google Cloud Run", "Serverless Container Auto-Scaling to Zero"),
            ("Google Cloud Build", "Automated CI/CD Pipeline (cloudbuild.yaml)"),
            ("Google Cloud Storage", "Encrypted Medical Invoice & Flyer Storage"),
            ("Firebase / Cloud Firestore", "Sub-Second Real-Time Transaction Ledger")
        ], GREEN)
    ]

    tier_w = (W - 120 - 40) // 5
    start_x, start_y = 60, 140
    tier_h = 640

    for t_idx, (tier_title, items, col) in enumerate(tiers):
        tx = start_x + t_idx * (tier_w + 10)
        draw.rounded_rectangle([tx, start_y, tx + tier_w, start_y + tier_h], radius=12, fill=CARD, outline=col, width=2)

        # Tier Header
        draw.rounded_rectangle([tx + 10, start_y + 15, tx + tier_w - 10, start_y + 60], radius=8, fill=(18, 35, 60), outline=col, width=1)
        draw.text((tx + 18, start_y + 25), tier_title, font=get_font(12, bold=True), fill=col)

        # Items
        for i_idx, (head, sub) in enumerate(items):
            iy = start_y + 80 + i_idx * 130
            draw.rounded_rectangle([tx + 12, iy, tx + tier_w - 12, iy + 115], radius=8, fill=(15, 28, 48), outline=(35, 60, 95), width=1)
            draw.text((tx + 22, iy + 14), head, font=get_font(13, bold=True), fill=CYAN)
            
            words = sub.split()
            l1 = " ".join(words[:4])
            l2 = " ".join(words[4:])
            draw.text((tx + 22, iy + 45), l1, font=get_font(11), fill=WHITE)
            if l2: draw.text((tx + 22, iy + 70), l2, font=get_font(11), fill=MUTED)

    img.save(ARCH_PATH)
    print(f"✅ Generated Architecture Diagram: {ARCH_PATH}")

if __name__ == "__main__":
    create_process_flow_diagram()
    create_architecture_diagram()
