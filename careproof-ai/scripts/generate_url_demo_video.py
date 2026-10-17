#!/usr/bin/env python3
"""
CareProof AI — URL-by-URL Platform Demo Video Generator
Specifically showcases and explains all 7 pages/URLs:
1. Live Discovery Grid (/)
2. Live Escrow & Overfunding (/campaign/cmp_rohan_heart)
3. Gemini Creator Studio (/creator-studio)
4. Viral Story Scanner (/creator-studio Tab 5)
5. Verifier Copilot (/verifier)
6. Hospital Escrow Ledger (/hospital-escrow)
7. Health API (/healthz) - with visual explanation of REST API JSON monitoring
"""

import os
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Dimensions
WIDTH = 1280
HEIGHT = 720
FPS = 15

# Color Palette (Dark Glassmorphic)
BG_COLOR = (10, 25, 47)         # #0A192F Deep Navy
CARD_BG = (23, 42, 69)          # #172A45 Slate Navy
CYAN = (100, 255, 218)          # #64FFDA Accent Cyan
TEAL = (13, 148, 136)           # #0D9488
WHITE = (240, 246, 252)         # Off White
MUTED = (136, 146, 176)         # Slate Gray
AMBER = (245, 158, 11)          # #F59E0B Warning/Overfunding
GREEN = (34, 197, 94)           # #22C55E Verified Green
RED = (239, 68, 68)             # #EF4444 Alert Red
URL_BG = (15, 30, 55)           # URL bar background

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SAMPLE_IMG_PATH = os.path.join(BASE_DIR, "backend/app/static/sample_docs/sample_viral_reel_elroy.jpg")
os.makedirs(DOCS_DIR, exist_ok=True)
OUTPUT_MP4 = os.path.join(DOCS_DIR, "CareProof_AI_URL_Walkthrough_Demo.mp4")

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except:
    FFMPEG_EXE = "ffmpeg"

PUBLIC_BASE = "https://integrate-europe-compilation-planets.trycloudflare.com"

SCENES = [
    {
        "id": "url_1_discovery",
        "page_num": 1,
        "page_name": "Live Discovery Grid",
        "url_path": "/",
        "narration": "Page one is the Live Discovery Grid at the root URL. Donors and supporters browse authentic, AI-assisted campaigns. Each card displays real-time funding progress, hospital verification badges, and patient details across active, target reached, and pending states."
    },
    {
        "id": "url_2_escrow",
        "page_num": 2,
        "page_name": "Live Escrow & Overfunding Protection",
        "url_path": "/campaign/cmp_rohan_heart",
        "narration": "Page two is the Live Campaign and Overfunding page for Rohan Verma. Funds route strictly to Apollo Hospitals with creator access blocked at zero percent. When a donation fulfills the goal, the thread-safe mutex locks the campaign instantly at one hundred percent, and excess funds are transparently redirected to the Hospital Pediatric Emergency Pool."
    },
    {
        "id": "url_3_studio",
        "page_num": 3,
        "page_name": "Gemini Multilingual Creator Studio",
        "url_path": "/creator-studio",
        "narration": "Page three is the Gemini Creator Studio. Creators use Google Gemini 2.0 Flash to synthesize 9:16 vertical video scripts in Hindi, Spanish, Tamil, and English. The studio generates visual hooks and captions while embedding the holographic CareProof badge, and flags unauthorized personal payment links."
    },
    {
        "id": "url_4_scanner",
        "page_num": 4,
        "page_name": "Viral Story Scanner (Gemini Vision)",
        "url_path": "/creator-studio (Tab 5)",
        "narration": "Page four is Tab 5 of Creator Studio: the Viral Story Scanner. Using Gemini Vision, users upload an Instagram or TikTok flyer, like the viral Save Elroy campaign. In seconds, Gemini inspects the image, flags personal UPI IDs like limsontt1 at fbl, and provides a one-click migration into verified hospital escrow."
    },
    {
        "id": "url_5_verifier",
        "page_num": 5,
        "page_name": "Human-in-the-Loop Verifier Copilot",
        "url_path": "/verifier",
        "narration": "Page five is the Human-in-the-Loop Verifier Copilot. Medical auditors inspect flagged campaigns. For Vikram Singh, Gemini identifies an 89 percent discrepancy between the thirty-five thousand dollar request and the eighteen thousand five hundred dollar Fortis hospital quote, allowing auditors to request documents or issue a cryptographic SHA-256 certificate."
    },
    {
        "id": "url_6_ledger",
        "page_num": 6,
        "page_name": "Hospital Escrow Settlement Ledger",
        "url_path": "/hospital-escrow",
        "narration": "Page six is the Hospital Escrow Portal. Designed for hospital billing departments, this live ledger displays every inward settlement routed to Apollo Hospitals with immutable receipt hashes. Hospital accountants can reconcile treatments and audit emergency pediatric pool balances in real time."
    },
    {
        "id": "url_7_health",
        "page_num": 7,
        "page_name": "Health API & Machine Monitoring",
        "url_path": "/healthz",
        "narration": "Page seven is the Health API at slash healthz. When opened in a browser, it displays raw JSON showing status healthy and version one point zero. This is a REST API machine endpoint designed for Google Cloud Run health checks and uptime monitoring to guarantee that CareProof AI is always online."
    }
]

