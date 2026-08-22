---
marp: true
paginate: true
theme: default
---

# Session 5 · Agents, Governance, Your Capstone

So far you wrote every plan. Now the model plans for itself. Under limits
you set.

Plan: idea 10 min · demo 18 min · lab 22 min · capstones 20 min · close 5.

---

# By 11:45 you can

1. Explain precisely what separates an agent from a workflow, and when each
   is the right tool.
2. Read an agent loop and point at every governance lever in the code.
3. Run a governed agent on a company pair you chose, and pass its human gate.
4. Present your own AI workflow in five minutes, with a trust story.

---

# What makes an agent different

In a workflow, you fix the steps and the model fills one of them. In an
agent, you give a goal and a set of tools, and the model decides which tool
to use next, looks at the result, and decides again.

That freedom is useful when the path depends on what the data says. It is
also exactly what must be governed, because an agent can wander, loop, or
be confidently wrong at scale. Autonomy is a dial you set, not a switch.

---

# The whole mystery is a loop

```python
while steps < MAX_STEPS:
    response = claude(messages, tools=TOOLS)
    if response.wants_tool:
        result = run_tool(...)        # your code executes
        messages += [response, result]
    else:
        break
```

The model proposes. Your code disposes. The conversation is the memory.
Forty lines. Read them once today and no vendor will ever mystify you
again.

---

# Governance is code you can point at

A step limit, so it cannot loop forever. A token budget, because an agent
without a budget is an incident report. A tool whitelist, so the model
never touches data or disk directly. A forced final format, so the
recommendation is machine readable. A human gate, so nothing is saved
without your yes. An audit trail of every tool call.

When compliance asks why the agent did something, this list is the answer.

---

# The demo contains a trap

The task: compare Novo Nordisk with Eli Lilly.

Novo Nordisk reports in Danish kroner. A naive agent compares 300 billion
kroner with 65 billion dollars and concludes Novo is five times bigger.

Our compare tool refuses to mix currencies, and the agent's rules force it
to compare growth and margins instead. You will build both protections
yourself, then run your agent on a company pair you choose.

---

# Your lab, then your five minutes

Lab: build the currency tool and the agent's rules, run your agent on your
own pair, pass the human gate.

Capstone, five minutes, hard stop: the job your workflow does, the live
run, the trust story, one honest number, the next step.

The trust story decides the grade: one failure you caught, and the check
that caught it. A caught failure beats a suspicious success.

---

# What you own now

Prompts that refuse to guess. A comps tool on your GitHub. A DCF with
tests. An earnings engine with a lie detector. A live SEC screener. An
agent with a leash.

One challenge for next week: pick one recurring task at your desk and turn
it into a workflow. Show one colleague.

## Never ship a number you haven't verified.
