---
marp: true
paginate: true
theme: default
---

# Session 3 · Debugging, Testing and Earnings

**Two skills that make AI usable on a finance desk: direct Claude to repair
a valuation model under the discipline of tests, and machine-check an
AI-written analysis against its source.**

Plan: concepts 12' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 3 you can

1. **Read** a traceback and have Claude diagnose the cause before it proposes a fix
2. **Direct** Claude to repair a broken valuation, one failing test at a time
3. **Use** tests as the contract that lets you trust AI-written code
4. **Catch** a fabricated quote automatically, with code you wrote

---

# What we are doing, and why

- **Session 2 ended with a measured premium and an open question**: is it
  justified? The tool that answers it is the **discounted cash flow model (DCF)** —
  worth computed from the company's own future cash flows. Today you work on one.
- **Before trusting any model, make it correct.** Tests encode financial
  rules; they are **the contract** that lets you accept AI-written fixes
  without taking anyone's word.
- **Before trusting any AI analysis, verify its evidence.** Every claim must
  carry a quote your own code can find in the source. This is **the trust
  layer**.
- **The skill throughout is direction and review**: Claude writes, the tests
  and checks decide, you judge.

---

# The storyline of this session

```
 a broken DCF model              Part A · run it, read the failure
        ↓
 seven failing tests             the specification of correctness
        ↓
 Claude repairs, you review      Lab 1 · one test at a time
        ↓
 an earnings-call transcript     Part C · the model extracts claims
        ↓
 every quote machine-checked     Lab 2 · the fabrication detector
        ↓
 an evidence-verified memo       the deliverable
```

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
  answer is computable by hand. When the code disagrees with the hand
  computation, the code contains an error.

---

# The broken model you will fix

**Meridian Semiconductor** (fictional). The market prices it at one level;
the broken model concludes it is worth almost twice that.

The six planted errors, all real ones:

1. First year's cash flow **never discounted**
2. **Tax shield forgotten** in the cost of debt
3. Terminal value **taken at face value** (it sits 5 years away)
4. Net debt **added** instead of subtracted
5. **Impossible growth accepted** (g above r means infinite value)
6. Horizon **hardcoded**

**Claude makes every fix; you review every diff.** Corrected, the model
prints the reference value, and the investment discussion can begin.

---

# The earnings engine: every claim verified

```
transcript → model extracts claims → every claim carries a verbatim quote
           → your code checks each quote against the document
           → an unmatched quote is flagged as unverified
```

- **The company is fictional by design**: the model has no memory to lean
  on, only the document
- **One quote in today's data is planted**: your engine is complete when it
  catches it

---

# The libraries in this session

| Library | Role here | Standing |
|---|---|---|
| `pytest` | your financial rules, run as tests | the standard Python test runner |
| `pydantic` | declares and validates output schemas | the industry standard for validation |
| `anthropic` | schema-forced calls to Claude | the official Claude SDK |

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
- **Milestone A**: all 7 tests pass and the model prints the reference value
- **Lab 2**: build `verify_evidence`, the fabrication detector
- **Milestone B**: the engine flags **exactly one** fabricated quote

---

# Key takeaway

**A correct model requires both: green tests and a plausible result.**

Next session: retrieving filings programmatically from the U.S. Securities
and Exchange Commission.
