"""
Video analysis — tries engines in order until one succeeds.

  Priority order:
    1. Gemini 2.5 Flash     — native video + YouTube URLs  (GEMINI_API_KEY)
    2. OpenRouter           — free vision models           (OPENROUTER_API_KEY)
    3. GitHub Models        — free GPT-4o mini vision      (GITHUB_TOKEN)
    4. Nvidia NIM           — free vision endpoint         (NVIDIA_API_KEY)
    5. Mistral Pixtral      — vision model                 (MISTRAL_API_KEY)
    6. Cloudflare Workers   — free open-source vision      (CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID)
    7. Cerebras             — fast text fallback            (CEREBRAS_API_KEY)
    8. OpenAI GPT-4o        — frame-based fallback          (OPENAI_API_KEY)

Usage:
  python3 analyze_video.py <video_path_or_youtube_url> [prompt]
  python3 analyze_video.py video.mp4
  python3 analyze_video.py https://youtube.com/watch?v=...
  python3 analyze_video.py video.mp4 "What are the key moments?"
  python3 analyze_video.py video.mp4 --engine gemini
  python3 analyze_video.py video.mp4 --engine openrouter
"""

import base64
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PROMPT = (
    "Give me a detailed second-by-second breakdown of this video. "
    "For every single second from 0:00 to the end, give one timestamp on "
    "its own line in this format:  MM:SS — description of what's happening."
)


def is_youtube_url(value: str) -> bool:
    return value.startswith(("http://", "https://")) and (
        "youtube.com" in value or "youtu.be" in value
    )


def _key(name: str) -> str:
    return os.environ.get(name, "")


def _missing(name: str) -> bool:
    v = _key(name)
    return not v or v == "YOUR_KEY_HERE"


# ── Frame extraction (ffmpeg) ─────────────────────────────────────────────────

def extract_frames(video_path: str, tmpdir: str, max_frames: int = 20) -> list:
    out_pattern = os.path.join(tmpdir, "frame_%04d.jpg")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True,
    )
    duration = float(result.stdout.strip() or "60")
    fps = max(0.1, max_frames / duration)
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-vf", f"fps={fps:.3f}",
         "-q:v", "3", "-vframes", str(max_frames), out_pattern],
        capture_output=True, check=True,
    )
    return sorted(Path(tmpdir).glob("frame_*.jpg"))


def _frames_to_messages(frames: list, prompt: str) -> list:
    content = [{"type": "text", "text": prompt}]
    for frame in frames:
        data = base64.b64encode(frame.read_bytes()).decode()
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{data}", "detail": "low"},
        })
    return [{"role": "user", "content": content}]


def _openai_compat(base_url: str, api_key: str, model: str,
                   video_path: str, prompt: str, max_frames: int = 20,
                   extra_headers: dict = None) -> str:
    from openai import OpenAI
    kwargs = {"api_key": api_key, "base_url": base_url}
    if extra_headers:
        kwargs["default_headers"] = extra_headers
    client = OpenAI(**kwargs)

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"  Extracting frames...", file=sys.stderr)
        frames = extract_frames(video_path, tmpdir, max_frames=max_frames)
        if not frames:
            raise RuntimeError("ffmpeg produced no frames")
        print(f"  Sending {len(frames)} frames...", file=sys.stderr)
        response = client.chat.completions.create(
            model=model,
            messages=_frames_to_messages(frames, prompt),
            max_tokens=4096,
        )
        return response.choices[0].message.content


# ── Engine 1: Gemini ──────────────────────────────────────────────────────────

