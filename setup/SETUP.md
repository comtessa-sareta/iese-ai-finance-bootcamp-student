# Setup — do this BEFORE Day 1 (~30 minutes)

> **Already set up?** (accounts, environment, keys, ✱ panel) — skip this page:
> open **`notebooks/00-setup.ipynb`**, run it, and if it's all green go
> straight to notebook 01. This page is only for getting a bare laptop ready.

Follow this page top to bottom. When you finish step 6, you are ready for the
course. If anything fails, the **Troubleshooting** section at the bottom has
the fix.

## Step 0 — the two accounts you need (~$25 total)

| Account | What for | Get it |
|---|---|---|
| **Claude Pro plan** (~$20, one month is enough) | The ✱ Claude panel in VS Code — your copilot in every lab | claude.ai → upgrade to Pro. ⚠️ The free account does NOT work |
| **Anthropic API key** with **$5** credit (you'll use €1–2) | The notebook cells where YOUR code calls Claude | console.anthropic.com (separate from Pro; same email fine) → Billing → add $5 → API Keys → Create Key → **copy it now** (shown only once) |

Already have a Console account but didn't save your key? **Just create a new
key** — keys are free and take 30 seconds; your credit stays on the account.
Check **Billing** shows some credit (≥$2 is fine for this course; top up $5
if empty).

## Step 0b — the three tools (skip what you already have)

If you took the Python/tools pre-course, you have all three — skip ahead.

| Tool | Check you have it | If not, install |
|---|---|---|
| **VS Code** | it opens | code.visualstudio.com |
| **Git** | `git --version` in a terminal | git-scm.com (Mac: running that check offers the install) |
| **Python** | `python3 --version` shows 3.10+ | Anaconda: anaconda.com/download (or any Python 3.10+) |

## Where do I type the commands?

In VS Code's built-in terminal: **Terminal → New Terminal** (opens at the
bottom). Every command below goes there.

## Step 1 — get the course

```bash
git clone https://github.com/comtessa-sareta/iese-ai-finance-bootcamp-student.git
cd iese-ai-finance-bootcamp-student
```

**The `cd` line matters**: `git clone` leaves your terminal *outside* the new
folder, and every command after this one must run *inside* it. Check with:

```bash
ls
```

You should see `requirements.txt`, `notebooks`, `setup`. If you do not, you
are in the wrong folder — run the `cd` line above.

Then **File → Open Folder** → choose the `iese-ai-finance-bootcamp-student`
folder (so the notebooks and the ✱ panel see the project). If you open a new
terminal after that, it starts inside the folder already.

## Step 2 — create the Python environment

```bash
conda create -n aifinance python=3.12 -y --override-channels -c conda-forge
conda activate aifinance
python -m pip install -r requirements.txt
```

(The `--override-channels -c conda-forge` part installs from the community
channel — without it, fresh Anaconda installs are blocked cold by a
Terms-of-Service prompt. Copy the line exactly.)

Then tell VS Code to use it: `Cmd+Shift+P` (Windows: `Ctrl+Shift+P`) →
**Python: Select Interpreter** → pick **aifinance**.

## Step 3 — your keys

```bash
cp .env.example .env
```

VS Code may pop up a notice about "terminal environment injection" the moment
this file appears — **dismiss it**, it changes nothing: the course reads `.env`
from inside the code.

Open the new `.env` file in VS Code and fill in two lines:
your name+email in `SEC_EDGAR_USER_AGENT`, and your API key from Step 0 in
`ANTHROPIC_API_KEY`. **Never share or commit this file.**

## Step 4 — the Claude panel

1. `Cmd+Shift+X` (Windows: `Ctrl+Shift+X`) → search **"Claude Code"**
   (publisher: Anthropic) → **Install**.
2. Click the **✱ icon** (top-right of the editor, or the bottom status bar)
   → **Sign in** with your **Pro** account.
3. In the panel, type `/status` — it should show your Pro plan.

⚠️ **Wrong-chat warning:** if a chat panel mentions GPT, Gemini or "credits",
that's VS Code's built-in Copilot — NOT the course tool. The course tool is
always the **✱** panel. (More detail: [claude-code-setup.md](claude-code-setup.md).)

## Step 5 — verify

```bash
python setup/check_setup.py
```

