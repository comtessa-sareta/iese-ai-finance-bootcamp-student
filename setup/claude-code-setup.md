# Claude Code — access, verification, and the two credentials

The first pre-course (Python & tools) already installed Claude Code and signed
you in. This page is the **safety net**: verify everything works, fix it if it
doesn't, and set up the ONE extra credential this course adds.

## The two credentials — know which is which

| Credential | What it powers | Where it comes from | Cost |
|---|---|---|---|
| **Claude account (Pro plan)** | Claude Code — the interactive copilot you use in every lab | claude.ai subscription (the "basic license" from the program email) | ~$20 for one month — **the free claude.ai account does NOT include Claude Code** ([Anthropic docs](https://code.claude.com/docs/en/setup#authenticate)) |
| **Anthropic Console API key** | Sessions 3–5 scripts, where YOUR Python code calls Claude (earnings engine, workflows, the agent) | console.anthropic.com — separate account, pay-as-you-go | load **$5** of credit; the whole course typically uses **€1–2** |

A Pro subscription does not include API credits, and API credits don't include
the Pro app — you need both. Same email for both accounts is fine.

## 1. Verify Claude Code works (30 seconds)

```bash
claude --version
```

A version number = installed. Then, from the course repo:

```bash
claude
```

It should open a session (first run asks you to log in via browser — use your
**Pro** account). Type `/status` to confirm which account you're on; type
`exit` (or Ctrl+C twice) to leave. For deeper diagnostics: `claude doctor`.

## 2. If it's missing — install (2 minutes)

**macOS / Linux / WSL:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
```

(Alternatives: `brew install --cask claude-code`, `winget install
Anthropic.ClaudeCode`, or `npm install -g @anthropic-ai/claude-code`.
Full options: https://code.claude.com/docs/en/setup)

Then run `claude` and log in. **VS Code users:** the Claude Code extension
(marketplace: "Claude Code") gives you the same thing inside the editor — the
first pre-course covered it; the terminal version is equivalent and this
course's instructions work in either.

## 3. Create the API key (5 minutes — needed from Session 3)

1. Go to https://console.anthropic.com and sign up (your normal email is fine).
2. **Billing** → add **$5** of prepaid credit.
   Recommended: set a spend limit of $5 too — an agent with a budget is a
   theme of this course.
3. **API Keys** → Create key → copy it (you won't see it again).
4. In the course repo: `cp .env.example .env`, open `.env`, paste it as
   `ANTHROPIC_API_KEY=sk-ant-...`
5. Never commit `.env`, never paste the key into chat/screenshots. If a key
   leaks: revoke it in the console, don't just delete the message.

Verify: `python setup/check_setup.py` → the API-key line turns `[ OK ]`.

## What if…

- **You hit Pro usage limits mid-lab** (rare at course intensity): limits are
  rolling — pair up with a neighbour for the rest of the lab, or continue the
  lab's script parts, which bill your API credit instead.
- **You can't get a Pro plan at all**: Claude Code also runs on the Console
  account directly — start `claude` with your `ANTHROPIC_API_KEY` set and
  approve it as the login; usage then bills your $5 credit. Fine for this
  course's scale.
- **No Claude Code at all** (IT restrictions?): every lab is still doable by
  pasting code and errors into claude.ai chat — clunkier, but the course's
  `--dry-run` modes and your API key keep all scripts working. Tell the
  instructor before Day 1.
