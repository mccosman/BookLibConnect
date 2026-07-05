#!/bin/bash
# Coseman Web Design Plugin — Session Start Hook
# Runs when a new Claude Code session begins

set -e

# Load .env if present in plugin or home dir
if [ -f "$HOME/.config/gemini/.env" ]; then
    export $(grep -v '^#' "$HOME/.config/gemini/.env" | xargs) 2>/dev/null
fi

# Verify Gemini key is available (used for Google AI Studio code gen)
if [ -n "$GEMINI_API_KEY" ]; then
    echo "[coseman-web-design] Gemini API key loaded (${GEMINI_API_KEY:0:8}...)"
else
    echo "[coseman-web-design] WARNING: GEMINI_API_KEY not set."
    echo "  → Get a free key at aistudio.google.com"
    echo "  → Keys now start with AQ. (not AIza)"
    echo "  → Set it: export GEMINI_API_KEY=AQ.your_key_here"
fi

# Ensure Python helper is executable
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [ -f "$SCRIPT_DIR/scripts/generate_site.py" ]; then
    chmod +x "$SCRIPT_DIR/scripts/generate_site.py"
fi

echo "[coseman-web-design] Premium Web Design skill ready."
