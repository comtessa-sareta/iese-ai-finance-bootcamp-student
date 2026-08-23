---
marp: true
paginate: true
theme: default
---

# Session 3 · The Growth Rate Hidden in Apple's Price

**Session 2 measured Apple's premium. Today you state precisely what believing
it requires — with a small valuation model that Claude writes and your tests
verify — and you build the layer that lets you trust an AI-written analysis.**

Plan: concepts 12' · live demo 22' · your lab 30' · debrief 8'

---

# By the end of Session 3 you can

1. **Direct** Claude to build working code, function by function, accepting
   only what the tests confirm
2. **Explain** a discounted cash flow model in one idea, and run it backwards
3. **State** what growth rate a market price assumes, and how the answer
   moves with the assumptions
4. **Catch** a fabricated quote in an AI-written analysis, with code you wrote

---

# What we are doing, and why

- **Yesterday ended with a measured premium and an open question**: the
  market prices Apple near the top of its peer group — is that justified?
- **We do not forecast anything.** We take one real number — Apple's current
  free cash flow — imagine it growing at a rate `g`, convert the future cash
  into today's money, and **find the `g` that makes the total equal today's
  price**. That `g` is **the implied growth**: the story you must believe to
  pay the price.
- **Claude writes the model; your tests decide.** Each check has an answer
  known in advance — one is computable by hand — so acceptance rests on
  verification, not on confidence. This is **the contract**.
- **Then the second trust problem**: an AI can read an earnings call and
  write the analysis — so your code checks every quoted claim against the
  source. This is **the trust layer**.

---

# The storyline of this session

```
 Apple's real free cash flow     fetched live from its SEC filing
        ↓
 two small functions             Lab 1 · Claude writes, your tests decide
        ↓
 the model, run backwards        what growth does the price assume?
        ↓
 the verdict                     a precise, judgeable claim about the future
        ↓
 an earnings-call transcript     loaded visibly; real ones come from
                                 investor-relations pages, not EDGAR
        ↓
 every quote machine-checked     Lab 2 · the fabrication detector
```

---

# The discounted cash flow model, in one idea

**Money later is worth less than money now.**

```
value today  =   cash year 1        cash year 2               cash year N + beyond
                ─────────────  +  ──────────────  +  ...  +  ─────────────────────
                  (1 + r)¹          (1 + r)²                      (1 + r)ᴺ
```

- `r` is the **required return**: the yearly return an investor demands for
  holding a risky stock — an assumption, stated and varied openly
- Forwards: assume a growth rate, get a value. **Backwards: take the price,
  solve for the growth it assumes** — nothing is predicted; the price is
  *translated* into its assumption

---

# When the code breaks: the debugging protocol

| | **The crash** | **The wrong number** |
|---|---|---|
| Announces itself | Yes, with a traceback | No: it returns a plausible figure |
| Defense | read the traceback bottom-up | a check whose answer is known in advance |

- **Diagnose before fixing**: make Claude explain the cause first, then
  change one thing at a time
- One check in this lab is **exact by hand**: two flat flows of 100 at a 10%
  return are worth precisely 1000.00 — if the code disagrees, the code is wrong

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
| `pytest`-style checks | your acceptance tests for AI-written code | the standard verification practice |
| `pydantic` | declares and validates output schemas | the industry standard for validation |
| `anthropic` | schema-forced calls to Claude | the official Claude SDK |

---

# How the labs work

Every exercise sits between two markers. **You fill the gaps. Nothing else changes.**

```python
### START CODE HERE ###
value_today = value_today + flow / (1 + r) ** None   # compounded how many times?
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

- **The opening cell** fetches Apple's real cash flows live from its filing
- **Exercises 1–2**: Claude writes the two DCF functions; your checks decide
- **The payoff cell**: the growth rate hidden in the price, at three
  different required returns — then last year's actual, for contrast
- **Lab 2 · Exercise 3**: build `verify_evidence`, the fabrication detector
- **Milestone**: the engine flags **exactly one** planted fabricated quote

---

# Key takeaway

**A market price is a growth assumption in disguise. A small model makes the
assumption visible; whether it is plausible remains the analyst's judgment.**

Next session: the by-hand steps of these two days become one automated
workflow over live filings from the U.S. Securities and Exchange Commission.
