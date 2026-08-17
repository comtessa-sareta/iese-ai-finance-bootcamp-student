---
marp: true
paginate: true
theme: default
---

# Session 5 — AI Agents for Finance

**Deliverable: a working mini finance agent + your capstone.**

---

# Workflow vs agent

| | Workflow | Agent |
|---|---|---|
| Plan | fixed, yours | **chosen by the model**, step by step |
| Tools | called by your code | **requested** by model, executed by your code |
| Stops | script ends | model judges done — or hits **your limits** |
| Failure | a step errors loudly | wanders, loops, or is confidently wrong |

Autonomy is a **dial**, not a switch.

---

# An agent is a loop (really)

```python
while steps < MAX_STEPS:
    response = claude(messages, tools=TOOLS)
    if response.wants_tool:
        result = run_tool(response.tool, response.args)   # your code
        messages += [response, result]                    # memory
    else:
        break
```

`run_agent()` in the demo is ~40 lines. Read it once; own the concept forever.

---

# Governance lives in the code

- `MAX_STEPS` — no infinite loops
- `TOKEN_BUDGET` — *"an agent without a budget is an incident report"*
- **tool whitelist** — the model never touches EDGAR or disk directly
- `record_recommendation` — forced structure, exactly once
- **human gate** — nothing saved without approval
- **audit trail** — every tool call logged into the memo

---

# Live demo — Mini Investment Analyst Agent

*"Analyze Novo Nordisk (NVO) and compare it with Eli Lilly (LLY)."*

Watch the trap: **Novo files in Danish kroner.**
A naive agent: "Novo is 5× bigger." Ours: forbidden from cross-currency
absolutes — compares growth and margins, and says why.

<!-- Also the real story: LLY ~+45% growth vs NVO ~+6% in FY2025. Ask the room what they'd diligence. -->

---

# Memory & autonomy levels — the 90-second tour

- **Short-term memory** = the messages list (dies with the run)
- **Long-term memory** = `save_note` → a file that survives runs
- Levels: assistant (you drive) → workflow (fixed plan) →
  **supervised agent (today)** → autonomous fleets (not today, maybe not ever
  for an IC)

---

# Lab (22 min) — your research agent

`lab/research_agent_starter.py` — loop given, you build:

1. the two tools (financials, compare-with-currency-warning)
2. the system rules (currency! grounding! exactly-once recommendation!)
3. the human gate

Run it on **your** pair (pharma / banking / tech — two SEC filers).

---

# Capstone — 5 minutes, hard stop

1. The **job** (30") · 2. The **run** (2') · 3. The **trust story** (1'30) ·
4. **One number** (30") · 5. **Next step** (30")

The trust story wins the grade: one failure you caught + the check that
caught it + what stays human.

---

# When NOT to use an agent (exam-grade answer)

Repeatable? → **workflow** (cheaper, testable, auditable).
Open-ended, data-dependent path? → agent, **with the leash**.
If a regulator asks *"why did it do that?"* — you want the workflow's answer,
or the agent's audit trail.

---

# You leave with

Prompt playbook · comps tool · broken-DCF discipline · earnings engine ·
EDGAR workflow · screening engine · **a governed agent** · a capstone story

**One challenge for next week:** pick ONE recurring task at work.
Make it a workflow. Show a colleague.

*Never ship a number you haven't verified.*
