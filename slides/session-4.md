---
marp: true
paginate: true
theme: default
---

# Session 4 · Workflows on Live SEC Data

Yesterday you pasted data by hand. Today your code fetches it from the SEC.

Plan: idea 15 min · live demo 22 min · your lab 30 min · debrief 8 min.

---

# By 10:15 you can

1. Draw the workflow pattern and defend why code does math while the model
   writes prose.
2. Pull real fundamentals from SEC filings with one function call.
3. Build a screen you can rerun tomorrow, with criteria as dials.
4. Audit the model's own writing: every number traced to an input.

---

# A workflow is a plan the model cannot change

```
INPUT → RETRIEVE → STRUCTURE → REASON → VALIDATE → HUMAN
```

Code retrieves the filings. Code computes the numbers. The model reasons
once, in the middle, about a table it is given. Code then audits what the
model wrote. You approve before anything is saved.

Why this division? Because language models make arithmetic mistakes with
total confidence, and pandas does not. Code does math. The model does
judgment. The human owns the decision.

---

# EDGAR: every filing, free, no key

EDGAR is the SEC's public database. Every annual report, every quarterly,
every company, since the nineties. Your code can read it directly.

What it does not contain: market prices and analyst estimates. Filings are
fundamentals, not quotes.

Three traps you will meet, because companies tag their own accounts:
the same item changes names across years, foreign companies report in their
home currency, and most pharma companies never report an operating income
line at all. Real data has footnotes. Yours will too.

---

# Demo: a market intelligence memo, five steps

NVIDIA against AMD and Intel, live from the filings.

Watch for two moments. The finished memo lists its own data gaps, meaning
what it could not know from the inputs. An analysis that declares its blind
spots is worth ten that sound complete.

Then I sabotage it: one invented number goes into the memo, and the audit
step traces every figure back to the inputs and flags the intruder.

---

# Your lab · notebook 04 · 30 minutes

You build a screening engine over sixteen real industrial and pharma
companies, live from EDGAR.

Exercise 1: fetch three years of fundamentals per company, and survive the
companies that fail.
Exercise 2: the filter. Pandas decides who passes, never the model.
Exercise 3: the model writes one short rationale per survivor, and your
audit checks every number in its prose.

One question to answer before the debrief: why did we screen on net margin
instead of operating margin? Exercise 1 will show you.

---

# Remember this one

A screen you can rerun tomorrow is worth ten analyses you did once.

At 10:30 the model starts making its own plan. We hold the leash.
