# Session 2 datasets — provenance and caveats

## Files

| File | Purpose |
|------|---------|
| `tech_financials.csv` | Clean dataset for the comps lab. One row per company, USD **millions**. |
| `tech_financials_messy.csv` | Same data with 8 deliberate defects — used in the live cleaning demo. |
| `prices.csv` | Share prices used to build both files. **Hand-maintained — update before class.** |
| `make_dataset.py` | Rebuilds both CSVs from live SEC EDGAR data. |

## Provenance

- **Fundamentals are real**: pulled from each company's XBRL company facts on SEC
  EDGAR (latest three fiscal years as filed in 10-Ks). Regenerate any time with
  `python session-02-coding-copilot/data/make_dataset.py` from the repo root.
- **Prices are not in SEC data** (filings contain fundamentals, not market
  quotes — worth saying out loud in class). `prices.csv` carries an explicit
  `price_asof` date. Before teaching, update the prices and rerun the builder —
  or ask Claude Code to do it for you.

## Column dictionary (clean file)

| Column | Meaning |
|--------|---------|
| `fy_end` | End date of the latest fiscal year. **Fiscal years are NOT aligned across companies** (Apple ends September, NVIDIA January, Microsoft June, Oracle May). Comps across misaligned years is standard practice but know you're doing it. |
| `revenue_m`, `revenue_prior_m`, `revenue_prior2_m` | Revenue for FY, FY-1, FY-2 (USD m) |
| `operating_income_m`, `net_income_m` | Latest FY (USD m). Intel's are negative — your code must survive that. |
| `d_and_a_m` | Depreciation & amortization from cash-flow XBRL tags. Some issuers only tag the depreciation component (Microsoft, Alphabet, AMD) so this can **understate** true D&A — treat EV/EBITDA as approximate. |
| `cash_m` | Cash & equivalents only — excludes short-term investments, so net debt is **overstated** for cash-rich firms. |
| `total_debt_m` | Long-term + current debt + commercial paper where tagged. Excludes operating leases. |
| `shares_m` | Shares outstanding from the filing cover page; for multi-class filers (Alphabet, Meta) falls back to diluted weighted-average shares. |

## The honest footnote

This is what free, public XBRL data actually looks like: tags drift across
years, some values are components rather than totals, and every derived
multiple inherits those approximations. That is not a flaw in the course — it
*is* the course: know your data, document your approximations, and never quote
a multiple you can't trace to its inputs.

## Defects in the messy file (instructor reference)

1. Ugly headers (spaces, symbols, inconsistent case)
2. Revenue columns as strings with thousands separators
3. META reported in **billions** (see `Unit` column) while everyone else is in millions
4. MSFT row duplicated
5. `orcl ` — lower-case ticker with trailing space
6. Missing values: AMZN D&A, CRM net income
7. Junk `TOTAL` row at the bottom
8. Free-text `Notes` column
