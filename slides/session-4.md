---
marp: true
paginate: true
theme: default
---

# Session 4 — AI Workflows & System Design for Finance

**Deliverable: a screening engine on live SEC data — code filters, model
explains, everything validated.**

---

# The pattern of the day

```
INPUT → RETRIEVE → STRUCTURE → REASON → VALIDATE → HUMAN
         (code)     (code)     (model)    (code)    (you)
```

**Workflow** = a fixed plan written by you; the model fills designated steps.

Use for anything **repeatable**: screens, reconciliations, report drafts,
monitoring.

---

# Three design rules

1. **Code does math; the model does judgment**
   (growth rates in pandas; prose about them from Claude)
2. **Validate at the boundary**
   schema-forced output + numeric audit: every figure must trace to an input
3. **The human gate is the exit**
   nothing saved or sent without approval

---

# Tool calling = schemas with teeth

- Yesterday you *asked* for JSON and repaired failures
- Today the API **forces** it: define a tool whose input schema IS your output
  schema → the model must comply
- `toolkit/llm.py: ask_structured()` — you already used it without knowing

---

# SEC EDGAR — free, legal, current

**There:** every filing (10-K, 10-Q, 8-K, 20-F…), XBRL fundamentals for every
registrant, filing full text · **Not there:** market prices, estimates

Gotchas we hit building this course:
- **tag drift** (NVIDIA changed revenue tags; AMD's last standard D&A tag: 2019)
- **IFRS filers** report in local currency (Novo Nordisk → DKK)
- most pharma tags **no operating income** (no subtotal presented!)

---

# Live demo — Market Intelligence Workflow

```bash
python session-04-workflows/demo/market_intel_workflow.py NVDA --peers AMD INTC
```

Watch for: the **data_gaps** section (a system that says what it doesn't
know)… and the sabotage test — we plant a fake number, the validator flags it.

---

# Lab (30 min) — Company Screening Engine

16 industrials & pharma names, live EDGAR:

1. `fetch_metrics()` — defensive retrieval (one bad ticker ≠ dead screen)
2. `apply_screen()` — **pandas decides**: growth ≥ X, net margin ≥ Y, improving
3. `write_rationales()` — one schema-forced call, then **numeric audit**

Then move the criteria and watch the shortlist move.

---

# Question you must be able to answer after the lab

**Why did we screen on NET margin instead of operating margin?**

(Hint: try `OperatingIncomeLoss` on the pharma names. Data coverage is an
analytical decision — make it in the open.)

---

# Reflection

1. Could you swap the model out and keep the system? (Good architecture: yes)
2. What's missing before a real IC sees this screen?
3. Schema vs numeric audit — what does each protect against?

**Next (10:30):** the model makes the plan. Agents — with a leash.
