# Session 2 — Claude Code I: AI as a Coding Copilot

> 🎓 **Work in [`notebooks/02-coding-copilot.ipynb`](../notebooks/02-coding-copilot.ipynb)** — it contains this session's full teaching and lab. This README is the session brief and reference.

**You leave with:** your first complete finance Python project — a Comparable
Company Analysis tool — committed and pushed to your own GitHub repository.

## Working rhythm (this is the actual skill)

With Claude Code, you are the analyst-in-charge; the model is a very fast
junior. The loop that works:

1. **Ask small.** One function, one fix, one chart at a time.
2. **Read before you run.** If you can't explain a line, ask Claude to explain it.
3. **Commit at every green moment.** `git add -A && git commit -m "..."` —
   small commits keep every step reversible (`git revert` beats panic).

## Live demo — Financial Data Pipeline in 30 minutes

The instructor builds `demo/financial_data_pipeline.py` live from an empty
file: load `data/tech_financials.csv` (real SEC-filed fundamentals; a messy
variant with 8 planted defects exists as an optional exercise — see
`data/README.md`),
compute KPIs, chart them. Watch for:

- how each defect is discovered (inspect first, fix second),
- the unit trap (one company reported in $B — a silent 1000× error if missed),
- Intel's negative margins surviving the pipeline without special-casing.

## Lab (30 min) — build the comps tool

Open `lab/comps_starter.py`. Four TODOs take you from the clean dataset to an
analyst-grade table: growth, margins, EV/EBITDA, EV/Sales, P/E, medians,
export. Definitions are in the docstrings; approximations are documented in
`data/README.md` (read it — it changes how much you trust EV/EBITDA here).

Suggested prompts to Claude Code, one at a time:

- "Implement add_growth_and_margins in lab/comps_starter.py per its docstring."
- "Now add_multiples — note the rule about negative denominators."
- "Explain why Intel shows n.m. for P/E and what n.m. means in a comps table."

Then run the deterministic valuation cell and read each printed step.
Does it match your table? Now — and only now — trust the rest.

### Git & GitHub (last 10 minutes of the lab)

```bash
git init && git add . && git commit -m "Comps tool: first working version"
gh repo create my-finance-toolkit --private --source . --push
```

No `gh`? Create the repo on github.com and follow the "push an existing
repository" instructions. See `cheatsheets/git-github-for-finance.md`.

## Deliverable checklist

- [ ] `outputs/comps_summary.csv` produced by YOUR code
- [ ] One multiple hand-verified (say which one in your commit message)
- [ ] Intel handled correctly (n.m., not a negative multiple)
- [ ] Repo on GitHub with ≥3 meaningful commits
- [ ] Stretch: growth-vs-multiple scatter — is growth priced in?
