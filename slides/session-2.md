---
marp: true
paginate: true
theme: default
---

# Session 2 · Claude Code as Your Coding Copilot

**Today you ship your first finance tool. To GitHub. Before lunch.**

Agenda: idea (15') · live demo (22') · your lab (30') · debrief (8')

---

# The working rhythm. This is the skill.

1. Ask small. One function at a time.
2. Read before you run.
3. **Verify one number by hand. Every table. Forever.**
4. Commit at every green moment.

You are the analyst in charge. Claude is a very fast junior.

---

# Pandas in one slide

A DataFrame is the analyst's table.

Columns are vectors: `df["a"] / df["b"]` divides whole columns at once.

You do not memorize pandas. You specify what you want. Then you verify.

---

# Real data is messy. Ours is real.

Today's file: 10 tech companies, from actual SEC filings, with 8 defects:

ugly headers · numbers stored as text · **one company in billions** ·
a duplicated row · a dirty ticker · missing values · a junk TOTAL row

Question: what happens if we miss the billions one?

---

# The vocabulary of comps

EBITDA = operating income + D&A
Market cap = shares × price
**EV = market cap + debt − cash**

EV/EBITDA, EV/Sales, P/E: what you pay per unit of performance.

Negative earnings? The multiple is meaningless. We write **n.m.**, never a negative.

---

# Demo: pipeline in 20 minutes

Load the messy file. Inspect first. Fix every defect, explicitly.

Watch for the trap: one company reported in billions. Miss it and every
ratio is off by 1000x. Silently.

Intel has negative margins. Good code survives that without special cases.

---

# Your lab · notebook 02 · 30 minutes

- Exercise 1: growth and margins
- Exercise 2: market cap, EV, the three multiples
- Exercise 3: the summary table with a MEDIAN row

Then the rule: **verify Apple's EV/EBITDA on a calculator.** From the raw CSV.

Finish: commit and push to your own GitHub repo. Your first shipped tool.

---

# Remember

Intel shows n.m. on P/E. That is correct behavior, not a bug.

Next session: I hand you a valuation model that is wrong on purpose.
