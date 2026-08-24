# Session 5 — AI Agents for Finance

> 🎓 **Work in [`notebooks/05-agents.ipynb`](../notebooks/05-agents.ipynb)** — it contains this session's full teaching and lab. This README is the session brief and reference.

**You leave with:** a functioning mini finance agent, plus your capstone
presentation of "My AI-Native Finance Workflow".

## Workflow vs agent — the distinction that matters

| | Workflow (Session 4) | Agent (today) |
|---|---|---|
| Plan | fixed, written by you | chosen by the model, step by step |
| Tools | called by your code | *requested* by the model, executed by your code |
| Stops when | the script ends | the model judges the goal met (or hits YOUR limits) |
| Failure mode | a step errors loudly | it wanders, loops, or confidently does the wrong thing |
| Use when | the task is known and repeatable | the path varies with what the data says |

An agent is not magic: it is a **loop** — model proposes a tool call, your
code executes it, the result goes back, repeat. Read `run_agent()` in
`demo/mini_analyst_agent.py`; it's ~40 lines and it is the whole idea.

## Governance is in the code, not the slide

Every guardrail in the demo is a line you can point at:

- **max_steps** — no infinite loops
- **TOKEN_BUDGET** — no unbounded spend ("an agent without a budget is an incident report")
- **tools are the only world-interface** — the model never touches EDGAR or disk directly
- **record_recommendation** — forced structured output, exactly once
- **human gate** — nothing written without approval
- **audit trail** — every tool call logged into the memo

## Live demo — Mini Investment Analyst Agent

```bash
python session-05-agents/demo/mini_analyst_agent.py \
  "Analyze Apple (AAPL) and compare it with Sony (SONY)."
```

Watch the trace: the agent plans, pulls both companies, compares — and hits
the trap we set: **Sony files in Japanese yen.** The compare tool
warns; the system prompt forbids cross-currency absolute comparisons; the
recommendation must reason in growth and margins. That's governance working.

No API key? `--preflight` prints the agent's system prompt, tool catalog and
guardrails — the "spec" of the agent.

## Lab (25 min) — your research agent + capstone prep

1. Open `lab/research_agent_starter.py` (the loop is given). Implement the two
   tools, write the system rules, add the human gate (TODOs 1-4).
2. Run it on YOUR company pair (pharma, banking or tech — two SEC filers).
3. Save your memo, commit, and build your 5-minute capstone per
   `capstone/capstone-brief.md`.

## Deliverable checklist

- [ ] Your agent runs end-to-end on your company pair
- [ ] Trace shows ≥3 tool calls and a recorded recommendation
- [ ] You can point to each guardrail in your own code
- [ ] `outputs/agent_memo.md` committed
- [ ] Capstone: 5-minute story ready (working demo + trust story + one number)

## When NOT to use an agent (exam-grade answer)

Reconciliation, report generation, screening, anything repeatable →
**workflow** (cheaper, testable, auditable). Open-ended research with
data-dependent paths → agent, with the guardrails above. If a regulator will
ask "why did it do that?" — you want the workflow's answer, or the agent's
audit trail. Autonomy is a dial, not a switch.
