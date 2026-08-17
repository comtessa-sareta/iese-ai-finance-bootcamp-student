"""Session 2 live demo — a Financial Data Pipeline in 30 minutes.

Load a messy financials file, clean it, compute KPIs, chart the result.
This file is the demo's END STATE: in class it is built live, step by step,
with Claude Code (the exact prompts are in the instructor guide).

Run from the repo root:

    python session-02-coding-copilot/demo/financial_data_pipeline.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA = Path(__file__).resolve().parent.parent / "data" / "tech_financials_messy.csv"
OUT = Path(__file__).resolve().parents[2] / "outputs"


# ---------------------------------------------------------------- step 1: load

def load_raw(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


# ---------------------------------------------------------------- step 2: clean

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix every defect in the messy file — each line answers a real-world mess.

    Golden rule: cleaning is *explicit*. Every transformation is visible and
    reviewable; nothing happens silently inside a black box.
    """
    df = df.copy()

    # 2a. Headers: strip whitespace, lowercase, snake_case
    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace(r"[^\w]+", "_", regex=True).str.strip("_")
    )
    rename = {
        "revenue_fy_m": "revenue_m", "revenue_fy_1_m": "revenue_prior_m",
        "revenue_fy_2_m": "revenue_prior2_m", "op_income_m": "operating_income_m",
        "d_a_m": "d_and_a_m", "shares_m_1": "shares_m", "price": "price_usd",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    # 2b. Drop junk: the TOTAL row and the free-text notes column
    df = df[df["ticker"].str.strip().str.upper() != "TOTAL"]
    df = df.drop(columns=[c for c in ["notes"] if c in df.columns])

    # 2c. Normalize tickers ("orcl " -> "ORCL") and drop exact duplicates
    df["ticker"] = df["ticker"].str.strip().str.upper()
    before = len(df)
    df = df.drop_duplicates(subset="ticker", keep="first")
    if len(df) < before:
        print(f"  dropped {before - len(df)} duplicate row(s)")

    # 2d. Numbers stored as text ("416,161.0" -> 416161.0)
    numeric_cols = [
        "revenue_m", "revenue_prior_m", "revenue_prior2_m", "operating_income_m",
        "net_income_m", "d_and_a_m", "cash_m", "total_debt_m", "shares_m", "price_usd",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False), errors="coerce"
        )

    # 2e. Unit trap: one company is reported in billions — normalize to millions
    if "unit" in df.columns:
        in_billions = df["unit"] == "USD_B"
        scale_cols = [c for c in numeric_cols if c not in ("price_usd",)]
        df.loc[in_billions, scale_cols] = df.loc[in_billions, scale_cols] * 1000
        print(f"  rescaled {int(in_billions.sum())} row(s) from $B to $M")
        df = df.drop(columns=["unit"])

    print(f"Clean: {len(df)} companies")
    return df.reset_index(drop=True)


# ---------------------------------------------------------------- step 3: KPIs

def add_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["revenue_growth"] = df["revenue_m"] / df["revenue_prior_m"] - 1
    df["op_margin"] = df["operating_income_m"] / df["revenue_m"]
    df["ni_margin"] = df["net_income_m"] / df["revenue_m"]
    return df


# ---------------------------------------------------------------- step 4: chart

def chart(df: pd.DataFrame) -> Path:
    OUT.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    d = df.sort_values("revenue_growth", ascending=False)
    sns.barplot(data=d, x="ticker", y="revenue_growth", ax=axes[0], color="#2a6fdb")
    axes[0].set_title("Revenue growth (latest FY vs prior)")
    axes[0].yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("")

    d = df.sort_values("op_margin", ascending=False)
    colors = ["#c0392b" if v < 0 else "#2a9d5c" for v in d["op_margin"]]
    axes[1].bar(d["ticker"], d["op_margin"], color=colors)
    axes[1].set_title("Operating margin (negative in red)")
    axes[1].yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    axes[1].axhline(0, color="black", linewidth=0.8)

    fig.suptitle("Large-cap tech — latest fiscal year (SEC filings)", fontweight="bold")
    fig.tight_layout()
    out = OUT / "pipeline_kpis.png"
    fig.savefig(out, dpi=150)
    print(f"Chart saved to {out}")
    return out


def main() -> None:
    df = add_kpis(clean(load_raw(DATA)))
    cols = ["ticker", "revenue_m", "revenue_growth", "op_margin", "ni_margin"]
    print("\n", df[cols].round(3).to_string(index=False), "\n", sep="")
    chart(df)
    if matplotlib.get_backend().lower() != "agg":
        plt.show()


if __name__ == "__main__":
    main()
