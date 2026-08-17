# Git & GitHub — the 10% you need, for finance work

**Mental model:** git = a lab notebook for code. Every commit is a signed,
timestamped save point you can return to. GitHub = the shared, backed-up copy
(and your public portfolio).

## The daily six

```bash
git status                        # what changed?
git diff                          # show me exactly
git add -A                        # stage everything changed
git commit -m "comps: EV/EBITDA working, AAPL hand-verified"
git push                          # send to GitHub
git log --oneline -10             # recent history
```

## Undo (calmly)

```bash
git restore <file>        # discard uncommitted changes to a file
git restore --staged <f>  # unstage (keep the edits)
git revert <sha>          # undo a commit WITH history (the professional undo)
git stash                 # park everything; git stash pop brings it back
```

Avoid `reset --hard` until you know why you'd want history destroyed.

## New project → GitHub (once per project)

```bash
git init
git add . && git commit -m "initial version"
gh repo create my-finance-toolkit --private --source . --push
# no gh CLI? create empty repo on github.com, then:
git remote add origin git@github.com:<you>/my-finance-toolkit.git
git push -u origin main
```

## Commit messages that age well

`what changed: why it matters` — "screen: net margin basis (op income untagged
for pharma)" beats "fixes". Your future self is the audience.

## Rules that save careers

- **Never commit secrets.** `.env` is git-ignored here for a reason. A pushed
  API key is compromised the moment it lands — revoke, don't delete.
- Commit **small and often** — every green moment.
- Data files: commit small reference CSVs (like this course's), not gigabytes
  or licensed data.
- Pull before you push when collaborating; you're solo this week.

## Claude Code + git

Claude Code reads your repo and can run git for you — but YOU own the commit.
Useful asks: *"summarize my uncommitted changes as a commit message"*,
*"why does git say diverged and what are my options?"*
