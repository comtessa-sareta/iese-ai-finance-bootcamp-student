"""Minimal SEC EDGAR client for the bootcamp.

Everything here uses only free, public, key-less SEC endpoints:

- Ticker map:        https://www.sec.gov/files/company_tickers.json
- Filings metadata:  https://data.sec.gov/submissions/CIK##########.json
- XBRL facts:        https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
- Filing documents:  https://www.sec.gov/Archives/edgar/data/<cik>/<accession>/<doc>

SEC fair-access rules (https://www.sec.gov/os/accessing-edgar-data):
identify yourself with a User-Agent ("Name email") and stay under 10 req/s.
This module throttles every request and caches responses on disk, so a
classroom of students re-running labs stays polite.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path

import requests

TICKER_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
DOC_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession}/{doc}"

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache" / "edgar"
_MIN_INTERVAL = 0.15  # seconds between requests — well under SEC's 10 req/s cap
_last_request_at = 0.0
_session = requests.Session()

ANNUAL_FORMS = {"10-K", "10-K/A", "20-F", "20-F/A", "40-F"}


class EdgarError(RuntimeError):
    """Raised when EDGAR data is missing or a request fails."""


def _user_agent() -> str:
    ua = os.environ.get("SEC_EDGAR_USER_AGENT", "").strip()
    if not ua or ua.startswith("Your Name"):
        # SEC's edge rejects (HTTP 403) any User-Agent without an email-format
        # contact, so the fallback must contain one. Still: be a good citizen
        # and set your real name/email in .env.
        ua = "IESE AI-Finance Bootcamp unconfigured-student@example.com (set SEC_EDGAR_USER_AGENT in .env)"
    return ua


def _cache_path(url: str) -> Path:
    return CACHE_DIR / (hashlib.sha1(url.encode()).hexdigest() + ".cache")


def _get(url: str, use_cache: bool = True, max_age_hours: float = 24.0) -> bytes:
    """Throttled GET with a simple disk cache (default: reuse for 24h)."""
    global _last_request_at
    cache = _cache_path(url)
    if use_cache and cache.exists():
        age_h = (time.time() - cache.stat().st_mtime) / 3600
        if age_h < max_age_hours:
            return cache.read_bytes()

    wait = _MIN_INTERVAL - (time.monotonic() - _last_request_at)
    if wait > 0:
        time.sleep(wait)
    resp = _session.get(url, headers={"User-Agent": _user_agent()}, timeout=30)
    _last_request_at = time.monotonic()
    if resp.status_code != 200:
        raise EdgarError(f"EDGAR returned HTTP {resp.status_code} for {url}")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(resp.content)
    return resp.content


def _get_json(url: str, **kw) -> dict:
    return json.loads(_get(url, **kw))


# ---------------------------------------------------------------- lookups

def ticker_map() -> dict[str, dict]:
    """Return {TICKER: {cik_str, ticker, title}} for every SEC registrant."""
    raw = _get_json(TICKER_URL)
    return {row["ticker"].upper(): row for row in raw.values()}


def cik_for(ticker: str) -> str:
    """10-digit zero-padded CIK for a ticker, e.g. 'AAPL' -> '0000320193'."""
    row = ticker_map().get(ticker.upper())
    if row is None:
        raise EdgarError(f"Ticker {ticker!r} not found in SEC registry")
    return f"{int(row['cik_str']):010d}"


def company_name(ticker: str) -> str:
    row = ticker_map().get(ticker.upper())
    return row["title"] if row else ticker.upper()


# ---------------------------------------------------------------- filings

def get_submissions(ticker: str) -> dict:
    """Full submissions JSON: company metadata + recent filings index."""
    return _get_json(SUBMISSIONS_URL.format(cik=cik_for(ticker)))


def recent_filings(ticker: str, forms: list[str] | None = None, limit: int = 10) -> list[dict]:
    """Most recent filings, newest first, optionally filtered by form type.

    Returns dicts with: form, filed, report_date, accession, primary_doc, url.
    """
    subs = get_submissions(ticker)
    recent = subs["filings"]["recent"]
    cik_int = int(subs["cik"])
    out: list[dict] = []
    for i in range(len(recent["form"])):
        form = recent["form"][i]
        if forms and form not in forms:
            continue
        accession = recent["accessionNumber"][i].replace("-", "")
        doc = recent["primaryDocument"][i]
        out.append({
            "form": form,
            "filed": recent["filingDate"][i],
            "report_date": recent["reportDate"][i],
            "accession": accession,
            "primary_doc": doc,
            "url": DOC_URL.format(cik_int=cik_int, accession=accession, doc=doc),
        })
        if len(out) >= limit:
            break
    return out


class _TextExtractor(HTMLParser):
    _SKIP = {"script", "style"}

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self._chunks.append(data)

    def text(self) -> str:
        joined = " ".join(self._chunks)
        return re.sub(r"[ \t\xa0]+", " ", re.sub(r"\n{3,}", "\n\n", joined)).strip()


def fetch_filing_text(filing: dict, max_chars: int = 400_000) -> str:
    """Download a filing's primary document and return it as plain text."""
    html = _get(filing["url"]).decode("utf-8", errors="replace")
    parser = _TextExtractor()
    parser.feed(html)
    return parser.text()[:max_chars]


