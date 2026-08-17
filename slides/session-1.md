---
marp: true
paginate: true
theme: default
---

<!-- Render: npx @marp-team/marp-cli slides/session-1.md -o slides/session-1.pdf
     Or teach straight from this file — the demos are the real slides. -->

# AI-Augmented Productivity for Finance
## Session 1 — LLM Systems, Prompt Engineering & Financial Reasoning

IESE MiF 2027 · Prof. Sara Bisbe

**Never ship a number you haven't verified.**

---

# The next two days

| | You build | You leave with |
|---|---|---|
| S1 | the **brain** | Finance Prompt Playbook |
| S2 | the **hands** | Comps tool on GitHub |
| S3 | the **discipline** | Earnings engine + tests |
| S4 | the **assembly line** | SEC/EDGAR workflows |
| S5 | the **analyst** | Mini finance agent + capstone |

One cumulative asset: **Your AI Financial Analyst** — a portfolio, not notes.

---

# What an LLM actually does

- Predicts the most plausible continuation — **fluent first, true second**
- Reasoning emerges when you give it **structure and material**
- The context window is **your desk**: it reasons well over what's ON the desk…
- …and **hallucinates** about what you left in the drawer

<!-- Say: "It has read everything and remembers approximately. You would fire an analyst who worked from memory. So we won't let it." -->

---

# Where LLMs are strong / weak — in finance

**Strong:** summarization, structuring, drafting, extraction, transformation,
tireless first drafts

**Weak / dangerous:**
- fabricated figures & citations (confident fiction)
- arithmetic — especially period counts (CAGR off-by-one)
- false balance & sycophancy (completes YOUR framing)
- injected instructions hiding in documents

---

# The 5-part production prompt

1. **ROLE** — who is writing, for whom
2. **TASK** — decomposed steps: extract → organize → assess
3. **CONTEXT** — the material, inside delimiters
4. **SCHEMA** — fixed output shape (JSON/table)
5. **VALIDATION** — rules + your checklist afterwards

> Missing one ⇒ improvisation, not production.

---

# The two rules that buy the most safety

```
Use ONLY the material inside <context>.
If something needed is not there, write: NOT IN CONTEXT.
```

```
Every number must be copied or derived from the context —
show the derivation.
```

<!-- "NOT IN CONTEXT is the most valuable output an AI can give you." -->

---

# Live demo — Equity Research Assistant

v1 naive → v2 role+task → v3 **context+refusal** → v4 **schema+self-check**

Case: NVIDIA / AMD / Intel (real filings data)

<!-- Demo now. Fact sheet: session-01-prompting/data/semis_fact_sheet.md -->

---

# AI risk, the 60-second version

- **Hallucination** → grounding rules + verification (this course, everywhere)
- **Prompt injection** → documents are DATA, not instructions (lab exercise 5)
- **Data leakage** → what you paste may be retained; no MNPI, no client data,
  know your firm's policy
- **Accountability** → the model is never the signer. You are.

---

# Lab (30 min) — your Finance Prompt Playbook

1. Complete the 3 templates in `session-01-prompting/playbook/`
2. Test each on the case companies
3. **Attack your own prompts** — 2+ exercises from `red-team-exercises.md`
4. Write every failure you find into the template's failure-mode table

Checkpoint at +15': swap prompts with another pair. Break theirs.

---

# Reflection

1. When did the model sound **most confident while wrong**?
2. Which rule bought the most reliability per word?
3. Playbook vs chatting — what's the difference?

**Next (10:30):** your playbook becomes **code**. Same rigor, new superpower.