def analyze_with_gemini(video_path: str, prompt: str) -> str:
    if _missing("GEMINI_API_KEY"):
        raise EnvironmentError("GEMINI_API_KEY not set")
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=_key("GEMINI_API_KEY"))
    if is_youtube_url(video_path):
        contents = [
            types.Part(file_data=types.FileData(file_uri=video_path, mime_type="video/*")),
            types.Part(text=prompt),
        ]
    else:
        path = Path(video_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {video_path}")
        print("  Uploading to Gemini...", file=sys.stderr)
        uploaded = client.files.upload(file=str(path))
        print("  Processing...", file=sys.stderr)
        while uploaded.state.name == "PROCESSING":
            time.sleep(2)
            uploaded = client.files.get(name=uploaded.name)
        if uploaded.state.name == "FAILED":
            raise RuntimeError(f"Gemini upload failed: {uploaded.name}")
        contents = [
            types.Part(file_data=types.FileData(file_uri=uploaded.uri, mime_type=uploaded.mime_type)),
            types.Part(text=prompt),
        ]
    response = client.models.generate_content(model="gemini-2.5-flash", contents=contents)
    return response.text


# ── Engine 2: OpenRouter (free vision models) ─────────────────────────────────

def analyze_with_openrouter(video_path: str, prompt: str) -> str:
    if _missing("OPENROUTER_API_KEY"):
        raise EnvironmentError("OPENROUTER_API_KEY not set")
    if is_youtube_url(video_path):
        raise ValueError("OpenRouter engine requires a local file")
    return _openai_compat(
        base_url="https://openrouter.ai/api/v1",
        api_key=_key("OPENROUTER_API_KEY"),
        model="meta-llama/llama-3.2-11b-vision-instruct:free",
        video_path=video_path,
        prompt=prompt,
        extra_headers={"HTTP-Referer": "https://github.com/mccosman/BookLibConnect"},
    )


# ── Engine 3: GitHub Models (free GPT-4o mini vision) ────────────────────────

def analyze_with_github(video_path: str, prompt: str) -> str:
    if _missing("GITHUB_TOKEN"):
        raise EnvironmentError("GITHUB_TOKEN not set")
    if is_youtube_url(video_path):
        raise ValueError("GitHub Models engine requires a local file")
    return _openai_compat(
        base_url="https://models.inference.ai.azure.com",
        api_key=_key("GITHUB_TOKEN"),
        model="gpt-4o-mini",
        video_path=video_path,
        prompt=prompt,
    )


# ── Engine 4: Nvidia NIM (free vision endpoint) ───────────────────────────────

def analyze_with_nvidia(video_path: str, prompt: str) -> str:
    if _missing("NVIDIA_API_KEY"):
        raise EnvironmentError("NVIDIA_API_KEY not set")
    if is_youtube_url(video_path):
        raise ValueError("Nvidia NIM engine requires a local file")
    return _openai_compat(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=_key("NVIDIA_API_KEY"),
        model="microsoft/phi-3.5-vision-instruct",
        video_path=video_path,
        prompt=prompt,
        max_frames=10,
    )


# ── Engine 5: Mistral Pixtral ─────────────────────────────────────────────────

def analyze_with_mistral(video_path: str, prompt: str) -> str:
    if _missing("MISTRAL_API_KEY"):
        raise EnvironmentError("MISTRAL_API_KEY not set")
    if is_youtube_url(video_path):
        raise ValueError("Mistral engine requires a local file")
    return _openai_compat(
        base_url="https://api.mistral.ai/v1",
        api_key=_key("MISTRAL_API_KEY"),
        model="pixtral-12b-2409",
        video_path=video_path,
        prompt=prompt,
    )


# ── Engine 6: Cloudflare Workers AI ──────────────────────────────────────────

def analyze_with_cloudflare(video_path: str, prompt: str) -> str:
    if _missing("CLOUDFLARE_API_TOKEN") or _missing("CLOUDFLARE_ACCOUNT_ID"):
        raise EnvironmentError("CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set")
    if is_youtube_url(video_path):
        raise ValueError("Cloudflare engine requires a local file")
    account_id = _key("CLOUDFLARE_ACCOUNT_ID")
    return _openai_compat(
        base_url=f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
        api_key=_key("CLOUDFLARE_API_TOKEN"),
        model="@cf/llava-1.5-7b-hf",
        video_path=video_path,
        prompt=prompt,
        max_frames=10,
    )


# ── Engine 7: Cerebras (text only — transcript/description fallback) ──────────

def analyze_with_cerebras(video_path: str, prompt: str) -> str:
    if _missing("CEREBRAS_API_KEY"):
        raise EnvironmentError("CEREBRAS_API_KEY not set")
    from openai import OpenAI
    client = OpenAI(api_key=_key("CEREBRAS_API_KEY"), base_url="https://api.cerebras.ai/v1")
    note = (
        f"The user wants to analyze a video at: {video_path}\n"
        f"Since this is a text-only model, describe what you would expect to find "
        f"and answer the prompt as best you can.\nPrompt: {prompt}"
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": note}],
        max_tokens=2048,
    )
    return response.choices[0].message.content


# ── Engine 8: OpenAI GPT-4o (frame-based) ────────────────────────────────────

def analyze_with_openai(video_path: str, prompt: str) -> str:
    if _missing("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY not set")
    if is_youtube_url(video_path):
        raise ValueError("OpenAI engine requires a local file")
    return _openai_compat(
        base_url="https://api.openai.com/v1",
        api_key=_key("OPENAI_API_KEY"),
        model="gpt-4o",
        video_path=video_path,
        prompt=prompt,
    )


# ── Engine registry ───────────────────────────────────────────────────────────

ENGINES = {
    "gemini":      ("Gemini 2.5 Flash",        analyze_with_gemini),
    "openrouter":  ("OpenRouter (Llama Vision)", analyze_with_openrouter),
    "github":      ("GitHub Models (GPT-4o mini)", analyze_with_github),
    "nvidia":      ("Nvidia NIM (Phi-3.5 Vision)", analyze_with_nvidia),
    "mistral":     ("Mistral Pixtral",          analyze_with_mistral),
    "cloudflare":  ("Cloudflare Workers AI",    analyze_with_cloudflare),
    "cerebras":    ("Cerebras (text fallback)",  analyze_with_cerebras),
    "openai":      ("OpenAI GPT-4o",            analyze_with_openai),
}

ENGINE_ORDER = ["gemini", "openrouter", "github", "nvidia", "mistral",
                "cloudflare", "cerebras", "openai"]


def analyze_video(video_path: str, prompt: str, engine: str = None) -> str:
    order = [engine] if engine else ENGINE_ORDER
    errors = []

    for key in order:
        if key not in ENGINES:
            raise ValueError(f"Unknown engine '{key}'. Choose from: {', '.join(ENGINES)}")
        name, fn = ENGINES[key]
        try:
            print(f"Trying {name}...", file=sys.stderr)
            result = fn(video_path, prompt)
            print(f"Done ({name}).", file=sys.stderr)
            return result
        except EnvironmentError:
            pass  # key not configured — skip silently
        except Exception as e:
            print(f"  {name} failed: {e}", file=sys.stderr)
            errors.append(f"{name}: {e}")

    raise RuntimeError(
        "All configured engines failed:\n" + "\n".join(errors) if errors
        else "No engines configured — add at least one API key to .env"
    )


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    engine = None
    if "--engine" in args:
        i = args.index("--engine")
        engine = args[i + 1]
        args = args[:i] + args[i + 2:]

    if not args:
        print("Error: video path or URL required.", file=sys.stderr)
        sys.exit(1)

    video = args[0]
    prompt = args[1] if len(args) > 1 else DEFAULT_PROMPT

    try:
        print(analyze_video(video, prompt, engine=engine))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
