# Coseman Video Watch

**Command:** `/coseman-video-watch`
**Trigger automatically when:** user pastes a YouTube URL, shares a video file path (.mp4 .mov .avi .mkv .webm), or asks to watch / analyze / summarize / describe a video.

> Multi-engine video analysis — 8 AI engines, automatic fallback, YouTube URLs + local files.

---

## Engine priority order
1. **Gemini 2.5 Flash** — native video + YouTube URLs (best, always try first)
2. **OpenRouter** — free Llama 3.2 vision
3. **GitHub Models** — free GPT-4o mini vision
4. **Nvidia NIM** — free Phi-3.5 vision
5. **Mistral Pixtral** — vision model
6. **Cloudflare Workers AI** — open-source LLaVA vision
7. **Cerebras** — fast text fallback
8. **OpenAI GPT-4o** — frame-based fallback

---

## Steps

### Step 1 — Identify input
- If user gave a YouTube URL → use it directly (Gemini reads it natively)
- If user gave a local file path → use it directly
- If no input yet → ask: "Drop a YouTube URL or a video file path and I'll analyze it."

### Step 2 — Determine prompt
- If user asked a specific question about the video → use that as the prompt
- Default prompt (no question given): second-by-second breakdown

### Step 3 — Run analysis
```bash
python3 "$CLAUDE_PROJECT_DIR/analyze_video.py" "<video_path_or_url>" "<prompt>"
```
To target a specific engine:
```bash
python3 "$CLAUDE_PROJECT_DIR/analyze_video.py" "<video>" "<prompt>" --engine gemini
```

### Step 4 — Present results
- Show the full analysis to the user
- Offer: "Want me to ask it a specific question, re-run with a different engine, or analyze another video?"

### Step 5 — If ALL engines fail
Run the health check and show the user what's broken:
```bash
python3 "$CLAUDE_PROJECT_DIR/health_check.py"
```

---

## Key facts
- `.env` at project root holds all API keys (gitignored — never committed)
- YouTube URLs work with Gemini in remote/Co-work sessions; all engines work locally
- `--engine` flag lets you target one engine directly (gemini, openrouter, github, nvidia, mistral, cloudflare, cerebras, openai)
- Run `python3 health_check.py` anytime to see which engines are live and whether updates are available

---

## Self-update check
At the start of every session the hook runs `health_check.py` automatically.
If it detects stale models, missing keys, or a newer version of the toolkit, it will print a warning. When that happens, tell the user what needs attention.
