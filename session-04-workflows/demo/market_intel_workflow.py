"""Session 4 demo — AI Market Intelligence Workflow.

A DETERMINISTIC workflow (fixed steps, code in control) that combines live
SEC/EDGAR data with LLM reasoning and validates the result before a human
signs off:

    1. RETRIEVE   filings + XBRL financials from SEC EDGAR
    2. STRUCTURE  compute metrics in code (code does math, not the model)
    3. REASON     Claude writes the memo — grounded ONLY in step-2 data
    4. VALIDATE   schema is API-enforced; every number cross-checked vs inputs
    5. REVIEW     human approves before anything is saved (the loop's exit)

Run from the repo root:

    python session-04-workflows/demo/market_intel_workflow.py AAPL --peers MSFT GOOGL
    python session-04-workflows/demo/market_intel_workflow.py --dry-run   # no API key
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

from toolkit import edgar, llm, verify  # noqa: E402

OUT_DIR = REPO_ROOT / "outputs"
CANNED = Path(__file__).resolve().parent.parent / "data" / "example_intel_memo.json"

MEMO_SCHEMA = {
    "type": "object",
    "required": ["executive_summary", "kpi_read", "competitive_position",
                 "risks", "questions_for_management", "data_gaps"],
    "properties": {
        "executive_summary": {"type": "string"},
        "kpi_read": {
            "type": "array", "minItems": 3,
            "items": {
                "type": "object", "required": ["metric", "reading"],
                "properties": {"metric": {"type": "string"}, "reading": {"type": "string"}},
            },
        },
        "competitive_position": {"type": "string"},
        "risks": {"type": "array", "minItems": 2, "items": {"type": "string"}},
        "questions_for_management": {"type": "array", "minItems": 2, "items": {"type": "string"}},
        "data_gaps": {
            "type": "array", "items": {"type": "string"},
        },
    },
}

SYSTEM = """You are a market-intelligence analyst. Write for a partner who will
challenge every line. Ground rules:
- Use ONLY the data block provided. If something isn't in it, list it under
  data_gaps instead of guessing.
- Reuse figures exactly as given (you may round to one decimal). NEVER
  introduce a number that is not derivable from the data block.
