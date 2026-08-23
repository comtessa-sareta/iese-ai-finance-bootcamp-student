"""Pre-course environment check. Run from the repo root:

    python setup/check_setup.py

Verifies Python, packages, .env configuration, SEC EDGAR reachability, git and
Claude Code. Prints a scoreboard; exits non-zero if anything required is missing.
"""
from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PASS, FAIL, WARN = "[ OK ]", "[FAIL]", "[warn]"
failures = 0


def report(ok: bool, label: str, detail: str = "", required: bool = True) -> None:
    global failures
    tag = PASS if ok else (FAIL if required else WARN)
    if not ok and required:
        failures += 1
    print(f"  {tag} {label}" + (f" — {detail}" if detail else ""))


def main() -> int:
    print("\nIESE AI-Augmented Productivity for Finance — environment check\n")

    # 1. Python
    v = sys.version_info
    report(v >= (3, 10), f"Python {v.major}.{v.minor}.{v.micro}", "need 3.10+")

    # 2. Packages
    for pkg in ["pandas", "requests", "matplotlib", "seaborn", "plotly", "anthropic", "pydantic", "pydantic_ai", "dotenv", "pytest", "tabulate"]:
        try:
            importlib.import_module(pkg)
            report(True, f"package: {pkg}")
        except ImportError:
            report(False, f"package: {pkg}", "pip install -r requirements.txt")

    # 3. .env
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            pass
    report(env_file.exists(), ".env file exists", "copy .env.example to .env" if not env_file.exists() else "")
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    report(bool(key), "ANTHROPIC_API_KEY set",
           "needed from Session 1 — add it to .env" if not key else "value hidden", required=False)
    ua = os.environ.get("SEC_EDGAR_USER_AGENT", "")
    report(bool(ua) and "example.com" not in ua, "SEC_EDGAR_USER_AGENT set to your name/email",
           detail="" if ua else "set it in .env", required=False)

    # 4. Network: SEC EDGAR — the User-Agent MUST contain an email-format
    # contact or SEC's edge returns 403 (looks like a network error, isn't).
    try:
        import requests
        good_ua = ua if (ua and "@" in ua) else \
            "IESE AI-Finance Bootcamp setup-check contact@example.com"
        r = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers={"User-Agent": good_ua},
            timeout=15,
        )
        hint = "" if r.status_code == 200 else (
            f"HTTP {r.status_code}"
            + (" — 403 means SEC rejected the request (User-Agent needs a "
               "'Name email' contact; set SEC_EDGAR_USER_AGENT in .env), or a "
               "corporate proxy is interfering" if r.status_code == 403 else "")
        )
        report(r.status_code == 200, "SEC EDGAR reachable", hint)
    except Exception as exc:  # noqa: BLE001 — any network failure reads the same to a student
        report(False, "SEC EDGAR reachable", str(exc))

    # 5. Tooling
    report(shutil.which("git") is not None, "git installed")
    claude = shutil.which("claude")
    report(claude is not None, "Claude Code CLI on PATH",
           "fine if you use the VS Code extension (it bundles its own copy); "
           "otherwise see setup/claude-code-setup.md — note Claude Code needs a "
           "PAID plan, the free tier doesn't include it" if not claude else "",
           required=False)
    if shutil.which("git"):
        try:
            name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
            report(bool(name), "git identity configured",
                   'git config --global user.name "You"' if not name else name, required=False)
        except OSError:
            pass

    print()
    if failures:
        print(f"{failures} required check(s) failed — fix them before class.\n")
    else:
        print("All required checks passed. You are ready.\n")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
