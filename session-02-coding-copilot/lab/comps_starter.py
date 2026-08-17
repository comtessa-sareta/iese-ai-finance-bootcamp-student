"""Session 2 lab — Comparable Company Analysis tool (STARTER).

Goal: from the clean dataset, produce a comps table an analyst could actually
use: growth, margins, valuation multiples, sorted and exported.

Work with Claude Code, but stay in the driver's seat:
 - ask it to implement ONE function at a time,
 - read the code it writes before running it,
 - verify one company's numbers by hand (calculator!) before trusting the table.

Run from the repo root:

    python session-02-coding-copilot/lab/comps_starter.py

Definitions you'll need (also in the data README):
    EBITDA      = operating income + D&A          (approximation)
    Market cap  = shares outstanding x price
    EV          = market cap + total debt - cash  (enterprise value)
    EV/EBITDA, EV/Sales, P/E — the classic trading multiples
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data" / "tech_financials.csv"
OUT = Path(__file__).resolve().parents[2] / "outputs"


def load_data(path: Path = DATA) -> pd.DataFrame:
    """Load the clean dataset. (This one is a freebie.)"""
    return pd.read_csv(path)


def add_growth_and_margins(df: pd.DataFrame) -> pd.DataFrame:
    """TODO 1 — add these columns:
    revenue_growth_1y : revenue_m / revenue_prior_m - 1
    revenue_cagr_2y   : (revenue_m / revenue_prior2_m) ** 0.5 - 1
    ebitda_m          : operating_income_m + d_and_a_m
    op_margin, ebitda_margin, ni_margin : each vs revenue_m
    """
    raise NotImplementedError("TODO 1")


def add_multiples(df: pd.DataFrame) -> pd.DataFrame:
    """TODO 2 — add these columns:
    mcap_m    : shares_m * price_usd
    ev_m      : mcap_m + total_debt_m - cash_m
    ev_ebitda : ev_m / ebitda_m      -> only when ebitda_m > 0, else NaN
    ev_sales  : ev_m / revenue_m
    pe        : mcap_m / net_income_m -> only when net_income_m > 0, else NaN

    Multiples on negative denominators are meaningless — return NaN, never a
    negative multiple. (Intel will test you on this.)
    """
    raise NotImplementedError("TODO 2")


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    """TODO 3 — return a clean summary table:
    - columns: ticker, revenue_m, revenue_growth_1y, ebitda_margin, ev_ebitda, ev_sales, pe
    - sorted by ev_ebitda (ascending, NaN last)
    - add a final row 'MEDIAN' with the column medians (skip NaN)
    """
    raise NotImplementedError("TODO 3")


def export(summary: pd.DataFrame) -> None:
    """TODO 4 — write the summary to outputs/comps_summary.csv and print it
    nicely (percentages as %, multiples with 1 decimal and an 'x' suffix)."""
    raise NotImplementedError("TODO 4")


# Stretch goals (if you finish early):
#  5. A scatter chart: revenue_growth_1y (x) vs ev_ebitda (y), ticker labels.
#     Is growth priced in?
#  6. A sanity_check(df) function that asserts: no duplicate tickers,
#     shares_m > 0, and |ebitda_margin| < 1. Run it before export.
#  7. Read a second ticker list from the command line and filter the table.


def main() -> None:
    df = load_data()
    df = add_growth_and_margins(df)
    df = add_multiples(df)
    summary = build_summary(df)
    export(summary)


if __name__ == "__main__":
    main()
