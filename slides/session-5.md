---
marp: true
paginate: true
theme: default
---

# Session 5 · Agents, Governance, Your Capstone

**So far you wrote every plan. Now the model plans. Under your limits.**

Plan: idea 10' · demo 18' · lab 22' · capstones 20' · close 5'

---

# By the end of Session 5 you can

1. **Explain** what separates an agent from a workflow, and when each wins
2. **Read** an agent loop and point at every governance lever in the code
3. **Run** a governed agent on your own company pair, and pass its human gate
4. **Present** your AI workflow in five minutes, with a trust story

---

# Workflow vs agent

| | **Workflow** (yesterday) | **Agent** (today) |
|---|---|---|
| The plan | fixed, yours | **chosen by the model**, step by step |
| Tools | your code calls them | model requests, **your code executes** |
| Stops when | the script ends | it decides. Or hits **YOUR limits**. |
| Use for | repeatable work | paths that **depend on the data** |

**Autonomy is a dial, not a switch.**

---

# The whole mystery is a loop

```python
while steps < MAX_STEPS:
    response = claude(messages, tools=TOOLS)
    if response.wants_tool:
        result = run_tool(...)        # YOUR code executes
        messages += [response, result]  # the conversation IS the memory
    else:
        break
```

**Forty lines.** Read them once today. No vendor mystifies you again.

---

# Governance: six levers, all in code

| Lever | Failure it prevents |
|---|---|
| **MAX_STEPS** | looping forever |
| **TOKEN_BUDGET** | unbounded spend |
| **Tool whitelist** | doing anything you gave no tool for |
| **Forced output schema** | an essay instead of a decision |
| **Human gate** | anything saved without your yes |
| **Audit trail** | "why did it do that?" with no answer |

---

# The demo contains a trap

**Task: compare Novo Nordisk with Eli Lilly.**

```
naive agent:  DKK 300bn  vs  USD 65bn  →  "Novo is 5x bigger"  ✗
our agent:    tool detects mixed units → warning → compares
              growth and margins only                           ✓
```

- **Defense in depth**: a rule in the prompt AND a check in the tool
- You build both protections yourself, then run your own pair

---

# Your lab, then your five minutes

**Lab (22')**: build the currency tool + the agent's rules → run YOUR pair → pass the gate

**Capstone (5', hard stop)**:

1. The **job** your workflow does
2. The **live run**
3. The **trust story**: one failure you caught + the check that caught it
4. One honest **number**
5. The **next step**

**The trust story decides the grade.** A caught failure beats a suspicious success.

---

# What you own now

**Prompts that refuse · a comps tool · a tested DCF · an earnings engine
with a lie detector · a live SEC screener · an agent with a leash**

- **Challenge for next week**: one recurring task at your desk → make it a
  workflow → show one colleague

## Never ship a number you haven't verified.