# ---------------------------------------------------------------- XBRL facts

def get_company_facts(ticker: str) -> dict:
    """All XBRL facts the company has ever reported (large JSON)."""
    return _get_json(FACTS_URL.format(cik=cik_for(ticker)))


def _pick_unit(units: dict, preferred: str | None) -> str | None:
    if preferred and preferred in units:
        return preferred
    for u in ("USD", "EUR", "DKK", "GBP", "JPY", "CHF"):  # common currencies
        if u in units:
            return u
    return next(iter(units), None)


def annual_values(
    facts: dict,
    tags: list[str],
    unit: str | None = "USD",
    n: int = 4,
) -> dict:
    """Annual (full fiscal year) values for the first tag that has data.

    Searches us-gaap first, then ifrs-full (foreign private issuers, e.g. Novo
    Nordisk, report under IFRS — often NOT in USD, so check the returned unit!).

    Returns {"tag", "taxonomy", "unit", "values": [{"fy_end", "val", "form"} ...]}
    oldest→newest, up to the last n fiscal years. Raises EdgarError if no tag matches.

    Companies change tags over the years (e.g. NVIDIA moved from
    RevenueFromContractWithCustomer... back to plain Revenues), so we check every
    candidate and keep the one whose data reaches the most recent fiscal year.
    """
    candidates: list[dict] = []
    for taxonomy in ("us-gaap", "ifrs-full"):
        bucket = facts.get("facts", {}).get(taxonomy, {})
        for tag in tags:
            units = bucket.get(tag, {}).get("units", {})
            unit_used = _pick_unit(units, unit)
            if not unit_used:
                continue
            rows = _annual_rows(units[unit_used], n)
            if rows:
                candidates.append(
                    {"tag": tag, "taxonomy": taxonomy, "unit": unit_used, "values": rows}
                )
    if not candidates:
        raise EdgarError(f"No annual data for tags {tags}")
    return max(candidates, key=lambda c: (c["values"][-1]["fy_end"], len(c["values"])))


