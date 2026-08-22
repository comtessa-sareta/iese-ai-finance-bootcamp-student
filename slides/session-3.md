---
marp: true
paginate: true
theme: default
---

# Session 3 · Debugging, Testing and Earnings

**An error that stops execution is visible. An error that returns a wrong number is costly.**

Plan: idea 12' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 3 you can

1. **Read** a traceback and make Claude diagnose before it fixes
2. **Write** a financial rule as a test, including one checkable on a napkin
3. **Build** a DCF that survives its own test suite: 75.61
4. **Catch** a fabricated quote automatically, with code you wrote

---

# Two kinds of bugs

| | **The crash** | **The lie** |
|---|---|---|
| Announces itself | Yes, with a traceback | No. Returns a number. |
| Risk | Low: it forces a fix | High: it can reach a client |
| Today | Fix in 2 minutes | The rest of the session |

**Protocol**: read bottom up → diagnose before fixing → one change at a time

---

# A test is finance, written as a rule

```python
def test_equity_value_subtracts_net_debt():
    """Debt holders get paid first."""
```

- **One test = one financial rule**, checked forever, on every change
- **The napkin test**: flat cash flows, round rates → you can compute the
  answer by hand. Model disagrees with algebra? **The model is wrong.**

---

# The broken model you will fix

**Meridian Semiconductor** (fictional) · trades at **$62** · my model says **$115+**

The six planted errors, all real ones:

1. First year's cash flow **never discounted**
2. **Tax shield forgotten** in the cost of debt
3. Terminal value **taken at face value** (it sits 5 years away)
4. Net debt **added** instead of subtracted
5. **Impossible growth accepted** (g above r means infinite value)
6. Horizon **hardcoded**

Fixed correctly: **$75.61**. Now the investment conversation starts.

---

# Part 2: an engine that demands evidence

```
transcript → model extracts claims → EVERY claim carries a verbatim quote
           → YOUR code checks each quote against the document
           → quote not found = FABRICATION, flagged ⚠️
```

- **Company is fictional on purpose**: no memory to lean on, only the document
- **One quote in today's data is planted**: your engine catches it, or it is
  not finished

---

# How the labs work

Every exercise sits between two markers. **You fill the gaps. Nothing else changes.**

```python
### START CODE HERE ###
return equity_weight * None + debt_weight * None * (1 - None)
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

- **Exercises 1 to 4**: build the four DCF functions, a test under each
- **Finish line A**: the final cell says **75.61**
- **Exercise 5**: build the quote checker
- **Finish line B**: the engine flags **exactly one** fabricated quote

---

# Key takeaway

**A correct model requires both: green tests and a plausible result.**

Tomorrow, 9:00: retrieving live SEC filings programmatically.
