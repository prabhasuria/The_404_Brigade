#!/usr/bin/env python3
"""
CareProof AI — Video Generator
Produces a high-definition (720p 16:9), synchronized MP4 demo video with:
- Spoken voiceover narration using macOS text-to-speech
- Dynamic UI simulations (discovery grid, escrow diagram, live progress bar animation, overfunding lock)
- Smartphone mockup showing Gemini multilingual 9:16 Reel scripts
- Baby Elroy viral flyer forensic scan (Gemini Vision)
- Verifier copilot and hospital settlement ledger
- Subtitles, glassmorphism cards, and Google H2S hackathon branding
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

# Color Palette (Glassmorphic Dark Theme)
BG_COLOR = (10, 25, 47)         # #0A192F Deep Navy
CARD_BG = (23, 42, 69)          # #172A45 Slate Navy
CYAN = (100, 255, 218)          # #64FFDA Accent Cyan
TEAL = (13, 148, 136)           # #0D9488
WHITE = (240, 246, 252)         # Off White
MUTED = (136, 146, 176)         # Slate Gray
AMBER = (245, 158, 11)          # #F59E0B Warning/Overfunding
GREEN = (34, 197, 94)           # #22C55E Verified Green
RED = (239, 68, 68)             # #EF4444 Alert Red

# Font paths
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
OUTPUT_MP4 = os.path.join(DOCS_DIR, "CareProof_AI_Demo_Video.mp4")

# Path to ffmpeg from imageio_ffmpeg
try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except:
    FFMPEG_EXE = "ffmpeg"

# -------------------------------------------------------------
# Scenes & Narration Script
# -------------------------------------------------------------
SCENES = [
    {
        "id": "scene_1_intro",
        "title": "Welcome to CareProof AI",
        "subtitle": "Transparent Social Media Fundraising | Google H2S Hackathon",
        "narration": "Welcome to CareProof AI, built by The 404 Brigade for the Google H2S Hackathon. When medical emergencies go viral on social media, millions are raised, but donors cannot verify bills, money lands in creator personal accounts, and viral campaigns overfund with zero caps. CareProof AI fixes this with Gemini verification and direct hospital escrow.",
        "duration_hint": 14.0
    },
    {
        "id": "scene_2_discovery",
        "title": "Verified Campaign Discovery & Escrow",
        "subtitle": "Zero-Wallet Intermediation: 100% Direct to Hospital",
        "narration": "On CareProof AI, donors discover authentic, hospital-verified campaigns. For six-year-old Rohan Verma, all donations route directly to the Apollo Hospitals escrow account. Influencers and creators have zero access to the money, eliminating fraud and wallet diversion completely.",
        "duration_hint": 13.0
    },
    {
        "id": "scene_3_overfunding",
        "title": "Thread-Safe Overfunding Protection",
        "subtitle": "Real-Time Mutex Lock & Emergency Pediatric Pool Routing",
        "narration": "Watch our thread-safe overfunding engine in action. When a donation fulfills the remaining requirement, the campaign locks down instantly at 100%. Surplus funds are automatically routed to the Hospital Emergency Pediatric Pool per disclosed policy, and subsequent donations are strictly rejected.",
        "duration_hint": 14.0
    },
    {
        "id": "scene_4_creator",
        "title": "Google Gemini Multilingual Reel Studio",
        "subtitle": "High-Converting 9:16 Vertical Video Scripts in 6 Languages",
        "narration": "To help families reach a global audience ethically, our Gemini Creator Studio generates 9:16 vertical Reel scripts in Hindi, Spanish, Tamil, and English. Gemini writes visual hooks, spoken voiceovers, and generates captions while embedding the tamper-evident CareProof verification badge.",
        "duration_hint": 14.0
    },
    {
        "id": "scene_5_vision",
        "title": "Viral Story Scanner (Gemini Vision)",
        "subtitle": "Multimodal Flyer Forensics & Payment Vector Auditing",
        "narration": "Our multimodal Gemini Vision scanner inspects viral Instagram flyers like this Save Elroy campaign. It automatically detects personal UPI IDs, flags the absence of a hospital quote, and provides a one-click path to convert fragmented viral posts into a transparent, capped escrow campaign.",
        "duration_hint": 15.0
    },
    {
        "id": "scene_6_verifier",
        "title": "Human-in-the-Loop Verifier & Hospital Ledger",
        "subtitle": "AI Discrepancy Flagging & Cryptographic Settlement Ledger",
        "narration": "For full governance, Gemini acts as a copilot for medical verifiers, flagging invoice inflation, like a thirty-five thousand dollar claim on an eighteen thousand dollar quote. Once approved, hospitals track settlements in real time with immutable transaction receipts.",
        "duration_hint": 14.0
    },
    {
        "id": "scene_7_outro",
        "title": "Built on Google Cloud & Gemini",
        "subtitle": "16 of 16 Tests Passing | Production-Ready on Cloud Run",
        "narration": "CareProof AI combines Google Gemini 2.0 Flash, Cloud Run, Cloud Storage, and Firebase Firestore. With sixteen of sixteen automated integration tests passing, CareProof AI restores donor trust and ensures every single dollar reaches verified patient care.",
        "duration_hint": 13.0
    }
]

def generate_voiceover(scene_idx, text, temp_dir):
    """Uses macOS 'say' to synthesize high quality speech to a wav file."""
    aiff_path = os.path.join(temp_dir, f"scene_{scene_idx}.aiff")
    wav_path = os.path.join(temp_dir, f"scene_{scene_idx}.wav")
    
    # Run macOS say with Samantha voice (high quality natural voice)
    cmd = ["say", "-v", "Samantha", "-r", "175", "-o", aiff_path, text]
    subprocess.run(cmd, check=True)
    
    # Convert aiff to wav using ffmpeg
    cmd_conv = [FFMPEG_EXE, "-y", "-i", aiff_path, "-ar", "44100", "-ac", "2", wav_path]
    subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Get actual duration of wav
    cmd_probe = [
        FFMPEG_EXE, "-i", wav_path
    ]
    res = subprocess.run(cmd_probe, stderr=subprocess.PIPE, text=True)
    # Parse Duration: 00:00:12.34
    dur = 12.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            dur = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break
            
    # Add 1.0 second padding at end for natural transition
    dur += 1.0
    return wav_path, dur

# -------------------------------------------------------------
# Drawing Helpers
# -------------------------------------------------------------
def draw_rounded_card(draw, x, y, w, h, bg_color=CARD_BG, border_color=CYAN, radius=16, border_width=2):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color, outline=border_color, width=border_width)

def draw_header_bar(draw, scene_num, total_scenes, tag_text, title_text):
    # Top Hackathon Tag
    f_tag = get_font(14, bold=True)
    draw.text((60, 36), "GOOGLE H2S HACKATHON | THE 404 BRIGADE", font=f_tag, fill=CYAN)
    
    # Step indicator
    step_str = f"STEP {scene_num} OF {total_scenes}"
    draw.text((WIDTH - 180, 36), step_str, font=f_tag, fill=MUTED)
    
    # Main Header
    f_title = get_font(28, bold=True)
    draw.text((60, 62), title_text, font=f_title, fill=WHITE)
    
    # Decorative line
    draw.line([(60, 106), (WIDTH - 60, 106)], fill=(30, 50, 80), width=1)

def draw_subtitle_strip(draw, text):
    f_sub = get_font(15)
    # Background pill
    draw.rounded_rectangle([60, HEIGHT - 55, WIDTH - 60, HEIGHT - 20], radius=8, fill=(15, 30, 55), outline=(40, 70, 110), width=1)
    draw.text((80, HEIGHT - 46), f"🎙️  {text[:120]}...", font=f_sub, fill=(200, 220, 245))

# -------------------------------------------------------------
# Scene Renderers
# -------------------------------------------------------------
def render_frame_scene_1(t, total_dur):
    """Intro & The 3 Crises"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header_bar(draw, 1, 7, "INTRODUCTION", "CareProof AI — Transparent Medical Crowdfunding")
    
    # Hero Title Card
    draw_rounded_card(draw, 60, 130, WIDTH - 120, 130, bg_color=(18, 36, 62), border_color=CYAN, radius=12)
    f_hero = get_font(22, bold=True)
    f_desc = get_font(15)
    draw.text((90, 148), "Rebuilding Trust in Social Media Healthcare Philanthropy", font=f_hero, fill=CYAN)
    draw.text((90, 185), "Connecting viral social campaigns with verified hospital escrow & thread-safe overfunding protection.", font=f_desc, fill=WHITE)
    draw.text((90, 215), "Powered by Google Gemini 2.0 Flash • Google Cloud Run • Firebase Firestore", font=f_desc, fill=MUTED)
    
    # 3 Problem Cards
    cards = [
        ("🚨 1. Unverifiable Claims", "Anyone can post fake hospital estimates or exaggerate medical bills by 100% on Instagram.", RED),
        ("💸 2. Creator Wallet Diversion", "Donations land in creator personal PayPal or private UPI handles (e.g. limsontt1@fbl).", AMBER),
        ("📈 3. Overfunding Black Holes", "Viral campaigns raise 300%+ with zero caps. Excess millions remain unaccounted for.", CYAN)
    ]
    
    card_w = (WIDTH - 120 - 40) // 3
    for i, (title, desc, color) in enumerate(cards):
        cx = 60 + i * (card_w + 20)
        draw_rounded_card(draw, cx, 290, card_w, 240, bg_color=CARD_BG, border_color=color, radius=12)
        f_ctitle = get_font(18, bold=True)
        f_cdesc = get_font(14)
        draw.text((cx + 20, 315), title, font=f_ctitle, fill=color)
        
        # Word wrap desc
        words = desc.split()
        line1 = " ".join(words[:6])
        line2 = " ".join(words[6:12])
        line3 = " ".join(words[12:])
        draw.text((cx + 20, 365), line1, font=f_cdesc, fill=WHITE)
        draw.text((cx + 20, 395), line2, font=f_cdesc, fill=WHITE)
        draw.text((cx + 20, 425), line3, font=f_cdesc, fill=WHITE)
        
    draw_subtitle_strip(draw, SCENES[0]["narration"])
    return np.array(img)

