---
marp: true
paginate: true
theme: default
---

# Session 2 · Claude Code as Your Coding Copilot

Goal today: ship your first finance tool to GitHub. Before lunch.

Plan: idea 15 min · live demo 22 min · your lab 30 min · debrief 8 min.

---

# You are the analyst in charge

Claude writes code fast. Speed is not the skill. The skill is staying in
charge, and it has four habits.

Ask small: one function per request, so you can review what comes back.
Read before you run: code you cannot explain is code you cannot defend.
Verify one number by hand: pick one cell of every table and check it on a
calculator, every time, forever.
Commit at every green moment: each commit is an undo button.

---

# Pandas in one idea

A DataFrame is your spreadsheet, controlled by commands instead of clicks.

Columns operate on whole columns: revenue divided by shares gives you every
company's number at once. That single idea covers most of what analysts do
in pandas. The rest you ask the panel for. Nobody memorizes pandas.

---

# Why we clean data explicitly

Today's file holds ten real companies from real SEC filings, plus eight
defects I planted from real life: text where numbers should be, a duplicate
row, missing values, a junk total row.

The dangerous one: a single company reported in billions while the rest are
in millions. Miss it and every ratio for that company is wrong by a factor
of one thousand. Python raises no error. Silence is why every cleaning step
we write announces itself with a print.

---

# The vocabulary of comps

EBITDA is operating income plus depreciation and amortization: profit
before financing choices and accounting age.

Enterprise value is market cap plus debt minus cash: the price of the whole
business, not just the shares.

EV to EBITDA, EV to Sales, and P E answer the same question: how much am I
paying per unit of performance? When earnings are negative the answer is
meaningless, so professionals write n.m. instead. A negative multiple in a
table marks you as an amateur.

---

# Your lab · notebook 02 · 30 minutes

Exercise 1: growth and margins.
Exercise 2: market cap, enterprise value, the three multiples.
Exercise 3: the summary table with a median row.

Then the habit that outlives this course: verify Apple's EV to EBITDA on a
calculator, from the raw file. Only then trust the rest of the table.

Finish by pushing the tool to your own GitHub. Your first shipped project.

---

# Remember this one

Intel shows n.m. today. That is your code being right, not broken.

At 12:00 I hand you a valuation model that is wrong on purpose.
