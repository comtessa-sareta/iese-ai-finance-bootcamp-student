---
marp: true
paginate: true
theme: default
---

# Session 3 · Debugging, Testing and Earnings

**An error that stops execution is visible. An error that returns a wrong number is costly.**

Plan: concepts 12' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 3 you can

1. **Read** a traceback and have Claude diagnose the cause before it proposes a fix
2. **Direct** Claude to repair a broken valuation, one failing test at a time
3. **Use** tests as the contract that lets you trust AI-written code
4. **Catch** a fabricated quote automatically, with code you wrote

---

# Two kinds of bugs

| | **The crash** | **The wrong number** |
|---|---|---|
| Announces itself | Yes, with a traceback | No: it returns a plausible figure |
| Risk | Low, because it forces a fix | High, because it can reach a client |
| Today | Fix in 2 minutes | The rest of the session |

**Protocol**: read bottom up → diagnose before fixing → one change at a time

---

# A test is finance, written as a rule

```python
def test_equity_value_subtracts_net_debt():
    """Debt holders get paid first."""
```

- **One test encodes one financial rule**, checked automatically on every change
- **The hand-check**: choose flat cash flows and round rates, so the correct
  answer is computable by hand. If the model disagrees with the algebra,
  **the model is wrong.**

---

# The broken model you will fix

**Meridian Semiconductor** (fictional) · trades at **$62** · the broken model
says over **$115**

The six planted errors, all real ones:

1. First year's cash flow **never discounted**
2. **Tax shield forgotten** in the cost of debt
3. Terminal value **taken at face value** (it sits 5 years away)
4. Net debt **added** instead of subtracted
5. **Impossible growth accepted** (g above r means infinite value)
6. Horizon **hardcoded**

**Claude makes every fix; you review every diff.** Corrected, the model gives
**$75.61**, and the investment discussion can begin.

---

# Part 2: an engine that demands evidence

```
transcript → model extracts claims → EVERY claim carries a verbatim quote
           → YOUR code checks each quote against the document
           → quote not found = FABRICATION, flagged ⚠️
```

- **The company is fictional by design**: the model has no memory to lean
  on, only the document
- **One quote in today's data is planted**: your engine is complete when it
  catches it

---

# How the labs work

Every exercise sits between two markers. **You fill the gaps. Nothing else changes.**

```python
### START CODE HERE ###
item["verified"] = bool(quote) and None in haystack   # the NORMALIZED quote
### END CODE HERE ###
```

- **`None`** → replace with the correct column, value or variable
- **`[QUESTION IN CAPITALS]`** → replace with the text the bracket asks for
- **Everything else is given.** Do not rewrite it.
- Then run the **✅ check cell** directly below. Green means correct: continue.

Stuck for two minutes? Select the lines, press `Option+K` (`Alt+K` on Windows),
and ask the ✱ panel.

---

# Your lab · notebook 03 · 30 minutes

- **Lab 1**: direct the ✱ panel to repair `broken_dcf.py`, one failing test
  at a time, reading every diff before accepting
- **Milestone A**: all 7 tests pass; Meridian is valued at **$75.61 per share**
- **Lab 2**: build `verify_evidence`, the fabrication detector
- **Milestone B**: the engine flags **exactly one** fabricated quote

---

# Key takeaway

**A correct model requires both: green tests and a plausible result.**

Next session: retrieving live SEC filings programmatically.
