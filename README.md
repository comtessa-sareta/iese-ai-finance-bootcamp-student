# AI-Augmented Productivity for Finance

**IESE Business School · MiF 2027 · Prof. Sara Bisbe**
Two-day bootcamp, 24–25 August 2026 · 5 sessions × 75 minutes

> From day one you do real finance work with AI: only Python and Claude,
> free public SEC/EDGAR filings, and one rule that never bends —
> **never ship a number you haven't verified.**

## What you build (a portfolio, not notes)

Across five sessions you assemble **"Your AI Financial Analyst"**:

| Session | You build | Deliverable |
|---|---|---|
| 1 · Prompting & financial reasoning | the analyst's **brain** | Finance Prompt Playbook |
| 2 · Claude Code as coding copilot | the **hands** | Comps tool, on your GitHub |
| 3 · Debugging, testing & analytics | the **discipline** | Earnings engine + investment memo |
| 4 · Workflows & SEC/EDGAR | the **assembly line** | Market-intel workflow + screening engine |
| 5 · Agents & governance | the **analyst** | Mini finance agent + capstone |

## Start here

- **Students:** [setup/SETUP.md](setup/SETUP.md) (15 min, before Day 1), then
  **open `notebooks/00-setup.ipynb` in VS Code and work through the notebooks
  in order** — one per session, self-contained: teaching first, then a lab of
  fill-the-gaps exercises between `### START CODE HERE ###` markers (the
  Python structure is given; every `None` and `[BLANK]` is yours), each with a
  ✅ self-check cell below it. The session folders hold the data,
  reference scripts and briefs the notebooks draw on.
  checklist, minute-by-minute guides, contingencies.

## Repo map

```
notebooks/                  THE COURSE: 00-setup + one notebook per session (work in order)
setup/                      environment setup + checker
toolkit/                    shared package: edgar.py (SEC client), llm.py (Claude helpers), verify.py (grounding checks)
cheatsheets/                git, Claude Code, prompt patterns — pocket cards
session-01-prompting/       playbook templates, red-team exercises, fact sheet
session-02-coding-copilot/  pipeline demo, comps lab, real SEC datasets
session-03-debugging/       broken DCF + tests, earnings engine, transcript
session-04-workflows/       market-intel workflow, screening engine, EDGAR cheatsheet
session-05-agents/          mini analyst agent, research-agent lab, capstone brief
slides/                     Marp-markdown decks (render with marp-cli, or teach from the repo)
solutions/ (per session)    reference implementations — attempt the lab starter first
```

## Ground rules for the data and the outputs

- **Fundamentals are real** — pulled from SEC EDGAR XBRL filings; datasets are
  reproducible (`make dataset`). Share prices are hand-maintained with an
  explicit as-of date (filings contain fundamentals, not quotes).
- **Approximations are documented** — read
  [session-02-coding-copilot/data/README.md](session-02-coding-copilot/data/README.md)
  before trusting a multiple.
- The Session 3 transcript and its company (**Meridian Semiconductor**) are
  **fictional**, created for teaching — chosen so the model must work from the
  document, not from memory.
- Everything produced here is **coursework, not investment advice**, and
  AI-generated drafts are labeled as such.

## Quick commands

```bash
make check          # verify your environment
make test           # Session 3 sanity tests (fail on the broken DCF — that's the exercise)
make dataset        # rebuild Session 2 data from live EDGAR
```

LLM-calling scripts all support `--dry-run` (full pipeline, no API key).

## Requirements

Python 3.10+, packages in `requirements.txt`, a Claude account with Claude
Code, an Anthropic API key from Session 3 (see setup), internet access to
`sec.gov` / `data.sec.gov`.