def generate_voiceover(scene_idx, text, temp_dir):
    aiff_path = os.path.join(temp_dir, f"scene_{scene_idx}.aiff")
    wav_path = os.path.join(temp_dir, f"scene_{scene_idx}.wav")
    
    cmd = ["say", "-v", "Samantha", "-r", "175", "-o", aiff_path, text]
    subprocess.run(cmd, check=True)
    
    cmd_conv = [FFMPEG_EXE, "-y", "-i", aiff_path, "-ar", "44100", "-ac", "2", wav_path]
    subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    cmd_probe = [FFMPEG_EXE, "-i", wav_path]
    res = subprocess.run(cmd_probe, stderr=subprocess.PIPE, text=True)
    dur = 12.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            dur = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break
            
    dur += 1.0  # slight padding
    return wav_path, dur

def draw_browser_mockup(draw, page_num, total_pages, page_name, url_path):
    # Top Browser Chrome Bar
    draw.rounded_rectangle([40, 20, WIDTH - 40, 95], radius=12, fill=(18, 32, 54), outline=(35, 60, 95), width=2)
    
    # 3 Traffic light dots
    draw.ellipse([60, 42, 74, 56], fill=(239, 68, 68))   # Red
    draw.ellipse([84, 42, 98, 56], fill=(245, 158, 11))  # Yellow
    draw.ellipse([108, 42, 122, 56], fill=(34, 197, 94)) # Green
    
    # Browser URL Address Bar
    full_url = f"{PUBLIC_BASE}{url_path}"
    draw.rounded_rectangle([150, 32, WIDTH - 260, 68], radius=8, fill=URL_BG, outline=CYAN, width=1)
    
    # Lock icon and URL text
    draw.text((165, 42), "🔒", font=get_font(13), fill=GREEN)
    draw.text((190, 42), full_url, font=get_font(14, bold=True), fill=WHITE)
    
    # Page indicator pill on right
    draw.rounded_rectangle([WIDTH - 240, 32, WIDTH - 60, 68], radius=8, fill=CYAN)
    draw.text((WIDTH - 225, 42), f"URL {page_num} OF {total_pages}", font=get_font(13, bold=True), fill=(10, 25, 47))
    
    # Page Name Header beneath URL
    draw.text((60, 108), f"PAGE {page_num}: {page_name.upper()}", font=get_font(20, bold=True), fill=CYAN)
    draw.line([(40, 138), (WIDTH - 40, 138)], fill=(30, 50, 80), width=1)

def draw_subtitle_strip(draw, text):
    draw.rounded_rectangle([40, HEIGHT - 55, WIDTH - 40, HEIGHT - 18], radius=8, fill=(15, 30, 55), outline=(40, 70, 110), width=1)
    draw.text((60, HEIGHT - 46), f"🎙️  {text[:125]}...", font=get_font(14), fill=(200, 220, 245))

# -------------------------------------------------------------
# 7 URL Page Renderers
# -------------------------------------------------------------

