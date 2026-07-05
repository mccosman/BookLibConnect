#!/bin/bash
set -euo pipefail

# Only run in remote/web sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "==> Installing claude-video-vision dependencies..."

# ffmpeg — frame extraction
if ! command -v ffmpeg &>/dev/null; then
  apt-get install -y --fix-missing ffmpeg --no-install-recommends 2>&1 | tail -3 || true
fi

# yt-dlp — YouTube URL support
if ! command -v yt-dlp &>/dev/null; then
  pip3 install --quiet yt-dlp
fi

# openai-whisper — local audio transcription
if ! python3 -c "import whisper" &>/dev/null 2>&1; then
  pip3 install --quiet openai-whisper --no-deps
  pip3 install --quiet tiktoken tqdm numpy torch --index-url https://download.pytorch.org/whl/cpu
fi

# claude-video-vision MCP server
if ! command -v claude-video-vision &>/dev/null; then
  npm install -g --silent claude-video-vision@latest
fi

# Plugin config (local Whisper backend, images mode, index enabled)
mkdir -p ~/.claude-video-vision
if [ ! -f ~/.claude-video-vision/config.json ]; then
  cat > ~/.claude-video-vision/config.json << 'JSON'
{
  "backend": "local",
  "whisper_engine": "python",
  "whisper_model": "small",
  "whisper_at": false,
  "frame_mode": "images",
  "frame_format": "jpeg",
  "frame_resolution": 512,
  "default_fps": "auto",
  "max_frames": 100,
  "frame_describer_model": "sonnet",
  "enable_index": true,
  "session_max_age_days": 7,
  "downloads_max_age_days": 7,
  "audio_max_output_tokens": 65536,
  "audio_chunk_trigger_seconds": 1200,
  "audio_chunk_size_seconds": 600,
  "audio_chunk_overlap_seconds": 0
}
JSON
fi

echo "==> claude-video-vision setup complete"
