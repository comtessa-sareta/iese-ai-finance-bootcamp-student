# Setup — do this BEFORE Day 1 (15 minutes)

You come from the Data Analytics Bootcamp, so Python (Anaconda), VS Code, Git
and Claude Code are already installed. This adds the course kit.

**Where do I type all these commands?** In VS Code's built-in terminal:
**Terminal → New Terminal** (it opens at the bottom of the window). Every
command in this guide — and in the whole course — runs there. (Windows: if
your terminal is PowerShell and a command misbehaves, switch the terminal
dropdown to *Command Prompt* or *Git Bash*.)

## 1. Get the course repo

In the VS Code terminal:

```bash
git clone https://github.com/comtessa-sareta/iese-ai-finance-bootcamp-student.git
```

Then **File → Open Folder** → choose the `iese-ai-finance-bootcamp-student`
folder you just cloned. Opening the folder matters twice: the terminal now
starts in the right place, and the Claude panel reads the course's context
file from it.

## 2. Install the Python dependencies

In the terminal (now inside the course folder):

```bash
# Anaconda users (recommended — matches your bootcamp setup):
conda create -n aifinance python=3.12 -y
conda activate aifinance
pip install -r requirements.txt

# (or plain venv:  python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
```

**If you see `command not found: conda`:** either your terminal was never
initialized for Anaconda — run `conda init zsh` from the Anaconda prompt/app,
or on Windows pick the *Anaconda Prompt* terminal profile, then open a NEW
terminal — or Anaconda isn't installed on this machine, in which case just
use the plain-venv line above instead; the course doesn't care which.

**If conda demands Terms-of-Service acceptance** (fresh installs do): run the
two `conda tos accept ...` commands it prints (Anaconda's repo ToS — free for
individual/educational use), then rerun the create command.

Then tell VS Code to use this environment: `Cmd+Shift+P` (Mac) /
`Ctrl+Shift+P` (Windows) → **Python: Select Interpreter** → pick
**aifinance**. From now on, new terminals in this folder activate it for you;
if a terminal ever shows the wrong environment, run `conda activate aifinance`
in it.

## 3. Configure your environment

```bash
cp .env.example .env
```

Edit `.env`:

- `SEC_EDGAR_USER_AGENT` — your name and email (the SEC asks automated
  clients to identify themselves; it's polite and required).
- `ANTHROPIC_API_KEY` — needed from **Session 1** (the course notebooks call
  Claude from your own code). Create at https://console.anthropic.com →
  API Keys, load a small budget ($5 is plenty — expect to use €1–2 all
  course). **Never commit this file.**

## 3b. Claude Code — verify it, and understand the two credentials

Your Claude **Pro** subscription (the "basic license" from the program email —
the free claude.ai account is NOT enough) powers Claude Code, the copilot you
use in every lab. The API key above is a **separate** credential for the
scripts. Verify both and fix anything missing with
[claude-code-setup.md](claude-code-setup.md) — 5 minutes.

## 4. Verify

```bash
python setup/check_setup.py
```

Everything required should show `[ OK ]` (the API key may show `[warn]` until
Session 3 — that's fine). If something fails, the message tells you the fix;
bring stubborn cases to 15 minutes before Session 1.

## 5. Smoke test (optional but satisfying)

```bash
python session-02-coding-copilot/demo/financial_data_pipeline.py
```

You should see a cleaned table of real big-tech financials and a chart in
`outputs/`. That data came from SEC filings — you'll learn to fetch it
yourself on Day 2.
