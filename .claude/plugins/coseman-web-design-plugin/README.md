# Coseman Premium Web Design Plugin

> Build award-winning animated websites with AI — SaaS, gaming, luxury, real estate, WordPress delivery.

Built from 5 professional web design courses. Claude executes the full workflow:
- ChatGPT prompts → Magnific AI / FlexClip video → Google AI Studio / Claude code generation → WordPress theme delivery

## Styles Supported

| Style | Key Features | Value |
|-------|-------------|-------|
| SaaS Dark | Neon accents, feature grids, GSAP scroll | $1,500–$3,000 |
| Gaming / FPS | HUD overlays, video background, bold CTAs | $1,500–$3,000 |
| Luxury / Editorial | GLSL shaders, cursor-reactive, editorial type | $3,000–$6,000 |
| Real Estate | Scroll-scrubbed video reveal, cinematic | $2,000–$5,000 |

## Installation

1. Download `coseman-web-design-plugin-v1.0.0.zip`
2. In Claude Code: **Plugins → Install from ZIP**
3. Set your Gemini API key (see Setup below)

## Setup

```bash
# Copy .env.example to ~/.config/gemini/.env
cp .env.example ~/.config/gemini/.env

# Edit and add your keys
nano ~/.config/gemini/.env
```

**Gemini API Key** (required for Google AI Studio):
- Get free at: https://aistudio.google.com
- Keys now start with `AQ.` (2026 format — NOT `AIza...`)
- Use `gemini-2.5-flash` model (not 2.0)

## Usage

Just ask Claude naturally:

- "Build me a SaaS landing page for my app called FlowSync"
- "Create a luxury brand website for my jewelry line"
- "Design a gaming website for my FPS game WARZONE-X"
- "Make a real estate website for Elevate Developments"
- "Build me a WordPress theme for this website"

Claude will:
1. Ask 5 quick questions (brand, style, animation type, etc.)
2. Generate ChatGPT prompts for images/video
3. Generate the complete HTML/CSS/JS site
4. Convert to WordPress theme .zip on request

## Helper Script

```bash
# Check your Gemini key
python3 scripts/generate_site.py --check-key

# Preview design system for a style
python3 scripts/generate_site.py --style luxury --brand "MyBrand" --output design

# Generate all build prompts
python3 scripts/generate_site.py --style saas --brand "FlowSync" --tagline "Ship faster." --output prompts
```

## Workflow Summary

```
1. Ask Claude → get design questions answered
2. Claude generates ChatGPT image prompts
3. You generate images in ChatGPT / DALL-E 3
4. Animate with Magnific AI or FlexClip (Seedance 2.0)
5. Claude builds the site from video URL + reference image
6. Claude exports WordPress theme .zip
7. Upload to WordPress → client edits via Customizer
```

## Quota / Key Issues

If Gemini returns quota errors:
1. Go to https://aistudio.google.com
2. Create a new API key (free, unlimited for standard models)
3. Keys start with `AQ.` — this is normal for 2026 format
4. Update `~/.config/gemini/.env` with the new key
