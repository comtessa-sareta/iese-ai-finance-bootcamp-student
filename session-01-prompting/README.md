# Session 1 — LLM Systems, Prompt Engineering & Financial Reasoning

> 🎓 **Work in [`notebooks/01-prompting.ipynb`](../notebooks/01-prompting.ipynb)** — it contains this session's full teaching and lab. This README is the session brief and reference.

**You leave with:** a personal *Finance Prompt Playbook* — reusable, validated
prompt templates you'll use all week and after the course.

## The mental model (what the demo shows)

1. **LLMs predict, then reason.** They produce the most plausible continuation;
   with structure and context, plausible becomes reliable. Without them, it
   becomes confident fiction.
2. **The context window is your desk.** The model reasons well over what you
   put on the desk (filings, tables, transcripts) and hallucinates about what
   you left in the drawer.
3. **Structure is control.** Role → task → context → output schema →
   validation. Every professional prompt in this course has those five parts.
4. **Trust is a workflow, not a feeling.** You'll learn to force JSON/tables,
   demand verbatim evidence, and check outputs — by hand today, in code
   tomorrow (Session 3 automates it).

## Live demo — Equity Research Assistant

The instructor builds one prompt in four versions, live, on the
NVIDIA / AMD / Intel case (real figures: `data/semis_fact_sheet.md`):

| Version | Change | What you'll observe |
|---|---|---|
| v1 | naive ask (raw API — a clean room: no search, no context) | fluent and confident; numbers from memory, unverifiable, fiscal years unlabeled |
| v2 | + role & task decomposition | sharper, still unverifiable |
| v3 | + context injection (fact sheet) + "NOT IN CONTEXT" rule | grounded, gaps admitted |
| v4 | + fixed JSON schema + self-check | reusable machine-readable output |

## Lab (30 min) — write your three production prompts

Work in pairs. For each template in `playbook/`:

1. Start from the template structure (role / task / context slots / schema /
   validation checklist).
2. Run it on the case companies in Claude.
3. **Attack your own prompt**: pick two exercises from
   `red-team-exercises.md` and run them against it.
4. Record what broke and the fix in the template's *Failure modes* section.

Checkpoint at +15 min: swap prompts with another pair; break theirs.

## Deliverable checklist

- [ ] `playbook/company-deep-dive.md` — completed and tested on one company
- [ ] `playbook/earnings-call-summary.md` — completed (you'll wire it into code in Session 3)
- [ ] `playbook/competitive-landscape.md` — completed and tested on the semis trio
- [ ] Each template has ≥2 documented failure modes with mitigations
- [ ] You made the model say "NOT IN CONTEXT" at least once — on purpose

## Files

- `playbook/` — the four template files (one blank pattern + three finance prompts)
- `red-team-exercises.md` — five attacks to run on your own prompts
- `data/semis_fact_sheet.md` — real NVIDIA/AMD/Intel figures from SEC filings (context injection material)