def render_frame_scene_2(t, total_dur):
    """Discovery & Direct Hospital Escrow"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 2, 7, "CAMPAIGN DISCOVERY", "Direct Hospital Escrow Routing (Zero Wallet Intermediation)")
    
    # Left Card: Campaign Card Mockup (Rohan Verma)
    draw_rounded_card(draw, 60, 130, 520, 400, bg_color=CARD_BG, border_color=CYAN, radius=12)
    f_badge = get_font(12, bold=True)
    draw.rounded_rectangle([85, 155, 230, 180], radius=6, fill=(16, 185, 129))
    draw.text((95, 160), "✓ CAREPROOF VERIFIED", font=f_badge, fill=WHITE)
    
    f_pname = get_font(22, bold=True)
    draw.text((85, 195), "Rohan Verma (6y - VSD Heart Surgery)", font=f_pname, fill=WHITE)
    f_hosp = get_font(15)
    draw.text((85, 230), "Treating Hospital: Apollo Hospitals Bannerghatta", font=f_hosp, fill=MUTED)
    draw.text((85, 255), "Target Bill: $22,000  •  Raised So Far: $19,450", font=f_hosp, fill=CYAN)
    
    # Progress Bar (88%)
    draw.rounded_rectangle([85, 295, 540, 315], radius=10, fill=(30, 50, 75))
    draw.rounded_rectangle([85, 295, 85 + int(455 * 0.88), 315], radius=10, fill=CYAN)
    f_pct = get_font(13, bold=True)
    draw.text((85, 325), "88.4% Funded • Remaining: $2,550", font=f_pct, fill=CYAN)
    
    # Escrow Credential Box
    draw.rounded_rectangle([85, 360, 540, 490], radius=8, fill=(15, 30, 55), outline=(40, 70, 110), width=1)
    f_esc = get_font(13)
    draw.text((100, 375), "🏥 Beneficiary: Apollo Hospitals Escrow Account", font=f_esc, fill=WHITE)
    draw.text((100, 405), "🔒 Account Number: ESCROW-APOLLO-984210", font=f_esc, fill=CYAN)
    draw.text((100, 435), "🚫 Creator Wallet Intermediation: BLOCKED (0.00%)", font=f_esc, fill=GREEN)
    draw.text((100, 462), "🛡️ SHA-256 Certificate Hash: c8f921...e3b4", font=f_esc, fill=MUTED)

    # Right Card: Direct Escrow Routing Flow Diagram
    draw_rounded_card(draw, 620, 130, 600, 400, bg_color=CARD_BG, border_color=TEAL, radius=12)
    f_diag_t = get_font(19, bold=True)
    draw.text((650, 155), "Direct Escrow Settlement Architecture", font=f_diag_t, fill=WHITE)
    
    nodes = [
        ("Donor Credit Card / UPI", "Public Webhook", CYAN),
        ("CareProof Smart Gateway", "Pydantic Input Sanitizer", TEAL),
        ("Apollo Hospital Escrow", "Direct Billing Account", GREEN),
        ("Creator / Influencer", "ACCESS STRICTLY BLOCKED", RED)
    ]
    
    for idx, (title, sub, col) in enumerate(nodes):
        ny = 210 + idx * 72
        draw.rounded_rectangle([650, ny, 1180, ny + 56], radius=8, fill=(18, 36, 62), outline=col, width=1)
        f_nt = get_font(15, bold=True)
        f_ns = get_font(12)
        draw.text((670, ny + 10), title, font=f_nt, fill=col)
        draw.text((670, ny + 32), sub, font=f_ns, fill=MUTED)
        
    draw_subtitle_strip(draw, SCENES[1]["narration"])
    return np.array(img)

def render_frame_scene_3(t, total_dur):
    """Thread-Safe Overfunding Mutex Lock Simulation"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 3, 7, "OVERFUNDING PROTECTION", "Thread-Safe Mutex Lock & Surplus Routing")
    
    # Progress animation over time
    # From 0s to 5s: 88% -> 100%
    # From 5s onward: LOCKED banner appears!
    progress_ratio = min(1.0, 0.88 + (t / (total_dur * 0.4)) * 0.12)
    current_raised = 19450 + int((22000 - 19450) * min(1.0, (t / (total_dur * 0.4))))
    is_locked = t >= (total_dur * 0.4)
    
    # Main Campaign Container
    draw_rounded_card(draw, 60, 130, WIDTH - 120, 400, bg_color=CARD_BG, border_color=AMBER if is_locked else CYAN, radius=12)
    
    f_t = get_font(24, bold=True)
    draw.text((95, 155), "Rohan Verma — Pediatric Cardiac Surgery", font=f_t, fill=WHITE)
    
    # Raised numbers
    f_num = get_font(32, bold=True)
    draw.text((95, 200), f"${current_raised:,} Raised", font=f_num, fill=AMBER if is_locked else CYAN)
    f_tgt = get_font(20)
    draw.text((360, 212), "of $22,000 Target Bill", font=f_tgt, fill=MUTED)
    
    # Animated Progress Bar
    bar_w = WIDTH - 120 - 70
    draw.rounded_rectangle([95, 260, 95 + bar_w, 290], radius=15, fill=(30, 50, 75))
    fill_w = int(bar_w * progress_ratio)
    draw.rounded_rectangle([95, 260, 95 + fill_w, 290], radius=15, fill=AMBER if is_locked else CYAN)
    
    f_pct = get_font(16, bold=True)
    pct_text = "100.0% FUNDED — TARGET ACHIEVED" if is_locked else f"{progress_ratio*100:.1f}% Funded"
    draw.text((95, 305), pct_text, font=f_pct, fill=AMBER if is_locked else CYAN)
    
    # Dynamic Status Banner
    if is_locked:
        # Amber Lockdown Banner
        draw.rounded_rectangle([95, 350, 95 + bar_w, 440], radius=10, fill=(60, 40, 10), outline=AMBER, width=2)
        f_b1 = get_font(18, bold=True)
        f_b2 = get_font(14)
        draw.text((120, 365), "🔒 OVERFUNDING PROTECTION ACTIVATED — CAMPAIGN AUTO-LOCKED", font=f_b1, fill=AMBER)
        draw.text((120, 395), "• Hospital target bill is 100% satisfied. Thread-safe mutex lock has disabled further incoming payments.", font=f_b2, fill=WHITE)
        draw.text((120, 415), "• Inflow surplus (+$500.00) automatically diverted to: Apollo Emergency Pediatric Pool.", font=f_b2, fill=CYAN)
        
        # Disabled Button Simulation
        draw.rounded_rectangle([95, 460, 350, 505], radius=8, fill=(40, 50, 65))
        draw.text((125, 475), "🚫 Donations Closed (Target Met)", font=get_font(14, bold=True), fill=MUTED)
    else:
        # Active Donation Button
        draw.rounded_rectangle([95, 360, 95 + bar_w, 420], radius=10, fill=(15, 35, 60), outline=TEAL, width=1)
        f_a = get_font(15)
        draw.text((120, 380), "⚡ Webhook incoming: $2,550.00 settling directly into Apollo Escrow Ledger...", font=f_a, fill=CYAN)
        
    draw_subtitle_strip(draw, SCENES[2]["narration"])
    return np.array(img)

