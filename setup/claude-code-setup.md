# Claude Code — access, verification, and the two credentials

The first pre-course (Python & tools) already installed Claude Code and signed
you in. This page is the **safety net**: verify everything works, fix it if it
doesn't, and set up the ONE extra credential this course adds.

## The two credentials — know which is which

| Credential | What it powers | Where it comes from | Cost |
|---|---|---|---|
| **Claude account (Pro plan)** | Claude Code — the interactive copilot you use in every lab | claude.ai subscription (the "basic license" from the program email) | ~$20 for one month — **the free claude.ai account does NOT include Claude Code** ([Anthropic docs](https://code.claude.com/docs/en/setup#authenticate)) |
| **Anthropic Console API key** | The notebook cells where YOUR Python code calls Claude — used from **Session 1** (grounding tests, earnings engine, workflows, the agent) | console.anthropic.com — separate account, pay-as-you-go | load **$5** of credit; the whole course typically uses **€1–2** |

A Pro subscription does not include API credits, and API credits don't include
the Pro app — you need both. Same email for both accounts is fine.

**Is Pro enough for the course?** Yes, comfortably. Its usage limits are sized
for exactly our lab profile — short coding sprints in small codebases — and
this course's labs are 30-minute sessions on single-file scripts. If you ever
hit a limit mid-lab anyway, see "What if" below.

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

(Alternatives, pick the one for YOUR system — do not try the others:
macOS with Homebrew already installed → `brew install --cask claude-code`;
Windows → `winget install Anthropic.ClaudeCode`; any OS with Node.js
installed → `npm install -g @anthropic-ai/claude-code`. `brew` and `winget`
are each tied to one operating system — running the wrong one always fails
with a "not recognized" error, which does not mean anything is broken.
Full options: https://code.claude.com/docs/en/setup)

Then run `claude` and log in.

## Using Claude in VS Code instead? Same thing — here's your version

The VS Code extension (Extensions view → search **"Claude Code"** → Install)
is the same Claude Code with a graphical panel — same paid-account
requirement, same behavior, and every prompt in this course works identically
there. If the first pre-course set you up this way, you're set. To verify:

1. Open the course repo folder in VS Code (**File → Open Folder** — Claude
   reads the repo's `CLAUDE.md` from there).
2. Open the panel: the **✱ Claude icon** in the editor toolbar (top-right,
   with a file open) or **✱ Claude Code** in the bottom status bar.
3. First time: click **Sign in** — use your **Pro** account.

**⚠️ Are you in the RIGHT chat?** Most VS Code setups have several AI panels
(GitHub Copilot, Gemini, others). If your chat shows model names like GPT or
Gemini, or a "credits" counter, you are in a **different extension** — the
course labs won't behave as described there. The Claude Code panel is the one
opened by the **✱** icon where `/status` shows your Claude account. Quick
self-test: with nothing selected or attached, ask *"What is the one rule that
always applies in this repo?"* — Claude Code answers from the repo's
CLAUDE.md by itself (never present an unverified number).

**Recommended: mute Copilot for the course.** Two cases:

- *Copilot installed as an extension:* `Cmd+Shift+X` → search "copilot" →
  gear ⚙️ → **Disable (Workspace)** → reload. Stays available elsewhere.
- *No Copilot extension but the GPT chat is still there:* that's VS Code's
  **built-in** Copilot chat (on by default in current VS Code). Hide it:
  click the chat icon in the top title bar → **Hide Copilot**, or Settings
  (`Cmd+,`) → search `chat.commandCenter` → untick.

Then drag the Claude panel to the right sidebar — where that chat used to
sit — so old habits land in the right place.

**No ✱ icon anywhere?** The Claude Code extension simply isn't installed —
don't assume the pre-course did it: `Cmd+Shift+X` → search **"Claude Code"**
(publisher: Anthropic) → Install → click the ✱ → Sign in with your Pro
account → `/status` shows Pro. Two minutes.

Two extension facts worth knowing:

- **It bundles its own copy of Claude Code**, so the `claude` terminal
  command may not exist on your machine. That's fine — our environment
  checker treats it as a non-issue. (You still run the course's *Python
  scripts* in the integrated terminal as usual.)
- **The killer feature for our labs:** select code in the editor (e.g. a
  TODO docstring) and press `Option+K` (Mac) / `Alt+K` (Windows) — it inserts
  an @-mention of that file and line range into your prompt. Fastest way to
  say "implement THIS".

Prefer the terminal look inside VS Code? Settings → Extensions → Claude Code
→ check **Use Terminal**.

## 3. Create the API key (5 minutes — needed from Day 1)

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
