# Session 4 — AI Workflows & System Design for Finance

> 🎓 **Work in [`notebooks/04-workflows-edgar.ipynb`](../notebooks/04-workflows-edgar.ipynb)** — it contains this session's full teaching and lab. This README is the session brief and reference.

**You leave with:** a Company Screening Engine that combines live SEC/EDGAR
data, deterministic filtering and validated LLM reasoning.

## The pattern of the day

```
INPUT → RETRIEVE (code) → STRUCTURE (code) → REASON (model) → VALIDATE (code) → HUMAN
```

A **workflow** is a fixed plan written by you, where the model fills in
designated steps. Three design rules carry the whole session:

1. **Code does math; the model does judgment.** Filtering, growth rates and
   margins are computed in pandas. The model writes grounded prose about them.
2. **Validate at the boundary.** Schema-forced output (`llm.ask_structured`),
   then a numeric audit: any figure in the prose that doesn't trace back to
   the input data gets flagged (`toolkit/verify.py`).
3. **The human gate is the exit.** Nothing is saved or sent without approval.

## Live demo — AI Market Intelligence Workflow

```bash
python session-04-workflows/demo/market_intel_workflow.py AAPL --peers MSFT GOOGL
```

Five numbered steps print as they run — retrieval from EDGAR, metrics in code,
a schema-forced memo, the numeric cross-check, the approval gate. Also worth
seeing: `--dry-run` runs the identical pipeline with a canned memo (no API
key), which is how you test workflow plumbing cheaply.

New data skills inside: SEC EDGAR (`toolkit/edgar.py`, endpoints and XBRL
gotchas in `edgar-cheatsheet.md`) — filings metadata, XBRL company facts, and
the tag-drift reality documented the hard way.

## Lab (30 min) — Company Screening Engine

Open `lab/screening_starter.py` (running it unmodified stops at TODO 1 — your
entry point; after TODOs 1-2 it runs keyless with `--dry-run`). Build:

1. `fetch_metrics()` — 3-year fundamentals per ticker from EDGAR, defensive
   (one bad ticker must not kill the screen).
2. `apply_screen()` — the deterministic filter: growth ≥ X, net margin ≥ Y,
   optionally improving. **Pandas decides, not Claude.**
3. `write_rationales()` — one schema-forced call for the whole shortlist,
   grounded in your metrics table, then audited with `verify.novel_numbers`.

Run your screen on the 16-company universe (`data/universe.csv` — industrials
and pharma), then change the criteria and watch the shortlist move:

```bash
python session-04-workflows/lab/screening_starter.py --min-growth 0.10 --require-improving
python session-04-workflows/lab/screening_starter.py --sector industrials
```

Question to answer in your reflection: why did we screen on NET margin, not
operating margin? (Try operating income on the pharma names and see.)

## Deliverable checklist

- [ ] `outputs/screen_report.md` from your engine, criteria stated in the header
- [ ] At least one run with modified criteria — note what changed
- [ ] One rationale audited: which numbers did the checker trace? any ⚠️?
- [ ] Committed to your GitHub repo
- [ ] Stretch: add `--min-revenue-bn`; screen your own universe CSV
