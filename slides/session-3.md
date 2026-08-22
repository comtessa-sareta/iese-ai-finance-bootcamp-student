---
marp: true
paginate: true
theme: default
---

# Session 3 · Debugging, Testing and Earnings

**A model that crashes is annoying. A model that lies is expensive.**

Plan: idea 12' · live demo 22' · your lab 30' · debrief 8'

---

# By 13:15 you can

1. **Read** a traceback and make Claude diagnose before it fixes
2. **Write** a financial rule as a test, including one checkable on a napkin
3. **Build** a DCF that survives its own test suite: 75.61
4. **Catch** a fabricated quote automatically, with code you wrote

---

# Two kinds of bugs

| | **The crash** | **The lie** |
|---|---|---|
| Announces itself | Yes, with a traceback | No. Returns a number. |
| Danger | Low: you must fix it | High: it can reach a client |
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

# Your lab · notebook 03 · 30 minutes

- **Exercises 1 to 4**: build the four DCF functions, a test under each
- **Finish line A**: the final cell says **75.61**
- **Exercise 5**: build the quote checker
- **Finish line B**: the engine flags **exactly one** fabricated quote

---

# Remember this one

**Green tests AND a plausible number. You need both. Always.**

Tomorrow, 9:00: your code pulls live SEC filings by itself.
