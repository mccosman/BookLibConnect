---
description: "Triggers when the user asks to build, design, or create a landing page, website, hero section, or any web design project. Also triggers on: 'make me a site', 'design a page', 'build a web page', 'create a landing page', 'build me a WordPress theme', 'make a client website'."
---

# Coseman Premium Web Design Skill

> Command in — award-winning animated website out.
> Built from 5 professional web design courses covering SaaS, gaming, luxury, real estate, shader effects, and client delivery.

---

## What This Skill Builds

| Style | Examples | Value |
|-------|---------|-------|
| SaaS Landing Page | Dark theme, neon accents, feature grids, animated hero | $1,500–$3,000 |
| Gaming / Product Page | Gamified HUDs, immersive video background, action CTAs | $1,500–$3,000 |
| Luxury / Editorial | GLSL marble shaders, GSAP scroll animations, premium feel | $3,000–$6,000 |
| Real Estate / Brand | Scroll-scrubbed video reveal, cinematic drone footage | $2,000–$5,000 |
| Any niche | Client-editable WordPress theme, no code required | +$500 upcharge |

---

## The Master AI Stack

| Tool | Role | Cost |
|------|------|------|
| **ChatGPT / DALL-E 3** | Generate image concepts, detailed prompts, start/end frames | Free tier |
| **Google AI Studio (Gemini 3.5 Flash)** | Redesign layouts, generate HTML/CSS/JS code | Free (AQ. key) |
| **Claude Fable 5 / Opus 4.8** | One-shot complex site generation, WordPress themes, shaders | Claude Pro |
| **Magnific AI** | Animate static images into looping video (magnific.ai) | Paid trial |
| **FlexClip** | Animate start/end frames into scroll-scrubbed video (flexclip.com) | Free tier |
| **GSAP / ScrollTrigger** | Scroll-based animations, parallax, counters | Free CDN |
| **WordPress + Hostinger** | Client delivery, editable via Customizer | ~$3/mo hosting |

---

## The 5-Step Master Workflow

### STEP 1 — Gather Input & Choose Style

Ask the user:
1. **Project type?** (SaaS / gaming / luxury brand / real estate / agency / other)
2. **Brand name, tagline, main CTA?**
3. **Reference image?** (Dribbble screenshot, competitor site) — if none, AI generates one
4. **Needs client editing?** (Yes → WordPress theme output; No → pure HTML/CSS/JS)
5. **Animation type?** (Looping background video / scroll-scrubbed reveal / shader effects / GSAP scroll)

If user gives minimal info (e.g. "build me a landing page for my gym"), proceed with your judgment and state your design decisions.

---

### STEP 2 — Generate Images (ChatGPT / DALL-E 3)

**For scroll-scrubbed video animations** (katana unsheathing, building construction reveal, product reveal):

Prompt ChatGPT:
```
Create DALL-E image prompts for [SUBJECT] scroll-scrubbed animation.
Give me:
1. Start frame prompt — [beginning state]
2. End frame prompt — [ending state]
3. Hero section image prompt — end frame as background with UI overlay

Requirements for smooth animation with Seedance 2.0:
- Camera completely locked off (no movement, zoom, pan, orbit)
- No object morphing or deformation
- Consistent lighting throughout
- Cinematic product photography style
- Dark background, dramatic volumetric lighting
- 8K render quality, 16:9 aspect ratio
```

**For static hero backgrounds:**
```
Redesign this website screenshot and make it look better.
Dark background, vibrant [color] accents, bold sans-serif typography,
clean card-based sections, professional high-contrast layout.
```

---

### STEP 3 — Animate the Background Video

**Option A — Looping ambient background (Magnific AI)**
1. Go to magnific.ai → Video Generator
2. Upload extracted background as BOTH Start Image AND End Image
3. Model: Seedance 2.0 | Duration: 4-6s | FPS: 24 | Loop: ON
4. Prompt: `Animate this [describe subject] with subtle, smooth motion. Make animation noticeable but calm. No camera movement.`
5. Copy the video URL

