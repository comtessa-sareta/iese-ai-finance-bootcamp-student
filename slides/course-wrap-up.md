---
marp: true
paginate: true
theme: default
---

# Course wrap-up · AI-Augmented Productivity for Finance

**Two days, five sessions, one tool on your GitHub — and the habits that
make an AI output trustworthy.**

---

# The storyline of the course

```
 1 · grounded prompts           the model answers only from evidence you supply
 2 · valuation vs peers         Apple valued against 7 peers, live from EDGAR
 3 · debugging & verification   the valuation repaired; every quote verified
 4 · the screening workflow     16 companies in, a justified shortlist out
 5 · the governed agent         the model plans its steps, inside limits you wrote
```

Each session produced a working artifact; together they are one tool.

---

# The division of labor that carried every session

- **Code does the math** — pandas and numpy are deterministic; the model is not
- **The model does judgment, in words** — grounded in the data you supply,
  nothing else
- **Code checks the words** — schemas, sanity tests, evidence verification,
  numeric audits
- **A human signs** — the gate before anything is saved, sent or published

---

# What makes an AI output trustworthy

- **Grounding**: the model saw only your data, so every claim traces to a source
- **Validation at the boundary**: typed contracts — malformed output cannot pass
- **Measured quality**: a forecast ships with its holdout error; a quote with
  its evidence
- **Limits in code**: steps, budgets, tool whitelists, audit trails — autonomy
  granted like a mandate

---

# The toolbox you met

| Tool | What it does | Sessions |
|---|---|---|
| Claude API | drafts, explains, reasons — inside your rules | all |
| pandas · numpy | deterministic math: screens, valuations, forecasts | 2–4 |
| SEC EDGAR | primary-source fundamentals, free | 2–5 |
| Pydantic | typed contracts at the model boundary | 3–5 |
| LangGraph | workflows and agents as explicit graphs | 4–5 |
| PydanticAI | the governed agent loop, packaged | 5 |
| Skills (`SKILL.md`) | procedures the agent loads on demand | 5 |
| git · GitHub | your work, versioned and public | 2–5 |

---

# Your capstone submission

- **What**: your repository URL + a one-page memo inside the repository
- **The memo**: the job · a real run on your own pair · the trust story ·
  one honest number · the next step
- **Grading**: the trust story carries the most weight — a documented, caught
  failure is stronger evidence than an unexamined success
- **How**: post your repository URL in the class chat at the end of this session

Brief and rubric: `session-05-agents/capstone/capstone-brief.md`
