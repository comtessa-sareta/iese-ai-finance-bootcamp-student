# Template: Earnings-Call Summarization

## When to use
Turn a full earnings-call transcript into a decision-ready note: what
management said, what they dodged, what changed. (In Session 3 this exact
prompt becomes code — `session-03-debugging/lab/earnings_starter.py`.)

## Inputs required
The complete transcript, pasted (or attached). Partial transcripts produce
partial truths — say so in the header if you only have prepared remarks.

## The prompt

```text
ROLE
You are a buy-side analyst writing an internal earnings note. Your PM reads
the verdict first and checks your quotes when something matters.

TASK
1. VERDICT: overall read of the quarter — one of:
   positive | cautiously_positive | neutral | cautious | negative — plus a
   2-sentence rationale referencing specific results.
2. NUMBERS: the reported figures management highlighted (revenue, margins,
   EPS, guidance) — exactly as stated, with who said them.
3. THEMES: 3-5 key themes, each with a VERBATIM supporting quote.
4. GUIDANCE: what was guided, AND what was explicitly excluded or caveated —
   exclusions are where risk hides.
5. Q&A QUALITY: for each analyst exchange, was the answer direct / partial /
   evasive? Evasive answers are findings, not filler.
6. RED FLAGS: contradictions between speakers, recurring "one-time" items,
   deteriorating working-capital signals, unfalsifiable claims.

RULES
- ONLY the transcript. Missing → NOT IN CONTEXT.
- Quotes VERBATIM — they will be machine-checked against the source.
- Numbers exactly as spoken (units and all); no recomputation.
- Distinguish management framing from fact: "described as one-time" ≠ "one-time".

<context>
{FULL_TRANSCRIPT}
</context>

OUTPUT — only this JSON:
{
  "overall_sentiment": "", "sentiment_rationale": "",
  "reported_figures": [{"metric": "", "value_as_stated": "", "speaker": ""}],
  "key_themes": [{"theme": "", "evidence_quote": ""}],
  "guidance": {"given": "", "exclusions_and_caveats": ""},
  "qa_assessment": [{"topic": "", "answer_quality": "direct|partial|evasive", "note": ""}],
  "red_flags": [{"flag": "", "why_it_matters": "", "evidence_quote": ""}],
  "summary_paragraph": ""
}

Re-read your output once against the RULES before answering.
```

## Validation checklist
- [ ] Search the transcript for 2 random quotes — must match verbatim
- [ ] Reported figures match the source exactly (units!)
- [ ] Guidance EXCLUSIONS captured (the fine print is the point)
- [ ] At least one evasive/partial answer identified — calls always have one
- [ ] Sentiment justified by cited results, not tone-matching the CEO

## Known failure modes
| Failure observed | Trigger | Mitigation |
|---|---|---|
| Paraphrased "quotes" | no verbatim rule | verbatim + "machine-checked" warning |
| Missed the guidance exclusion | asked only "what was guided" | explicit exclusions field |
| Sentiment parroted management optimism | no rationale requirement | rationale tied to results + red-flag hunt |
| *(add yours)* | | |

## Version log
- v1 (2026-08-24): initial. Becomes code in Session 3.