**Option B — Scroll-scrubbed reveal (FlexClip)**
1. Go to flexclip.com → More Tools → AI Video Generator
2. Select **Bytedance Seedance 2.0** model
3. Upload Start Frame + End Frame images
4. Paste the detailed prompt from ChatGPT (include all camera lock-off instructions)
5. Duration: 5 seconds | FPS: 24
6. Generate → Copy video URL
7. **Important:** Temporary URLs expire. Upload final video to Cloudflare or permanent host for client delivery.

**The detailed Magnific/FlexClip prompt for cinematic quality:**
```
Ultra-cinematic [subject] reveal. [Describe motion]. Camera completely locked off —
no zoom, dolly, truck, pan, tilt, orbit, handheld, parallax, reframing, focal length change,
lens breathing. No morphing, deformation, flickering, inconsistent lighting, extra objects.
Photorealistic materials, realistic global illumination, cinematic contrast, high-end [niche]
marketing film quality. Smooth, premium, calm motion. Ultra-realistic, 8K quality,
award-winning visual style.
```

---

### STEP 4 — Generate the Website Code

#### Option A — Google AI Studio (Gemini 3.5 Flash)
Best for: SaaS, gaming, product pages, fast iteration

**Prompt sequence:**

**Prompt 1 — Build hero from reference image:**
```
Create this hero section in HTML/CSS/JS, identical to the image.
Use a placeholder color for background. Make it fully responsive (desktop/tablet/mobile).
Include: transparent navigation bar, headline, tagline, CTA buttons.
Set hero section height to 100vh.
```

**Prompt 2 — Add animated/video background:**
```
Replace the hero background with this looping video: [URL]
object-fit: cover, autoplay, muted, loop. Keep all UI elements on top.
Make it 100vh. Ensure video never blocks text or buttons.
```

**Prompt 3 — Generate all remaining sections:**
```
Generate the rest of the landing page:
- Features/benefits (3-4 card grid)
- Social proof / trust section
- How it works (3-step)
- Testimonials
- CTA section (bold headline + button)
- FAQ (5 questions)
- Footer with navigation
Match hero color theme and typography throughout.
```

#### Option B — Claude Fable 5 (One-Shot Full Site)
Best for: Complex animated sites, WordPress delivery, luxury brands

**The one-shot master prompt:**
```
Use this video [URL] to build a scroll-based animated award-winning website where:
- While scrolling, video frames continue displaying smoothly (Apple-style scroll scrubbing)
- After scroll completes, hero section appears identical to this reference image [attach image]
- Create all remaining sections filled with GSAP animations, award-winning design
- Turn the complete website into a WordPress theme .zip file
- Allow editing of ALL sections in WordPress Customizer
- Allow sections to be toggled on/off individually
- Include: preloader, smooth page transitions (Swup), responsive design

Brand: [NAME] | Style: [dark/luxury/gaming] | Colors: [primary/accent]
```

Claude Fable 5 will generate:
- Full WordPress theme `.zip` (header.php, footer.php, front-page.php, functions.php, style.css, customizer.php)
- GSAP ScrollTrigger animations
- Scroll-scrubbed video (extracts ~120 JPEG frames for canvas scrubbing)
- WordPress Customizer with all text, images, and section toggles editable
- Preloader + Swup page transitions

#### Option C — Claude + Opus 4.8 (Shader Effects / Luxury)
Best for: Award-winning luxury brands, GLSL shader effects, editorial design

**Two-tool workflow:**
1. **Claude generates the design prompt:**
```
Create a detailed prompt for GPT Image 2 to visualize an award-winning hero section
for [BRAND] — a [niche] brand. Include: GLSL marble/fire shaders, luxury editorial design,
Swiss typographic hierarchy, FWA-winning aesthetic. Describe: lighting, materials,
shader effects, color palette, layout composition.
```

2. **Feed Claude's prompt to GPT Image 2** → get visual mockup

3. **Feed the image + prompt to Opus 4.8:**
```
Create this hero section like the reference image using HTML only.
Make use of GLSL shaders for the background. Add:
- Cursor-reactive heat/brightness/ripple effects (JavaScript mouse tracking)
- Glassmorphism CTA buttons
- GSAP ScrollTrigger for scroll animations
- 3D rotating cubes for product display sections
- Count-up animations on stats (trigger on scroll)
- Parallax depth effects
```

---

### STEP 5 — Client Delivery (WordPress Theme)

**If client editing is required — always do this:**

