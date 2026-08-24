---
marp: true
paginate: true
theme: default
---

# AI-Augmented Productivity for Finance

IESE MiF · Prof. Sara Bisbe

- **The goal of the two days**: a working AI financial analyst, built by you
- **Format**: you build it on your own laptop, session by session
- **The result is a portfolio**: everything you build leaves with you

---

# Part 1 · Course overview

---

# Five sessions, one system

| Session | You build | The skill |
|---|---|---|
| **1 · Prompting** | grounded prompts | a model that refuses rather than guesses |
| **2 · Coding copilot** | Apple valued against its peers | direct Claude Code; verify its work |
| **3 · Debugging & analytics** | that valuation, repaired + an earnings engine | prove a number is right |
| **4 · Workflows** | a company screening engine on live SEC filings | code decides; the model explains |
| **5 · Agents** | a governed agent, published on GitHub + capstone | the model plans, within your limits |

SEC = the U.S. Securities and Exchange Commission, whose public filing
database supplies the course's data.

---

# Agenda

| | Monday | Tuesday |
|---|---|---|
| 9:00 | **1 · Prompting** and financial reasoning | **4 · Workflows** on live SEC data |
| 10:30 | **2 · Claude Code** as coding copilot | **5 · Agents** + your capstone |
| 12:00 | **3 · Debugging**, testing, analytics | |

- **Capstone**: submitted Tuesday — your repository URL plus a one-page memo
  of your workflow.

---

# The libraries you will use

| | Library | Standing |
|---|---|---|
| Data | `pandas` · `numpy` | the industry standards for data and numerical work |
| Charts | `plotly` | best in class for interactive visuals |
| Testing & validation | `pytest` · `pydantic` | the standard test runner; the standard validation library |
| Claude | `anthropic` · **PydanticAI** | the official SDK; a state-of-the-art agent framework |
| Workflows | **LangGraph** | the industry standard for AI pipelines, from the LangChain ecosystem |

Each appears exactly when its job appears — nothing is used before it is explained.

---

# Part 2 · How every session works

---

# The session rhythm, identical all five times

```
  I explain  →  we run it  →  you build  →  a check confirms it is right
  (concepts)     (live)       (the lab)      (green means continue)
```

| Segment | Minutes |
|---|---|
| Concepts, with runnable demonstrations | 10–15 |
| Live demonstration | 15–22 |
| **Your lab** — the largest block | 25–30 |
| Debrief and bridge to the next session | 5–8 |

---

# How the labs work

Every exercise sits between two markers. **You fill the gaps. Nothing else changes.**

```python
### START CODE HERE ###
df["revenue_growth_1y"] = df[None] / df[None] - 1
### END CODE HERE ###
```

- **`None`** → replace with the correct column, value or variable
- **`[QUESTION IN CAPITALS]`** → replace with the text the bracket asks for
- Run the **✅ check cell** below each exercise; green means correct, continue
- **When you are stuck**: ask the **✱ Claude panel** — using it well is part
  of what this course teaches

---

# Asking Claude about specific code

**`Option+K`** (Mac) / **`Alt+K`** (Windows) — the one shortcut to learn today.

```
1. highlight the lines you are asking about
2. press Option+K   →  the selection lands in the ✱ panel with its
                       address: file, cell, exact line numbers
3. type your question next to it, press Enter
```

- The answer is about **exactly those lines**, not about code in general
- Ask for the **cause before the fix**: *"explain why this fails before
  proposing a change"* — you learn the diagnosis, not just the patch
- Claude's edits arrive as a **diff**: read it, then accept or reject
- Shortcut not working? Copy the lines into the panel by hand — same result

---

# Your two AI tools, and how to tell them apart

| | **✱ Claude panel** | **API key in `.env`** |
|---|---|---|
| What | Your copilot in VS Code | Claude answering **your code** |
| Paid by | Pro subscription | Your $5 credit |
| Used for | Help while building | The tools you build |

API stands for application programming interface: the channel through which
your own code calls Claude. If a chat panel mentions GPT, Gemini or credits, it is VS Code's built-in
assistant, not the course tool. The course tool is always the **✱** panel.

---

# Part 3 · Setup — first 15 minutes, in class

---

# Setup: your first commands

Open VS Code → **Terminal → New Terminal**, and run:

```
git clone https://github.com/comtessa-sareta/iese-ai-finance-bootcamp-student.git
cd iese-ai-finance-bootcamp-student
```

Then: **File → Open Folder** → choose `iese-ai-finance-bootcamp-student`,
open **`setup/SETUP.md`**, and follow it top to bottom — it contains every
remaining command, in order.

- **Both lines matter**: `clone` downloads the folder, `cd` moves you *into*
  it. Every later command runs from inside — `ls` should show `requirements.txt`
- The link is also in the **Zoom chat**: click it there instead of typing
- `git` not found? `SETUP.md` step 0b covers installing it

---

# What SETUP.md walks you through

| Step | What | You already have |
|---|---|---|
| 0 | Accounts: Claude **Pro** + Anthropic **API key** ($5 credit) | Pro ✓ — a lost key is re-created in 30 seconds |
| 1 | Clone the course repository | Git, from the tools pre-course |
| 2 | Create the `aifinance` Python environment | Anaconda, from the pre-course |
| 3 | Put your keys in `.env` | — |
| 4 | Sign in to the **✱** Claude panel in VS Code | — |
| 5–6 | Verify: checker all `[ OK ]`, then notebook `00` all green | — |

**Copy-paste every command; never retype.**

---

# Setup: the finish line, and helping each other

- **Finished and green?** Raise your hand — then help a neighbor
- **Stuck more than 3 minutes?** Work on your neighbor's laptop; we repair
  yours at the break — nobody sits out
- Every failure message in the checker includes its own fix; the
  Troubleshooting section of `SETUP.md` covers the rest

---

# The one rule of this course

<br>

## Never ship a number you haven't verified.

<br>

- In finance, a confidently delivered wrong number carries serious professional consequences
- Everything we build makes verification **cheap, fast, automatic**
