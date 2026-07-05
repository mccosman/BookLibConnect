#!/usr/bin/env python3
"""
Coseman Premium Web Design - Site Generation Helper
Assists with the AI web design pipeline:
  1. Validates Gemini API key (for Google AI Studio code generation)
  2. Generates build prompts for each section
  3. Outputs structured design plan

Usage: python3 generate_site.py --style saas --brand "MyBrand" --tagline "Tagline here"
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"

STYLES = {
    "saas": {
        "bg": "#0a0a0a",
        "accent1": "#00ff88",
        "accent2": "#8b5cf6",
        "text": "#ffffff",
        "headline_font": "Inter Bold",
        "body_font": "Inter Regular",
        "animation": "GSAP ScrollTrigger fade-in + parallax",
        "cta1": "Start Free",
        "cta2": "See How It Works",
    },
    "gaming": {
        "bg": "#000000",
        "accent1": "#ef4444",
        "accent2": "#ffffff",
        "text": "#ffffff",
        "headline_font": "Bold Uppercase Sans-Serif",
        "body_font": "Monospace",
        "animation": "HUD overlays + GSAP scroll",
        "cta1": "DEPLOY NOW",
        "cta2": "WATCH TRAILER",
    },
    "luxury": {
        "bg": "#0a0a0a",
        "accent1": "#d97706",
        "accent2": "#dc2626",
        "text": "#f5f5f5",
        "headline_font": "Swiss Editorial Bold",
        "body_font": "Light Serif",
        "animation": "GLSL marble/fire shaders + GSAP + cursor-reactive",
        "cta1": "Explore Collection",
        "cta2": "Watch The Story",
    },
    "realestate": {
        "bg": "#0f172a",
        "accent1": "#d4af37",
        "accent2": "#f5f0eb",
        "text": "#ffffff",
        "headline_font": "Bold Sans-Serif",
        "body_font": "Light Sans-Serif",
        "animation": "Scroll-scrubbed video reveal (Apple-style) + GSAP",
        "cta1": "ENQUIRE NOW",
        "cta2": "Download Brochure",
    },
}


def check_gemini_key():
    if not GEMINI_KEY:
        print("WARNING: GEMINI_API_KEY not set. Set it in your environment.")
        print("Get a free key at: https://aistudio.google.com")
        print("Note: New keys use AQ. format (not AIza...)")
        return False

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}?key={GEMINI_KEY}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            if "name" in data:
                print(f"Gemini API key valid. Model: {data['name']}")
                return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if "QUOTA" in body or "429" in str(e.code):
            print("Gemini quota exhausted. Get a new key at aistudio.google.com (free).")
        elif "403" in str(e.code) or "401" in str(e.code):
            print(f"Gemini key invalid (HTTP {e.code}). Check your AQ. key.")
        else:
            print(f"Gemini API error: {e.code} - {body[:200]}")
    except Exception as ex:
        print(f"Gemini connection error: {ex}")
    return False


def build_hero_prompt(style, brand, tagline, video_url=None, reference_image=None):
    s = STYLES.get(style, STYLES["saas"])
    bg_desc = "looping video background" if video_url else "animated gradient/shader background"

    prompt = f"""Create a hero section in HTML/CSS/JS for '{brand}'.

Style: {style.upper()} / {s['animation']}
Colors: bg {s['bg']}, accent {s['accent1']}, text {s['text']}
Font: {s['headline_font']} for headlines, {s['body_font']} for body

Requirements:
- Transparent navigation bar with logo '{brand}' on left, nav links on right
- Hero height: 100vh
- Background: {bg_desc}
- Headline: bold, uppercase, dominant
- Tagline: {tagline}
- CTA buttons: '{s['cta1']}' (primary) and '{s['cta2']}' (secondary, outlined)
- Fully responsive (desktop 1200px / tablet 768px / mobile 375px)
- No colored navbar background — transparent only"""

    if video_url:
        prompt += f"\n\nVideo URL for background: {video_url}\nUse: autoplay, muted, loop, object-fit: cover, 100vh"

    if reference_image:
        prompt += f"\n\nReference image provided — match the visual layout exactly."

    return prompt


def build_sections_prompt(style, brand):
    return f"""Generate all remaining landing page sections for '{brand}' ({style.upper()} style):