def render_page_1(t, total_dur):
    """URL 1: Live Discovery Grid (/)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_mockup(draw, 1, 7, "Live Discovery Grid", "/")
    
    # Discovery Grid Cards (4 campaigns)
    cards = [
        ("Rohan Verma (6y)", "Apollo Hospitals", "$19,450 / $22,000", "ACTIVE", CYAN, "88% Funded"),
        ("Ananya Roy (9y)", "Tata Memorial", "$15,000 / $15,000", "TARGET REACHED", AMBER, "100% Locked"),
        ("Vikram Singh (34y)", "Fortis Healthcare", "$35,000 Claimed", "DISCREPANCY FLAGGED", RED, "Quote: $18,500"),
        ("Baby Elroy (1y)", "Apollo Pediatric", "$1.78M / $2.1M", "SMA TYPE 1 (ACTIVE)", GREEN, "Zolgensma Gene Rx")
    ]
    
    card_w = (WIDTH - 80 - 45) // 4
    for i, (name, hosp, raised, status, col, note) in enumerate(cards):
        cx = 40 + i * (card_w + 15)
        draw.rounded_rectangle([cx, 155, cx + card_w, 480], radius=12, fill=CARD_BG, outline=col, width=2)
        
        # Status Pill
        draw.rounded_rectangle([cx + 15, 175, cx + card_w - 15, 205], radius=6, fill=(18, 35, 60), outline=col, width=1)
        draw.text((cx + 25, 182), status, font=get_font(11, bold=True), fill=col)
        
        draw.text((cx + 15, 225), name, font=get_font(16, bold=True), fill=WHITE)
        draw.text((cx + 15, 255), hosp, font=get_font(13), fill=MUTED)
        
        draw.text((cx + 15, 295), raised, font=get_font(15, bold=True), fill=CYAN)
        draw.text((cx + 15, 325), note, font=get_font(12), fill=MUTED)
        
        # Visual Progress Bar
        draw.rounded_rectangle([cx + 15, 360, cx + card_w - 15, 375], radius=6, fill=(30, 50, 75))
        pct = 1.0 if "100%" in note else (0.88 if "88%" in note else (0.85 if "1.78M" in raised else 0.0))
        draw.rounded_rectangle([cx + 15, 360, cx + 15 + int((card_w - 30) * pct), 375], radius=6, fill=col)
        
        # View Campaign Button
        draw.rounded_rectangle([cx + 15, 415, cx + card_w - 15, 455], radius=6, fill=TEAL)
        draw.text((cx + 35, 428), "View Verified Page", font=get_font(12, bold=True), fill=WHITE)
        
    draw_subtitle_strip(draw, SCENES[0]["narration"])
    return np.array(img)

def render_page_2(t, total_dur):
    """URL 2: Live Escrow & Overfunding (/campaign/cmp_rohan_heart)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_mockup(draw, 2, 7, "Live Escrow & Overfunding", "/campaign/cmp_rohan_heart")
    
    progress_ratio = min(1.0, 0.88 + (t / (total_dur * 0.4)) * 0.12)
    current_raised = 19450 + int((22000 - 19450) * min(1.0, (t / (total_dur * 0.4))))
    is_locked = t >= (total_dur * 0.4)
    
    # Left Card: Campaign Details & Animated Cap
    draw.rounded_rectangle([40, 155, 680, 500], radius=12, fill=CARD_BG, outline=AMBER if is_locked else CYAN, width=2)
    draw.text((65, 175), "Rohan Verma — VSD Surgical Repair", font=get_font(22, bold=True), fill=WHITE)
    draw.text((65, 215), f"${current_raised:,} Raised of $22,000 Target", font=get_font(28, bold=True), fill=AMBER if is_locked else CYAN)
    
    # Progress Bar
    draw.rounded_rectangle([65, 270, 655, 300], radius=10, fill=(30, 50, 75))
    fill_w = int((655 - 65) * progress_ratio)
    draw.rounded_rectangle([65, 270, 65 + fill_w, 300], radius=10, fill=AMBER if is_locked else CYAN)
    
    if is_locked:
        draw.rounded_rectangle([65, 325, 655, 415], radius=8, fill=(55, 35, 10), outline=AMBER, width=2)
        draw.text((80, 338), "🔒 OVERFUNDING PROTECTION ACTIVE — TARGET REACHED", font=get_font(15, bold=True), fill=AMBER)
        draw.text((80, 365), "• Thread-safe mutex lock has closed further incoming donations.", font=get_font(13), fill=WHITE)
        draw.text((80, 388), "• Overflow surplus routed to: Apollo Emergency Pediatric Pool.", font=get_font(13), fill=CYAN)
        
        draw.rounded_rectangle([65, 435, 320, 475], radius=6, fill=(40, 50, 65))
        draw.text((95, 448), "🚫 Donations Closed (Capped)", font=get_font(13, bold=True), fill=MUTED)
    else:
        draw.text((65, 325), "⚡ 88.4% Funded • $2,550 Remaining to Fulfill Hospital Quote", font=get_font(14), fill=CYAN)
        draw.rounded_rectangle([65, 365, 320, 410], radius=6, fill=CYAN)
        draw.text((105, 380), "Donate to Hospital Escrow", font=get_font(13, bold=True), fill=(10, 25, 47))

    # Right Card: Hospital Escrow Guarantee
    draw.rounded_rectangle([710, 155, WIDTH - 40, 500], radius=12, fill=CARD_BG, outline=GREEN, width=2)
    draw.text((735, 175), "Direct Hospital Escrow Guarantee", font=get_font(19, bold=True), fill=WHITE)
    
    esc_rows = [
        ("Beneficiary Hospital", "Apollo Hospitals Bannerghatta", CYAN),
        ("Escrow Account Number", "ESCROW-APOLLO-984210", WHITE),
        ("Creator / Influencer Cut", "0.00% (STRICTLY BLOCKED)", GREEN),
        ("Settlement Mechanism", "Direct Bank-to-Bank Webhook", WHITE),
        ("Surplus Redistribution", "Hospital Indigent Patient Welfare", AMBER),
        ("Receipt Verification Hash", "SHA-256 (CP-REC-948102)", MUTED)
    ]
    for idx, (lbl, val, col) in enumerate(esc_rows):
        ry = 220 + idx * 44
        draw.text((735, ry), f"{lbl}:", font=get_font(13, bold=True), fill=MUTED)
        draw.text((930, ry), val, font=get_font(13), fill=col)

    draw_subtitle_strip(draw, SCENES[1]["narration"])
    return np.array(img)

