# Template: Competitive Landscape

## When to use
Structured comparison of 2-4 competitors — market positioning section of a
memo, prep for a management meeting, or sizing a competitive threat.

## Inputs required
A facts block per company covering the SAME period basis (note fiscal-year
misalignment explicitly — e.g. NVDA ends January, INTC December). Financials
from filings; strategy claims only if you paste supporting excerpts.

## The prompt

```text
ROLE
You are a strategy-and-equity analyst mapping a competitive field for an
investment committee. Committee members will challenge any claim that smells
like received wisdom, so every claim must trace to the context.

TASK
1. TABLE: one row per company — revenue (state FY + currency), growth,
   profitability (state which margin), scale ratio vs the largest player.
2. POSITIONING: for each company, its competitive position IN THIS CONTEXT'S
   EVIDENCE: where it wins, where it bleeds. Cite the number or excerpt.
3. DYNAMICS: what the numbers imply about the direction of competition
   (share shifts, margin pressure, investment races). Derivations only.
4. WATCH ITEMS: 3 measurable indicators that would signal the balance is
   shifting, and for each, WHERE a public source would show it (10-K segment
   data, quarterly filings...).

RULES
- ONLY the context. Missing → NOT IN CONTEXT.
- No claims from memory about products, share, or strategy — if it's not in
  the context, it does not exist for this exercise.
- Fiscal years differ across companies: flag every cross-company comparison
  that spans different year-ends.
- Scale ratios and growth: show the arithmetic.

<context>
{COMPANY_A_FACTS}
{COMPANY_B_FACTS}
{COMPANY_C_FACTS}
</context>

OUTPUT — only this JSON:
{
  "period_basis_warning": "state the fiscal-year misalignments here",
  "comparison_table": [{"company": "", "fy": "", "revenue": "", "growth": "",
                        "profitability": "", "scale_vs_leader": ""}],
  "positioning": [{"company": "", "wins_where": "", "bleeds_where": "",
                   "evidence": ""}],
  "dynamics": ["", ""],
  "watch_items": [{"indicator": "", "signal_meaning": "", "public_source": ""}]
}

Re-read your output once against the RULES before answering.
```

## Validation checklist
- [ ] period_basis_warning actually names the misaligned year-ends
- [ ] Scale ratios recomputed by hand for one pair
- [ ] No product/roadmap claims that aren't in the context
- [ ] Watch items are measurable (a number, not "momentum")

## Known failure modes
| Failure observed | Trigger | Mitigation |
|---|---|---|
| Injected memorized market-share figures | famous companies | context-only rule + "does not exist" phrasing |
| Compared NVDA FY2026 to INTC FY2025 as same-year | misaligned FYs | period_basis_warning field forced first |
| "Winner" declared beyond evidence | asked for positioning | wins/bleeds + evidence structure |
| *(add yours)* | | |

## Version log
- v1 (2026-08-24): initial. Tested on NVDA/AMD/INTC.
