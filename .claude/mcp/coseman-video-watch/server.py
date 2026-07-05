"""
Coseman Video Watch — MCP Server
Provides Claude with tools to analyze videos directly mid-conversation.
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Project root is 4 levels up from this file:
# server.py → coseman-video-watch → mcp → .claude → project root
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent
ANALYZE_SCRIPT = PROJECT_DIR / "analyze_video.py"
HEALTH_SCRIPT  = PROJECT_DIR / "health_check.py"
ENV_FILE       = PROJECT_DIR / ".env"

app = Server("coseman-video-watch")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="coseman_video_analyze",
            description=(
                "Analyze a video with the Coseman Video Watch engine chain. "
                "Pass a YouTube URL or local file path (.mp4 .mov .avi .mkv .webm). "
                "Tries 8 AI engines in order — Gemini, OpenRouter, GitHub Models, "
                "Nvidia NIM, Mistral, Cloudflare, Cerebras, OpenAI — until one succeeds. "
                "Returns a second-by-second breakdown by default, or answers a custom prompt. "
                "YouTube URLs work best with Gemini. Use the engine param to force one."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "video": {
                        "type": "string",
                        "description": "YouTube URL or absolute path to a local video file",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Optional question or instruction. Default: second-by-second breakdown.",
                    },
                    "engine": {
                        "type": "string",
                        "description": "Force a specific engine: gemini, openrouter, github, nvidia, mistral, cloudflare, cerebras, openai",
                        "enum": ["gemini","openrouter","github","nvidia","mistral","cloudflare","cerebras","openai"],
                    },
                },
                "required": ["video"],
            },
        ),
        types.Tool(
            name="coseman_video_health",
            description=(
                "Run the Coseman Video Watch health check. "
                "Verifies all 9 API keys are set, pings live engines, "
                "and shows recommended model versions for each provider. "
                "Call this when an engine fails or to get a full status report."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="coseman_video_engines",
            description=(
                "List all Coseman Video Watch engines with key status and models. "
                "Quick view of which engines are ready (key set) vs missing. "
                "Faster than running the full health check."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="coseman_video_set_key",
            description=(
                "Add or update an API key in the project .env file. "
                "Use this when the user pastes a new key mid-conversation. "
                "Key names: GEMINI_API_KEY, OPENROUTER_API_KEY, GITHUB_TOKEN, "
                "NVIDIA_API_KEY, MISTRAL_API_KEY, CLOUDFLARE_API_TOKEN, "
                "CLOUDFLARE_ACCOUNT_ID, CEREBRAS_API_KEY, OPENAI_API_KEY, GROQ_API_KEY"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "key_name": {
                        "type": "string",
                        "description": "Environment variable name (e.g. GEMINI_API_KEY)",
                    },
                    "key_value": {
                        "type": "string",
                        "description": "The API key value to set",
                    },
                },
                "required": ["key_name", "key_value"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    # ── coseman_video_analyze ────────────────────────────────────────────────
    if name == "coseman_video_analyze":
        video  = arguments["video"]
        prompt = arguments.get("prompt", "")
        engine = arguments.get("engine", "")

        cmd = [sys.executable, str(ANALYZE_SCRIPT), video]
        if prompt:
            cmd.append(prompt)
        if engine:
            cmd += ["--engine", engine]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300,
                env={**os.environ, "DOTENV_PATH": str(ENV_FILE)},
            )
            output = result.stdout or result.stderr
            if result.returncode != 0:
                return [types.TextContent(type="text", text=f"Engine error:\n{output}")]
            return [types.TextContent(type="text", text=output)]
        except subprocess.TimeoutExpired:
            return [types.TextContent(type="text", text="Timed out after 5 minutes.")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {e}")]

    # ── coseman_video_health ─────────────────────────────────────────────────
    elif name == "coseman_video_health":
        result = subprocess.run(
            [sys.executable, str(HEALTH_SCRIPT)],
            capture_output=True, text=True, timeout=30,
        )
        return [types.TextContent(type="text", text=result.stdout + result.stderr)]

    # ── coseman_video_engines ────────────────────────────────────────────────
    elif name == "coseman_video_engines":
        from dotenv import load_dotenv
        load_dotenv(ENV_FILE)

        PLACEHOLDER = "YOUR_KEY_HERE"
        def is_set(k):
            v = os.environ.get(k, "")
            return bool(v and v != PLACEHOLDER)

        engines = [
            ("gemini",     "GEMINI_API_KEY",      "gemini-2.5-flash"),
            ("openrouter", "OPENROUTER_API_KEY",  "llama-3.2-11b-vision:free"),
            ("github",     "GITHUB_TOKEN",        "gpt-4o-mini"),
            ("nvidia",     "NVIDIA_API_KEY",      "phi-3.5-vision-instruct"),
            ("mistral",    "MISTRAL_API_KEY",     "pixtral-12b-2409"),
            ("cloudflare", "CLOUDFLARE_API_TOKEN","@cf/llava-1.5-7b-hf"),
            ("cerebras",   "CEREBRAS_API_KEY",    "llama-3.3-70b"),
            ("openai",     "OPENAI_API_KEY",      "gpt-4o"),
            ("groq",       "GROQ_API_KEY",        "whisper-large-v3 (audio)"),
        ]
        lines = ["Coseman Video Watch — Engines\n", "-" * 44]
        for eng, key, model in engines:
            icon = "✅" if is_set(key) else "❌"
            lines.append(f"{icon}  {eng:<12} {model}")
        return [types.TextContent(type="text", text="\n".join(lines))]

    # ── coseman_video_set_key ────────────────────────────────────────────────
    elif name == "coseman_video_set_key":
        key_name  = arguments["key_name"].strip()
        key_value = arguments["key_value"].strip()

        if not ENV_FILE.exists():
            return [types.TextContent(type="text", text=f".env not found at {ENV_FILE}")]

        content = ENV_FILE.read_text()
        import re
        pattern = re.compile(rf"^{re.escape(key_name)}=.*$", re.MULTILINE)
        new_line = f"{key_name}={key_value}"

        if pattern.search(content):
            content = pattern.sub(new_line, content)
        else:
            content = content.rstrip("\n") + f"\n{new_line}\n"

        ENV_FILE.write_text(content)
        os.environ[key_name] = key_value
        return [types.TextContent(type="text", text=f"✅ {key_name} updated in .env")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