def _annual_rows(entries: list[dict], n: int) -> list[dict]:
    """Filter duration facts to full-year periods from annual reports, dedupe by period end."""
    best: dict[str, dict] = {}
    for e in entries:
        if e.get("form") not in ANNUAL_FORMS or "start" not in e or "end" not in e:
            continue
        try:
            days = (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days
        except ValueError:
            continue
        if not 320 <= days <= 400:  # full fiscal year, not a quarter
            continue
        prev = best.get(e["end"])
        if prev is None or e.get("filed", "") > prev.get("filed", ""):
            best[e["end"]] = e
    rows = [
        {"fy_end": e["end"], "val": e["val"], "form": e["form"]}
        for e in sorted(best.values(), key=lambda x: x["end"])
    ]
    return rows[-n:]


def latest_instant(facts: dict, tags: list[str], unit: str | None = "USD") -> dict | None:
    """Latest balance-sheet (point-in-time) value for the first matching tag."""
    for taxonomy in ("us-gaap", "ifrs-full"):
        bucket = facts.get("facts", {}).get(taxonomy, {})
        for tag in tags:
            units = bucket.get(tag, {}).get("units", {})
            unit_used = _pick_unit(units, unit)
            if not unit_used:
                continue
            instants = [e for e in units[unit_used] if "start" not in e and "end" in e]
            if instants:
                e = max(instants, key=lambda x: (x["end"], x.get("filed", "")))
                return {"tag": tag, "taxonomy": taxonomy, "unit": unit_used,
                        "asof": e["end"], "val": e["val"]}
    return None


def latest_shares_outstanding(facts: dict) -> dict | None:
    """Latest common shares outstanding.

    Primary source: the filing cover page (dei taxonomy). Multi-class filers
    (Alphabet, Meta) report per-class values that companyfacts drops, so we fall
    back to annual diluted weighted-average shares — close enough for teaching
    multiples, and the 'source' field tells you which one you got.
    """
    units = (
        facts.get("facts", {})
        .get("dei", {})
        .get("EntityCommonStockSharesOutstanding", {})
        .get("units", {})
        .get("shares", [])
    )
    instants = [e for e in units if "end" in e]
    if instants:
        e = max(instants, key=lambda x: (x["end"], x.get("filed", "")))
        return {"asof": e["end"], "val": e["val"], "source": "dei cover page"}
    for taxonomy in ("us-gaap", "ifrs-full"):
        entries = (
            facts.get("facts", {})
            .get(taxonomy, {})
            .get("WeightedAverageNumberOfDilutedSharesOutstanding", {})
            .get("units", {})
            .get("shares", [])
        )
        rows = _annual_rows(entries, n=1)
        if rows:
            return {"asof": rows[-1]["fy_end"], "val": rows[-1]["val"],
                    "source": "diluted weighted-average (annual)"}
    return None


# Tag candidate lists used across the course (XBRL tagging varies by company).
REVENUE_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "SalesRevenueNet",
    "Revenue",                          # ifrs-full
    "RevenueFromContractsWithCustomers",  # ifrs-full
]
OPERATING_INCOME_TAGS = [
    "OperatingIncomeLoss",
    "ProfitLossFromOperatingActivities",  # ifrs-full
]
NET_INCOME_TAGS = [
    "NetIncomeLoss",
    "ProfitLoss",  # ifrs-full
]
DEPRECIATION_AMORTIZATION_TAGS = [
    "DepreciationDepletionAndAmortization",
    "DepreciationAmortizationAndAccretionNet",
    "DepreciationAndAmortization",
    "DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss",  # ifrs-full
    "Depreciation",  # last resort: depreciation only (understates D&A) — MSFT, GOOGL
]
CASH_TAGS = [
    "CashAndCashEquivalentsAtCarryingValue",
    "CashAndCashEquivalents",  # ifrs-full
]
DEBT_TAGS_TOTAL = ["LongTermDebt", "DebtLongtermAndShorttermCombinedAmount"]
DEBT_TAGS_PARTS = ["LongTermDebtNoncurrent", "LongTermDebtCurrent", "CommercialPaper"]


def total_debt(facts: dict) -> dict | None:
    """Approximate total debt, robust to stale tags.

    Companies drift between tags over the years (AMD last used LongTermDebt in
    2021!), so we build every candidate — each total tag, plus the sum of the
    parts — and keep the one with the most recent balance-sheet date, breaking
    ties toward the larger (more complete) figure.

    Teaching approximation: ignores operating leases and some short-term
    borrowings — good enough for comparable screens, not for a fairness opinion.
    """
    candidates: list[dict] = []
    for tag in DEBT_TAGS_TOTAL:
        hit = latest_instant(facts, [tag])
        if hit:
            candidates.append({"val": float(hit["val"]), "asof": hit["asof"], "source": tag})
    parts = [latest_instant(facts, [t]) for t in DEBT_TAGS_PARTS]
    parts = [p for p in parts if p]
    if parts:
        asof = max(p["asof"] for p in parts)
        same_date = [p for p in parts if p["asof"] == asof]
        candidates.append({
            "val": sum(float(p["val"]) for p in same_date),
            "asof": asof,
            "source": "+".join(p["tag"] for p in same_date),
        })
    if not candidates:
        return None
    return max(candidates, key=lambda c: (c["asof"], c["val"]))


def annual_financials(ticker: str, n: int = 4) -> dict:
    """One-call summary used by Session 4/5 tools: revenue, operating income,
    net income series + latest balance-sheet items. Values in the filer's
    reporting currency (see 'unit')."""
    facts = get_company_facts(ticker)
    rev = annual_values(facts, REVENUE_TAGS, unit=None, n=n)
    out = {
        "ticker": ticker.upper(),
        "company": company_name(ticker),
        "unit": rev["unit"],
        "revenue": rev["values"],
    }
    for key, tags in [
        ("operating_income", OPERATING_INCOME_TAGS),
        ("net_income", NET_INCOME_TAGS),
    ]:
        try:
            out[key] = annual_values(facts, tags, unit=rev["unit"], n=n)["values"]
        except EdgarError:
            out[key] = []
    cash = latest_instant(facts, CASH_TAGS, unit=rev["unit"])
    out["cash"] = cash["val"] if cash else None
    debt = total_debt(facts)
    out["total_debt"] = debt["val"] if debt else None
    shares = latest_shares_outstanding(facts)
    out["shares_outstanding"] = shares["val"] if shares else None
    return out


if __name__ == "__main__":  # quick self-test:  python toolkit/edgar.py NVDA
    import sys

    t = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    print(json.dumps(annual_financials(t), indent=2))
