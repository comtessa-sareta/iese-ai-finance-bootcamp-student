---
marp: true
paginate: true
theme: default
---

# Session 5 · Agents, Governance, and Your Capstone

**So far you wrote the plan. Now the model plans. We hold the leash.**

Agenda: idea (10') · demo (18') · your lab (22') · capstones (20') · close (5')

---

# Workflow versus agent

| | Workflow (yesterday) | Agent (today) |
|---|---|---|
| Plan | fixed, yours | chosen by the model |
| Tools | your code calls them | the model requests, your code executes |
| Stops | script ends | model decides. Or hits YOUR limits. |

Autonomy is a dial. Not a switch.

---

# An agent is a loop. Really.

```python
while steps < MAX_STEPS:
    response = claude(messages, tools=TOOLS)
    if response.wants_tool:
        result = run_tool(...)        # your code
        messages += [response, result]
    else:
        break
```

Forty lines. Read them once. Own the concept forever.

---

# Governance lives in the code

- `MAX_STEPS`: no infinite loops
- `TOKEN_BUDGET`: an agent without a budget is an incident report
- Tool whitelist: the model never touches data or disk directly
- Forced structured output: one recommendation, machine readable
- Human gate: nothing saved without your yes
- Audit trail: every tool call, logged

When compliance asks "why did it do that", this list is the answer.

---

# Demo: the trap

Task: compare Novo Nordisk and Eli Lilly.

Novo files in **Danish kroner**. A naive agent says Novo is 5x bigger.

Ours is forbidden from comparing across currencies.
Watch the warning fire, and the agent adapt.

---

# Your lab, then your stage

Lab (22'): build the currency tool and the agent's rules. Run it on YOUR
company pair. Pass the human gate.

Capstone (5 minutes, hard stop):
the job · the live run · **the trust story** · one number · next step

The trust story wins: one failure you caught, and the check that caught it.

---

# When NOT to use an agent

Repeatable task? Workflow. Cheaper, testable, auditable.

Open-ended research, path depends on the data? Agent. With the leash.

If a regulator will ask why, you want the workflow's answer
or the agent's audit trail.

---

# You leave with

Prompts that refuse · a comps tool · a tested DCF · an earnings engine
with a lie detector · a live SEC screener · **an agent with a leash**

One challenge for next week: pick one recurring task at work.
Make it a workflow. Show a colleague.

## Never ship a number you haven't verified.
