---
marp: true
paginate: true
theme: default
---

# Session 4 · Workflows on Live SEC Data

**Yesterday you pasted data. Today your code fetches it.**

Agenda: idea (15') · demo (22') · your lab (30') · debrief (8')

---

# The pattern of the day

```
INPUT → RETRIEVE → STRUCTURE → REASON → VALIDATE → HUMAN
         (code)     (code)     (model)   (code)    (you)
```

A workflow is a fixed plan, written by you. The model fills one step.

Use it for anything repeatable: screens, reconciliations, reports.

---

# Three design rules

1. **Code does math. The model does judgment.**
2. **Validate at the boundary.** Schema forced. Numbers audited.
3. **The human gate is the exit.** Nothing ships without a yes.

Break rule 1 and you get confident arithmetic errors at scale.

---

# SEC EDGAR: free, legal, current

Every filing. Every registrant's financials. No key. No cost.

Not there: market prices, estimates. Filings are fundamentals, not quotes.

Three traps we hit building this course:
tags drift across years · foreign filers report in **local currency** ·
most pharma tags no operating income at all

---

# Demo: market intelligence, five steps

NVIDIA versus AMD versus Intel. Live.

Watch two things:

The memo's **data gaps** section. A system that says what it does NOT know.

The numeric audit. Every figure in the prose must trace to an input.
I will plant a fake number. The audit flags it.

---

# Your lab: the screening engine

16 industrials and pharma names. Live filings. Your criteria.

- Exercise 1: fetch three years of fundamentals per ticker
- Exercise 2: the filter. **Pandas decides, not Claude.**
- Exercise 3: grounded rationales, then audit the model's own prose

Question you must answer today: why net margin, not operating margin?

---

# Remember

A workflow you can rerun is worth ten analyses you did once.

Next session: the model makes the plan. Agents. With a leash.
