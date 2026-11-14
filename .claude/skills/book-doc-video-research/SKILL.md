# Book Documentary Video Research

**Command:** `/book-doc-video-research`
**Trigger automatically when:** a YouTube URL or video file path is dropped in conversation while working on the Book-to-Documentary Series (Sacred, Secular & Society).

> Analyze any YouTube video or URL through the lens of documentary production — clip hunt, voice ID, copyright check, and MotionVid/clip slot recommendations.

---

## Purpose

Wraps the Coseman Video Watch engine with Sacred, Secular & Society production intelligence. Use it during research, the clip hunt, or whenever a reference video lands in chat. Outputs are formatted to drop directly into Notion, the Clip Bank doc, or the Production Pack.

---

## Steps

### Step 1 — Identify input
- YouTube URL or local video file path → proceed
- If neither is present → ask: "Drop a YouTube URL or video file path and I'll break it down for the show."

### Step 2 — Determine research mode
Ask (or infer from context):
- **Clip Hunt** — looking for usable left/right commentary clips for a specific episode
- **Reference / Background** — studying how other creators cover this history
- **Full Breakdown** — second-by-second analysis for deep research

Default when no context: Full Breakdown.

### Step 3 — Run the video analysis
```bash
python3 "$CLAUDE_PROJECT_DIR/analyze_video.py" "<video_url_or_path>" "<prompt>"
```

**Prompt by mode:**

- **Clip Hunt:** "Watch this video and extract: (1) every strong argument or claim made, with its timestamp, (2) which political/ideological side the speaker represents, (3) any quote under 30 seconds that could serve as a documentary clip, (4) any moment that pairs with the opposite side, (5) copyright risk level."
- **Reference:** "Watch this video and extract: (1) how the creator frames the topic, (2) their sourcing approach, (3) any facts or quotes I should verify or borrow, (4) gaps in their coverage, (5) their thumbnail and title strategy."
- **Full Breakdown:** "Give a second-by-second breakdown covering: speaker, arguments, sources cited, notable quotes with timestamps, visual/editing approach, and anything usable for a historical documentary series."

### Step 4 — Format output for the show

After the raw analysis comes back, reformat it into the following sections:

---

#### VIDEO RESEARCH REPORT
**URL/Source:** `<url>`
**Analyzed:** `<date>`
**Mode:** `<clip hunt / reference / full breakdown>`
**Series/Episode context:** `<if known>`

---

**WHAT IT IS**
- Creator name and channel
- Topic and framing angle
- Length
- Left / Right / Neutral / Both sides

---

**USABLE CLIPS** *(Clip Hunt mode — log these in the Clip Bank)*

For each usable clip:
| # | Timestamp | Speaker | Quote (verbatim) | Side | Length | Copyright risk |
|---|-----------|---------|------------------|------|--------|----------------|
| 1 | 0:00–0:00 | Name | "exact words" | L/R/N | Xs | Low/Med/High |

- **Pairing note:** does this clip pair with an opposite-side clip you already have?
- **Backup:** suggest a MotionVid quote card if the clip is too risky to use

---

**CLIP SLOT CANDIDATES** *(which of the show's 3–4 clip slots could this fill?)*
- Clip Slot 1 (Stakes) — `<yes/no + reasoning>`
- Clip Slot 2 (The Mirror) — `<yes/no + reasoning>`
- Clip Slot 3 (Reframe/Landing) — `<yes/no + reasoning>`

---

**RESEARCH NOTES** *(for Notion research page)*
- Key facts or claims worth verifying
- Sources the creator cites (check against the book)
- "Nobody connects" thread candidates
- Gaps in their coverage (your episode can fill these)
- Blind-spot grid hits: Left squirm / Right squirm / Both squirm

---

**COPYRIGHT FLAGS**
- Risk level: Low / Medium / High
- Reason:
- Safe harbor note: 10–30s commentary use is generally fair use; check for ContentID on the channel
- Backup plan if claimed: `<MotionVid quote card alternative>`

---

**THUMBNAIL / TITLE INTEL** *(Reference mode)*
- Their title formula
- Thumbnail approach
- What's working (high views relative to subscribers?)
- How to do it differently for Sacred, Secular & Society

---

### Step 5 — Offer next steps

After delivering the report, offer:
1. "Log the clips to the Clip Bank doc now?"
2. "Add the research notes to the Notion page for this series?"
3. "Find an opposite-side clip to pair with this one?"
4. "Analyze another video?"

---

## Engine notes
- Gemini 2.5 Flash handles YouTube URLs natively — no download needed
- In Claude Code cloud sessions (Co-work), only Gemini works (proxy restriction); all engines available locally
- Run `python3 "$CLAUDE_PROJECT_DIR/health_check.py"` if the analysis fails to see which engines are live

---

## Commentator reference (Sacred, Secular & Society pairs)
When identifying speaker side, check against the show's established pairs:

| Left | Right |
|------|-------|
| Lemon | Carlson |
| Reid | Beck |
| Phillip | Kelly |
| Martin | Tatum |
| Sanders-Townsend | Owens |
| Maher | Crowder |
| Przybyla | Shapiro |
| Talarico | Boebert / Knowles |

If the speaker is on this list, flag them by name and pair so you know which side you need next.

---

## Rules (inherited from the show)
- **Never** use clips over 30 seconds without noting the copyright risk
- **Always** verify a quote shown on screen against the original source
- Living people: never note their image for AI lip-sync — quote card only
- Slurs in clips: log them in the Clip Bank as `[CENSORED — slur]`, flag for text-only treatment
- Contested claims from the video: frame as "as argued by [name]" not as fact
