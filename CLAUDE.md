# CLAUDE.md — AI-Augmented Productivity for Finance (IESE MiF)

This repo is the course kit for a 5-session finance + AI bootcamp. Students use
Claude Code inside this repo during labs. These instructions apply to every
session opened here.

## The one rule that always applies

**Never present a financial number you haven't verified against the source
data.** When producing analysis, state where each figure came from (which file,
which SEC filing, which computed column). If something is not in the provided
context, say `NOT IN CONTEXT` instead of guessing.

## Repo map

- `setup/` — environment setup + `check_setup.py` verification script
- `toolkit/` — shared Python package: `edgar.py` (SEC EDGAR client), `llm.py` (Claude API helpers with JSON validation)
- `session-01-prompting/` — prompt playbook templates, red-team exercises (no code)
- `session-02-coding-copilot/` — pandas pipeline demo, comparable-company-analysis lab, datasets
- `session-03-debugging/` — intentionally broken DCF + tests, earnings-analysis-engine lab
- `session-04-workflows/` — SEC/EDGAR market-intelligence workflow, company screening lab
- `session-05-agents/` — mini investment-analyst agent (tool-use loop), capstone brief
- `instructor/` — teaching guides (instructor repo only; absent in the student copy)
- `solutions/` folders — reference implementations (instructor repo; published to students after the course). Students: attempt the `lab/` starter with Claude Code before looking at any solution.

## Conventions

- Run all scripts **from the repo root**: `python session-02-coding-copilot/demo/financial_data_pipeline.py`
- Scripts write generated files to `outputs/` (git-ignored). Never overwrite files in `data/`.
- Secrets live in `.env` (see `.env.example`). Never hardcode or commit API keys.
- SEC EDGAR requests must send the `SEC_EDGAR_USER_AGENT` identification header — `toolkit/edgar.py` handles this; don't bypass it or hammer the API (it throttles to well under SEC's 10 req/s limit).
- LLM scripts accept `--dry-run` to exercise the full pipeline without an API key.
- Dataset caveats (fiscal-year misalignment, EBITDA and net-debt approximations) are documented in `session-02-coding-copilot/data/README.md` — read it before drawing conclusions from the numbers.

## When helping a student

Prefer explaining over doing: show the failing line, explain *why*, then fix.
Small functions, clear names, no cleverness. If a student asks you to just
produce the lab answer, help them build it step by step instead — the lab is
the point of the course.
