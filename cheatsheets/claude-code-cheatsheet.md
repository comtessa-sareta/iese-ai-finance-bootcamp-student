# Claude Code — course cheatsheet

Claude Code is Claude in your terminal/editor with hands: it reads your repo,
edits files, and runs commands — with your permission.

## Start — terminal or VS Code panel, same tool

**Terminal:**

```bash
cd <your-project>
claude
```

**VS Code extension** (what the tools pre-course set up): open the repo
folder (**File → Open Folder**), then click the **✱ Claude icon** (editor
toolbar top-right, or the status bar bottom-right). Same account, same
behavior — every prompt in this course works identically in both. Extension
extras worth using in the labs:

- **Select code → `Option+K` (Mac) / `Alt+K` (Win)** inserts an @-mention of
  that file+lines into your prompt — the fastest "implement THIS TODO".
- The **permission-mode indicator** at the bottom of the prompt box shows how
  much Claude may do without asking — know your setting.
- Diffs and plans render in the editor; review them there before accepting.

First run in a repo: try `/init` (writes a CLAUDE.md so future sessions know
the project). This course repo already has one — read it once.

## The asks that work (course-tested)

| Situation | Say |
|---|---|
| New function | "Implement `add_multiples` in lab/comps_starter.py per its docstring." |
| Don't understand code | "Explain load_raw line by line, for a finance person." |
| Crash | paste traceback + "Diagnose this. Explain the cause BEFORE proposing a fix." |
| Failing test | "test_x fails. Show the offending line, explain the finance error, fix only that." |
| Review | "Any bugs or silent assumptions in this diff? Be critical." |
| Data first | "Look at data/x.csv and LIST the data-quality problems. No code yet." |
| Commit | "Summarize my changes as a commit message." |

## The habits that keep you in charge

1. **One thing at a time.** Big asks → big diffs → unread diffs → trouble.
2. **Read every diff.** You sign it, you own it.
3. **Let it run the code.** "Run the script and fix what breaks" is fair game —
   the read-diff rule still applies.
4. **Plan before big changes:** ask it to propose a plan first, then execute
   step by step (or use plan mode if your version has it).
5. **Context is king:** name files explicitly; point at docstrings; paste
   errors whole.

## Course conventions (from this repo's CLAUDE.md)

- Run scripts from the **repo root**
- Outputs go to `outputs/` — never overwrite `data/`
- Secrets in `.env` only
- Never present a number you haven't verified against source data

## When Claude Code is the wrong tool

Thinking about WHAT to build (use chat/paper first), firm-confidential data on
a personal account (policy first), and anything you wouldn't be able to
explain afterwards.
