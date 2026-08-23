---
marp: true
paginate: true
theme: default
---

# Session 5 · Agents, Governance, Your Capstone

**Until now you wrote every plan. Now the model plans its own steps, within limits you define.**

Plan: concepts 10' · demo 18' · lab 22' · capstones 20' · close 5'

---

# By the end of Session 5 you can

1. **Explain** what separates an agent from a workflow, and when each wins
2. **Read** an agent loop and point at every governance lever in the code
3. **Run** a governed agent on your own company pair, and pass its human gate
4. **Present** your AI workflow in five minutes, with a trust story

---

# Workflow vs agent

| | **Workflow** (Session 4) | **Agent** (now) |
|---|---|---|
| The plan | fixed, written by you | **chosen by the model**, step by step |
| Tools | your code calls them | the model requests, **your code executes** |
| Stops when | the script ends | when it decides, or at **the limits you set** |
| Use for | repeatable work | paths that **depend on the data** |

---

# The agent mechanism is a loop

```python
while steps < MAX_STEPS:
    response = claude(messages, tools=TOOLS)
    if response.wants_tool:
        result = run_tool(...)        # YOUR code executes
        messages += [response, result]  # the conversation IS the memory
    else:
        break
```

**About forty lines.** Once you have read them, you can evaluate any
vendor's agent claims from first principles — the notebook then shows the
same discipline in **PydanticAI** and maps every lever to **LangGraph**.

---

# Governance: six levers, all in code

| Lever | Failure it prevents |
|---|---|
| **MAX_STEPS** | the agent looping indefinitely |
| **TOKEN_BUDGET** | unbounded spend |
| **Tool whitelist** | doing anything you gave no tool for |
| **Forced output schema** | an essay instead of a decision |
| **Human gate** | anything saved without your yes |
| **Audit trail** | "why did it do that?" with no answer |

---

# The demonstration: a currency trap

**Task: compare Novo Nordisk with Eli Lilly.**

```
naive agent:  DKK 300bn  vs  USD 65bn  →  "Novo is 5x bigger"        (wrong)
our agent:    tool detects mixed units → warning → compares
              growth and margins only                            (correct)
```

- **Defense in depth**: a rule in the prompt AND a check in the tool
- You build both protections yourself, then run your own pair

---

# The libraries in this session

| Library | Role here | Standing |
|---|---|---|
| `pydantic` | the typed recommendation | the industry standard for validation |
| **PydanticAI** | the agent loop, packaged (live demo) | state-of-the-art agent framework, by the Pydantic team |
| **LangGraph** | graph agents (mapped, not built) | the other leading agent framework |

---

# How the labs work

Every exercise sits between two markers. **You fill the gaps. Nothing else changes.**

```python
### START CODE HERE ###
"3. ALWAYS check the [WHICH FIELD?] field before comparing figures."
### END CODE HERE ###
```

- **`None`** → replace with the correct column, value or variable
- **`[QUESTION IN CAPITALS]`** → replace with the text the bracket asks for
- **Everything else is given.** Do not rewrite it.
- Then run the **✅ check cell** directly below. Green means correct: continue.

Stuck for two minutes? Select the lines, press `Option+K` (`Alt+K` on Windows),
and ask the ✱ panel.

---

# Your lab, then your five minutes

**Lab (22')**: build the currency tool + the agent's rules → run YOUR pair → pass the gate

**Capstone (5', hard stop)**:

1. The **job** your workflow does
2. The **live run**
3. The **trust story**: one failure you caught + the check that caught it
4. One honest **number**
5. The **next step**

**The trust story carries the most weight in grading.** A documented,
caught failure is stronger evidence than an unexamined success.

---

# What you own now

**Grounded prompts · a comparable-company analysis tool · a tested
discounted-cash-flow model · an earnings engine with
fabrication detection · a screener on live regulatory filings · a governed agent**

- **A challenge for the coming week**: choose one recurring task at your
  desk, build it as a workflow, and show a colleague

## Never ship a number you haven't verified.
