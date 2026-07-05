"""
Coseman Video Watch — Protect Secrets Hook
Blocks Claude from reading or leaking sensitive files and credentials.
Runs as a preToolUse hook before every file read, write, edit, or bash command.
"""

import json
import re
import sys

SECRET_FILE_PATTERNS = [
    r"(^|[/\\])\.env(\.|$)",
    r"\.pem$",
    r"\.key$",
    r"\.p12$",
    r"\.pfx$",
    r"(^|[/\\])credentials(\.|$)",
    r"id_rsa",
    r"id_ed25519",
    r"\.netrc$",
    r"\.npmrc$",
    r"\.pypirc$",
    r"(^|[/\\])auth\.json$",
]

# Match actual key values (long enough to not be pattern strings)
HARDCODED_KEY_PATTERNS = [
    r"sk-[a-zA-Z0-9]{40,}",           # OpenAI keys (real keys are 51+ chars)
    r"sk-or-v1-[a-zA-Z0-9]{60,}",     # OpenRouter
    r"gsk_[a-zA-Z0-9]{50,}",          # Groq
    r"nvapi-[a-zA-Z0-9_-]{50,}",      # Nvidia
    r"ghp_[a-zA-Z0-9]{36}",           # GitHub PAT
    r"cfat_[a-zA-Z0-9]{40,}",         # Cloudflare
    r"csk-[a-zA-Z0-9]{50,}",          # Cerebras
    r"AIza[a-zA-Z0-9_-]{35}",         # Google API key
]

SAFE_PREFIXES = (
    "git ", "python3 ", "python ", "pip3 ", "pip ",
    "npm ", "node ", "ffmpeg ", "ffprobe ", "yt-dlp ",
    "ls ", "mkdir ", "chmod ", "which ", "type ",
)

TRULY_DANGEROUS = [
    (r"\brm\s+-rf\s+/[^/]",       "rm -rf on root/system path"),
    (r"\bdd\s+if=.*of=/dev/",     "dd writing to disk device"),
    (r"\bmkfs\b",                  "filesystem format command"),
    (r":\(\)\s*\{.*\|.*&.*\}",   "fork bomb pattern"),
]


def is_secret_path(path: str) -> bool:
    return any(re.search(p, path, re.IGNORECASE) for p in SECRET_FILE_PATTERNS)


def contains_hardcoded_key(text: str) -> bool:
    return any(re.search(p, text) for p in HARDCODED_KEY_PATTERNS)


def is_truly_dangerous(cmd: str) -> tuple:
    for pattern, reason in TRULY_DANGEROUS:
        if re.search(pattern, cmd):
            return True, reason
    return False, ""


def block(reason: str):
    print(reason, file=sys.stderr)
    sys.exit(2)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool   = data.get("tool_name", "")
    inputs = data.get("tool_input", {})

    # ── File reads / writes / edits ───────────────────────────────────────────
    if tool in ("Read", "Edit", "Write"):
        path = inputs.get("file_path", "")
        if is_secret_path(path):
            block(
                f"🔒 BLOCKED: Access to '{path}' denied.\n"
                f"This file may contain API keys or credentials. "
                f"Store secrets in .env (gitignored) and load with os.environ."
            )
        content = inputs.get("content", "") + inputs.get("new_string", "")
        if contains_hardcoded_key(content):
            block(
                "🔒 BLOCKED: Content contains what looks like a hardcoded API key.\n"
                "Store secrets in .env and reference via os.environ — never hardcode them."
            )

    # ── Bash commands ─────────────────────────────────────────────────────────
    if tool == "Bash":
        cmd = inputs.get("command", "")
        first = cmd.strip().split("\n")[0].strip()

        if any(first.startswith(p) for p in SAFE_PREFIXES):
            sys.exit(0)

        dangerous, reason = is_truly_dangerous(cmd)
        if dangerous:
            block(
                f"🔒 BLOCKED: Dangerous command detected ({reason}).\n"
                f"Command: {cmd[:120]}\n"
                f"If you intended this, run it manually in your terminal."
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
