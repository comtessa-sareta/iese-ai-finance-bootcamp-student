---
marp: true
paginate: true
theme: default
---

# Session 4 · Workflows on Live SEC Data

**Yesterday you pasted data by hand. Today your code fetches it from the
U.S. Securities and Exchange Commission (SEC).**

Plan: concepts 15' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 4 you can

1. **Draw** the workflow pattern and defend the code-vs-model split
2. **Pull** real fundamentals from SEC filings with one function call
3. **Build** a screen you can rerun tomorrow, criteria as dials
4. **Audit** the model's own prose: every number traced to an input
5. **Train** a forecasting model and measure its error before trusting it

---

# A workflow is a plan the model cannot change

```
INPUT → RETRIEVE → STRUCTURE → REASON → VALIDATE → HUMAN
         (code)     (code)     (model)   (code)    (you)
```

- **Code does the arithmetic**: pandas is deterministic; the model is not
- **The model reasons once**, in the middle, about a table it is *given*
- **Code audits the prose**, and a human approves: nothing is published
  without explicit sign-off

---

# EDGAR: every filing, free, no key

- **EDGAR** (Electronic Data Gathering, Analysis and Retrieval) is the U.S.
  Securities and Exchange Commission's public filing database
- **What it contains**: every 10-K, 10-Q and 8-K since the nineties,
  machine readable
- **What it does not contain**: market prices and analyst estimates —
  filings are not market data

Three traps you will meet, because **companies tag their own accounts**:

1. The same item **changes names** across years
2. Foreign filers report in **local currency**
3. Most pharma reports **no operating income line at all**

---

# Demo: a memo with two moments to watch

**NVIDIA vs AMD vs Intel, live from the filings.**

- **First, the data gaps**: the memo lists what it could *not* know from
  its inputs — the blind spots are declared, not hidden
- **Second, a planted error**: one figure in the memo is altered by hand,
  and the audit finds it

```
audit: every figure in the prose  →  checked against inputs  →  the altered
                                                                figure is flagged
```

---

# The libraries in this session

| Library | Role here | Standing |
|---|---|---|
| `requests` | fetches SEC filings over HTTP | the standard HTTP library |
| `pandas` | the deterministic screen | the industry standard for data work |
| `numpy` | trains the least-squares forecaster | the numerical foundation of Python |
| `pydantic` | typed, validated model output | the industry standard for validation |

---

# How the labs work

Every exercise sits between two markers. **You fill the gaps. Nothing else changes.**

```python
### START CODE HERE ###
mask = (df[None] >= min_growth) & (df[None] >= min_margin)
### END CODE HERE ###
```

- **`None`** → replace with the correct column, value or variable
- **`[QUESTION IN CAPITALS]`** → replace with the text the bracket asks for
- **Everything else is given.** Do not rewrite it.
- Then run the **✅ check cell** directly below. Green means correct: continue.

Stuck for two minutes? Select the lines, press `Option+K` (`Alt+K` on Windows),
and ask the ✱ panel.

---

# Your lab · notebook 04 · 30 minutes

**A screening engine: 16 real industrials and pharma, live from EDGAR**

- **Exercise 1**: fetch 3 years of fundamentals, tolerating failed tickers
- **Exercise 2**: the filter — **pandas decides which companies pass, never
  the model**
- **Exercise 3**: one grounded rationale per survivor + numeric audit
- **Exercise 4**: train a revenue forecaster; the measured error is the product

**Question to answer before the debrief**: why net margin, not operating margin?

---

# Key takeaway

**A screen you can rerun tomorrow is worth more than ten analyses performed once.**

Next session: the model plans its own steps, under controls you define.
