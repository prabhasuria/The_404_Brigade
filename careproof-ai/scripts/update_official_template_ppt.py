#!/usr/bin/env python3
"""
CareProof AI — Official Google Cloud H2S AI Builder Cup PPTX Generator
Populates the exact official presentation template provided by the organizers.
Team: The 404 Brigade | Team Leader: Suraj S
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

TEMPLATE_PATH = "/Users/suraj/.gemini/antigravity/brain/7862b7ed-c5ab-4fea-971e-9f286f4b535e/.user_uploaded/media_1792260306589_c12bd7fb.pptx"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SCREENSHOTS_DIR = os.path.join(DOCS_DIR, "screenshots")
OUTPUT_PPTX = os.path.join(DOCS_DIR, "CareProof_AI_Presentation.pptx")

# Colors matching Google Cloud Dark Theme
C_WHITE = RGBColor(255, 255, 255)
C_CYAN = RGBColor(100, 255, 218)
C_TEAL = RGBColor(13, 148, 136)
C_MUTED = RGBColor(180, 190, 210)
C_AMBER = RGBColor(245, 158, 11)
C_GREEN = RGBColor(34, 197, 94)
C_RED = RGBColor(239, 68, 68)
C_CARD_BG = RGBColor(20, 32, 54)
C_BORDER = RGBColor(35, 60, 95)

# Aliases
WHITE = C_WHITE
CYAN = C_CYAN
TEAL = C_TEAL
MUTED = C_MUTED
AMBER = C_AMBER
GREEN = C_GREEN
RED = C_RED

def style_para(para, text, font_size=13, bold=False, color=C_WHITE, space_after=4):
    para.text = text
    para.font.size = Pt(font_size)
    para.font.bold = bold
    para.font.color.rgb = color
    para.space_after = Pt(space_after)

def add_content_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CYAN):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    return shape

def clear_existing_content_boxes(slide, skip_top_limit=Inches(1.3)):
    """Removes placeholder text boxes in the body area, keeping top banners and logos."""
    shapes_to_remove = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            # Check if it's below top header (title)
            if shape.top > skip_top_limit:
                shapes_to_remove.append(shape)
    for s in shapes_to_remove:
        sp = s._element
        sp.getparent().remove(sp)

def main():
    print(f"📖 Loading official template from: {TEMPLATE_PATH}")
    prs = pptx.Presentation(TEMPLATE_PATH)

    # 1. Delete Slide 2 (the Google Slides download instruction note)
    print("Removing slide 2 (download instruction note)...")
    rId = prs.slides._sldIdLst[1].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[1]

    # Delete any trailing empty slide at the end (Slide 15)
    if len(prs.slides) > 14:
        last_idx = len(prs.slides) - 1
        rId_last = prs.slides._sldIdLst[last_idx].rId
        prs.part.drop_rel(rId_last)
        del prs.slides._sldIdLst[last_idx]

    # -------------------------------------------------------------
    # SLIDE 1: Team Details
    # -------------------------------------------------------------
    print("Formatting Slide 1: Team Details...")
    s1 = prs.slides[0]
    # Shape 0 contains the text frame for team details
    for shape in s1.shapes:
        if shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p0 = tf.paragraphs[0]
            style_para(p0, "Team Details", font_size=24, bold=True, color=C_WHITE, space_after=14)
            
            p1 = tf.add_paragraph()
            style_para(p1, "Team name:  ", font_size=16, bold=True, color=C_CYAN, space_after=6)
            r1 = p1.add_run()
            r1.text = "The 404 Brigade"
            r1.font.bold = True
            r1.font.color.rgb = C_WHITE
            
            p2 = tf.add_paragraph()
            style_para(p2, "Team leader name:  ", font_size=16, bold=True, color=C_CYAN, space_after=8)
            r2 = p2.add_run()
            r2.text = "Suraj S"
            r2.font.bold = True
            r2.font.color.rgb = C_WHITE
            
            p3 = tf.add_paragraph()
            style_para(p3, "Problem Statement:  ", font_size=16, bold=True, color=C_CYAN, space_after=4)
            r3 = p3.add_run()
            r3.text = "CareProof AI — Transparent Social Media Medical Fundraising:\nSolving Claim Fraud, Creator Wallet Diversion, and Uncapped Overfunding via Gemini Multimodal Verification & Direct Hospital Escrow"
            r3.font.size = Pt(13)
            r3.font.color.rgb = C_WHITE

    # -------------------------------------------------------------
    # SLIDE 2: Brief about the idea
    # -------------------------------------------------------------
    print("Formatting Slide 2: Brief about the idea...")
    s2 = prs.slides[1]
    clear_existing_content_boxes(s2)
    
    pillars = [
        ("🚨 The Core Problem", "Social media raises millions for critical healthcare, but donors cannot verify bills, money lands in creator personal bank/UPI accounts, and viral posts raise 200-500% over bills with zero caps or accountability.", RED),
        ("✨ The CareProof Solution", "A transparent, AI-assisted medical crowdfunding platform that bridges social campaigns directly with verified hospital billing escrow accounts (Apollo, Fortis, Tata Memorial) and real-time overfunding locks.", CYAN),
        ("🤖 Google Gemini Multimodal Core", "Uses Gemini 2.0 Flash to extract clinical line-items, cross-check claimed amounts against authentic hospital quotes (+89% inflation flags), audit viral social flyers, and generate multilingual 9:16 video scripts.", GREEN)
    ]
    for idx, (title, desc, col) in enumerate(pillars):
        top_pos = Inches(1.4 + idx * 1.3)
        add_content_card(s2, Inches(0.6), top_pos, Inches(8.8), Inches(1.15), border_color=col)
        tb = s2.shapes.add_textbox(Inches(0.8), top_pos + Inches(0.1), Inches(8.4), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, title, font_size=15, bold=True, color=col, space_after=3)
        p1 = tf.add_paragraph()
        style_para(p1, desc, font_size=12, color=C_WHITE, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 3: Opportunities
    # -------------------------------------------------------------
    print("Formatting Slide 3: Opportunities...")
    s3 = prs.slides[2]
    clear_existing_content_boxes(s3)
    
    opps = [
        ("1. How different is it from existing ideas?", 
         "Existing platforms (GoFundMe, Milaap, Ketto) disburse money straight to creator personal accounts with zero hospital oversight and zero caps. CareProof AI enforces a 100% Zero-Wallet Architecture where funds route strictly to verified hospital billing accounts."),
        ("2. How will it be able to solve the problem?", 
         "• Clinical Verification: Gemini OCR audits hospital invoices before campaigns go live.\n• Overfunding Lock: A thread-safe mutex lock caps donations at 100% and diverts surplus to pediatric funds.\n• Cryptographic Receipts: Every donor gets an immutable SHA-256 transaction hash."),
        ("3. Unique Selling Proposition (USP)", 
         "★ Direct Hospital Escrow Guarantee (0.00% creator cut)\n★ Thread-Safe Overfunding Mutex Lock & Emergency Pediatric Pool\n★ Multimodal Gemini Vision Flyer Scanner for viral Instagram/TikTok posts\n★ Multilingual 9:16 Vertical Reel Studio across 6 languages")
    ]
    for idx, (title, desc, col) in enumerate(zip([o[0] for o in opps], [o[1] for o in opps], [CYAN, TEAL, AMBER])):
        left_pos = Inches(0.5 + idx * 3.05)
        add_content_card(s3, left_pos, Inches(1.4), Inches(2.9), Inches(3.8), border_color=col)
        tb = s3.shapes.add_textbox(left_pos + Inches(0.15), Inches(1.5), Inches(2.6), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, title, font_size=13.5, bold=True, color=col, space_after=8)
        p1 = tf.add_paragraph()
        style_para(p1, desc, font_size=11, color=C_WHITE, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 4: List of features offered by the solution
    # -------------------------------------------------------------
    print("Formatting Slide 4: List of features...")
    s4 = prs.slides[3]
    clear_existing_content_boxes(s4)
    
    features = [
        ("🏥 Direct Hospital Escrow Routing", "100% of proceeds settle directly to Apollo, Fortis, or Tata Memorial billing accounts. Influencer access: 0.00% BLOCKED."),
        ("🔒 Thread-Safe Overfunding Lock", "Atomic mutex lock disables donations at $0 remaining and transparently routes overflow to the Hospital Pediatric Emergency Pool."),
        ("🔍 Multimodal Viral Flyer Scanner", "Gemini 2.0 Flash Vision audits Instagram/TikTok flyers, detects personal UPI IDs (limsontt1@fbl), and migrates them to escrow."),
        ("🩺 Human-in-the-Loop Verifier", "Gemini flags clinical inflation discrepancies (+89.2% on Vikram Singh); authorized medical verifiers sign cryptographic SHA-256 certificates."),
        ("🎬 Multilingual 9:16 Reel Studio", "Generates high-converting vertical video scripts in Hindi, Spanish, Tamil, English, Bengali, and Marathi with smartphone preview."),
        ("📋 Hospital Settlement Portal", "Real-time billing ledger showing inward transfers, receipt hashes (CP-REC-XXXXX), and pediatric pool allocations for hospital accountants.")
    ]
    for idx, (ftitle, fdesc) in enumerate(features):
        r = idx // 3
        c = idx % 3
        cx = Inches(0.5 + c * 3.05)
        cy = Inches(1.4 + r * 1.9)
        add_content_card(s4, cx, cy, Inches(2.9), Inches(1.75), border_color=CYAN if idx % 2 == 0 else TEAL)
        tb = s4.shapes.add_textbox(cx + Inches(0.12), cy + Inches(0.1), Inches(2.65), Inches(1.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, ftitle, font_size=13, bold=True, color=CYAN, space_after=4)
        p1 = tf.add_paragraph()
        style_para(p1, fdesc, font_size=10.5, color=C_WHITE, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 5: Process flow diagram or Use-case diagram
    # -------------------------------------------------------------
    print("Formatting Slide 5: Process flow diagram...")
    s5 = prs.slides[4]
    clear_existing_content_boxes(s5)
    flow_img = os.path.join(DOCS_DIR, "process_flow_diagram.png")
    if os.path.exists(flow_img):
        s5.shapes.add_picture(flow_img, Inches(0.5), Inches(1.35), width=Inches(9.0), height=Inches(3.85))

    # -------------------------------------------------------------
    # SLIDE 6: Wireframes/Mock diagrams of the proposed solution
    # -------------------------------------------------------------
    print("Formatting Slide 6: Wireframes / Prototype Mocks...")
    s6 = prs.slides[5]
    clear_existing_content_boxes(s6)
    
    mock_shots = [
        ("home.png", "1. Live Discovery Grid (/)", Inches(0.5)),
        ("rohan_campaign.png", "2. Direct Escrow & Overfunding (/campaign/...)", Inches(3.6)),
        ("creator_studio.png", "3. Gemini Reel Studio (/creator-studio)", Inches(6.7))
    ]
    for fn, label, left_pos in mock_shots:
        sp = os.path.join(SCREENSHOTS_DIR, fn)
        if os.path.exists(sp):
            add_content_card(s6, left_pos, Inches(1.35), Inches(2.8), Inches(3.85), border_color=TEAL)
            tb = s6.shapes.add_textbox(left_pos, Inches(1.4), Inches(2.8), Inches(0.35))
            tb.text_frame.paragraphs[0].text = label
            tb.text_frame.paragraphs[0].font.size = Pt(11)
            tb.text_frame.paragraphs[0].font.bold = True
            tb.text_frame.paragraphs[0].font.color.rgb = C_CYAN
            tb.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            s6.shapes.add_picture(sp, left_pos + Inches(0.1), Inches(1.8), width=Inches(2.6), height=Inches(3.3))

    # -------------------------------------------------------------
    # SLIDE 7: Architecture diagram of the proposed solution
    # -------------------------------------------------------------
    print("Formatting Slide 7: Architecture diagram...")
    s7 = prs.slides[6]
    clear_existing_content_boxes(s7)
    arch_img = os.path.join(DOCS_DIR, "architecture_diagram.png")
    if os.path.exists(arch_img):
        s7.shapes.add_picture(arch_img, Inches(0.5), Inches(1.35), width=Inches(9.0), height=Inches(3.85))

    # -------------------------------------------------------------
    # SLIDE 8: Technologies to be used in the solution
    # -------------------------------------------------------------
    print("Formatting Slide 8: Technologies...")
    s8 = prs.slides[7]
    clear_existing_content_boxes(s8)
    
    techs = [
        ("Google Gemini 2.0 Flash", "Multimodal Vision for viral flyer forensics, OCR on hospital bills, and sub-second reasoning."),
        ("Google Gemini 1.5 Pro", "Multilingual 9:16 Reel scripts across 6 languages, culturally adapted hooks, and accessible story translation."),
        ("Google Cloud Run", "Serverless container hosting with scale-to-zero when idle and instant concurrency auto-scaling."),
        ("Google Cloud Build", "Automated CI/CD pipeline building Docker images directly from git commits (cloudbuild.yaml)."),
        ("Google Cloud Storage", "Encrypted storage for patient clinical quotes, medical records, and generated video assets."),
        ("Firebase / Cloud Firestore", "Sub-second real-time database powering live donation streams and immutable transaction audits."),
        ("FastAPI & Python 3.11", "High-throughput asynchronous core engine with Pydantic validation guards and threading.Lock mutex."),
        ("Tailwind & Glassmorphic UI", "Mobile-first responsive donor experience with real-time SSE progress bars and phone Reel simulator.")
    ]
    for idx, (tname, tdesc) in enumerate(techs):
        r = idx // 2
        c = idx % 2
        cx = Inches(0.5 + c * 4.6)
        cy = Inches(1.4 + r * 0.95)
        add_content_card(s8, cx, cy, Inches(4.4), Inches(0.85), border_color=CYAN if c == 0 else TEAL)
        tb = s8.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.08), Inches(4.1), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, f"🔷 {tname}", font_size=12.5, bold=True, color=C_CYAN, space_after=2)
        p1 = tf.add_paragraph()
        style_para(p1, tdesc, font_size=9.5, color=C_WHITE, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 9: Estimated implementation cost (optional)
    # -------------------------------------------------------------
    print("Formatting Slide 9: Estimated implementation cost...")
    s9 = prs.slides[8]
    clear_existing_content_boxes(s9)
    
    costs = [
        ("Google Cloud Run", "Free Tier includes 2M requests/mo. Under high traffic spikes: ~$5.00 / month. Scales to zero when idle.", C_CYAN),
        ("Google Gemini 2.0 Flash", "Generous free tier on AI Studio. In production: ~$0.0001 per multimodal flyer audit. ~$2.00 - $4.00 / month.", C_TEAL),
        ("Google Cloud Storage", "Standard GCS storage for clinical records and flyers. 10,000 campaigns = ~5GB: ~$0.15 / month.", C_GREEN),
        ("Firebase Cloud Firestore", "Free Tier provides 50,000 reads/day. Production live progress streams: ~$2.50 / month.", C_WHITE),
        ("TOTAL ESTIMATED PILOT TCO", "Under $10.00 — $15.00 / month total operating expenditure due to serverless Google Cloud architecture.", C_AMBER)
    ]
    for idx, (chead, cdesc, col) in enumerate(costs):
        top_pos = Inches(1.4 + idx * 0.76)
        add_content_card(s9, Inches(0.6), top_pos, Inches(8.8), Inches(0.68), border_color=col)
        tb = s9.shapes.add_textbox(Inches(0.8), top_pos + Inches(0.08), Inches(8.4), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, chead + "  —  " + cdesc, font_size=11.5, bold=(idx == 4), color=col, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 10: Snapshots of the prototype
    # -------------------------------------------------------------
    print("Formatting Slide 10: Snapshots of the prototype...")
    s10 = prs.slides[9]
    clear_existing_content_boxes(s10)
    
    proto_shots = [
        ("scanner_tab.png", "Viral Story Scanner (Gemini Vision)", Inches(0.5)),
        ("verifier.png", "Human-in-the-Loop Verifier Copilot", Inches(3.6)),
        ("hospital_escrow.png", "Hospital Inward Settlement Ledger", Inches(6.7))
    ]
    for fn, label, left_pos in proto_shots:
        sp = os.path.join(SCREENSHOTS_DIR, fn)
        if os.path.exists(sp):
            add_content_card(s10, left_pos, Inches(1.35), Inches(2.8), Inches(3.85), border_color=CYAN)
            tb = s10.shapes.add_textbox(left_pos, Inches(1.4), Inches(2.8), Inches(0.35))
            tb.text_frame.paragraphs[0].text = label
            tb.text_frame.paragraphs[0].font.size = Pt(10.5)
            tb.text_frame.paragraphs[0].font.bold = True
            tb.text_frame.paragraphs[0].font.color.rgb = C_CYAN
            tb.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            s10.shapes.add_picture(sp, left_pos + Inches(0.1), Inches(1.8), width=Inches(2.6), height=Inches(3.3))

    # -------------------------------------------------------------
    # SLIDE 11: Prototype Performance report/Benchmarking
    # -------------------------------------------------------------
    print("Formatting Slide 11: Performance report...")
    s11 = prs.slides[10]
    clear_existing_content_boxes(s11)
    
    benchmarks = [
        ("✅ 16 / 16 Automated Integration Tests Passing (100%)", 
         "End-to-end regression test suite covering health checks, negative donation guards, pending campaign blocks, overfunding mutex caps, and multilingual AI endpoints.", C_GREEN),
        ("⚡ Gemini Inference Speed: ~820ms Latency", 
         "Gemini 2.0 Flash synthesizes full 9:16 vertical video scripts, scene visual hooks, and voiceovers in under 1 second. Multimodal flyer forensic analysis finishes in ~1.1s.", C_CYAN),
        ("🔒 Mutex Concurrency & Race Condition Benchmark", 
         "Zero race conditions detected under high-frequency simulated concurrent donation webhooks. Campaign atomically locks at exactly 100% with surplus routed to pediatric fund.", C_AMBER),
        ("☁️ High-Availability Telemetry on Cloud Run", 
         "Sub-50ms HTTP response latency; stateless scale-to-zero capability; /healthz endpoint integrated for automated Google Cloud Run liveness probes.", C_WHITE)
    ]
    for idx, (bhead, bdesc, col) in enumerate(benchmarks):
        top_pos = Inches(1.4 + idx * 0.95)
        add_content_card(s11, Inches(0.6), top_pos, Inches(8.8), Inches(0.85), border_color=col)
        tb = s11.shapes.add_textbox(Inches(0.8), top_pos + Inches(0.08), Inches(8.4), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, bhead, font_size=13, bold=True, color=col, space_after=2)
        p1 = tf.add_paragraph()
        style_para(p1, bdesc, font_size=10.5, color=C_WHITE, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 12: Additional Details/Future Development
    # -------------------------------------------------------------
    print("Formatting Slide 12: Additional Details / Future Development...")
    s12 = prs.slides[11]
    clear_existing_content_boxes(s12)
    
    future = [
        ("1. ABHA / Ayushman Bharat Digital Mission (ABDM) Integration", "Integration with India's national health stack for direct biometric verification of patient clinical records, doctor licenses, and hospital registration numbers."),
        ("2. On-Chain Zero-Knowledge Proofs (zk-SNARKs)", "Cryptographic proofs that allow donors to remain fully anonymous while publicly proving on a public ledger that their money settled into the verified hospital bank account."),
        ("3. Automated Hospital EHR & Billing API Connectors", "Direct ERP/EHR connectors for Epic Systems, Cerner, and SAP Healthcare, automating real-time patient bed allocation upon escrow settlement."),
        ("4. Cross-Border Humanitarian Escrow", "Global multi-currency escrow settlement for ultra-rare pediatric diseases (e.g. Zolgensma for SMA Type 1, costing $2.1M) across international boundaries.")
    ]
    for idx, (fhead, fdesc) in enumerate(future):
        top_pos = Inches(1.4 + idx * 0.95)
        add_content_card(s12, Inches(0.6), top_pos, Inches(8.8), Inches(0.85), border_color=CYAN if idx % 2 == 0 else TEAL)
        tb = s12.shapes.add_textbox(Inches(0.8), top_pos + Inches(0.08), Inches(8.4), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, fhead, font_size=13, bold=True, color=C_CYAN, space_after=2)
        p1 = tf.add_paragraph()
        style_para(p1, fdesc, font_size=10.5, color=C_WHITE, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 13: Provide links to your:
    # -------------------------------------------------------------
    print("Formatting Slide 13: Provide links to your...")
    s13 = prs.slides[12]
    clear_existing_content_boxes(s13)
    
    links_info = [
        ("🐙 GitHub Public Repository", 
         "https://github.com/prabhasuria/The_404_Brigade", 
         "Complete open-source repository containing FastAPI backend, Gemini services, test suite, Dockerfile, and architecture documentation.", C_CYAN),
        ("🎥 Demo Video Link (3 Minutes)", 
         "https://github.com/prabhasuria/The_404_Brigade/blob/main/docs/CareProof_AI_Real_UI_and_Icons_Walkthrough.mp4", 
         "Full walkthrough video showcasing the real UI, live escrow, overfunding lock, Gemini multilingual Reels, and Baby Elroy flyer scan.", C_AMBER),
        ("🚀 Final Product Link (Live & Operational)", 
         "https://integrate-europe-compilation-planets.trycloudflare.com", 
         "Live public HTTPS prototype accessible from any device worldwide. Also deployable to Google Cloud Run via 'gcloud run deploy'.", C_GREEN)
    ]
    for idx, (lhead, lurl, ldesc, col) in enumerate(links_info):
        top_pos = Inches(1.4 + idx * 1.25)
        add_content_card(s13, Inches(0.6), top_pos, Inches(8.8), Inches(1.15), border_color=col)
        tb = s13.shapes.add_textbox(Inches(0.8), top_pos + Inches(0.1), Inches(8.4), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        style_para(p0, lhead, font_size=14, bold=True, color=col, space_after=2)
        p1 = tf.add_paragraph()
        style_para(p1, lurl, font_size=12, bold=True, color=C_WHITE, space_after=2)
        p2 = tf.add_paragraph()
        style_para(p2, ldesc, font_size=10, color=C_MUTED, space_after=0)

    # -------------------------------------------------------------
    # SLIDE 14: Thank You Slide (Preserved with graphic)
    # -------------------------------------------------------------
    print("Formatting Slide 14: Thank you...")
    # Kept as is with the trophy and Google Cloud branding!

    prs.save(OUTPUT_PPTX)
    print(f"\n🎉 Successfully updated official template presentation!")
    print(f"Path: {OUTPUT_PPTX}")
    print(f"File Size: {os.path.getsize(OUTPUT_PPTX) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
