---
marp: true
paginate: true
theme: default
---

# Session 3 · Debugging, Testing and Earnings

**A model that crashes is annoying. A model that lies is expensive.**

Agenda: idea (12') · demo (22') · your lab (30') · debrief (8')

---

# The debugging protocol

1. Read the traceback bottom up. Last line says what. Marked line says where.
2. Diagnose before you fix. Make Claude explain the cause first.
3. One change at a time. Re-run after each.

Crashes are the friendly bugs. They announce themselves.

The dangerous ones return a number.

---

# Tests are financial logic, written down

```python
def test_equity_value_subtracts_net_debt():
    """Debt holders get paid first."""
```

Each test states one piece of finance the code must respect.

The best one: a case simple enough for a napkin. If your model cannot
reproduce a hand calculation, you have a rumor, not a model.

---

# Demo: the broken DCF

Meridian Semiconductor. Fictional. Trades at $62.

The model I give you crashes. After the crash fix, it says $115+.

Would you sign that memo?

Then: tests. Six failures. Each names a finance error. We fix by test.

---

# The six errors, in finance words

- First year cash flow not discounted
- WACC forgot the tax shield
- Terminal value taken at face value. It sits 5 years away.
- Net debt ADDED to enterprise value
- Growth above the discount rate accepted. Infinite value.
- A horizon hardcoded to 5

Correct answer: $75.61. Market: $62. Now the conversation starts.

---

# Part 2: the earnings engine

You get a call transcript. Fictional company. The model cannot rely on memory.

Your engine extracts: sentiment, themes, risks, guidance, red flags.

Every claim must carry a **verbatim quote**. Then YOUR code checks each
quote against the document.

One quote in today's data is fabricated. Your code will catch it.

---

# Your lab · notebook 03 · 30 minutes

- Exercises 1 to 4: build the DCF right. Test below each function.
- Final cell: value Meridian. Expect $75.61.
- Exercise 5: the trust layer. Verify every quote.
- Run the engine: it must flag exactly one fabrication.

---

# Remember

Green tests AND a plausible number. You need both.

Tomorrow: we stop pasting data and start pulling it. Live SEC filings.
