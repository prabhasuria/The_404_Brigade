#!/usr/bin/env python3
"""
CareProof AI — Word (.docx) and PowerPoint (.pptx) Documentation Generator
Team: The 404 Brigade | Google H2S Hackathon
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import pptx
from pptx.util import Inches as PInches, Pt as PPt
from pptx.dml.color import RGBColor as PRGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
os.makedirs(OUTPUT_DIR, exist_ok=True)
DOCX_PATH = os.path.join(OUTPUT_DIR, "CareProof_AI_System_Documentation.docx")
PPTX_PATH = os.path.join(OUTPUT_DIR, "CareProof_AI_Presentation.pptx")

# -------------------------------------------------------------
# 1. WORD (.DOCX) GENERATOR
# -------------------------------------------------------------
def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_word_document():
    doc = docx.Document()
    
    # Page Setup - Margins 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(33, 37, 41)
    
    # Document Title Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_sub = title_p.add_run("GOOGLE H2S HACKATHON | TEAM: THE 404 BRIGADE\n")
    run_sub.font.size = Pt(10)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(13, 148, 136) # Teal
    
    run_title = title_p.add_run("CareProof AI: System Architecture & Technical Whitepaper")
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    
    desc_p = doc.add_paragraph()
    desc_p.paragraph_format.space_after = Pt(20)
    r_desc = desc_p.add_run("A Transparent, AI-Assisted Medical Crowdfunding Infrastructure with Direct Hospital Escrow & Thread-Safe Overfunding Protection")
    r_desc.font.size = Pt(13)
    r_desc.font.italic = True
    r_desc.font.color.rgb = RGBColor(71, 85, 105)
    
    # Metadata Box
    meta_table = doc.add_table(rows=1, cols=1)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = meta_table.cell(0, 0)
    c.width = Inches(6.5)
    set_cell_background(c, "F1F5F9")
    set_cell_margins(c, top=140, bottom=140, left=200, right=200)
    mp = c.paragraphs[0]
    mp.paragraph_format.space_after = Pt(2)
    mrun = mp.add_run("Platform: ")
    mrun.bold = True
    mp.add_run("CareProof AI  |  ")
    mrun2 = mp.add_run("Submission Track: ")
    mrun2.bold = True
    mp.add_run("Google H2S Hackathon  |  ")
    mrun3 = mp.add_run("Status: ")
    mrun3.bold = True
    mp.add_run("Production Prototype (16/16 Tests Passing)\n")
    mrun4 = mp.add_run("Google Utilities: ")
    mrun4.bold = True
    mp.add_run("Google Gemini 2.0 Flash / 1.5, Google Cloud Run, Cloud Storage, Firebase / Firestore")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(13, 148, 136)
        return p

    # Section 1: Executive Summary
    add_h1("1. Executive Summary")
    doc.add_paragraph(
        "Social media has emerged as humanity's most potent vehicle for emergency healthcare fundraising. "
        "A 60-second video clip or viral Instagram Story can mobilize hundreds of thousands of dollars within hours. "
        "However, the current medical crowdfunding landscape is plagued by three systemic failures that erode donor trust:"
    )
    
    bp1 = doc.add_paragraph(style='List Bullet')
    r1 = bp1.add_run("Unverifiable Claims & Invoice Tampering: ")
    r1.bold = True
    bp1.add_run("Donors have zero automated mechanisms to verify whether claimed treatment costs match genuine hospital quotes or whether bills have been fabricated.")
    
    bp2 = doc.add_paragraph(style='List Bullet')
    r2 = bp2.add_run("Creator Wallet Diversion: ")
    r2.bold = True
    bp2.add_run("Over 95% of social campaigns collect funds into the creator's personal bank account, PayPal, or private UPI handle (e.g. limsontt1@fbl). Intermediaries frequently embezzle or misuse donations.")
    
    bp3 = doc.add_paragraph(style='List Bullet')
    r3 = bp3.add_run("The Overfunding Black Hole: ")
    r3.bold = True
    bp3.add_run("Viral algorithms do not respect financial caps. Campaigns routinely collect 200% to 500% over the actual medical bill with zero real-time shutdown triggers or surplus reconciliation.")
    
    doc.add_paragraph(
        "CareProof AI resolves this crisis by establishing a trust bridge between viral social media and accredited hospital escrow accounts. "
        "Powered by Google Gemini multimodal intelligence and a thread-safe overfunding engine, CareProof AI ensures 100% of donated capital routes "
        "directly to verified hospital billing accounts with automated target caps, cryptographic receipts, and instant surplus redirection."
    )
    
    # Section 2: Problem vs. Solution Table
    add_h1("2. Problem vs. Solution Matrix")
    
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    hdr[0].width = Inches(1.8)
    hdr[1].width = Inches(2.3)
    hdr[2].width = Inches(2.4)
    
    headers = ["Fundraising Dimension", "Traditional Social Crowdfunding", "CareProof AI Implementation"]
    for i, h_text in enumerate(headers):
        set_cell_background(hdr[i], "0F172A")
        set_cell_margins(hdr[i], top=120, bottom=120, left=120, right=120)
        p = hdr[i].paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    matrix_data = [
        ("Clinical Verification", "Self-reported claims; easily forged hospital letterheads; zero OCR verification.", "Google Gemini 2.0 / 1.5 extracts line-item quotes, flags discrepancies, and alerts Human Verifiers."),
        ("Fund Routing", "Funds land in the influencer's or parent's private bank account or personal UPI handle.", "Direct Hospital Escrow: 100% of funds route to hospital accounts (Apollo, Fortis, Tata Memorial)."),
        ("Overfunding Control", "No limits; viral posts keep receiving money long after the hospital bill is settled.", "Thread-Safe Overfunding Engine: Mutex lock auto-locks campaign at $0 remaining and diverts surplus."),
        ("Viral Story Forensics", "Fragmented flyers split donations across GoFundMe and unverified personal QR codes.", "Gemini Vision Story Scanner: Audits flyer images, detects UPI handles, and identifies missing data."),
        ("Global Accessibility", "Monolingual English/Hindi posts limiting reach to specific geographic bubbles.", "Multilingual Creator Studio: Gemini generates vertical 9:16 Reel scripts in 6 major languages.")
    ]
    
    for row_idx, (col1, col2, col3) in enumerate(matrix_data):
        row_cells = table.add_row().cells
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for i, val in enumerate([col1, col2, col3]):
            set_cell_background(row_cells[i], bg_col)
            set_cell_margins(row_cells[i], top=100, bottom=100, left=120, right=120)
            p = row_cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if i == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # Section 3: Architecture & System Design
    add_h1("3. Comprehensive System Architecture")
    doc.add_paragraph(
        "CareProof AI is engineered as an asynchronous, event-driven web platform utilizing FastAPI, Starlette, "
        "and Google Cloud Run. The architecture is divided into five specialized tiers:"
    )
    
    add_h2("Tier 1: Client & Social Media Interaction Layer")
    doc.add_paragraph(
        "Provides donor interfaces, creator workstations, human verifier copilots, and hospital portals. "
        "Built with modern Tailwind CSS and Glassmorphic aesthetics, offering real-time progress bars via SSE/polling "
        "and interactive 9:16 vertical smartphone Reel previews."
    )
    
    add_h2("Tier 2: Asynchronous API Gateway (FastAPI)")
    doc.add_paragraph(
        "Manages request routing, payload validation using Pydantic schemas, cryptographic token verification, and "
        "session authorization. Enforces strict input guards rejecting negative, zero, or pending campaign donations."
    )
    
    add_h2("Tier 3: Google Gemini Intelligence Engine")
    doc.add_paragraph(
        "Employs Gemini 2.0 Flash and 1.5 Pro multimodal models for clinical quote analysis, flyer visual forensics, "
        "multilingual script generation, and draft caption inconsistency auditing."
    )
    
    add_h2("Tier 4: Thread-Safe Escrow & Overfunding Protection Engine")
    doc.add_paragraph(
        "Guarantees financial integrity across concurrent payment webhooks. Utilizes a Python threading.Lock() mutex "
        "to ensure that the remaining campaign balance is re-calculated atomically. Calculates patient allocation, "
        "surplus allocation, and triggers immediate campaign lockdown."
    )
    
    add_h2("Tier 5: Persistence & Cloud Infrastructure")
    doc.add_paragraph(
        "Data access is abstracted across an in-memory transactional database with JSON persistence for hackathon "
        "demonstrations, architecturally mapped for direct drop-in replacement with Google Cloud Firestore and Google Cloud Storage."
    )
    
    # Section 4: Google Utilities & Stack
    add_h1("4. Google Technologies & Utilities Utilized")
    
    tech_table = doc.add_table(rows=1, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    thdr = tech_table.rows[0].cells
    thdr[0].width = Inches(1.8)
    thdr[1].width = Inches(2.2)
    thdr[2].width = Inches(2.5)
    
    for i, h_text in enumerate(["Google Technology", "System Role", "Strategic Benefit"]):
        set_cell_background(thdr[i], "0D9488")
        set_cell_margins(thdr[i], top=120, bottom=120, left=120, right=120)
        p = thdr[i].paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    tech_data = [
        ("Google Gemini 2.0 Flash", "Multimodal flyer auditing, clinical OCR, and discrepancy detection.", "Sub-second inference with high-context visual reasoning; extracts text from complex flyers."),
        ("Google Gemini 1.5 Pro", "Multilingual 9:16 vertical Reel scripts and accessible storytelling.", "Deep linguistic fluency across 6 languages; translates complex medical jargon to 6th-grade level."),
        ("Google Cloud Run", "Serverless container deployment of the entire FastAPI core.", "Zero infrastructure maintenance; scales from 0 to thousands of instances during viral traffic spikes."),
        ("Google Cloud Build", "CI/CD automated container build pipeline via cloudbuild.yaml.", "Repeatable, automated cloud deployment directly from source control."),
        ("Google Cloud Storage (GCS)", "Secure repository for clinical invoices and verification documents.", "High durability, encryption at rest, and fine-grained access control for sensitive records."),
        ("Google Cloud Firestore", "Real-time NoSQL campaign and transaction ledger.", "Sub-second synchronization for live donation progress bars and instant overfunding locks.")
    ]
    
    for row_idx, (col1, col2, col3) in enumerate(tech_data):
        row_cells = tech_table.add_row().cells
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F0FDFA"
        for i, val in enumerate([col1, col2, col3]):
            set_cell_background(row_cells[i], bg_col)
            set_cell_margins(row_cells[i], top=100, bottom=100, left=120, right=120)
            p = row_cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if i == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # Section 5: Technical Deep-Dive
    add_h1("5. Technical Innovations Deep-Dive")
    
    add_h2("5.1 Overfunding Mutex & Surplus Redistribution Policy")
    doc.add_paragraph(
        "In viral fundraising, multiple payments can hit the server simultaneously. Without locking, two concurrent "
        "$500 transactions could both see $200 remaining, leading to an over-collection of $800. "
        "CareProof AI implements thread-safe mutex synchronization:"
    )
    
    callout = doc.add_table(rows=1, cols=1)
    callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    cc = callout.cell(0, 0)
    cc.width = Inches(6.5)
    set_cell_background(cc, "F8FAFC")
    set_cell_margins(cc, top=100, bottom=100, left=160, right=160)
    cp = cc.paragraphs[0]
    cp.paragraph_format.space_after = Pt(0)
    cprun = cp.add_run(
        "with self._lock:\n"
        "    current_campaign = db.get_campaign(campaign_id)\n"
        "    remaining_needed = current_campaign.target_amount - current_campaign.raised_amount\n"
        "    if amount <= remaining_needed:\n"
        "        applied = amount; surplus = 0.0\n"
        "    else:\n"
        "        applied = remaining_needed; surplus = amount - remaining_needed\n"
        "        campaign.status = CampaignStatus.TARGET_REACHED\n"
        "        surplus_destination = 'Hospital Emergency Pediatric Pool'"
    )
    cprun.font.name = 'Courier New'
    cprun.font.size = Pt(9)
    cprun.font.color.rgb = RGBColor(15, 23, 42)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    add_h2("5.2 Direct Hospital Escrow Architecture")
    doc.add_paragraph(
        "Unlike traditional platforms that issue checks to individuals, CareProof AI links each verified campaign to "
        "an escrow sub-ledger associated with an accredited healthcare facility. The hospital portal maintains a transparent "
        "inward settlement ledger where hospital accountants can view transaction hashes (e.g. CP-REC-892147), timestamps, "
        "patient identifiers, and gross/net settlements. Creator wallet access is programmatically hardcoded to 0.00%."
    )
    
    add_h2("5.3 Multimodal Viral Story Scanner (Gemini Vision)")
    doc.add_paragraph(
        "Using Gemini's Part.from_bytes() vision API, CareProof AI accepts uploaded Instagram Story flyers (such as the viral #SaveElroy flyer) "
        "and automatically extracts: (1) Diagnosed disease and urgency level, (2) Target financial sum, (3) Payment mechanisms, and "
        "(4) Identifying clinical credentials. When a flyer directs donors to private accounts (e.g. limsontt1@fbl) without a declared bill target, "
        "the scanner flags high-risk non-compliance and auto-generates a structured CareProof campaign to reroute funds into verified hospital escrow."
    )
    
    # Section 6: Demonstration Walkthrough
    add_h1("6. Hackathon Demonstration Walkthrough")
    doc.add_paragraph("Judges can verify all eight hackathon requirements by executing this guided 5-step walkthrough:")
    
    steps = [
        ("Step 1: Campaign Discovery & Lifecycle States (/)", 
         "View four live campaigns: Rohan Verma ($19,450 raised of $22,000, Active), Ananya Roy ($15,000 Target Reached, Overfunding Active), Vikram Singh (Discrepancy Flagged), and Baby Elroy SMA ($2.1M viral case)."),
        ("Step 2: Real-Time Donation & Mutex Auto-Lock (/campaign/cmp_rohan_heart)", 
         "Observe the direct escrow routing to Apollo Hospitals. Click 'Test Overfunding Protection'. Watch the progress bar instantly hit 100%, trigger the amber lock banner, and verify that subsequent donation attempts are rejected."),
        ("Step 3: Gemini Multilingual Creator Studio (/creator-studio)", 
         "Select Hindi or Spanish to generate a 9:16 vertical Reel script with shot-by-shot visual cues and voiceovers. View it rendered live inside the interactive smartphone simulator with the CareProof Verified Badge."),
        ("Step 4: Viral Story Scanner (Tab 5 of Creator Studio)", 
         "Run the Gemini Vision scanner on the Baby Elroy viral flyer. Observe the forensic analysis flagging the personal UPI ID and unlinked GoFundMe campaign, with an instant one-click path to transparent escrow."),
        ("Step 5: Verifier Copilot & Hospital Settlement Ledger (/verifier & /hospital-escrow)", 
         "Review Vikram Singh's pending campaign where Gemini flags the +89% inflation discrepancy ($35k requested vs $18.5k hospital quote). Then view Apollo's live settlement ledger showing cryptographic payout records.")
    ]
    
    for title, desc in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(title + "\n")
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(13, 148, 136)
        r_d = p.add_run(desc)
        r_d.font.size = Pt(10.5)
        
    # Section 7: Verification & Test Suite
    add_h1("7. Quality Assurance & Test Suite (16/16 Passing)")
    doc.add_paragraph(
        "The system has been rigorously tested against edge cases, concurrency locks, and malicious inputs. "
        "The automated test suite in test_suite.py validates 16 comprehensive test scenarios:"
    )
    
    tests_summary = [
        "1. Health check & uptime telemetry",
        "2. Campaign registry & filtering",
        "3. Live-status polling stream (2.5s cadence)",
        "4. Standard donation settlement lifecycle",
        "5. Rejection of negative & zero-dollar donations",
        "6. Guard against donating to pending/unverified campaigns",
        "7. Thread-safe overfunding cap & atomic state flip",
        "8. Rejection of donations following campaign completion",
        "9. Surplus routing to emergency pediatric pool",
        "10. Live hospital escrow settlement ledger API",
        "11. Human-in-the-Loop review & SHA-256 certificate generation",
        "12. Gemini 2.0 Flash multilingual Reel script synthesis",
        "13. Gemini social media caption generation",
        "14. Gemini post draft discrepancy auditing",
        "15. Plain-language medical story accessibility translation",
        "16. Gemini Vision multimodal flyer forensic scanning"
    ]
    
    for t in tests_summary:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)
        r = bp.add_run(t)
        r.font.size = Pt(10)
        
    # Section 8: Conclusion & Team
    add_h1("8. Social Impact & Team")
    doc.add_paragraph(
        "CareProof AI fundamentally redefines how society responds to pediatric and emergency medical crises. "
        "By replacing unmonitored personal accounts with transparent, AI-verified hospital escrows, we restore donor faith "
        "and ensure that every dollar contributed translates directly into life-saving clinical care."
    )
    
    team_p = doc.add_paragraph()
    team_p.paragraph_format.space_before = Pt(8)
    trun = team_p.add_run("Created with dedication by The 404 Brigade for Google H2S Hackathon.")
    trun.bold = True
    trun.font.color.rgb = RGBColor(15, 23, 42)
    
    doc.save(DOCX_PATH)
    print(f"✅ Successfully generated Word document: {DOCX_PATH}")


# -------------------------------------------------------------
# 2. POWERPOINT (.PPTX) GENERATOR
# -------------------------------------------------------------
def set_slide_background(slide, prgb_color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = prgb_color

def create_powerpoint_presentation():
    prs = pptx.Presentation()
    # Set 16:9 Widescreen dimensions
    prs.slide_width = PInches(13.333)
    prs.slide_height = PInches(7.5)
    
    blank_layout = prs.slide_layouts[6] # Blank
    
    # Palette
    C_BG_DARK = PRGBColor(10, 25, 47)      # Deep Navy
    C_BG_CARD = PRGBColor(23, 42, 69)      # Slate Navy Card
    C_CYAN = PRGBColor(100, 255, 218)      # Teal / Cyan
    C_WHITE = PRGBColor(230, 241, 255)     # Off-white
    C_MUTED = PRGBColor(136, 146, 176)     # Muted Slate
    C_AMBER = PRGBColor(245, 158, 11)     # Amber Accent
    
    def add_header(slide, tag_text, title_text):
        tb = slide.shapes.add_textbox(PInches(1.0), PInches(0.6), PInches(11.333), PInches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.space_after = PPt(4)
        r0 = p0.add_run()
        r0.text = tag_text.upper()
        r0.font.bold = True
        r0.font.size = PPt(11)
        r0.font.color.rgb = C_CYAN
        
        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = title_text
        r1.font.bold = True
        r1.font.size = PPt(26)
        r1.font.color.rgb = C_WHITE

    # ------------------ SLIDE 1: Title Slide ------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_BG_DARK)
    
    # Title Box
    tb1 = s1.shapes.add_textbox(PInches(1.2), PInches(1.8), PInches(10.9), PInches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p_tag = tf1.paragraphs[0]
    p_tag.space_after = PPt(8)
    r_tag = p_tag.add_run()
    r_tag.text = "GOOGLE H2S HACKATHON 2026 | SUBMISSION"
    r_tag.font.bold = True
    r_tag.font.size = PPt(13)
    r_tag.font.color.rgb = C_CYAN
    
    p_main = tf1.add_paragraph()
    p_main.space_after = PPt(14)
    r_main = p_main.add_run()
    r_main.text = "CareProof AI"
    r_main.font.bold = True
    r_main.font.size = PPt(52)
    r_main.font.color.rgb = C_WHITE
    
    p_sub = tf1.add_paragraph()
    p_sub.space_after = PPt(24)
    r_sub = p_sub.add_run()
    r_sub.text = "Transparent Social Media Medical Crowdfunding Connected to\nVerified Hospital Escrow & Thread-Safe Overfunding Protection"
    r_sub.font.size = PPt(20)
    r_sub.font.color.rgb = C_MUTED
    
    p_team = tf1.add_paragraph()
    r_team = p_team.add_run()
    r_team.text = "Developed by: The 404 Brigade  |  Powered by: Google Gemini 2.0 & Google Cloud Run"
    r_team.font.bold = True
    r_team.font.size = PPt(14)
    r_team.font.color.rgb = C_CYAN
    
    # ------------------ SLIDE 2: Problem Statement ------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_DARK)
    add_header(s2, "The Crisis in Social Crowdfunding", "Three Fatal Loopholes in Today's Medical Fundraising")
    
    cards_data = [
        ("🚨 1. Unverifiable Claims", 
         "Anyone can fabricate hospital bills or exaggerate medical estimates on social media.\n\n• Zero automated clinical OCR\n• Inflated target figures (+80-100%)\n• Discrepancies go undetected by donors"),
        ("💸 2. Creator Wallet Diversion", 
         "Donations flow straight into personal accounts, PayPal, or private UPI handles (e.g. limsontt1@fbl).\n\n• Intermediary embezzlement risk\n• No hospital billing oversight\n• Creators control all disbursements"),
        ("📈 3. Overfunding Black Holes", 
         "Viral posts continue raising money with zero real-time caps or surplus reconciliation.\n\n• Viral campaigns raise 200-500% over bills\n• Millions in excess remain unaccounted for\n• No transparent refund or reallocation policy")
    ]
    
    for i, (card_title, card_body) in enumerate(cards_data):
        left_pos = PInches(1.0 + i * 3.85)
        # Background card shape
        shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, PInches(2.2), PInches(3.6), PInches(4.4))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_BG_CARD
        shape.line.color.rgb = C_CYAN if i == 0 else PRGBColor(40, 60, 90)
        
        tb = s2.shapes.add_textbox(left_pos + PInches(0.2), PInches(2.4), PInches(3.2), PInches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.space_after = PPt(12)
        r = p.add_run()
        r.text = card_title
        r.font.bold = True
        r.font.size = PPt(18)
        r.font.color.rgb = C_CYAN
        
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = card_body
        r2.font.size = PPt(14)
        r2.font.color.rgb = C_WHITE

    # ------------------ SLIDE 3: The CareProof AI Solution ------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_DARK)
    add_header(s3, "Our Paradigm Shift", "CareProof AI: Trust & Verification Infrastructure")
    
    sol_cards = [
        ("Google Gemini Verification", "Clinical fact extraction & discrepancy checking comparing claimed amounts against authentic hospital quotes. Human-in-the-Loop review."),
        ("Direct Hospital Escrow", "Funds never touch creator wallets. 100% of proceeds route directly to Apollo, Fortis, or Tata Memorial Hospital escrow accounts."),
        ("Thread-Safe Overfunding Cap", "Atomic mutex lock shuts down donations at $0 remaining. Excess funds are automatically redirected to the Hospital Pediatric Emergency Pool."),
        ("Multimodal Story Scanner", "Gemini Vision audits viral flyers, detects private UPI QR codes, identifies missing doctors, and maps campaigns to verified ledgers.")
    ]
    
    for i, (title, text) in enumerate(sol_cards):
        row = i // 2
        col = i % 2
        left_pos = PInches(1.0 + col * 5.8)
        top_pos = PInches(2.2 + row * 2.3)
        
        shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, PInches(5.5), PInches(2.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_BG_CARD
        shape.line.color.rgb = PRGBColor(45, 70, 105)
        
        tb = s3.shapes.add_textbox(left_pos + PInches(0.3), top_pos + PInches(0.2), PInches(4.9), PInches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.space_after = PPt(6)
        r = p.add_run()
        r.text = f"✨ {title}"
        r.font.bold = True
        r.font.size = PPt(17)
        r.font.color.rgb = C_CYAN
        
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = text
        r2.font.size = PPt(13.5)
        r2.font.color.rgb = C_WHITE

    # ------------------ SLIDE 4: Architecture & Flow ------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_DARK)
    add_header(s4, "System Engineering", "End-to-End Architectural Flow")
    
    flow_steps = [
        ("1. Ingestion & AI OCR", "Creator submits bill; Gemini extracts line-items & computes Trust Score (0-100)."),
        ("2. Human-in-the-Loop", "Medical verifiers inspect discrepancies & issue tamper-evident SHA-256 hash."),
        ("3. Multilingual Reels", "Gemini Creator Studio generates 9:16 vertical scripts & captions in 6 languages."),
        ("4. Escrow Routing", "Donors click verified link; funds route directly to hospital escrow sub-account."),
        ("5. Mutex Overfunding Lock", "Instant target met: Engine locks donations & diverts surplus to pediatric pool.")
    ]
    
    for i, (stitle, sdesc) in enumerate(flow_steps):
        left_pos = PInches(0.9 + i * 2.35)
        shape = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, PInches(2.2), PInches(2.2), PInches(4.4))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_BG_CARD
        shape.line.color.rgb = C_CYAN if i == 4 else PRGBColor(45, 70, 105)
        
        tb = s4.shapes.add_textbox(left_pos + PInches(0.15), PInches(2.4), PInches(1.9), PInches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.space_after = PPt(10)
        r = p.add_run()
        r.text = stitle
        r.font.bold = True
        r.font.size = PPt(15)
        r.font.color.rgb = C_CYAN
        
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = sdesc
        r2.font.size = PPt(13)
        r2.font.color.rgb = C_WHITE

    # ------------------ SLIDE 5: Google Utilities ------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_BG_DARK)
    add_header(s5, "Technology Stack", "Google Technologies & Cloud Utilities Powering CareProof")
    
    g_techs = [
        ("Google Gemini 2.0 Flash", "Multimodal Vision for viral flyer forensic scans & real-time clinical quote extraction."),
        ("Google Gemini 1.5 Pro", "Multilingual 9:16 Reel scripts across 6 languages & plain-language story translation."),
        ("Google Cloud Run", "Serverless containerized hosting; scales from 0 to thousands during viral traffic spikes."),
        ("Google Cloud Build", "CI/CD automated container build pipeline (cloudbuild.yaml) for rapid deployment."),
        ("Google Cloud Storage", "Encrypted, compliant storage for medical bills, clinical letters, and social collateral."),
        ("Google Cloud Firestore", "Sub-second real-time sync for live donation progress bars and atomic status locks.")
    ]
    
    for i, (t_title, t_desc) in enumerate(g_techs):
        row = i // 2
        col = i % 2
        left_pos = PInches(1.0 + col * 5.8)
        top_pos = PInches(2.2 + row * 1.5)
        
        shape = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, PInches(5.5), PInches(1.3))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_BG_CARD
        shape.line.color.rgb = PRGBColor(45, 70, 105)
        
        tb = s5.shapes.add_textbox(left_pos + PInches(0.25), top_pos + PInches(0.15), PInches(5.0), PInches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.space_after = PPt(4)
        r = p.add_run()
        r.text = f"🔷 {t_title}"
        r.font.bold = True
        r.font.size = PPt(16)
        r.font.color.rgb = C_CYAN
        
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = t_desc
        r2.font.size = PPt(12.5)
        r2.font.color.rgb = C_WHITE

    # ------------------ SLIDE 6: Demo Walkthrough ------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_BG_DARK)
    add_header(s6, "Hackathon Demo Walkthrough", "Five Core Demonstrations to Experience in Action")
    
    demo_steps = [
        ("1. Live Discovery Grid (/)", "4 seeded campaigns illustrating Active, Target Reached, Discrepancy Flagged, and SMA viral case."),
        ("2. Live Mutex Overfunding (/campaign/cmp_rohan_heart)", "Click 'Test Overfunding Protection': progress bar hits 100%, locks donations, and routes surplus to hospital."),
        ("3. Gemini Creator Studio (/creator-studio)", "Generate 9:16 vertical Reel scripts in Hindi/Spanish and preview inside interactive smartphone mockup."),
        ("4. Viral Flyer Scanner (Tab 5)", "Gemini Vision audits the Baby Elroy flyer, flags personal UPI (limsontt1@fbl), and generates verified escrow."),
        ("5. Hospital Escrow Portal (/hospital-escrow)", "View real-time inward settlement records with cryptographic transaction hashes and 0% creator cut.")
    ]
    
    for i, (d_title, d_desc) in enumerate(demo_steps):
        top_pos = PInches(2.2 + i * 0.95)
        shape = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PInches(1.0), top_pos, PInches(11.333), PInches(0.8))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_BG_CARD
        shape.line.color.rgb = C_CYAN if i == 1 else PRGBColor(45, 70, 105)
        
        tb = s6.shapes.add_textbox(PInches(1.3), top_pos + PInches(0.12), PInches(10.7), PInches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = d_title + " — "
        r.font.bold = True
        r.font.size = PPt(15)
        r.font.color.rgb = C_CYAN
        
        r2 = p.add_run()
        r2.text = d_desc
        r2.font.size = PPt(13.5)
        r2.font.color.rgb = C_WHITE

    # ------------------ SLIDE 7: QA & Impact ------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_BG_DARK)
    add_header(s7, "Results & Impact", "Test Suite Perfection & Transformational Impact")
    
    # Left Box - Test Results
    s_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PInches(1.0), PInches(2.2), PInches(5.4), PInches(4.4))
    s_l.fill.solid()
    s_l.fill.fore_color.rgb = C_BG_CARD
    s_l.line.color.rgb = C_CYAN
    
    tb_l = s7.shapes.add_textbox(PInches(1.3), PInches(2.4), PInches(4.8), PInches(4.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    pl1 = tf_l.paragraphs[0]
    pl1.space_after = PPt(10)
    rl1 = pl1.add_run()
    rl1.text = "✅ 16 / 16 Automated Tests Passing"
    rl1.font.bold = True
    rl1.font.size = PPt(18)
    rl1.font.color.rgb = C_CYAN
    
    test_points = (
        "• Negative & $0 donation guards verified\n"
        "• Mutex concurrency lock under race conditions\n"
        "• Rejection of donations on completed campaigns\n"
        "• Live-status real-time polling stream\n"
        "• Human verifier cryptographic certificate hash\n"
        "• Gemini Multilingual Reel & Caption generation\n"
        "• Multimodal Vision viral flyer forensic scanner"
    )
    pl2 = tf_l.add_paragraph()
    rl2 = pl2.add_run()
    rl2.text = test_points
    rl2.font.size = PPt(13)
    rl2.font.color.rgb = C_WHITE
    
    # Right Box - Real-world Impact
    s_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PInches(6.9), PInches(2.2), PInches(5.4), PInches(4.4))
    s_r.fill.solid()
    s_r.fill.fore_color.rgb = C_BG_CARD
    s_r.line.color.rgb = C_AMBER
    
    tb_r = s7.shapes.add_textbox(PInches(7.2), PInches(2.4), PInches(4.8), PInches(4.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    pr1 = tf_r.paragraphs[0]
    pr1.space_after = PPt(10)
    rr1 = pr1.add_run()
    rr1.text = "🌍 Humanitarian Impact"
    rr1.font.bold = True
    rr1.font.size = PPt(18)
    rr1.font.color.rgb = C_AMBER
    
    impact_points = (
        "• Rebuilds donor trust in social media philanthropy\n"
        "• Guarantees 100% of donated capital settles at hospitals\n"
        "• Eliminates creator embezzlement & wallet diversion\n"
        "• Ensures overfunding flows to emergency pediatric care\n"
        "• Democratizes fundraising across 6 regional languages\n"
        "• Ready for instant deployment on Google Cloud Run"
    )
    pr2 = tf_r.add_paragraph()
    rr2 = pr2.add_run()
    rr2.text = impact_points
    rr2.font.size = PPt(13)
    rr2.font.color.rgb = C_WHITE

    prs.save(PPTX_PATH)
    print(f"✅ Successfully generated PowerPoint presentation: {PPTX_PATH}")

if __name__ == "__main__":
    create_word_document()
    create_powerpoint_presentation()
