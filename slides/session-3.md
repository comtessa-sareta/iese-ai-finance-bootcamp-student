---
marp: true
paginate: true
theme: default
---

# Session 3 — Claude Code II: Debugging, Testing & Financial Analytics

**Deliverable: an investment-memo draft from YOUR earnings engine — with a
fabrication detector.**

---

# The debugging protocol

1. **Read the traceback bottom-up** — last line = what; marked line = where
2. Reproduce it
3. **Diagnose before fixing** — make Claude explain the cause first
4. One change at a time; re-run after each

> Crashes are the *friendly* bugs. They announce themselves.
> The dangerous ones return a number.

---

# Tests = financial logic, written down

```python
def test_equity_value_subtracts_net_debt():
    """Debt holders get paid first: equity = EV - net debt."""
```

- Each sanity test names one piece of finance the code must respect
- The **napkin test**: one case simple enough to compute by hand
- If your model can't reproduce a hand-checkable case, you don't have a
  model — you have a rumour

---

# Live demo — Fix a Broken Valuation Model

Meridian Semiconductor (fictional), trades at **$62**

1. Run → **crash** → traceback → fix
2. Runs → says **$115+** → would you sign?
3. `pytest` → six failures, each a finance error
4. Fix by test: discounting off-by-one · WACC tax shield ·
   **undiscounted terminal value** · net-debt sign · missing g<r guard
5. Green + plausible: **$75.61**

---

# Evals, in one slide

- Tests check **code**. Evals check **model outputs**.
- Cheapest useful eval in finance: **evidence verification** —
  every claim carries a verbatim quote; code checks the quote exists
- You build exactly that in the next 30 minutes

---

# Lab (30 min) — Earnings Analysis Engine

`lab/earnings_starter.py` (+ synthetic Meridian call transcript — fictional
company, so the model can't lean on memorized knowledge)

1. **Grounding rules** (system prompt)
2. **verify_evidence()** — quote checker: the trust layer
3. Finish the memo renderer

The dry-run analysis hides **one fabricated quote**. Your code will catch it.

---

# What a good engine finds in this transcript

- "One-time" ramp costs… for the **third consecutive quarter**
- CEO says margins "structurally improving"; CFO **won't guide** a recovery
- Guidance **excludes** the pending export-license review (~14% of revenue)
- Inventory **+41%**, DSO **71 vs 58** days
- Largest customer **15% → 22%** of revenue

<!-- Different runs will find different subsets — that's the non-determinism conversation. -->

---

# Reflection

1. How do you now *know* a number is right?
2. The quote-checker caught what your eyes missed. Where else does that generalize?
3. Would you sign your engine's memo? What's still missing?

**Tomorrow 9:00:** we stop pasting context and start **fetching** it —
live SEC filings at scale.