def render_frame_scene_4(t, total_dur):
    """Gemini Multilingual Creator Studio"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 4, 7, "CREATOR STUDIO", "Google Gemini Multilingual 9:16 Vertical Reel Studio")
    
    # Left Box: Controls & Prompt
    draw_rounded_card(draw, 60, 130, 720, 400, bg_color=CARD_BG, border_color=CYAN, radius=12)
    f_t = get_font(20, bold=True)
    draw.text((90, 155), "AI Script Generation (Gemini 2.0 Flash / 1.5 Pro)", font=f_t, fill=WHITE)
    
    # Language pills
    langs = [("Hindi (हिंदी)", True), ("Spanish (Español)", False), ("Tamil (தமிழ்)", False), ("English", False)]
    for i, (lname, active) in enumerate(langs):
        lx = 90 + i * 160
        draw.rounded_rectangle([lx, 195, lx + 145, 225], radius=6, fill=CYAN if active else (20, 35, 55), outline=CYAN, width=1)
        draw.text((lx + 15, 202), lname, font=get_font(12, bold=True), fill=(10, 25, 47) if active else WHITE)
        
    # Script Output Box
    draw.rounded_rectangle([90, 245, 750, 495], radius=8, fill=(15, 30, 50), outline=(40, 70, 110), width=1)
    f_code = get_font(13)
    draw.text((105, 260), "🎬 SCENE 1 [0-5s] (HOOK): Close-up of 6yo Rohan smiling with toy stethoscope.", font=f_code, fill=CYAN)
    draw.text((105, 290), "🗣️ VOICEOVER (Hindi): 'छह साल के रोहन को चाहिए एक नया जीवन।'", font=f_code, fill=WHITE)
    draw.text((105, 320), "🎬 SCENE 2 [5-15s]: Official Apollo Hospitals quote document on screen.", font=f_code, fill=CYAN)
    draw.text((105, 350), "🗣️ VOICEOVER: 'हर एक रुपया सीधे अपोलो अस्पताल के एस्क्रो खाते में जमा होता है।'", font=f_code, fill=WHITE)
    draw.text((105, 380), "🛡️ ON-SCREEN BADGE: Holographic CareProof Verified Stamp (#ESCROW-APOLLO)", font=f_code, fill=GREEN)
    draw.text((105, 410), "🚫 AUDITOR GUARD: No personal UPI or PayPal allowed in caption or comments.", font=f_code, fill=AMBER)
    draw.text((105, 445), "⚡ Captions & Hashtags Generated in 0.8s via Google Gemini 2.0 Flash", font=get_font(12), fill=MUTED)

    # Right Box: Smartphone Mockup
    draw_rounded_card(draw, 810, 130, 410, 400, bg_color=(15, 25, 45), border_color=TEAL, radius=24, border_width=3)
    # Notch & speaker
    draw.rounded_rectangle([950, 142, 1070, 152], radius=4, fill=(40, 60, 90))
    # Phone screen content
    draw.text((850, 180), "Instagram Reel Preview", font=get_font(14, bold=True), fill=MUTED)
    draw.rounded_rectangle([840, 210, 1190, 460], radius=12, fill=(25, 40, 65))
    
    # Verified Badge on Video
    draw.rounded_rectangle([860, 230, 1020, 260], radius=15, fill=(16, 185, 129))
    draw.text((875, 238), "✓ CareProof Verified", font=get_font(12, bold=True), fill=WHITE)
    
    draw.text((860, 290), "Save Rohan's Heart ❤️", font=get_font(18, bold=True), fill=WHITE)
    draw.text((860, 320), "Target: $22,000 | Apollo Hospital", font=get_font(13), fill=CYAN)
    draw.rounded_rectangle([860, 360, 1160, 400], radius=8, fill=CYAN)
    draw.text((910, 372), "Donate Direct to Hospital", font=get_font(14, bold=True), fill=(10, 25, 47))
    draw.text((860, 420), "🔒 100% Escrow • Zero Influencer Cut", font=get_font(11), fill=MUTED)

    draw_subtitle_strip(draw, SCENES[3]["narration"])
    return np.array(img)

def render_frame_scene_5(t, total_dur):
    """Viral Story Scanner — Gemini Vision (Baby Elroy Case)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 5, 7, "VIRAL STORY SCANNER", "Gemini Vision Multimodal Flyer Forensics (Baby Elroy Case)")
    
    # Left Box: Embedded Sample Flyer
    draw_rounded_card(draw, 60, 130, 440, 400, bg_color=CARD_BG, border_color=RED, radius=12)
    f_t = get_font(17, bold=True)
    draw.text((85, 150), "Input: Viral Social Flyer (@abbii.krish)", font=f_t, fill=WHITE)
    
    # Load and paste thumbnail of sample flyer if present
    if os.path.exists(SAMPLE_IMG_PATH):
        try:
            flyer = Image.open(SAMPLE_IMG_PATH)
            flyer.thumbnail((390, 320))
            img.paste(flyer, (85, 185))
        except:
            draw.text((100, 250), "[Baby Elroy SMA Flyer Loaded]", font=get_font(14), fill=MUTED)
    else:
        draw.text((100, 250), "[Baby Elroy SMA Flyer Loaded]", font=get_font(14), fill=MUTED)

    # Right Box: Gemini Multimodal Vision Forensic Analysis
    draw_rounded_card(draw, 530, 130, 690, 400, bg_color=CARD_BG, border_color=CYAN, radius=12)
    draw.text((560, 150), "Gemini 2.0 Flash Multimodal Vision Audit", font=get_font(19, bold=True), fill=CYAN)
    
    findings = [
        ("🚨 CRITICAL: Personal UPI Handle Detected", "Payment vector resolves to: limsontt1@fbl (Federal Bank). Funds do not route to hospital.", RED),
        ("⚠️ DUAL-RAIL FRAGMENTATION", "Splits donations between private UPI and unlinked GoFundMe without unified balance.", AMBER),
        ("⚠️ MISSING FINANCIAL TARGET & HOSPITAL", "Flyer does not declare Zolgensma drug cost ($2.1M) or hospital billing registration.", AMBER),
        ("✅ CAREPROOF ONE-CLICK REMEDIATION", "Automatically maps patient details to verified campaign 'cmp_elroy_sma' with direct hospital escrow.", GREEN)
    ]
    
    for idx, (title, desc, col) in enumerate(findings):
        fy = 195 + idx * 75
        draw.rounded_rectangle([560, fy, 1190, fy + 65], radius=8, fill=(15, 30, 52), outline=col, width=1)
        draw.text((575, fy + 8), title, font=get_font(14, bold=True), fill=col)
        draw.text((575, fy + 32), desc, font=get_font(12), fill=WHITE)
        
    draw_subtitle_strip(draw, SCENES[4]["narration"])
    return np.array(img)

