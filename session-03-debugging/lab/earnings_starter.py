"""Session 3 lab — Earnings Analysis Engine (STARTER).

Transcript in -> structured, evidence-verified analysis -> investment memo out.

Try it right now (works without an API key):

    python session-03-debugging/lab/earnings_starter.py --dry-run

The plumbing (schema, API call, file handling) is done. YOUR work is the part
that makes it trustworthy:

  TODO 1 — grounding rules in the system prompt (stop hallucinations at the source)
  TODO 2 — verify_evidence(): machine-check every quote against the transcript
  TODO 3 — finish the memo renderer (risks table + red flags)

Build with Claude Code function by function; run --dry-run after each step.
The dry-run analysis contains ONE fabricated quote on purpose — when your
TODO 2 works, your memo will catch it.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / ".env")
except ImportError:
    pass

from toolkit import llm  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_TRANSCRIPT = DATA_DIR / "transcript_meridian_q2_fy2026.txt"
CANNED = DATA_DIR / "example_analysis.json"
OUT_DIR = REPO_ROOT / "outputs"

# ---------------------------------------------------------------- TODO 1
# Write the ground rules that make the model trustworthy. At minimum cover:
#   - use ONLY the transcript, no outside knowledge
#   - every evidence_quote VERBATIM (say that it will be machine-checked!)
#   - if unsupported by the transcript, don't claim it
#   - separate management framing from fact
SYSTEM = """You are a buy-side equity analyst preparing an internal note.
TODO: your ground rules here.
"""

EARNINGS_SCHEMA = {
    "type": "object",
    "required": [
        "overall_sentiment", "sentiment_rationale", "key_themes",
        "management_priorities", "guidance", "risks", "red_flags",
        "qa_assessment", "summary",
    ],
    "properties": {
        "overall_sentiment": {
            "type": "string",
            "enum": ["positive", "cautiously_positive", "neutral", "cautious", "negative"],
        },
        "sentiment_rationale": {"type": "string"},
        "key_themes": {
            "type": "array", "minItems": 3,
            "items": {
                "type": "object", "required": ["theme", "evidence_quote"],
                "properties": {"theme": {"type": "string"}, "evidence_quote": {"type": "string"}},
            },
        },
        "management_priorities": {"type": "array", "items": {"type": "string"}},
        "guidance": {
            "type": "object", "required": ["next_quarter", "notable_exclusions"],
            "properties": {
                "next_quarter": {"type": "string"},
                "notable_exclusions": {"type": "string"},
            },
        },
        "risks": {
            "type": "array", "minItems": 3,
            "items": {
                "type": "object", "required": ["risk", "severity", "evidence_quote"],
                "properties": {
                    "risk": {"type": "string"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                    "evidence_quote": {"type": "string"},
                },
            },
        },
        "red_flags": {
            "type": "array",
            "items": {
                "type": "object", "required": ["flag", "why_it_matters", "evidence_quote"],
                "properties": {
                    "flag": {"type": "string"},
                    "why_it_matters": {"type": "string"},
                    "evidence_quote": {"type": "string"},
                },
            },
        },
        "qa_assessment": {
            "type": "array",
            "items": {
                "type": "object", "required": ["topic", "answer_quality", "note"],
                "properties": {
                    "topic": {"type": "string"},
                    "answer_quality": {"type": "string", "enum": ["direct", "partial", "evasive"]},
                    "note": {"type": "string"},
                },
            },
        },
        "summary": {"type": "string"},
    },
}


def load_transcript(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def analyze(transcript: str, dry_run: bool = False) -> dict:
    """Call Claude with the transcript, forced into EARNINGS_SCHEMA. (Done for you.)"""
    if dry_run:
        analysis = json.loads(CANNED.read_text())
        analysis.pop("_note", None)
        return analysis
    prompt = (
        "Analyze this earnings-call transcript and produce the structured "
        f"analysis.\n\n<transcript>\n{transcript}\n</transcript>"
    )
    return llm.ask_structured(
        prompt, name="record_earnings_analysis", schema=EARNINGS_SCHEMA, system=SYSTEM
    )


def verify_evidence(analysis: dict, transcript: str) -> dict:
    """TODO 2 — the trust layer.

    For every item in key_themes, risks and red_flags:
      - normalize both quote and transcript (collapse whitespace, lowercase,
        straighten curly quotes) so formatting can't cause false negatives
      - set item["verified"] = True/False (is the quote a substring of the source?)
    Store totals in analysis["_verification"] = {"quotes_checked": X, "quotes_failed": Y}.

    Until you implement it, this stub verifies nothing — look at the memo:
    EVERY quote shows ⚠️ UNVERIFIED. No verification, no trust. Your job is to
    earn the ✅ — and to catch the one quote that doesn't deserve it.
    """
    print("NOTE: verify_evidence is not implemented yet (TODO 2) — "
          "every quote in the memo will show UNVERIFIED")
    return analysis


def render_memo(analysis: dict, source_name: str) -> str:
    """TODO 3 — finish the memo. Sections still missing: Risks (markdown table,
    sorted high->low severity), Red flags, Q&A quality, Summary. Mark every
    quote ✅ or ⚠️ UNVERIFIED using item["verified"]."""
    lines = [
        "# Earnings note — Meridian Semiconductor (MSH), Q2 FY2026",
        "",
        f"*AI-generated draft from `{source_name}` — verify before any distribution.*",
        "",
        f"## Verdict: {analysis['overall_sentiment'].replace('_', ' ')}",
        "",
        analysis["sentiment_rationale"],
        "",
        "## Key themes",
        "",
    ]
    for t in analysis["key_themes"]:
        mark = "✅" if t.get("verified") else "⚠️ UNVERIFIED"
        lines += [f"- **{t['theme']}**", f"  > \"{t['evidence_quote']}\"  {mark}"]
    lines += ["", "## Guidance", "",
              f"- **Next quarter:** {analysis['guidance']['next_quarter']}",
              f"- **Exclusions / fine print:** {analysis['guidance']['notable_exclusions']}", ""]
    # TODO 3: risks table, red flags, Q&A quality, summary...
    return "\n".join(lines)


# Stretch goals:
#  4. Numeric cross-check: regex the transcript for figures ("58.3 percent",
#     "2.41 billion") and confirm any number in the summary appears in the source.
#  5. Point the engine at a real earnings release: fetch a recent 8-K with
#     toolkit.edgar (see session-04), save the text, run the engine on it.
#  6. Compare two quarters: run twice, ask Claude to diff management tone.


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("transcript", nargs="?", default=str(DEFAULT_TRANSCRIPT))
    ap.add_argument("--dry-run", action="store_true", help="use canned analysis; no API call")
    args = ap.parse_args()

    transcript_path = Path(args.transcript)
    transcript = load_transcript(transcript_path)
    print(f"Analyzing {transcript_path.name} ({len(transcript.split())} words)"
          + (" [dry run]" if args.dry_run else " with Claude ..."))

    analysis = verify_evidence(analyze(transcript, args.dry_run), transcript)

    OUT_DIR.mkdir(exist_ok=True)
    memo_path = OUT_DIR / "meridian_earnings_memo.md"
    memo_path.write_text(render_memo(analysis, transcript_path.name), encoding="utf-8")
    print(f"Memo written to {memo_path}")
    if not args.dry_run:
        print(f"Token usage: {llm.usage_summary()}")


if __name__ == "__main__":
    main()
