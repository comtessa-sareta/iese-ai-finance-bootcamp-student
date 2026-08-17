# Setup — do this BEFORE Day 1 (15 minutes)

You come from the Data Analytics Bootcamp, so Python (Anaconda), VS Code, Git
and Claude Code are already installed. This adds the course kit.

## 1. Get the course repo

```bash
git clone https://github.com/comtessa-sareta/iese-ai-finance-bootcamp-student.git
cd iese-ai-finance-bootcamp-student
```

(You need a GitHub account with access — the invite link is on MyIese.)

## 2. Install the Python dependencies

```bash
# Anaconda users (recommended — matches your bootcamp setup):
conda create -n aifinance python=3.12 -y
conda activate aifinance
pip install -r requirements.txt

# (or plain venv:  python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
```

## 3. Configure your environment

```bash
cp .env.example .env
```

Edit `.env`:

- `SEC_EDGAR_USER_AGENT` — your name and email (the SEC asks automated
  clients to identify themselves; it's polite and required).
- `ANTHROPIC_API_KEY` — needed from Session 3. Create at
  https://console.anthropic.com → API Keys, load a small budget ($5 is
  plenty — expect to use €1–2 all course). **Never commit this file.**

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