def render_frame_scene_6(t, total_dur):
    """Human-in-the-Loop Verifier & Hospital Settlement Ledger"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 6, 7, "GOVERNANCE & LEDGER", "Human-in-the-Loop Verifier Copilot & Live Hospital Ledger")
    
    # Left Card: Verifier Copilot (Vikram Singh Case)
    draw_rounded_card(draw, 60, 130, 560, 400, bg_color=CARD_BG, border_color=AMBER, radius=12)
    draw.text((85, 155), "AI Verifier Copilot (Discrepancy Flag)", font=get_font(18, bold=True), fill=WHITE)
    
    draw.rounded_rectangle([85, 195, 595, 290], radius=8, fill=(45, 25, 25), outline=RED, width=1)
    draw.text((100, 205), "⚠️ INCONSISTENCY FLAGGED: +89.2% INFLATION", font=get_font(14, bold=True), fill=RED)
    draw.text((100, 230), "• Creator Target Claim: $35,000", font=get_font(13), fill=WHITE)
    draw.text((100, 250), "• Fortis Hospital Official Quote: $18,500 (Discrepancy: +$16,500)", font=get_font(13), fill=AMBER)
    draw.text((100, 270), "• Gemini AI Trust Score: 48/100 (REQUIRES HUMAN AUDIT)", font=get_font(12, bold=True), fill=RED)
    
    draw.text((85, 310), "Human Review Actions:", font=get_font(14, bold=True), fill=MUTED)
    # Action buttons
    draw.rounded_rectangle([85, 335, 230, 375], radius=6, fill=GREEN)
    draw.text((100, 347), "Approve & Sign", font=get_font(13, bold=True), fill=WHITE)
    draw.rounded_rectangle([245, 335, 380, 375], radius=6, fill=AMBER)
    draw.text((260, 347), "Request Docs", font=get_font(13, bold=True), fill=WHITE)
    draw.rounded_rectangle([395, 335, 510, 375], radius=6, fill=RED)
    draw.text((425, 347), "Reject", font=get_font(13, bold=True), fill=WHITE)
    draw.text((85, 395), "Generates SHA-256 Tamper-Evident Verification Certificate", font=get_font(12), fill=CYAN)

    # Right Card: Hospital Portal Settlement Ledger
    draw_rounded_card(draw, 650, 130, 570, 400, bg_color=CARD_BG, border_color=TEAL, radius=12)
    draw.text((675, 155), "Apollo Hospitals Settlement Ledger", font=get_font(18, bold=True), fill=WHITE)
    
    records = [
        ("CP-REC-948102", "Rohan Verma", "$2,550.00", "Settled to Apollo Bank", GREEN),
        ("CP-REC-819204", "Rohan Verma", "$500.00", "Diverted to Pediatric Pool", AMBER),
        ("CP-REC-739105", "Baby Elroy", "$50,000.00", "Settled to Zolgensma Escrow", GREEN),
        ("CP-REC-619284", "Ananya Roy", "$15,000.00", "Settled to Tata Memorial", GREEN)
    ]
    
    for idx, (rec_id, pat, amt, status, col) in enumerate(records):
        ry = 200 + idx * 68
        draw.rounded_rectangle([675, ry, 1195, ry + 56], radius=6, fill=(18, 35, 60), outline=(35, 60, 95), width=1)
        draw.text((690, ry + 8), f"Receipt: {rec_id}  |  Patient: {pat}", font=get_font(13, bold=True), fill=WHITE)
        draw.text((690, ry + 30), f"Amount: {amt}  •  {status}", font=get_font(12), fill=col)

    draw_subtitle_strip(draw, SCENES[5]["narration"])
    return np.array(img)

def render_frame_scene_7(t, total_dur):
    """Google Cloud Architecture, Tests & Conclusion"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 7, 7, "SUMMARY & RESULTS", "Production-Ready on Google Cloud Run | The 404 Brigade")
    
    # Left Box: Google Tech Badges
    draw_rounded_card(draw, 60, 130, 540, 400, bg_color=CARD_BG, border_color=CYAN, radius=12)
    draw.text((85, 155), "Google Cloud & AI Technologies", font=get_font(20, bold=True), fill=CYAN)
    
    techs = [
        ("Google Gemini 2.0 Flash", "Multimodal OCR, vision forensics, high speed"),
        ("Google Gemini 1.5 Pro", "Multilingual 9:16 script synthesis in 6 languages"),
        ("Google Cloud Run", "Serverless container hosting with auto-scaling"),
        ("Google Cloud Storage", "Encrypted medical invoice & clinical scan storage"),
        ("Firebase Firestore", "Sub-second live donation balance sync")
    ]
    for idx, (title, sub) in enumerate(techs):
        ty = 200 + idx * 56
        draw.rounded_rectangle([85, ty, 575, ty + 46], radius=6, fill=(18, 36, 62), outline=TEAL, width=1)
        draw.text((100, ty + 6), f"🔷 {title}", font=get_font(13, bold=True), fill=WHITE)
        draw.text((100, ty + 24), sub, font=get_font(11), fill=MUTED)

    # Right Box: Results & Verification
    draw_rounded_card(draw, 630, 130, 590, 400, bg_color=CARD_BG, border_color=GREEN, radius=12)
    draw.text((660, 155), "Automated Test Suite & Verification", font=get_font(20, bold=True), fill=GREEN)
    
    draw.rounded_rectangle([660, 195, 1190, 260], radius=8, fill=(20, 50, 35), outline=GREEN, width=2)
    draw.text((680, 210), "✅ 16 OF 16 INTEGRATION TESTS PASSING", font=get_font(16, bold=True), fill=GREEN)
    draw.text((680, 235), "Full test coverage: Concurrency locks, negative amounts, overfunding cap", font=get_font(12), fill=WHITE)

    draw.text((660, 280), "Humanitarian Impact Delivered:", font=get_font(15, bold=True), fill=WHITE)
    impacts = [
        "• 100% direct hospital escrow eliminates creator theft",
        "• Automated overfunding cap stops runaway virality",
        "• Accessible plain-language storytelling empowers families",
        "• Full source code & whitepapers published on GitHub"
    ]
    for idx, imp in enumerate(impacts):
        draw.text((660, 310 + idx * 26), imp, font=get_font(13), fill=CYAN)
        
    draw.text((660, 435), "Thank you for reviewing CareProof AI! — Team The 404 Brigade", font=get_font(14, bold=True), fill=WHITE)

    draw_subtitle_strip(draw, SCENES[6]["narration"])
    return np.array(img)