1. Features/benefits grid (3-4 cards with icons, headline, one-line description)
2. Social proof / trust bar (logos or "Trusted by X+ teams")
3. How it works (3-step process with numbered circles)
4. Testimonials (2-3 cards with avatar, name, role, quote)
5. CTA section (bold headline + primary button)
6. FAQ accordion (5 questions)
7. Footer (logo, nav links, copyright)

Design rules:
- Match hero color theme and typography throughout
- All sections same max-width as hero
- GSAP ScrollTrigger fade-in on all sections
- Cards: bg #111827, border 1px solid rgba(255,255,255,0.1), border-radius 12px
- Consistent padding: 80px top/bottom on desktop, 40px on mobile"""


def build_wordpress_prompt(brand, zip_name=None):
    if not zip_name:
        zip_name = brand.lower().replace(" ", "-")
    return f"""Convert this complete website into a WordPress theme .zip file named '{zip_name}.zip'.

Make ALL of the following editable in the WordPress Customizer:
- Brand name and logo (Site Identity panel)
- All hero section text (headline, tagline, CTA labels)
- All animated intro text lines
- All section content (text, images, links)
- Individual section on/off toggles
- Navigation menu items
- Contact/inquiry form settings

Required theme files:
- style.css (with Theme Name: {brand}, Author, Version headers)
- functions.php (register customizer, enqueue scripts/styles, menu support)
- header.php (wp_head(), nav menu, logo)
- footer.php (wp_footer(), footer content)
- front-page.php (main homepage with all sections)
- customizer.php (all Kirki or native WP_Customize_Manager controls)
- index.php (blog fallback)
- screenshot.png (theme preview)
- assets/ folder (CSS, JS, images)

WordPress Customizer sections to register:
- Branding & Navigation
- Hero Section (headline, tagline, CTAs, video URL)
- Features Section (title, 4 feature cards)
- Testimonials Section
- CTA Section
- Footer

Each section must have a toggle control (checkbox) to show/hide it entirely."""


def main():
    parser = argparse.ArgumentParser(description="Coseman Web Design — Site Generator Helper")
    parser.add_argument("--style", choices=list(STYLES.keys()), default="saas")
    parser.add_argument("--brand", default="MyBrand")
    parser.add_argument("--tagline", default="The future, built today.")
    parser.add_argument("--video-url", default="", help="Video URL for scroll-scrubbed or background video")
    parser.add_argument("--check-key", action="store_true", help="Test Gemini API key and exit")
    parser.add_argument("--output", choices=["prompts", "design", "wordpress"], default="prompts")
    args = parser.parse_args()

    if args.check_key:
        ok = check_gemini_key()
        sys.exit(0 if ok else 1)

    s = STYLES[args.style]

    if args.output == "design":
        print(f"\n{'='*60}")
        print(f"  {args.brand} — {args.style.upper()} Design Plan")
        print(f"{'='*60}")
        print(f"  Background:  {s['bg']}")
        print(f"  Accent 1:    {s['accent1']}")
        print(f"  Accent 2:    {s['accent2']}")
        print(f"  Text:        {s['text']}")
        print(f"  Headlines:   {s['headline_font']}")
        print(f"  Body:        {s['body_font']}")
        print(f"  Animation:   {s['animation']}")
        print(f"  CTA Primary: {s['cta1']}")
        print(f"  CTA Second.: {s['cta2']}")
        print()

    elif args.output == "prompts":
        print("\n=== STEP 1: Hero Section Prompt ===\n")
        print(build_hero_prompt(args.style, args.brand, args.tagline, args.video_url or None))
        print("\n=== STEP 2: Remaining Sections Prompt ===\n")
        print(build_sections_prompt(args.style, args.brand))
        print("\n=== STEP 3: WordPress Theme Prompt ===\n")
        print(build_wordpress_prompt(args.brand))

    elif args.output == "wordpress":
        print(build_wordpress_prompt(args.brand))


if __name__ == "__main__":
    main()
