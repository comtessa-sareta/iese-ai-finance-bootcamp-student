# Template: Company Deep-Dive

## When to use
First-pass structured overview of a company for an internal brief — before a
meeting, a screen follow-up, or as the opening section of an initiation memo.

## Inputs required
A facts block: recent revenue/income figures (e.g. from `data/semis_fact_sheet.md`
or your Session 2 CSV), business description, and any filing excerpts you have.
No facts block → the model fills gaps from memory → unusable output.

## The prompt

```text
ROLE
You are a senior equity research analyst preparing an internal company brief
for a portfolio manager who has 3 minutes and zero tolerance for fluff.

TASK
1. EXTRACT the business model: what is sold, to whom, and what drives revenue.
2. ORGANIZE the financial profile: revenue level and 2-year trajectory,
   profitability (state which margin and which fiscal year), balance-sheet
   posture if given.
3. ASSESS competitive position: strengths and vulnerabilities — each tied to
   evidence in the context.
4. LIST what a diligent analyst would check next: the 3 most important open
   questions this context cannot answer.

RULES
- Use ONLY the material inside <context>. Missing → write NOT IN CONTEXT.
- Every number copied or derived from the context; show derivations
  (e.g. "growth = 215.9/130.5 - 1 = 65.5%").
- State the fiscal year and currency for every figure.
- Strengths/vulnerabilities without evidence are banned.

<context>
{FACTS_BLOCK}
{OPTIONAL_FILING_EXCERPTS}
</context>

OUTPUT — only this JSON:
{
  "company": "", "ticker": "", "fiscal_year_referenced": "",
  "business_model": "",
  "financial_profile": {
    "revenue": "", "growth_trajectory": "", "profitability": "",
    "balance_sheet_notes": ""
  },
  "competitive_position": {
    "strengths": [{"point": "", "evidence": ""}],
    "vulnerabilities": [{"point": "", "evidence": ""}]
  },
  "open_questions": ["", "", ""],
  "confidence_notes": "anything marked [CHECK] or NOT IN CONTEXT, listed"
}

Re-read your output once against the RULES before answering.
```

## Validation checklist
- [ ] Spot-check the growth arithmetic by hand
- [ ] Currency + fiscal year stated for every figure (watch Jan/Jun/Sep year-ends)
- [ ] Each strength/vulnerability has real evidence, not vibes
- [ ] Open questions are things the context truly can't answer

## Known failure modes
| Failure observed | Trigger | Mitigation |
|---|---|---|
| Filled market-share numbers from memory | no facts block pasted | context-only rule + NOT IN CONTEXT token |
| Mixed fiscal years silently (NVDA Jan FY vs INTC Dec FY) | multi-company context | "state the fiscal year for every figure" rule |
| Generic strengths ("strong brand") | no evidence requirement | evidence field required per point |
| *(add yours from the red-team lab)* | | |

## Version log
- v1 (2026-08-24): initial.
