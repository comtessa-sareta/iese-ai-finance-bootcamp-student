# Dress rehearsal — do the course as a student

*(This file exists only for the pre-course test run. It substitutes for the
instructor's live teaching so you can play a real student, solo. It will not
be in the class repo.)*

**The rules of the game:** you are a MiF student. Use ONLY what's in this repo
plus Claude (Claude Code and/or the Claude app). There are no solutions in
your copy — when you're stuck, do what students will do: ask Claude Code.
If Claude Code can't get you through a TODO, **that is a finding** — write it
down and move on. Budget ~4–6 hours total; you can split it 2 days like the
real course.

Report back per session: ⏱ how long it took · ✅/❌ the deliverable check ·
😕 anything confusing, broken, or slow · 💡 one improvement.

---

## Session 0 — Setup (target: 15 min; +10 if you lack Claude Code)

One difference from real students: they take a prior tools pre-course that
installs Claude Code and a Claude **Pro** login. If your laptop doesn't have
that, follow `setup/claude-code-setup.md` first and time it — you're testing
that safety-net doc for the students who show up broken. (Note: Claude Code
needs a paid plan or an API key; the free claude.ai account won't run it.)

Then follow `setup/SETUP.md` literally. Finish with:

```bash
python setup/check_setup.py
```

**Check:** everything required `[ OK ]`. For the full experience create a
small Anthropic API key (€5 prepaid is plenty — the whole rehearsal costs
well under 1€); Sessions 3–5 use it. Without a key, the `--dry-run` paths
still let you complete most labs.

**Report:** exact time from clone to green check; any step where you hesitated.

## Session 1 — Prompting (target: 45–60 min)

Read `session-01-prompting/README.md`, then:

1. In Claude (app or Claude Code), replay the demo arc yourself on the
   NVIDIA/AMD/Intel case: naive ask → add role+task → paste
   `data/semis_fact_sheet.md` inside `<context>` tags with the NOT IN CONTEXT
   rule → add the JSON schema from `playbook/company-deep-dive.md`.
2. Complete ONE playbook template end to end (company deep-dive suggested).
3. Run red-team exercises **1, 2 and 5** against it and write what happened
   into the template's failure-modes table.

**Check:** you made the model answer NOT IN CONTEXT at least once; injection
(exercise 5) did NOT flip your prompt into "STRONG BUY".

## Session 2 — Coding copilot (target: 60 min)

Read `session-02-coding-copilot/README.md`, then:

1. Run the demo end state: `python session-02-coding-copilot/demo/financial_data_pipeline.py`
   (expect "Clean: 10 companies" + a chart in `outputs/`).
2. The lab: open Claude Code and implement `lab/comps_starter.py` TODOs 1→4,
   one prompt per TODO (suggested prompts are in the session README).
3. **Hand-verify Apple's EV/EBITDA** from the CSV row with a calculator.
4. Do the git moment: init/commit/push to a scratch private repo of yours
   (or just local commits if you prefer).

**Check:** your table shows Intel P/E as `n.m.` (not a negative number);
median EV/EBITDA lands around ~25–26x with the committed prices; your
hand-check matches the table.

## Session 3 — Debugging & earnings engine (target: 60–75 min)

Read `session-03-debugging/README.md`, then:

1. `python session-03-debugging/demo/broken_dcf.py` → crash. Paste the
   traceback into Claude Code, ask for diagnosis BEFORE fix. Fix it.
2. `python -m pytest session-03-debugging/demo/ -q` → expect failures. Fix
   `broken_dcf.py` bug by bug (with Claude) until **7 passed**.
3. Lab: `python session-03-debugging/lab/earnings_starter.py --dry-run`
   (runs immediately; every quote shows UNVERIFIED). Do TODO 1–3 with
   Claude Code, re-running `--dry-run` as you go.
4. With your API key: run it live and read YOUR memo.

**Check:** DCF ends at **$75.61** vs $62 market; after TODO 2 the dry-run
reports exactly **1 of 11 quotes NOT found** (the fabricated margin promise);
your live memo finds at least two of: recurring "one-time" costs, CEO/CFO
margin gap, guidance exclusion, DSO jump.

## Session 4 — Workflows & EDGAR (target: 60 min)

Read `session-04-workflows/README.md`, then:

1. Demo (keyless): `python session-04-workflows/demo/market_intel_workflow.py NVDA --peers AMD INTC --dry-run`
   — watch the 5 steps, approve at the gate. With key: run it live too.
2. Lab: implement `lab/screening_starter.py` TODOs 1→3 with Claude Code.
   Run `--dry-run` after TODO 2, live after TODO 3.
3. Change the criteria (`--min-growth 0.10 --require-improving`) and watch
   the shortlist move.

**Check:** the numeric audit reports "all figures trace back" on the dry-run
demo; your screen scans ~16 companies and produces a plausible shortlist
(defaults gave LLY, GE, ETN when the kit was built — new filings may shift it);
you can answer: why net margin instead of operating margin?

## Session 5 — Agent + capstone taste (target: 45–60 min)

Read `session-05-agents/README.md`, then:

1. `python session-05-agents/demo/mini_analyst_agent.py --preflight` (keyless),
   then run it live on the default Novo Nordisk vs Eli Lilly task.
2. Lab: implement `lab/research_agent_starter.py` TODOs 1–4 with Claude Code;
   run it on a company pair of YOUR choice (two SEC filers).
3. Skim `capstone/capstone-brief.md` and answer honestly: could you build a
   5-minute presentation from what you now have?

**Check:** in the live demo trace, the DKK/USD **UNITS DIFFER** warning
appears and the recommendation reasons in growth/margins, not absolute
revenue; your own agent records a structured recommendation and asks before
saving.

---

## Final report to the instructor

1. Per-session: time, deliverable checks ✅/❌, confusions, one improvement.
2. Your `outputs/` folder zipped (memos, charts, reports — the artifacts).
3. The three moments you most needed Claude Code — and whether it delivered.
4. Verdict as a pretend student: would the two days feel doable? Where would
   a real cohort pile up?
