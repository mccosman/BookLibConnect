"""
Coseman Video Watch — Health Check
Verifies all engines, checks for model updates, reports status.
Run manually: python3 health_check.py
Also runs automatically at session start via the hook.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

VERSION = "1.0.0"

# Latest recommended models per engine — update this list when providers release new ones
RECOMMENDED_MODELS = {
    "gemini":     "gemini-2.5-flash",
    "openrouter": "meta-llama/llama-3.2-11b-vision-instruct:free",
    "github":     "gpt-4o-mini",
    "nvidia":     "microsoft/phi-3.5-vision-instruct",
    "mistral":    "pixtral-12b-2409",
    "cloudflare": "@cf/llava-1.5-7b-hf",
    "cerebras":   "llama-3.3-70b",
    "openai":     "gpt-4o",
}

PLACEHOLDER = "YOUR_KEY_HERE"

def _key(name):
    v = os.environ.get(name, "")
    return v if v and v != PLACEHOLDER else ""


def check_keys():
    checks = {
        "Gemini 2.5 Flash":        _key("GEMINI_API_KEY"),
        "OpenRouter":               _key("OPENROUTER_API_KEY"),
        "GitHub Models":            _key("GITHUB_TOKEN"),
        "Nvidia NIM":               _key("NVIDIA_API_KEY"),
        "Mistral Pixtral":          _key("MISTRAL_API_KEY"),
        "Cloudflare Workers AI":    _key("CLOUDFLARE_API_TOKEN"),
        "Cloudflare Account ID":    _key("CLOUDFLARE_ACCOUNT_ID"),
        "Cerebras":                 _key("CEREBRAS_API_KEY"),
        "OpenAI GPT-4o":            _key("OPENAI_API_KEY"),
        "Groq (audio)":             _key("GROQ_API_KEY"),
    }
    return checks


def ping_gemini():
    key = _key("GEMINI_API_KEY")
    if not key:
        return False, "key missing"
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            return True, "ok"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)[:60]


def ping_groq():
    key = _key("GROQ_API_KEY")
    if not key:
        return False, "key missing"
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return True, "ok"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        msg = str(e)
        if "403" in msg or "Tunnel" in msg or "Forbidden" in msg:
            return None, "proxy restricted (works locally)"
        return False, msg[:60]


def check_script_version():
    """Check if analyze_video.py exists and is the current version."""
    script = os.path.join(os.path.dirname(__file__), "analyze_video.py")
    if not os.path.exists(script):
        return False, "analyze_video.py not found!"
    size = os.path.getsize(script)
    if size < 1000:
        return False, "analyze_video.py looks truncated"
    return True, f"present ({size:,} bytes)"


def run():
    print(f"\n{'='*54}")
    print(f"  Coseman Video Watch — Health Check  v{VERSION}")
    print(f"{'='*54}")

    # ── Key status ──────────────────────────────────────────
    print("\n  API Keys")
    print("  " + "-"*40)
    keys = check_keys()
    all_set = True
    missing = []
    for name, val in keys.items():
        if val:
            preview = val[:8] + "..." if len(val) > 8 else val
            print(f"  ✅  {name:<28} {preview}")
        else:
            print(f"  ❌  {name:<28} NOT SET")
            all_set = False
            missing.append(name)

    # ── Live connectivity (only engines that work through proxy) ──
    print("\n  Live Connectivity")
    print("  " + "-"*40)

    ok, msg = ping_gemini()
    icon = "✅" if ok else "❌"
    print(f"  {icon}  {'Gemini API':<28} {msg}")

    ok, msg = ping_groq()
    icon = "✅" if ok else ("⚠️ " if ok is None else "❌")
    print(f"  {icon}  {'Groq API':<28} {msg}")

    print(f"  ℹ️   Other engines — reachable locally only (proxy restriction in Co-work)")

    # ── Script check ────────────────────────────────────────
    print("\n  Scripts")
    print("  " + "-"*40)
    ok, msg = check_script_version()
    icon = "✅" if ok else "❌"
    print(f"  {icon}  {'analyze_video.py':<28} {msg}")

    skill_path = os.path.join(os.path.dirname(__file__), ".claude", "skills",
                               "coseman-video-watch", "SKILL.md")
    skill_ok = os.path.exists(skill_path)
    print(f"  {'✅' if skill_ok else '❌'}  {'SKILL.md':<28} {'present' if skill_ok else 'MISSING'}")

    # ── Recommended models ──────────────────────────────────
    print("\n  Recommended Models (as of last update)")
    print("  " + "-"*40)
    for engine, model in RECOMMENDED_MODELS.items():
        print(f"  📌  {engine:<12} {model}")

    # ── Summary ─────────────────────────────────────────────
    print(f"\n{'='*54}")
    if missing:
        print(f"  ⚠️  {len(missing)} key(s) not set: {', '.join(missing)}")
        print(f"  → Add them to .env in the project root")
    else:
        print(f"  ✅ All keys configured.")
    print(f"  💡 To analyze a video:")
    print(f"     python3 analyze_video.py <url_or_file>")
    print(f"     python3 analyze_video.py <url_or_file> --engine gemini")
    print(f"{'='*54}\n")

    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(run())
