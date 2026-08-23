---
marp: true
paginate: true
theme: default
---

# Session 2 · Claude Code as Your Coding Copilot

**Objective: build and publish your first finance tool to GitHub within this session.**

Plan: concepts 15' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 2 you can

1. **Drive** Claude Code professionally: one function at a time, reviewed
2. **Clean** a messy financial dataset with every fix visible
3. **Compute** growth, margins and the three multiples in pandas
4. **Simulate** a valuation range per company with Monte Carlo sampling
5. **Verify** a multiple by hand, then publish to your own GitHub

---

# You are the analyst in charge: four habits

- **Ask small**: request one function at a time, so every change is reviewable
- **Read before you run**: accept only changes you can explain
- **Verify one number by hand**: for every table, confirm one cell on a calculator
- **Commit at every green moment**: small commits make each step reversible

---

# Pandas in one schema

```
DataFrame  =  your spreadsheet, driven by commands

df["ev_m"] / df["ebitda_m"]   →   the multiple for ALL companies at once
```

- **Operations apply to entire columns at once**, which is why the lab
  needs no loops
- **No one is expected to memorize pandas**: you specify, the panel writes,
  you verify

---

# Why we clean data explicitly

Today's file: **10 real companies** from real SEC filings + **8 planted defects**

- Text where numbers should be
- A duplicate row, missing values, a junk TOTAL row
- **The dangerous defect**: a single company reported in **billions**

```
missed unit trap  →  every ratio off by 1000x  →  no error raised
```

Every cleaning step we write prints what it changed, so no correction
happens silently.

---

# The vocabulary of comps

**Comparable-company analysis ("comps")** values a company *relative to its
peers*: what do their prices imply this one is worth? (Session 3 builds the
other pillar, *intrinsic* valuation: what the company's own cash flows imply.)

A **multiple** divides what you pay by what you get:

| Term | Formula | What it measures |
|---|---|---|
| **EBITDA** — earnings before interest, taxes, depreciation & amortization | operating income + D&A | what the operations earn, before financing and accounting choices |
| **Market capitalization** | shares × share price | the price of the equity alone |
| **Enterprise value (EV)** | market cap + debt − cash | the price of the whole business, debt included |
| **EV/EBITDA** | enterprise value ÷ EBITDA | the standard multiple: whole business over what it earns |
| **Price-to-earnings (P/E)** | market cap ÷ net income | the equity per unit of net profit |

When earnings are **negative**, a multiple has no meaning: professionals
write **n.m.** (not meaningful), never a negative multiple.

---

# Pricing a company with comps

The chain from a peer multiple to a share price:

```
1. peer EV/EBITDA multiple × company's EBITDA   =  implied enterprise value
2. implied EV − debt + cash                     =  implied equity value
3. implied equity value ÷ shares                =  implied share price
```

- **Each multiple prices its own denominator**: EV/EBITDA × EBITDA;
  EV/Sales × revenue (the fallback when EBITDA is negative)
- **Deterministic version**: one multiple, the peer *median* → one price.
  Today's data: 25.1× × Apple's 144.7bn EBITDA → **$246 implied vs $255 actual**
- **Monte Carlo version (Exercise 4)**: sample *all* peer multiples, 10,000
  times → a **range** of prices around that same answer

---

# The libraries in this session

| Library | Role here | Standing |
|---|---|---|
| `pandas` | tables, cleaning, ratios | **the** industry standard for data work |
| `plotly` | the interactive charts | best in class for interactive visuals |
| `numpy` | Monte Carlo sampling | the numerical foundation of Python |
| `matplotlib` / `seaborn` | static charts | the long-standing defaults |
| `git` + GitHub | version and publish | universal in professional work |

---

# How the labs work

Every exercise sits between two markers. **You fill the gaps. Nothing else changes.**

```python
### START CODE HERE ###
df["revenue_growth_1y"] = df[None] / df[None] - 1
### END CODE HERE ###
```

- **`None`** → replace with the correct column, value or variable
- **`[QUESTION IN CAPITALS]`** → replace with the text the bracket asks for
- **Everything else is given.** Do not rewrite it.
- Then run the **✅ check cell** directly below. Green means correct: continue.

Stuck for two minutes? Select the lines, press `Option+K` (`Alt+K` on Windows),
and ask the ✱ panel.

---

# Your lab · notebook 02 · 30 minutes

- **Exercise 1**: growth and margins
- **Exercise 2**: market cap, EV, the three multiples
- **Exercise 3**: summary table with a MEDIAN row, then an interactive chart
- **Exercise 4**: Monte Carlo — 10,000 sampled peer multiples put a value
  range around every company, next to its actual price
- **Verification**: confirm Apple's EV/EBITDA on a calculator, from the raw file
- **To finish**: publish the tool to your own GitHub repository

---

# Key takeaway

**A comps table gives every company a peer-implied value range. Analysis
begins where the market price and that range disagree.**

Next session: debugging a valuation model with deliberate errors.