def render_page_3(t, total_dur):
    """URL 3: Gemini Creator Studio (/creator-studio)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_mockup(draw, 3, 7, "Gemini Multilingual Creator Studio", "/creator-studio")
    
    # Left Box: AI Studio Controls & Script
    draw.rounded_rectangle([40, 155, 750, 500], radius=12, fill=CARD_BG, outline=CYAN, width=2)
    draw.text((65, 175), "9:16 Vertical Reel Script Generator (Google Gemini)", font=get_font(18, bold=True), fill=WHITE)
    
    # Language Tabs
    langs = [("Hindi (हिंदी)", True), ("Spanish (Español)", False), ("Tamil (தமிழ்)", False), ("English", False)]
    for i, (lname, act) in enumerate(langs):
        lx = 65 + i * 160
        draw.rounded_rectangle([lx, 210, lx + 145, 238], radius=6, fill=CYAN if act else (20, 35, 55), outline=CYAN, width=1)
        draw.text((lx + 15, 217), lname, font=get_font(12, bold=True), fill=(10, 25, 47) if act else WHITE)
        
    # Script Box
    draw.rounded_rectangle([65, 255, 725, 475], radius=8, fill=(15, 30, 50), outline=(40, 70, 110), width=1)
    f_c = get_font(13)
    draw.text((80, 270), "🎬 SCENE 1 [0-5s] (HOOK): Close-up of 6yo Rohan smiling with toy stethoscope.", font=f_c, fill=CYAN)
    draw.text((80, 298), "🗣️ VOICEOVER (Hindi): 'छह साल के रोहन को चाहिए एक नया जीवन। हर दान सीधे अपोलो में जाता है।'", font=f_c, fill=WHITE)
    draw.text((80, 326), "🎬 SCENE 2 [5-15s]: Official hospital estimate displayed on screen.", font=f_c, fill=CYAN)
    draw.text((80, 354), "🛡️ ON-SCREEN TRUST BADGE: CareProof Verified Stamp (#ESCROW-APOLLO)", font=f_c, fill=GREEN)
    draw.text((80, 382), "🚨 POST AUDITOR: Zero personal UPI/PayPal handles permitted in captions.", font=f_c, fill=AMBER)
    draw.text((80, 415), "⚡ Captions & Hashtags Synthesized in 0.8s via Gemini 2.0 Flash", font=get_font(12), fill=MUTED)

    # Right Box: Smartphone Reel Mockup
    draw.rounded_rectangle([780, 155, WIDTH - 40, 500], radius=20, fill=(18, 30, 50), outline=TEAL, width=2)
    draw.text((830, 180), "9:16 Vertical Reel Preview", font=get_font(14, bold=True), fill=MUTED)
    
    draw.rounded_rectangle([815, 210, WIDTH - 75, 470], radius=12, fill=(25, 40, 65))
    draw.rounded_rectangle([835, 230, 995, 260], radius=15, fill=(16, 185, 129))
    draw.text((850, 238), "✓ CareProof Verified", font=get_font(12, bold=True), fill=WHITE)
    
    draw.text((835, 290), "Save Rohan's Heart ❤️", font=get_font(18, bold=True), fill=WHITE)
    draw.text((835, 320), "Target: $22,000 | Apollo Hospital", font=get_font(13), fill=CYAN)
    draw.rounded_rectangle([835, 360, 1150, 400], radius=8, fill=CYAN)
    draw.text((880, 372), "Donate Direct to Hospital Escrow", font=get_font(14, bold=True), fill=(10, 25, 47))
    draw.text((835, 420), "🔒 100% Escrow • Zero Influencer Intermediation", font=get_font(11), fill=MUTED)

    draw_subtitle_strip(draw, SCENES[2]["narration"])
    return np.array(img)

def render_page_4(t, total_dur):
    """URL 4: Viral Story Scanner (/creator-studio Tab 5)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_mockup(draw, 4, 7, "Viral Story Scanner (Gemini Vision)", "/creator-studio (Tab 5)")
    
    # Left Box: Uploaded Flyer Thumbnail
    draw.rounded_rectangle([40, 155, 450, 500], radius=12, fill=CARD_BG, outline=RED, width=2)
    draw.text((65, 175), "Input: Viral Social Flyer (@abbii.krish)", font=get_font(16, bold=True), fill=WHITE)
    
    if os.path.exists(SAMPLE_IMG_PATH):
        try:
            flyer = Image.open(SAMPLE_IMG_PATH)
            flyer.thumbnail((390, 310))
            img.paste(flyer, (65, 210))
        except:
            draw.text((80, 280), "[Baby Elroy Flyer Loaded]", font=get_font(14), fill=MUTED)
    else:
        draw.text((80, 280), "[Baby Elroy Flyer Loaded]", font=get_font(14), fill=MUTED)

    # Right Box: Gemini Vision Forensics Report
    draw.rounded_rectangle([510, 155, WIDTH - 40, 500], radius=12, fill=CARD_BG, outline=CYAN, width=2)
    draw.text((535, 175), "Gemini 2.0 Flash Vision Forensics Report", font=get_font(19, bold=True), fill=CYAN)
    
    findings = [
        ("🚨 CRITICAL: Personal UPI Handle Detected", "Payment vector resolves to: limsontt1@fbl (Federal Bank). Money bypasses hospital billing.", RED),
        ("⚠️ DUAL-RAIL FRAGMENTATION", "Splits donations across private UPI QR codes and unlinked GoFundMe without unified balance.", AMBER),
        ("⚠️ MISSING FINANCIAL TARGET & HOSPITAL", "Flyer does not declare Zolgensma drug target ($2.1M) or hospital registration credentials.", AMBER),
        ("✅ ONE-CLICK CAREPROOF CONVERSION", "Automatically maps patient details to verified campaign 'cmp_elroy_sma' with direct hospital escrow.", GREEN)
    ]
    for idx, (title, desc, col) in enumerate(findings):
        fy = 220 + idx * 68
        draw.rounded_rectangle([535, fy, WIDTH - 65, fy + 60], radius=8, fill=(15, 30, 52), outline=col, width=1)
        draw.text((550, fy + 8), title, font=get_font(13, bold=True), fill=col)
        draw.text((550, fy + 30), desc, font=get_font(12), fill=WHITE)

    draw_subtitle_strip(draw, SCENES[3]["narration"])
    return np.array(img)

