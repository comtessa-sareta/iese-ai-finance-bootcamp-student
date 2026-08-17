"""Session 4 lab — Company Screening Engine (STARTER).

Define screening criteria in code, pull real fundamentals from SEC EDGAR,
shortlist the survivors, and have Claude write a grounded observation for each.

Running it before doing the TODOs stops at TODO 1 — that's your entry point.
Once TODOs 1-2 are in, this works WITHOUT an API key (LLM step skipped):

    python session-04-workflows/lab/screening_starter.py --dry-run

Division of labour — the whole lesson in one line:
    CODE does retrieval, math and filtering. The MODEL only writes prose,
    grounded in the table — and you verify even that.

Your work:
  TODO 1 — fetch_metrics(): 3-year fundamentals -> one screening row
  TODO 2 — apply_screen(): the deterministic filter (pandas decides, not Claude)
  TODO 3 — write_rationales(): grounded prose + novel-number check
  Stretch — add a --min-revenue-bn floor; add net margin; screen another sector
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

import pandas as pd  # noqa: E402

from toolkit import edgar, llm, verify  # noqa: E402

UNIVERSE = Path(__file__).resolve().parent.parent / "data" / "universe.csv"
OUT_DIR = REPO_ROOT / "outputs"

RATIONALE_SCHEMA = {
    "type": "object",
    "required": ["rationales"],
    "properties": {
        "rationales": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["ticker", "observation"],
                "properties": {
                    "ticker": {"type": "string"},
                    "observation": {"type": "string"},
                },
            },
        }
    },
}


def fetch_metrics(ticker: str) -> dict | None:
    """TODO 1 — call edgar.annual_financials(ticker, n=3) and return:

        {ticker, company, fy_end, revenue_bn, growth_1y, cagr_2y,
         net_margin, net_margin_prior}

    Rules:
      - wrap the EDGAR call in try/except edgar.EdgarError -> return None
        (one bad ticker must not kill a 16-company screen)
      - require 3 years of USD revenue, else return None
      - growth_1y   = rev[latest] / rev[prev] - 1
      - cagr_2y     = (rev[latest] / rev[oldest]) ** 0.5 - 1
      - net_margin  = net income / revenue, matched BY fiscal year end
        (why net and not operating margin? try operating income on the pharma
         names and see what comes back — most tag no operating subtotal at all)
    """
    raise NotImplementedError("TODO 1")


def apply_screen(df: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    """TODO 2 — return only rows meeting the criteria, sorted by growth desc:
      - growth_1y >= args.min_growth
      - net_margin >= args.min_margin
      - if args.require_improving: net_margin > net_margin_prior
    """
    raise NotImplementedError("TODO 2")


def write_rationales(shortlist: pd.DataFrame, dry_run: bool) -> dict[str, str]:
    """TODO 3 — {ticker: observation} for each shortlisted company.

    - dry_run: return a placeholder string per ticker (keeps the pipeline testable)
    - live: ONE llm.ask_structured() call with the whole shortlist as JSON,
      schema=RATIONALE_SCHEMA, and a system prompt that forbids outside
      knowledge and new numbers
    - then audit each observation with verify.novel_numbers() against the
      metric values you supplied; append a ⚠️ warning if anything is untraceable
    """
    raise NotImplementedError("TODO 3")


def render_report(df: pd.DataFrame, shortlist: pd.DataFrame,
                  rationales: dict[str, str], args: argparse.Namespace) -> str:
    """Markdown report. (Done for you — read it, you'll present from it.)"""
    fmt = df.copy()
    for col in ("growth_1y", "cagr_2y", "net_margin", "net_margin_prior"):
        fmt[col] = fmt[col].map(lambda v: f"{v:.1%}" if pd.notna(v) else "—")
    criteria = (
        f"revenue growth ≥ {args.min_growth:.0%}, net margin ≥ {args.min_margin:.0%}"
        + (", net margin improving y/y" if args.require_improving else "")
        + (f", sector = {args.sector}" if args.sector else "")
    )
    lines = [
        "# Company screen — SEC EDGAR fundamentals", "",
        f"*Criteria: {criteria}.*", "",
        "## Universe scanned", "", fmt.to_markdown(index=False), "",
        f"## Shortlist ({len(shortlist)} of {len(df)})", "",
    ]
    for _, row in shortlist.iterrows():
        lines += [f"### {row['company']} ({row['ticker']})",
                  rationales.get(row["ticker"], ""), ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-growth", type=float, default=0.08)
    ap.add_argument("--min-margin", type=float, default=0.10, help="minimum NET margin")
    ap.add_argument("--require-improving", action="store_true")
    ap.add_argument("--sector", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    universe = pd.read_csv(UNIVERSE)
    if args.sector:
        universe = universe[universe["sector"] == args.sector]
    print(f"Screening {len(universe)} companies from {UNIVERSE.name} ...")

    rows = [m for t in universe["ticker"] if (m := fetch_metrics(t)) is not None]
    df = pd.DataFrame(rows)
    shortlist = apply_screen(df, args)
    print(f"Shortlist: {', '.join(shortlist['ticker']) or '(none — loosen the criteria)'}")

    report = render_report(df, shortlist, write_rationales(shortlist, args.dry_run), args)
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / "screen_report.md"
    path.write_text(report, encoding="utf-8")
    print(f"Report written to {path}")


if __name__ == "__main__":
    main()
