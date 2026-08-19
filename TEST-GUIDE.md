# Dress rehearsal — do the course as a student

*(This file exists only for the pre-course test run. It substitutes for the
instructor's live teaching so you can play a real student, solo. It will not
be in the class repo.)*

**The rules of the game:** you are a MiF student with the CONFIRMED student
setup — a **paid Claude Pro plan, signed into the Claude Code extension in
VS Code** (that's what the tools pre-course leaves them with). Use ONLY
what's in this repo plus Claude. Drive the labs from the **VS Code panel**,
run scripts in the **integrated terminal**. There are no solutions in your
copy — when you're stuck, do what students will do: ask Claude Code. If
Claude Code can't get you through a TODO, **that is a finding** — write it
down and move on. Budget ~4–6 hours total; you can split it 2 days like the
real course.

**Track Pro usage:** after EVERY session, type `/usage` in the Claude panel
and write down the reading. Whether a whole class stays inside Pro limits at
lab intensity is one of the most valuable numbers this rehearsal produces.

Report back per session: ⏱ how long it took · ✅/❌ the deliverable check ·
📊 the /usage reading · 😕 anything confusing, broken, or slow · 💡 one
improvement.

---

## Session 0 — Set up as the student (target: 25 min)

What you need to impersonate the confirmed student profile:

- **VS Code** with the **Claude Code extension** (Extensions view →
  search "Claude Code" → Install)
- a **paid Claude Pro plan** (~$20 for one month — the free account won't run
  Claude Code; agree reimbursement with the instructor beforehand)
- an **Anthropic Console** account with **$5** credit (created in step 3 —
  the whole rehearsal uses well under 1€ of it)

Do these in order, timing each — this mirrors the students' pre-Monday email:

1. **Extension + Pro sign-in:** open this repo folder in VS Code
   (File → Open Folder), click the **✱ Claude** icon, sign in with the Pro
   account. In the panel, type `/status` and confirm it shows the Pro plan.
   Anything missing → `setup/claude-code-setup.md` is the students' safety
   net — you're testing it too, so follow it rather than improvising.
2. **Repo-context check:** ask the panel *"What is the one rule that always
   applies in this repo?"* — **without selecting or attaching anything** — it
   should answer from the repo's CLAUDE.md (never present an unverified
   number). If it doesn't, that's a finding. And check you're in the RIGHT
   panel: if your chat shows GPT/Gemini model names or a "credits" counter,
   that's Copilot or another extension, not Claude Code — a mistake real
   students WILL make, so note how easy it was to land in the wrong one.
3. **Course setup:** follow `setup/SETUP.md` in the integrated terminal —
   dependencies, `.env` (your SEC user agent + a fresh API key with $5
   credit), then `python setup/check_setup.py`. Note: the checker may say
   the `claude` CLI is not on PATH — with the extension that's expected and
   explicitly fine.
4. **Open `notebooks/00-setup.ipynb`** in VS Code (select the course kernel
   when prompted) and run it top to bottom. From here on, THE COURSE IS THE
   NOTEBOOKS — one per session, teaching first, then fill-the-gaps labs
   between `### START CODE HERE ###` markers (structure given; replace every
   `None` and `[BLANK]`), each with a ✅ self-check cell under it. Session
   folders' READMEs are reference. Judge the gap difficulty as a
   finance-not-CS student — too easy and too hard are both findings.

**Report:** total time from clone to green check; whether Pro sign-in and
plan detection worked first try; the CLAUDE.md context-check result; any
step where you hesitated.

## Session 1 — Prompting (target: 45–60 min)

**Open `notebooks/01-prompting.ipynb`** and work top to bottom — it contains
everything below (Part A sends you to claude.ai; Parts B/C are the coding lab
with self-checks). The notes that follow are what to pay attention to:

1. Everything runs **in the notebook** (the API cells are the "clean room" —
   no web search, no repo context; note the key is needed from THIS session).
2. Part A: naive → role+task → grounded (your RULES + `NOT IN CONTEXT`
   refusal) → schema run twice. Part C: the three red-team attack cells.
3. Write ≥2 failure-mode rows into
   `session-01-prompting/playbook/company-deep-dive.md` — check the table
   format makes sense to a first-timer.

**Check:** you made the model answer NOT IN CONTEXT with your own rules; the
injection cell did NOT flip the output to "STRONG BUY". Optional closing
beat: paste the naive ask into the ✱ Claude Code panel — it behaves better
than the raw API because CLAUDE.md was silently prompt-engineering for it.

## Session 2 — Coding copilot (target: 60 min)

**Open `notebooks/02-coding-copilot.ipynb`** and work top to bottom (the
messy-data demo runs; the comps lab has three fill-in exercises with
self-checks). Notes:

1. Run the demo end state: `python session-02-coding-copilot/demo/financial_data_pipeline.py`
   (expect "Clean: 10 companies" + a chart in `outputs/`).
2. The lab: implement `lab/comps_starter.py` TODOs 1→4 **from the VS Code
   panel**, one prompt per TODO — use the students' power move each time:
   select the TODO docstring, press `Option+K` (Mac) / `Alt+K` (Windows) to
   @-mention it, then ask. Watch how edits appear as reviewable diffs.
   (Bonus, only if you also have the `claude` CLI: do one TODO from the
   terminal to confirm parity.)
3. **Hand-verify Apple's EV/EBITDA** from the CSV row with a calculator.
4. Do the git moment: init/commit/push to a scratch private repo of yours
   (or just local commits if you prefer).

**Check:** your table shows Intel P/E as `n.m.` (not a negative number);
median EV/EBITDA lands around ~25–26x with the committed prices; your
hand-check matches the table.

## Session 3 — Debugging & earnings engine (target: 60–75 min)

**Open `notebooks/03-debugging-earnings.ipynb`** — you build the DCF function
by function (each with its test below, ending at $75.61 vs $62), then the
earnings engine's trust layer. Notes:

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

**Open `notebooks/04-workflows-edgar.ipynb`** — live EDGAR teaching cells,
then the screening lab (three fill-ins). Notes:

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

**Open `notebooks/05-agents.ipynb`** — inspect the agent's spec, build the
currency-trap tool and the operating rules (self-checked without a key), then
run your agent live and pass the human gate. Notes:

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

1. Per-session: time, deliverable checks ✅/❌, `/usage` reading, confusions,
   one improvement.
2. **The Pro-limits verdict:** across the whole rehearsal, how far did your
   Pro allowance get drawn down? Did you ever get warned or blocked? (This
   decides whether 40 students × 5 sessions survives on Pro.)
3. **The VS Code verdict:** sign-in, repo context pickup, @-mentions, diff
   review, permission prompts — anything that would confuse a first-time
   student in the panel UI?
4. Your `outputs/` folder zipped (memos, charts, reports — the artifacts).
5. The three moments you most needed Claude Code — and whether it delivered.
6. Verdict as a pretend student: would the two days feel doable? Where would
   a real cohort pile up?
