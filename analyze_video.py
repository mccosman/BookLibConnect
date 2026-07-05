import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


def is_youtube_url(value: str) -> bool:
    return value.startswith(("http://", "https://")) and (
        "youtube.com" in value or "youtu.be" in value
    )


def analyze_video(video_path: str, prompt: str) -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_KEY_HERE":
        raise ValueError(
            "GEMINI_API_KEY is missing or still set to placeholder.\n"
            "Edit .env and add your real key from https://aistudio.google.com/apikey"
        )

    client = genai.Client(api_key=api_key)

    if is_youtube_url(video_path):
        contents = [
            types.Part(
                file_data=types.FileData(
                    file_uri=video_path,
                    mime_type="video/*",
                )
            ),
            types.Part(text=prompt),
        ]
    else:
        path = Path(video_path)
        if not path.is_file():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        print(f"Uploading {path.name}...", file=sys.stderr)
        uploaded = client.files.upload(file=str(path))

        print("Waiting for Gemini to process the video...", file=sys.stderr)
        while uploaded.state.name == "PROCESSING":
            time.sleep(2)
            uploaded = client.files.get(name=uploaded.name)

        if uploaded.state.name == "FAILED":
            raise RuntimeError(f"Video upload failed: {uploaded.name}")

        contents = [
            types.Part(
                file_data=types.FileData(
                    file_uri=uploaded.uri,
                    mime_type=uploaded.mime_type,
                )
            ),
            types.Part(text=prompt),
        ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
    )
    return response.text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_video.py <video_path_or_youtube_url> [prompt]")
        print()
        print("Examples:")
        print("  python3 analyze_video.py path/to/video.mp4")
        print('  python3 analyze_video.py path/to/video.mp4 "Summarize the key moments as bullet points."')
        print('  python3 analyze_video.py https://www.youtube.com/watch?v=XXXX "Give a second-by-second breakdown."')
        sys.exit(1)

    video = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else (
        "Give me a detailed second-by-second breakdown of this video. "
        "For every single second from 0:00 to the end, give one timestamp on "
        "its own line in this format:  MM:SS — description of what's happening."
    )

    try:
        result = analyze_video(video, prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