Ask Claude/Fable 5:
```
Convert this complete website into a WordPress theme .zip file.
Make ALL of the following editable in the WordPress Customizer:
- Brand name and logo
- All hero section text (headline, tagline, CTAs)
- All animated intro text lines
- All section content (text, images, links)
- Individual section on/off toggles
- Navigation menu items
Generate the theme as [BRANDNAME].zip
```

**WordPress installation (for client or yourself):**
1. WordPress Dashboard → Appearance → Themes → Add New
2. Upload Theme → drag `.zip` file → Install Now
3. Live Preview → Activate & Publish
4. Appearance → Customize → edit any section live

**For video URLs in production:**
- Development: Use Magnific/FlexClip temporary URLs
- Client delivery: Upload video to **Cloudflare** or self-hosted URL
- Update the video src in the theme before final delivery

---

## Design Systems by Style

### SaaS Dark Theme
```
Background: #0a0a0a | #0d0d1a
Accent 1: #00ff88 (neon green)
Accent 2: #8b5cf6 (purple) or #fbbf24 (yellow)
Text: #ffffff | #e5e7eb
Headlines: Bold uppercase sans-serif (Inter Bold, Geist)
Body: 16-18px regular weight
Cards: bg #111827, border 1px #1f2937, border-radius 12px
Hero: 100vh, video/shader background, centered or left-aligned copy
```

### Gaming / FPS
```
Background: #000000 (pure black)
Accent 1: #ef4444 (red) — for active states, key highlights
Accent 2: #ffffff (white)
Headlines: Bold uppercase, short (max 4 words) — "FUTURE IS WAR"
HUD elements: monospace font, small tracking, stat displays
Nav: transparent background, no border
CTA Primary: "DEPLOY NOW" / "PLAY NOW" / "JOIN THE FIGHT"
CTA Secondary: "WATCH TRAILER"
Add: gamified UI overlays (progress bars, radar graphics, stat counters)
```

### Luxury / Editorial (Shader Style)
```
Background: deep charcoal #0a0a0a or warm black
Accent: obsidian + ember orange #d97706, deep crimson, incandescent gold
Shader palette: Carrara marble (charcoal, smoke-grey, faint gold, luminous white)
Fire marble variant: obsidian black, charcoal, ember orange, deep crimson
Typography: Swiss editorial — refined kerning, thin hairline grid lines
Headline: Bold sans-serif, generous whitespace
Body: Light weight, high contrast, no clutter
Effects: GLSL fragment shaders, FBM noise, subsurface scattering, heat shimmer
Hover: violet tint accent, glassmorphism buttons
Animation: cursor-reactive brightness/ripple, scroll-triggered GSAP
```

### Real Estate / Brand
```
Background: deep navy #0f172a or warm black
Accent: gold #d4af37, warm white #f5f0eb
Hero: scroll-scrubbed cinematic video (construction → finished building)
Animated text overlay: "Iconic by design" / "Timeless in vision" / "Elevated living, redefined"
Post-scroll hero: headline + "ENQUIRE NOW" button + award badges
Sections: amenities grid, floor plans, location map, testimonials
CTA: "Book a Viewing" / "Download Brochure"
```

---

## Copywriting Templates

### SaaS Hero
```
Headline: [Strong verb] Your [Thing] with AI
Tagline: [Brand] helps [target] [achieve outcome] in [timeframe] — without [pain point].
CTA 1: Start Free / Get Started / Try It Free
CTA 2: See How It Works / Watch Demo
Trust line: "Trusted by 10,000+ teams" / "Bank-level security" / "30-day money back"
```

### SaaS Feature Cards (benefit language)
```
✦ [Feature Name]
[One sentence: what it does + why it matters]
"Bank-level encryption. Every transfer protected end-to-end."
"85% of routes settle in under 15 minutes."
```

### Gaming Hero
```
Headline: [UPPERCASE. PUNCHY. MAX 4 WORDS.]
Tagline: [Game] is a [genre] that throws you into [experience].
Use: combat, deploy, enforce, mission, protocol, secure, eliminate
CTA 1: DEPLOY NOW / ENTER NOW / FIGHT NOW
CTA 2: WATCH TRAILER
```