- Attribute: say which company each claim is about.
- Plain, direct language. No hype."""


# ------------------------------------------------------------ 1. RETRIEVE

def retrieve(ticker: str, peers: list[str]) -> dict:
    print(f"[1/5] RETRIEVE — SEC EDGAR: {ticker} + peers {', '.join(peers)}")
    bundle = {"target": edgar.annual_financials(ticker, n=3), "peers": [], "filings": []}
    for p in peers:
        bundle["peers"].append(edgar.annual_financials(p, n=3))
    for f in edgar.recent_filings(ticker, forms=["10-K", "10-Q", "8-K"], limit=6):
        bundle["filings"].append({k: f[k] for k in ("form", "filed", "report_date")})
    return bundle


# ------------------------------------------------------------ 2. STRUCTURE

def _metrics(fin: dict) -> dict:
    rev = fin["revenue"]
    op = {v["fy_end"]: v["val"] for v in fin["operating_income"]}
    rows = []
    for i, r in enumerate(rev):
        row = {"fy_end": r["fy_end"], "revenue": r["val"], "operating_income": op.get(r["fy_end"])}
        if i > 0:
            row["revenue_growth"] = round(r["val"] / rev[i - 1]["val"] - 1, 4)
        if row["operating_income"] is not None:
            row["op_margin"] = round(row["operating_income"] / row["revenue"], 4)
        rows.append(row)
    return {"ticker": fin["ticker"], "company": fin["company"], "unit": fin["unit"], "years": rows}


def structure(bundle: dict) -> dict:
    print("[2/5] STRUCTURE — computing growth and margins in code")
    return {
        "target": _metrics(bundle["target"]),
        "peers": [_metrics(p) for p in bundle["peers"]],
        "recent_filings": bundle["filings"],
    }


# ------------------------------------------------------------ 3. REASON

def reason(data: dict, dry_run: bool) -> dict:
    if dry_run:
        print("[3/5] REASON — dry run: using canned memo JSON")
        memo = json.loads(CANNED.read_text())
        memo.pop("_note", None)
        return memo
    print(f"[3/5] REASON — asking {llm.default_model()} for the memo (schema-forced)")
    prompt = (
        "Write a market-intelligence memo on the target company versus its "
        "peers, using only this data block:\n\n"
        f"<data>\n{json.dumps(data, indent=2)}\n</data>"
    )
    return llm.ask_structured(prompt, name="record_memo", schema=MEMO_SCHEMA, system=SYSTEM)


# ------------------------------------------------------------ 4. VALIDATE

def source_values(data: dict) -> list[float]:
    vals: list[float] = []
    for m in [data["target"], *data["peers"]]:
        for y in m["years"]:
            vals += [y.get("revenue"), y.get("operating_income"),
                     y.get("revenue_growth"), y.get("op_margin")]
    return [v for v in vals if v is not None]


def validate(memo: dict, data: dict) -> list[float]:
    print("[4/5] VALIDATE — cross-checking every number in the memo against inputs")
    prose = json.dumps(memo)
    offenders = verify.novel_numbers(prose, source_values(data))
    if offenders:
        print(f"      ⚠️  numbers NOT traceable to source data: {offenders}")
        print("      (derived ratios the model computed — 'a 3.5x increase' — "
              "land here too: the checker can't derive, so a human judges them)")
    else:
        print("      all figures trace back to the data block ✅")
    return offenders


# ------------------------------------------------------------ 5. REVIEW + render

def render(memo: dict, data: dict, offenders: list[float]) -> str:
    t = data["target"]
    lines = [
        f"# Market intelligence — {t['company']} ({t['ticker']})",
        "",
        f"*Source: SEC EDGAR XBRL facts + filing index. Currency: {t['unit']}. "
        "AI-drafted, human-reviewed.*",
        "",
    ]
    if offenders:
        lines += [f"> ⚠️ **Validation warning** — untraceable figures: {offenders}", ""]
    lines += ["## Executive summary", "", memo["executive_summary"], "", "## KPI read", ""]
    lines += [f"- **{k['metric']}**: {k['reading']}" for k in memo["kpi_read"]]
    lines += ["", "## Competitive position", "", memo["competitive_position"], "", "## Risks", ""]
    lines += [f"- {r}" for r in memo["risks"]]
    lines += ["", "## Questions for management", ""]
    lines += [f"- {q}" for q in memo["questions_for_management"]]
    if memo["data_gaps"]:
        lines += ["", "## Data gaps (not in source — do not fill from memory)", ""]
        lines += [f"- {g}" for g in memo["data_gaps"]]
    lines += ["", "## Recent filings (target)", ""]
    lines += [f"- {f['form']} filed {f['filed']} (period {f['report_date']})"
              for f in data["recent_filings"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ticker", nargs="?", default="AAPL")
    ap.add_argument("--peers", nargs="*", default=["MSFT", "GOOGL"])
    ap.add_argument("--dry-run", action="store_true", help="canned memo; no API call")
    ap.add_argument("--yes", action="store_true", help="skip the human approval gate")
    args = ap.parse_args()

    data = structure(retrieve(args.ticker.upper(), [p.upper() for p in args.peers]))
    memo = reason(data, args.dry_run)
    offenders = validate(memo, data)
    rendered = render(memo, data, offenders)

    print("[5/5] REVIEW — memo preview:\n")
    print(rendered[:1200] + ("\n[... truncated ...]" if len(rendered) > 1200 else ""))
    if not args.yes:
        answer = input("\nApprove and save this memo? [y/N] ").strip().lower()
        if answer != "y":
            print("Not saved. (The human gate is a feature, not a formality.)")
            return
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / f"intel_memo_{args.ticker.upper()}.md"
    path.write_text(rendered, encoding="utf-8")
    print(f"Saved {path}")
    if not args.dry_run:
        print(f"Token usage: {llm.usage_summary()}")


if __name__ == "__main__":
    main()
