---
marp: true
paginate: true
theme: default
---

# Session 2 · Claude Code as Your Coding Copilot

**One question, answered with code: what is Apple worth? You will compute
what its peers' prices imply, compare that with what the market charges,
and publish the tool that does it.**

Plan: concepts 15' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 2 you can

1. **Drive** Claude Code professionally: one function at a time, reviewed
2. **Compute** what the market charges per unit of earnings, across a peer group
3. **Value** Apple at its peers' multiples, end to end
4. **Simulate** a valuation range per company with Monte Carlo sampling
5. **Publish** the finished tool to your own GitHub

---

# What we are doing, and why

- **The market gives every company a price**, but a price is not a judgment:
  it tells you what buyers pay, not whether they should.
  This is **the market price** — the latest close.
- **We compute an independent estimate of worth** from public SEC filings.
  This is **the implied price**: the peers' EV/EBITDA ratings, applied to
  the company's own earnings.
- **The difference between the two is the product.** It does not say "buy"
  or "sell"; it identifies the question to investigate next.
  This is **the premium** (or discount) — measured, not judged.
- **We build the analysis as a tool, with Claude Code, and publish it.**
  A reproducible analysis can be rerun, audited and extended; and directing
  and reviewing AI-generated code with discipline is a core professional
  capability this course develops.

---

# You are the analyst in charge: three habits

- **Ask small**: request one function at a time, so every change is reviewable
- **Read before you run**: accept only changes you can explain
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


# The storyline of this session

```
 the peers' SEC filings          real companies, latest annual filings
        ↓
 growth and margins              Exercise 1 · know the peer group
        ↓
 the multiples                   Exercise 2 · what the market charges
        ↓
 Apple valued at the median      Part B · the implied price vs the market's
        ↓
 the Monte Carlo range           Exercise 4 · honest uncertainty
        ↓
 your GitHub                     Part C · the tool, published
```

---

# The vocabulary of comparable-company analysis

**Comparable-company analysis** values a company *relative to its peers*:
what do their prices imply this one is worth? (Session 3 builds the other
pillar, *intrinsic* valuation, from the company's own cash flows.)

| Term | Formula | What it measures |
|---|---|---|
| **EBITDA** — earnings before interest, taxes, depreciation & amortization | operating income + D&A | operating earnings, before financing and accounting choices |
| **Market capitalization** | shares × share price | the price of the equity |
| **Enterprise value (EV)** | market cap + debt − cash | the price of the whole business |

---

# The two multiples we use

A **multiple is a rating, not a price** — like pricing flats per square
meter: it becomes a price estimate only when applied to a company's own
earnings. It divides what you pay by what you get:

| Term | Formula | What it measures |
|---|---|---|
| **EV/EBITDA** | enterprise value ÷ EBITDA | the whole business over what it earns |
| **Price-to-earnings (P/E)** | market cap ÷ net income | the equity per unit of net profit |

- **You compute both; the valuation uses EV/EBITDA**, because it compares
  whole businesses before financing choices distort the picture
- **P/E is reported alongside** — it is the multiple the press quotes, and
  it is distorted by debt and one-off items, which is why it does not anchor
  the analysis
- When earnings are **negative**, a multiple has no meaning: professionals
  write **n.m.** (not meaningful), never a negative multiple

---

# Pricing a company with peer multiples

The chain from a peer multiple to a share price:

```
1. peer EV/EBITDA multiple × company's EBITDA   =  implied enterprise value
2. implied EV − debt + cash                     =  implied equity value
3. implied equity value ÷ shares                =  implied share price
```

- **Peers are a choice**: companies whose current earnings are abnormal are
  excluded, and the notebook states why — the choice is part of the analysis
- **The deterministic version** applies one rating, the peer *median*, and
  produces one implied price to set against the market's
- **The Monte Carlo version** applies *every* peer rating and produces a
  range — where the market price sits inside that range is the finding

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

- **Exercise 1**: know the peer group — growth and margins
- **Exercise 2**: the EV bridge and the multiples (Intel must print n.m.)
- **Exercise 3**: the summary table whose **median** anchors the valuation
- **Part B**: read Apple valued end to end, then **Exercise 4**: the
  Monte Carlo range around it
- **To finish**: publish the tool to your own GitHub repository

---

# Key takeaway

**Comparable-company analysis gives every company a peer-implied value range. Analysis
begins where the market price and that range disagree.**

Next session: debugging a valuation model with deliberate errors.
