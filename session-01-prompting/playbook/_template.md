# Template: [name the analytical task]

> Every production prompt in this playbook has five parts:
> **Role → Task → Context → Output schema → Validation.**
> If one is missing, it's not production — it's improvisation.

## When to use
[One sentence: the finance task this prompt does, and for whom.]

## Inputs required
[What must be pasted into the context slots — filing excerpts, data table,
transcript. Rule: if the model needs it to be right, it goes IN the prompt.]

## The prompt

```text
ROLE
You are a [specific analyst role] preparing [specific artifact] for [audience].

TASK
[Numbered steps. Decompose: extract → compute/organize → assess → format.]

RULES
- Use ONLY the material inside <context>. If something needed is not there,
  write exactly: NOT IN CONTEXT — never guess.
- Every number must be copied from the context or arithmetically derived from
  numbers in it; show the derivation.
- Verbatim quotes for any claim about management statements.
- Flag any figure or claim you are less than certain about with [CHECK].

<context>
{PASTE INPUTS HERE}
</context>

OUTPUT
Respond with ONLY a JSON object matching:
{JSON SCHEMA HERE}

Before answering, re-read your output once and correct anything that violates
the RULES.
```

## Output schema
[The exact JSON schema / table spec. Fixed keys, enums where possible.]

## Validation checklist (run EVERY time)
- [ ] Every number traceable to the context (spot-check two by hand)
- [ ] All schema keys present; enums respected
- [ ] "NOT IN CONTEXT" used where the context is silent — not filled by memory
- [ ] No recommendation beyond what the task asked for
- [ ] [Task-specific check]

## Known failure modes
| Failure observed | Trigger | Mitigation now in the prompt |
|---|---|---|
| [what went wrong] | [what caused it] | [which rule/schema change fixed it] |

## Version log
- v1 (2026-08-24): initial. [Update as you refine — a playbook is a living asset.]
