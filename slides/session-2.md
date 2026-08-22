---
marp: true
paginate: true
theme: default
---

# Session 2 · Claude Code as Your Coding Copilot

**Goal: ship your first finance tool to GitHub. Before lunch.**

Plan: idea 15' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 2 you can

1. **Drive** Claude Code professionally: one function at a time, reviewed
2. **Clean** a messy financial dataset with every fix visible
3. **Compute** growth, margins and the three multiples in pandas
4. **Verify** a multiple by hand, then **ship** to your own GitHub

---

# You are the analyst in charge. Four habits.

- **Ask small**: one function per request → a diff you can actually review
- **Read before you run**: code you cannot explain is code you cannot defend
- **Verify one number by hand**: one cell per table, calculator, forever
- **Commit at every green moment**: each commit is an undo button

Claude is a very fast junior. Speed is its job. **Judgment is yours.**

---

# Pandas in one schema

```
DataFrame  =  your spreadsheet, driven by commands

df["ev_m"] / df["ebitda_m"]   →   the multiple for ALL companies at once
```

- **Columns operate on whole columns**: that is why the lab has no loops
- **Nobody memorizes pandas**: you specify, the panel writes, you verify

---

# Why we clean data explicitly

Today's file: **10 real companies** from real SEC filings + **8 planted defects**

- Text where numbers should be · duplicate row · missing values · junk TOTAL row
- **The dangerous one**: a single company reported in **billions**

```
missed unit trap  →  every ratio off by 1000x  →  NO error raised
```

**Silence is the enemy**: every cleaning step we write prints what it did.

---

# The vocabulary of comps

```
EBITDA  =  operating income + D&A
Mkt cap =  shares × price
EV      =  market cap + debt − cash        (the whole business, not just shares)
```

- **EV/EBITDA, EV/Sales, P/E**: price per unit of performance
- **Negative earnings** → the multiple is meaningless → write **n.m.**
- A negative P/E in a table marks you as an amateur

---

# Your lab · notebook 02 · 30 minutes

- **Exercise 1**: growth and margins
- **Exercise 2**: market cap, EV, the three multiples
- **Exercise 3**: summary table with a MEDIAN row
- **Then the habit**: verify Apple's EV/EBITDA on a calculator, from the raw file
- **Finish**: push to your own GitHub. First shipped project.

---

# Remember this one

**Intel shows n.m. today. That is your code being right.**

Next, 12:00: a valuation model that is wrong on purpose.
