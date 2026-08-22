---
marp: true
paginate: true
theme: default
---

# Session 4 · Workflows on Live SEC Data

**Yesterday you pasted data by hand. Today your code fetches it from the SEC.**

Plan: idea 15' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 4 you can

1. **Draw** the workflow pattern and defend the code-vs-model split
2. **Pull** real fundamentals from SEC filings with one function call
3. **Build** a screen you can rerun tomorrow, criteria as dials
4. **Audit** the model's own prose: every number traced to an input

---

# A workflow is a plan the model cannot change

```
INPUT → RETRIEVE → STRUCTURE → REASON → VALIDATE → HUMAN
         (code)     (code)     (model)   (code)    (you)
```

- **Code does math**: pandas does not hallucinate. Models do, confidently.
- **The model reasons once**, in the middle, about a table it is *given*
- **Code audits the prose**, then a human approves. Nothing ships without a yes.

---

# EDGAR: every filing, free, no key

- **What is there**: every 10-K, 10-Q, 8-K since the nineties, machine readable
- **What is NOT**: market prices, analyst estimates. Filings ≠ quotes.

Three traps you will meet, because **companies tag their own accounts**:

1. The same item **changes names** across years
2. Foreign filers report in **local currency**
3. Most pharma reports **no operating income line at all**

---

# Demo: a memo with two special moments

**NVIDIA vs AMD vs Intel, live from the filings.**

- **Moment 1, data gaps**: the memo lists what it could *not* know
  from the inputs. Blind spots, declared.
- **Moment 2, the sabotage**: I plant one fake number in the memo

```
audit: every figure in the prose  →  traced to inputs  →  intruder flagged ⚠️
```

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

- **Exercise 1**: fetch 3 years of fundamentals, survive failing tickers
- **Exercise 2**: the filter. **Pandas decides who passes. Never the model.**
- **Exercise 3**: one grounded rationale per survivor + numeric audit

**Question to answer before the debrief**: why net margin, not operating margin?

---

# Key takeaway

**A screen you can rerun tomorrow is worth more than ten analyses performed once.**

Next session, 10:30: the model plans its own steps, under controls you define.