def render_page_5(t, total_dur):
    """URL 5: Verifier Copilot (/verifier)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_mockup(draw, 5, 7, "Human-in-the-Loop Verifier Copilot", "/verifier")
    
    # Left Card: Vikram Singh Case Discrepancy Flag
    draw.rounded_rectangle([40, 155, 620, 500], radius=12, fill=CARD_BG, outline=AMBER, width=2)
    draw.text((65, 175), "AI Discrepancy Flagging (Vikram Singh Case)", font=get_font(18, bold=True), fill=WHITE)
    
    draw.rounded_rectangle([65, 215, 635, 315], radius=8, fill=(45, 25, 25), outline=RED, width=1)
    draw.text((80, 228), "⚠️ INCONSISTENCY FLAGGED: +89.2% INFLATION DETECTED", font=get_font(14, bold=True), fill=RED)
    draw.text((80, 255), "• Influencer Claimed Target: $35,000", font=get_font(13), fill=WHITE)
    draw.text((80, 275), "• Fortis Hospital Clinical Quote: $18,500 (Discrepancy: +$16,500)", font=get_font(13), fill=AMBER)
    draw.text((80, 295), "• Gemini AI Trust Score: 48/100 (FLAGGED FOR HUMAN AUDIT)", font=get_font(12, bold=True), fill=RED)
    
    draw.text((65, 335), "Human Review Actions:", font=get_font(14, bold=True), fill=MUTED)
    draw.rounded_rectangle([65, 360, 210, 400], radius=6, fill=GREEN)
    draw.text((80, 372), "Approve & Sign", font=get_font(13, bold=True), fill=WHITE)
    draw.rounded_rectangle([225, 360, 360, 400], radius=6, fill=AMBER)
    draw.text((240, 372), "Request Docs", font=get_font(13, bold=True), fill=WHITE)
    draw.rounded_rectangle([375, 360, 490, 400], radius=6, fill=RED)
    draw.text((405, 372), "Reject", font=get_font(13, bold=True), fill=WHITE)
    
    draw.text((65, 420), "Cryptographic Certificate Generated on Approval: SHA-256 Stamp", font=get_font(12), fill=CYAN)

    # Right Card: Verifier Security Specs
    draw.rounded_rectangle([680, 155, WIDTH - 40, 500], radius=12, fill=CARD_BG, outline=TEAL, width=2)
    draw.text((705, 175), "Security & Governance Rules", font=get_font(19, bold=True), fill=WHITE)
    
    rules = [
        ("AI Acts as Copilot", "Gemini provides analysis, but humans have sole approval authority."),
        ("Tamper-Evident Hashing", "Approved campaigns receive cryptographic SHA-256 certificate hashes."),
        ("Line-Item Matching", "Bill itemizations are verified against accredited hospital charge masters."),
        ("Medical License Check", "Attending physician registration numbers are checked against medical council records.")
    ]
    for idx, (head, desc) in enumerate(rules):
        ry = 225 + idx * 62
        draw.rounded_rectangle([705, ry, WIDTH - 65, ry + 52], radius=6, fill=(18, 35, 60), outline=(35, 60, 95), width=1)
        draw.text((720, ry + 8), f"🛡️ {head}", font=get_font(13, bold=True), fill=CYAN)
        draw.text((720, ry + 28), desc, font=get_font(12), fill=WHITE)

    draw_subtitle_strip(draw, SCENES[4]["narration"])
    return np.array(img)

def render_page_6(t, total_dur):
    """URL 6: Hospital Escrow Ledger (/hospital-escrow)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_mockup(draw, 6, 7, "Hospital Escrow Settlement Ledger", "/hospital-escrow")
    
    # Inward Settlement Table
    draw.rounded_rectangle([40, 155, WIDTH - 40, 500], radius=12, fill=CARD_BG, outline=TEAL, width=2)
    draw.text((65, 175), "Apollo Hospitals Bannerghatta — Live Inward Settlements", font=get_font(19, bold=True), fill=WHITE)
    
    # Table Header
    draw.rounded_rectangle([65, 215, WIDTH - 65, 255], radius=6, fill=(15, 30, 55))
    draw.text((80, 227), "RECEIPT ID", font=get_font(12, bold=True), fill=CYAN)
    draw.text((260, 227), "PATIENT / CAMPAIGN", font=get_font(12, bold=True), fill=CYAN)
    draw.text((540, 227), "SETTLEMENT AMOUNT", font=get_font(12, bold=True), fill=CYAN)
    draw.text((780, 227), "ACCOUNT ROUTING", font=get_font(12, bold=True), fill=CYAN)
    draw.text((1020, 227), "STATUS", font=get_font(12, bold=True), fill=CYAN)
    
    rows = [
        ("CP-REC-948102", "Rohan Verma (VSD Surgery)", "$2,550.00", "Apollo Main Escrow", "SETTLED (100%)", GREEN),
        ("CP-REC-819204", "Rohan Verma (Surplus)", "$500.00", "Pediatric Emergency Pool", "OVERFLOW POOL", AMBER),
        ("CP-REC-739105", "Baby Elroy (SMA Type 1)", "$50,000.00", "Zolgensma Escrow Acct", "SETTLED (Escrow)", GREEN),
        ("CP-REC-619284", "Ananya Roy (ALL Leukemia)", "$15,000.00", "Tata Memorial Billing", "SETTLED (Final)", GREEN)
    ]
    for idx, (rec, pat, amt, dest, stat, col) in enumerate(rows):
        ry = 270 + idx * 52
        draw.rounded_rectangle([65, ry, WIDTH - 65, ry + 44], radius=6, fill=(18, 35, 60), outline=(35, 60, 95), width=1)
        draw.text((80, ry + 12), rec, font=get_font(12, bold=True), fill=WHITE)
        draw.text((260, ry + 12), pat, font=get_font(12), fill=WHITE)
        draw.text((540, ry + 12), amt, font=get_font(13, bold=True), fill=CYAN)
        draw.text((780, ry + 12), dest, font=get_font(12), fill=MUTED)
        draw.text((1020, ry + 12), stat, font=get_font(12, bold=True), fill=col)

    draw_subtitle_strip(draw, SCENES[5]["narration"])
    return np.array(img)

