# SEC EDGAR — free data cheatsheet

Everything is public and key-less. Two rules from the SEC's fair-access policy
(https://www.sec.gov/os/accessing-edgar-data): identify yourself with a
`User-Agent: Name email` header, and stay under 10 requests/second.
`toolkit/edgar.py` does both, plus disk caching.

## The four endpoints that matter

| What | URL pattern |
|------|-------------|
| Ticker → CIK map | `https://www.sec.gov/files/company_tickers.json` |
| Company filings index | `https://data.sec.gov/submissions/CIK##########.json` (10-digit, zero-padded) |
| All XBRL facts for a company | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` |
| A filing's documents | `https://www.sec.gov/Archives/edgar/data/<cik>/<accession-no-dashes>/<primary-doc>` |

Also useful: one concept across ALL companies for a period ("frames"):
`https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2025.json`
Full-text search across filings — browse it at https://www.sec.gov/edgar/search/
or query the same index programmatically:
`https://efts.sec.gov/LATEST/search-index?q=%22your+phrase%22&forms=10-K`

## Form types you'll actually use

| Form | What it is | Cadence |
|------|-----------|---------|
| 10-K | Annual report (audited, with risk factors, MD&A) | yearly |
| 10-Q | Quarterly report (unaudited) | quarterly |
| 8-K | Material events — earnings releases arrive here as Exhibit 99 | as it happens |
| 20-F | Annual report for foreign private issuers (Novo Nordisk, SAP...) | yearly |
| DEF 14A | Proxy statement — compensation, governance | yearly |
| 13F | Institutional holdings | quarterly |

## XBRL reality check (learned the hard way in this course)

- **Tags drift.** NVIDIA moved revenue tags across years; AMD's last standard
  D&A tag is from 2019; Oracle's `LongTermDebt` died in 2022. Always prefer the
  tag whose data reaches the most recent fiscal year, and reject stale values.
- **Foreign private issuers file IFRS** (`ifrs-full` taxonomy) and often NOT in
  USD — Novo Nordisk reports in DKK. Check the `unit` before comparing.
- **Instant vs duration facts.** Balance-sheet items have only an `end` date;
  income-statement items have `start`+`end`. A "full year" is a duration of
  320-400 days from an annual form (10-K/20-F, `fp == "FY"`).
- **Multi-class share counts** (Alphabet, Meta) may be missing from
  companyfacts — fall back to diluted weighted-average shares.
- **Amended filings**: dedupe by period end, keep the latest `filed` date.
- **What's NOT here:** market prices, consensus estimates, segment KPIs beyond
  what's tagged. Filings ≠ market data.

## toolkit/edgar.py quick reference

```python
from toolkit import edgar

edgar.cik_for("AAPL")                          # '0000320193'
edgar.recent_filings("NVDA", forms=["10-K", "8-K"], limit=5)
facts = edgar.get_company_facts("MSFT")        # big raw JSON
edgar.annual_values(facts, edgar.REVENUE_TAGS, n=4)
edgar.latest_instant(facts, edgar.CASH_TAGS)
edgar.total_debt(facts)                        # staleness-aware
edgar.annual_financials("SONY", n=3)           # one-call summary (note unit: JPY!)
text = edgar.fetch_filing_text(edgar.recent_filings("AAPL", ["10-K"], 1)[0])
```