Everything required shows `[ OK ]` → you're set. Any failure message includes
its own fix; stubborn cases → Troubleshooting below, or bring your laptop at
8:45 on Day 1.

## Step 6 — start the course

Open **`notebooks/00-setup.ipynb`** → top-right **Select Kernel →
aifinance** → **Run All**. All green? Done. From here the course is the
notebooks, **in order 01 → 05**: each teaches first, then a lab where you fill
every `None` and `[BLANK]` between the `### START CODE HERE ###` markers and
run the ✅ self-check under each exercise. Stuck? Ask the ✱ panel — using it
well *is* the course.

---

## Troubleshooting

- **`Could not open requirements file: ... No such file or directory`** — your
  terminal is not inside the course folder. Run `cd iese-ai-finance-bootcamp-student`
  (then `ls` should list `requirements.txt`) and repeat the command. Same cause
  if any later command says a course file is missing.
- **VS Code says "An environment file is configured but terminal environment
  injection is disabled… Enable `python.terminal.useEnvFile`"** — harmless,
  dismiss it. That notification appears the moment a `.env` file exists. The
  course reads `.env` **inside the code** (every notebook and script calls
  `load_dotenv`), so the setting changes nothing here. Your `cp` command
  worked; continue with Step 3.
- **`command not found: conda`** — either run `conda init zsh` (Mac) from the
  Anaconda app / use the *Anaconda Prompt* profile (Windows) and open a NEW
  terminal, or Anaconda isn't installed: use the no-conda line instead —
  `python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt`
  — the course is equally happy with it. **Note:** on this path your
  environment shows up in VS Code as **`.venv`**, not `aifinance` — same
  thing; pick `.venv` wherever this guide says `aifinance`.
- **conda demands Terms-of-Service acceptance** — this happens when
  `conda create` is run WITHOUT the `--override-channels -c conda-forge`
  flags from Step 2. Rerun with the flags exactly as written. (Alternative:
  accept Anaconda's repo ToS with the two `conda tos accept ...` commands it
  prints — note their terms restrict commercial use at larger organizations,
  which is why the course defaults to conda-forge instead.)
- **`No module named 'requests'` (or pandas...)** — your packages landed in a
  different environment than the one running. `conda activate aifinance`,
  then `python -m pip install -r requirements.txt` (`python -m pip` always
  installs into the active Python). In notebooks, confirm the kernel says
  **aifinance** — or just run the **rescue cell** in `00-setup.ipynb`, which
  installs into whatever kernel you selected.
- **`You have reached your specified API usage limits`** — your account has a
  monthly spend limit set: console.anthropic.com → Settings → Limits → raise
  it (or wait for the reset date the error names).
- **`Your credit balance is too low` (or `BadRequestError` mentioning
  credit)** — your key works but its Console account has no money on it:
  console.anthropic.com → Billing → add $5 (the whole course uses €1–2).
  If you have another key with credit, put that one in `.env` instead.
- **`AttributeError: module 'toolkit.llm' has no attribute ...`** — your kernel
  is running code from before the last update. **Restart** the kernel and run
  from the top. (The first cell of each notebook also reloads the toolkit, so
  re-running it usually suffices.)
- **Notebook disagrees with the terminal** — notebook outputs show the LAST
  run, and the kernel snapshots your environment at start. After installing
  anything: **Restart → Run All**.
- **The instructor announces a course update during class** — run
  `python setup/update_course.py` from the repo folder. It backs up every
  notebook you have modified to `backups/<time>/` (your answers are never
  lost), restores the originals, and pulls the update. Copy your answers
  back from the backup where you need them.
- **After a `git pull`, an open notebook looks unchanged** — VS Code kept the
  old version in its editor tab (a ● dot on the tab means an unsaved buffer,
  which even survives closing and reopening). The reliable fix: focus the
  tab → `Cmd+Shift+P` (Win: `Ctrl+Shift+P`) → **Revert File** → Enter.
  Repeat for every tab with a dot, then **Restart → Run All**.
- **No ✱ icon anywhere / sign-in trouble / hitting Pro limits** — see
  [claude-code-setup.md](claude-code-setup.md).
- **The checker says the `claude` CLI is not on PATH** — fine if you use the
  VS Code extension (it bundles its own copy).