SCENE_RENDERERS = [
    render_frame_scene_1,
    render_frame_scene_2,
    render_frame_scene_3,
    render_frame_scene_4,
    render_frame_scene_5,
    render_frame_scene_6,
    render_frame_scene_7
]

def main():
    print("🎬 Starting CareProof AI Demo Video Generation...")
    print(f"Target Output: {OUTPUT_MP4}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_files = []
        video_segments = []
        
        for idx, scene in enumerate(SCENES):
            print(f"\n--- Processing Scene {idx+1}/{len(SCENES)}: {scene['title']} ---")
            
            # 1. Synthesize Voiceover Audio
            wav_path, duration = generate_voiceover(idx, scene["narration"], temp_dir)
            audio_files.append(wav_path)
            total_frames = int(duration * FPS)
            print(f"Voiceover duration: {duration:.2f}s ({total_frames} frames at {FPS}fps)")
            
            # 2. Render Frames to temporary raw video segment
            segment_video = os.path.join(temp_dir, f"seg_{idx}.mp4")
            
            # Pipe frames directly to ffmpeg
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
            
            # 3. Mux audio and video segment
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
            print(f"✅ Scene {idx+1} rendered and synchronized successfully.")

        # 4. Concatenate all segments into final MP4
        print("\nMerging all scenes into final video...")
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
        print(f"\n🎉 Demo Video Generated Successfully!")
        print(f"Path: {OUTPUT_MP4}")
        print(f"Size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    main()