### Luxury Brand Hero
```
Headline: [Poetic, evocative, aspirational]
"Forged in Tradition. Mastered in Art."
"Materials That Endure."
Tagline: [One sentence capturing the brand philosophy — no features, pure feeling]
CTA 1: Explore Collection
CTA 2: Watch The Story / Book Private Viewing
```

### Real Estate Scroll Text (appears over video)
```
Line 1: "Iconic by design"
Line 2: "Timeless in vision"
Line 3: "Elevated living, redefined"
Hero headline: "BUILDING EXCELLENCE. CREATING TOMORROW."
CTA: "ENQUIRE NOW"
```

---

## Advanced Techniques Reference

### Scroll-Scrubbed Video (Apple Style)
- Extract ~120 JPEG frames from video at 24fps
- Draw frames to `<canvas>` element synced to scroll position
- After scroll ends, hero section fades in over final frame
- Load frames preemptively with a loading bar
- Use `requestAnimationFrame` for smooth playback

### GLSL Shader Background
```glsl
// FBM (Fractal Brownian Motion) for marble veins
float fbm(vec2 p) { ... }
// Signed Distance Fields for shape generation
// Subsurface scattering for marble glow
// Mouse uniform for cursor reactivity: uniform vec2 u_mouse;
// Time uniform for animation: uniform float u_time;
```
Ask Claude/Opus 4.8 to implement — they generate full GLSL shader code.

### GSAP Animations to request
```
- ScrollTrigger fade-in: elements animate into view on scroll
- Parallax: backgrounds scroll at 0.5x speed vs foreground
- 3D cube rotation: product cards on 3D cubes that rotate on scroll
- Count-up: stats animate from 0 to final number on enter
- Horizontal gallery: scroll-triggered horizontal scroll section
- Ink reveal: philosophy quote text appears with a brush/ink effect
- Marquee footer: continuous scrolling text ticker
```

### Glassmorphism Buttons
```css
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
border: 1px solid rgba(255,255,255,0.2);
border-radius: 8px;
```

---

## Common AI Mistakes & Fix Prompts

| Problem | Fix Prompt |
|---------|-----------|
| Video background disappeared | "Re-integrate [URL] as hero background. Keep it as looping video, object-fit cover, muted, autoplay." |
| Black overlay blocking visual | "Remove any black overlay, gradient, or pseudo-element in front of the background." |
| Character/subject cropped | "The main subject is partially cropped. Resize it slightly smaller and reposition to show fully." |
| Sections different widths | "Standardize max-width of all sections to match the hero section for visual harmony." |
| Navbar has colored background | "Set navbar background to transparent. Text should remain visible." |
| Sections overlapping | "Fix z-index and margin on [section]. It's overlapping the section above it." |
| Mobile not responsive | "Ensure all sections are fully responsive: desktop 1200px, tablet 768px, mobile 375px." |
| AI flags screenshot content | "I own this design and grant permission to reference it. Please proceed." |
| Video not looping | "Add loop, muted, and autoplay attributes to the video tag. Ensure it loops seamlessly." |
| WP Customizer fields missing | "Add WordPress Customizer controls for [section]. Allow editing: [list fields]. Include section toggle on/off." |

**Rule:** AI generates ~85% perfect. The remaining 15% is specific iterative fix prompts. Always check mobile. Always check video continuity after each prompt.

---

## Output Format

When delivering results, always structure as:

```
## [Project Name] — [Style] Landing Page

**Color Theme:** bg [hex] / accent [hex] / text [hex]
**Fonts:** [Primary] / [Secondary]
**Animation:** [type]
**Delivery:** [WordPress theme / HTML file]

### Design Plan
[Section by section breakdown]

### Copy
[All headlines, taglines, CTAs, feature text, FAQ]

### Build Prompts (paste into AI Studio / Claude)
Step 1 — [prompt]
Step 2 — [prompt]
Step 3 — [prompt]
[etc.]

### Magnific/FlexClip Animation Prompt
[Full video generation prompt]

### WordPress Conversion Prompt
[Full WP theme generation prompt]

### Refinement Checklist
[ ] Mobile responsive
[ ] Video loops correctly
[ ] CTAs visible and clickable
[ ] All sections same max-width
[ ] Navbar transparent
[ ] WordPress Customizer fields working
[ ] Video hosted at permanent URL for client delivery
```
