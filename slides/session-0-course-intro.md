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

# What you leave with

| Session | You build |
|---|---|
| 1 | **Reliably grounded prompts** with verifiable answers |
| 2 | **A comps tool** on your own GitHub |
| 3 | **A tested DCF** and an earnings engine with **fabrication detection** |
| 4 | **A company screener** on live SEC filings |
| 5 | **A governed AI agent**, with limits you define |

---

# How every session works

```
  I explain  →  we run it  →  you build  →  a check confirms it is right
   (short)      (live)       (fill gaps)     (green means continue)
```

- **The gaps**: code between `START CODE HERE` and `END CODE HERE`, with
  `None` and `[BLANKS]` for you to fill
- **The check**: a cell under each exercise; green means correct, and you
  continue at your own pace
- **When you are stuck**: ask the **✱ Claude panel** — using it well is part
  of what this course teaches

---

# Your two AI tools, and how to tell them apart

| | **✱ Claude panel** | **API key in `.env`** |
|---|---|---|
| What | Your copilot in VS Code | Claude answering **your code** |
| Paid by | Pro subscription | Your $5 credit |
| Used for | Help while building | The tools you build |

If a chat panel mentions GPT, Gemini or credits, it is VS Code's built-in
assistant, not the course tool. The course tool is always the **✱** panel.

---

# Agenda

| | Monday | Tuesday |
|---|---|---|
| 9:00 | **1 · Prompting** and financial reasoning | **4 · Workflows** on live SEC data |
| 10:30 | **2 · Claude Code** as coding copilot | **5 · Agents** + your capstone |
| 12:00 | **3 · Debugging**, testing, earnings | |

- **Capstone**: 5 minutes, Tuesday. Your workflow, running, on screen.

---

# The one rule of this course

<br>

## Never ship a number you haven't verified.

<br>

- In finance, a confidently delivered wrong number carries serious professional consequences
- Everything we build makes verification **cheap, fast, automatic**