def render_page_7(t, total_dur):
    """URL 7: Health API (/healthz) — Machine Monitoring Explanation"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_mockup(draw, 7, 7, "Health API & Machine Monitoring", "/healthz")
    
    # Left Card: The Exact JSON Payload Returned
    draw.rounded_rectangle([40, 155, 620, 500], radius=12, fill=CARD_BG, outline=GREEN, width=2)
    draw.text((65, 175), "Browser Raw JSON Response", font=get_font(18, bold=True), fill=WHITE)
    
    # Code Terminal Box showing exact payload
    draw.rounded_rectangle([65, 215, 635, 410], radius=8, fill=(12, 20, 35), outline=(40, 70, 110), width=1)
    f_json = get_font(14)
    draw.text((80, 230), "{", font=f_json, fill=WHITE)
    draw.text((110, 260), '"status": "healthy",', font=f_json, fill=GREEN)
    draw.text((110, 290), '"service": "CareProof AI",', font=f_json, fill=CYAN)
    draw.text((110, 320), '"version": "1.0.0",', font=f_json, fill=WHITE)
    draw.text((110, 350), '"environment": "development"', font=f_json, fill=AMBER)
    draw.text((80, 380), "}", font=f_json, fill=WHITE)
    
    draw.text((65, 430), "✅ Status 200 OK — Backend Service is 100% Operational", font=get_font(14, bold=True), fill=GREEN)

    # Right Card: Why this is a REST API for Cloud Run / Uptime Monitoring
    draw.rounded_rectangle([680, 155, WIDTH - 40, 500], radius=12, fill=CARD_BG, outline=CYAN, width=2)
    draw.text((705, 175), "What is the Health API (/healthz)?", font=get_font(19, bold=True), fill=CYAN)
    
    explanations = [
        ("🤖 REST API Machine Endpoint", "This is not an HTML webpage; it is a machine-readable JSON probe used by automated monitoring systems."),
        ("☁️ Google Cloud Run Liveness Probes", "Google Cloud Run pings /healthz every 10 seconds to verify that the container is healthy and auto-heals if needed."),
        ("⚡ 99.99% Availability Monitoring", "External uptime monitors (e.g. Pingdom, Datadog) poll this endpoint to track server latency and service health."),
        ("🛡️ Zero-Downtime Deployment", "Cloud Build will only route traffic to a newly deployed revision once /healthz responds with status: healthy.")
    ]
    for idx, (head, desc) in enumerate(explanations):
        ry = 220 + idx * 65
        draw.rounded_rectangle([705, ry, WIDTH - 65, ry + 56], radius=6, fill=(18, 35, 60), outline=(35, 60, 95), width=1)
        draw.text((720, ry + 8), head, font=get_font(13, bold=True), fill=WHITE)
        draw.text((720, ry + 30), desc, font=get_font(12), fill=MUTED)

    draw_subtitle_strip(draw, SCENES[6]["narration"])
    return np.array(img)

SCENE_RENDERERS = [
    render_page_1,
    render_page_2,
    render_page_3,
    render_page_4,
    render_page_5,
    render_page_6,
    render_page_7
]

def main():
    print("🎬 Starting CareProof AI URL-by-URL Demo Video Generation...")
    print(f"Target Output: {OUTPUT_MP4}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_files = []
        video_segments = []
        
        for idx, scene in enumerate(SCENES):
            print(f"\n--- Processing URL Page {idx+1}/{len(SCENES)}: {scene['page_name']} ---")
            
            wav_path, duration = generate_voiceover(idx, scene["narration"], temp_dir)
            audio_files.append(wav_path)
            total_frames = int(duration * FPS)
            print(f"Voiceover duration: {duration:.2f}s ({total_frames} frames at {FPS}fps)")
            
            segment_video = os.path.join(temp_dir, f"seg_{idx}.mp4")
            
            cmd_vid = [
                FFMPEG_EXE, "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{WIDTH}x{HEIGHT}",
                "-pix_fmt", "rgb24",
                "-r", str(FPS),
                "-i", "-",
                "-an",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "ultrafast",
                "-crf", "22",
                segment_video
            ]
            
            proc = subprocess.Popen(cmd_vid, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            renderer = SCENE_RENDERERS[idx]
            
            for frame_idx in range(total_frames):
                t = frame_idx / FPS
                arr = renderer(t, duration)
                proc.stdin.write(arr.tobytes())
                
            proc.stdin.close()
            proc.wait()
            
            muxed_segment = os.path.join(temp_dir, f"muxed_{idx}.mp4")
            cmd_mux = [
                FFMPEG_EXE, "-y",
                "-i", segment_video,
                "-i", wav_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                muxed_segment
            ]
            subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            video_segments.append(muxed_segment)
            print(f"✅ URL Page {idx+1} ({scene['page_name']}) rendered and synchronized successfully.")

        print("\nMerging all URL scenes into final video...")
        concat_txt = os.path.join(temp_dir, "concat.txt")
        with open(concat_txt, "w") as f:
            for seg in video_segments:
                f.write(f"file '{seg}'\n")
                
        cmd_final = [
            FFMPEG_EXE, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-c", "copy",
            OUTPUT_MP4
        ]
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        file_size_mb = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)
        print(f"\n🎉 URL Demo Video Generated Successfully!")
        print(f"Path: {OUTPUT_MP4}")
        print(f"Size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    main()
