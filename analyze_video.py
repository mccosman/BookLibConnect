"""
Video analysis script — tries engines in order until one succeeds.
  1. Gemini 2.5 Flash  (native video + YouTube URLs, needs GEMINI_API_KEY)
  2. OpenAI GPT-4o     (frame-based, needs OPENAI_API_KEY + ffmpeg)

Usage:
  python3 analyze_video.py <video_path_or_youtube_url> [prompt]

Examples:
  python3 analyze_video.py path/to/video.mp4
  python3 analyze_video.py https://www.youtube.com/watch?v=XXXX
  python3 analyze_video.py video.mp4 "Summarize the key moments as bullet points."
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


# ── Engine 1: Gemini ─────────────────────────────────────────────────────────

def analyze_with_gemini(video_path: str, prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key or api_key == "YOUR_KEY_HERE":
        raise EnvironmentError("GEMINI_API_KEY not set")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    if is_youtube_url(video_path):
        contents = [
            types.Part(file_data=types.FileData(file_uri=video_path, mime_type="video/*")),
            types.Part(text=prompt),
        ]
    else:
        path = Path(video_path)
        if not path.is_file():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        print("Uploading to Gemini...", file=sys.stderr)
        uploaded = client.files.upload(file=str(path))
        print("Waiting for Gemini to process...", file=sys.stderr)
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


# ── Engine 2: OpenAI GPT-4o (frame-based) ────────────────────────────────────

def extract_frames(video_path: str, tmpdir: str, max_frames: int = 20) -> list[str]:
    out_pattern = os.path.join(tmpdir, "frame_%04d.jpg")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip() or "60")
    fps = max(0.1, max_frames / duration)

    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-vf", f"fps={fps:.3f}",
         "-q:v", "3", "-vframes", str(max_frames), out_pattern],
        capture_output=True, check=True
    )
    return sorted(Path(tmpdir).glob("frame_*.jpg"))


def analyze_with_openai(video_path: str, prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key or api_key == "YOUR_KEY_HERE":
        raise EnvironmentError("OPENAI_API_KEY not set")
    if is_youtube_url(video_path):
        raise ValueError("OpenAI engine requires a local file, not a YouTube URL")

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Extracting frames for OpenAI...", file=sys.stderr)
        frames = extract_frames(video_path, tmpdir)
        if not frames:
            raise RuntimeError("ffmpeg produced no frames")

        messages_content = [{"type": "text", "text": prompt}]
        for frame in frames:
            data = base64.b64encode(frame.read_bytes()).decode()
            messages_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{data}", "detail": "low"},
            })

        print(f"Sending {len(frames)} frames to GPT-4o...", file=sys.stderr)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": messages_content}],
            max_tokens=4096,
        )
        return response.choices[0].message.content


# ── Main ──────────────────────────────────────────────────────────────────────

ENGINES = [
    ("Gemini 2.5 Flash", analyze_with_gemini),
    ("OpenAI GPT-4o",    analyze_with_openai),
]


def analyze_video(video_path: str, prompt: str) -> str:
    errors = []
    for name, engine in ENGINES:
        try:
            print(f"Trying {name}...", file=sys.stderr)
            result = engine(video_path, prompt)
            print(f"Done ({name}).", file=sys.stderr)
            return result
        except EnvironmentError:
            pass  # key not configured — skip silently
        except Exception as e:
            print(f"{name} failed: {e}", file=sys.stderr)
            errors.append(f"{name}: {e}")

    raise RuntimeError("All engines failed:\n" + "\n".join(errors))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    video = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROMPT

    try:
        print(analyze_video(video, prompt))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
