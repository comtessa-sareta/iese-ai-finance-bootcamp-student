"""Rebuild the Session 2 datasets from live SEC EDGAR data.

Run from the repo root:

    python session-02-coding-copilot/data/make_dataset.py

Writes (into this data/ folder):
    tech_financials.csv        — clean dataset for the lab
    tech_financials_messy.csv  — same data with realistic defects, for the
                                 live cleaning demo (defects are deterministic)

Fundamentals come from SEC XBRL company facts (real filings, latest fiscal
years). Share prices are NOT in SEC data — they are read from prices.csv,
which the instructor updates by hand before class (note the as-of date).
"""
from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from toolkit import edgar  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent
TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "AMD", "INTC", "CRM", "ORCL"]

COLUMNS = [
    "ticker", "company", "fy_end",
    "revenue_m", "revenue_prior_m", "revenue_prior2_m",
    "operating_income_m", "net_income_m", "d_and_a_m",
    "cash_m", "total_debt_m", "shares_m",
    "price_usd", "price_asof",
]


def musd(value: float | None) -> float | None:
    """USD -> USD millions, 1 decimal."""
    return None if value is None else round(value / 1e6, 1)


def build_row(ticker: str, prices: dict[str, dict]) -> dict:
    facts = edgar.get_company_facts(ticker)
    rev = edgar.annual_values(facts, edgar.REVENUE_TAGS, n=3)
    if rev["unit"] != "USD":
        raise SystemExit(f"{ticker}: expected USD filer, got {rev['unit']}")
    revs = [v["val"] for v in rev["values"]]
    if len(revs) < 3:
        revs = [None] * (3 - len(revs)) + revs

    latest_fy_end = rev["values"][-1]["fy_end"]

    def latest_flow(tags: list[str]) -> float | None:
        """Latest annual value — but only if it belongs to the SAME fiscal year
        as revenue. Companies abandon tags over time (AMD's last standard D&A
        tag is from 2019); a stale number is worse than a missing one."""
        try:
            vals = edgar.annual_values(facts, tags, n=1)["values"]
        except edgar.EdgarError:
            return None
        if vals and vals[-1]["fy_end"] == latest_fy_end:
            return vals[-1]["val"]
        return None

    cash = edgar.latest_instant(facts, edgar.CASH_TAGS)
    debt = edgar.total_debt(facts)
    shares = edgar.latest_shares_outstanding(facts)
    price = prices.get(ticker, {})
    return {
        "ticker": ticker,
        "company": edgar.company_name(ticker),
        "fy_end": latest_fy_end,
        "revenue_m": musd(revs[2]),
        "revenue_prior_m": musd(revs[1]),
        "revenue_prior2_m": musd(revs[0]),
        "operating_income_m": musd(latest_flow(edgar.OPERATING_INCOME_TAGS)),
        "net_income_m": musd(latest_flow(edgar.NET_INCOME_TAGS)),
        "d_and_a_m": musd(latest_flow(edgar.DEPRECIATION_AMORTIZATION_TAGS)),
        "cash_m": musd(cash["val"] if cash else None),
        "total_debt_m": musd(debt["val"] if debt else None),
        "shares_m": musd(shares["val"] if shares else None),
        "price_usd": price.get("price_usd"),
        "price_asof": price.get("price_asof"),
    }


def make_messy(rows: list[dict]) -> tuple[list[str], list[list]]:
    """Inject deterministic, realistic defects for the cleaning demo.

    Defects (keep this list in sync with the data README):
      1. Ugly headers (spaces, symbols, inconsistent case)
      2. Revenue columns as strings with thousands separators
      3. One company reported in $B instead of $M (see the 'Unit' column)
      4. One duplicated row
      5. Lower-case ticker with trailing whitespace
      6. Missing values (D&A, net income) for two companies
      7. A junk 'TOTAL' row at the bottom
      8. A free-text 'Notes' column nobody asked for
    """
    rng = random.Random(42)
    headers = [
        "Ticker ", " Company", "FY End", "Revenue FY ($M)", "Revenue FY-1 ($M)",
        "Revenue FY-2 ($M)", "Op Income ($M)", "Net Income ($M)", "D&A ($M)",
        "Cash ($M)", "Total Debt ($M)", "Shares (M)", "Price ($)", "Price As Of",
        "Unit", "Notes",
    ]

    def fmt_thousands(v):
        return f"{v:,.1f}" if isinstance(v, (int, float)) else ""

    unit_b_ticker = "META"      # defect 3
    dup_ticker = "MSFT"         # defect 4
    lower_ticker = "ORCL"       # defect 5
    drop_dna, drop_ni = "AMZN", "CRM"  # defect 6

    out: list[list] = []
    for r in rows:
        scale = 1000.0 if r["ticker"] == unit_b_ticker else 1.0
        unit = "USD_B" if r["ticker"] == unit_b_ticker else "USD_M"

        def num(key, r=r, scale=scale):
            v = r[key]
            return round(v / scale, 3) if isinstance(v, (int, float)) else ""

        ticker_out = r["ticker"].lower() + " " if r["ticker"] == lower_ticker else r["ticker"]
        row = [
            ticker_out, r["company"], r["fy_end"],
            fmt_thousands(num("revenue_m")), fmt_thousands(num("revenue_prior_m")),
            fmt_thousands(num("revenue_prior2_m")),
            num("operating_income_m"),
            "" if r["ticker"] == drop_ni else num("net_income_m"),
            "" if r["ticker"] == drop_dna else num("d_and_a_m"),
            num("cash_m"), num("total_debt_m"), num("shares_m"),
            r["price_usd"], r["price_asof"], unit,
            rng.choice(["", "", "", "check w/ IR", "restated?", "from 10-K"]),
        ]
        out.append(row)
        if r["ticker"] == dup_ticker:
            out.append(list(row))

    total_rev = sum(r["revenue_m"] or 0 for r in rows)
    out.append(["TOTAL", "", "", f"{total_rev:,.1f}"] + [""] * 12)
    return headers, out


def main() -> None:
    prices: dict[str, dict] = {}
    with open(DATA_DIR / "prices.csv", newline="") as f:
        for row in csv.DictReader(f):
            prices[row["ticker"]] = {
                "price_usd": float(row["price_usd"]),
                "price_asof": row["price_asof"],
            }

    rows = []
    for t in TICKERS:
        print(f"  fetching {t} from SEC EDGAR ...")
        rows.append(build_row(t, prices))

    clean_path = DATA_DIR / "tech_financials.csv"
    with open(clean_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {clean_path}")

    headers, messy = make_messy(rows)
    messy_path = DATA_DIR / "tech_financials_messy.csv"
    with open(messy_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(messy)
    print(f"wrote {messy_path}")


if __name__ == "__main__":
    main()
