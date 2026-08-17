---
marp: true
paginate: true
theme: default
---

# Session 2 — Claude Code I: AI as a Coding Copilot

**From prompt playbook → working Python. Deliverable: your comps tool, on GitHub.**

---

# The working rhythm (the actual skill)

1. **Ask small** — one function, one fix, one chart at a time
2. **Read before you run** — can't explain a line? ask for the explanation
3. **Verify one number by hand** — every table, one cell, calculator. Forever.
4. **Commit at every green moment** — small commits are your undo button

<!-- "You are the analyst-in-charge; Claude is a very fast junior." -->

---

# Python for finance — the map, not the lecture

- **DataFrame** = the analyst's table (`pandas`)
- `read_csv` / `read_excel` → load; columns are vectors: `df["a"]/df["b"]`
- APIs = `requests.get(url).json()` (tomorrow: SEC EDGAR)
- Charts = `matplotlib`/`seaborn`, saved to files

You don't memorize pandas. You **specify** and **verify**.

---

# Git in three commands (and why)

```bash
git add -A && git commit -m "comps: margins working"   # save point
git revert <sha>                                       # undo, with history
git push                                               # backup + shipping
```

Your GitHub repo **is** your portfolio — recruiters read commits like CVs.

---

# Live demo — Financial Data Pipeline in 30'

`tech_financials_messy.csv` — real SEC-filed fundamentals, 8 realistic defects:

ugly headers · text numbers · **one row in $B** · duplicate row ·
dirty ticker · missing values · junk TOTAL row · stray notes column

Process: **inspect → clean explicitly → KPIs → chart → commit**

<!-- The unit trap is the star: a silent 1000x error if missed. -->

---

# Lab (30 min) — Comparable Company Analysis tool

`lab/comps_starter.py` — four TODOs:

1. growth + margins (incl. **EBITDA = op income + D&A**, approximation documented)
2. multiples: mcap, EV, **EV/EBITDA, EV/Sales, P/E** — negatives → n.m., never a negative multiple
3. summary table, sorted, with MEDIAN row
4. export + pretty print

Then: **hand-verify Apple's EV/EBITDA before trusting the rest.**

---

# Watch out for

- **Intel**: negative op income → P/E is *n.m.* (that's correct behavior)
- **AMD**: EV/EBITDA looks wild → D&A understated in XBRL (see data README)
- Fiscal years are **misaligned** across companies (Jan/Jun/Sep/Dec ends)
- Prices have an **as-of date** — fundamentals from filings, prices from markets

---

# Ship it

```bash
git init && git add . && git commit -m "Comps tool: first working version"
gh repo create my-finance-toolkit --private --source . --push
```

---

# Reflection

1. Where was Claude fast — and where were YOU essential?
2. Which check caught the most?
3. Why explicit cleaning instead of "AI, just clean it"?

**Next (12:00):** I hand you a valuation model that is **wrong on purpose**.
