---
marp: true
paginate: true
theme: default
---

# Session 3 · Debugging, Testing and Earnings

A model that crashes is annoying. A model that lies is expensive.

Plan: idea 12 min · live demo 22 min · your lab 30 min · debrief 8 min.

---

# Crashes are the friendly bugs

A crash announces itself: the last line of the error says what broke, the
marked line says where. You read it bottom up, you ask Claude to explain
the cause before touching anything, you change one thing, you run again.

The dangerous bug returns a number. No error, no warning, just a valuation
that is wrong. Those are the ones this session teaches you to catch.

---

# A test is finance, written as a rule

One line of finance: debt holders get paid first. One line of code: equity
value must equal enterprise value minus net debt. When the code violates
the finance, the test turns red and names the exact rule you broke.

The most valuable test uses inputs simple enough for a napkin: flat cash
flows, round rates. If your model cannot reproduce a number you computed by
hand, you do not have a model. You have a rumor.

---

# The broken model you will fix

Meridian Semiconductor, fictional, trades at 62 dollars. My model first
crashes. Repaired naively, it claims the stock is worth more than 115.

The six errors inside are real ones from real banks: the first year's cash
flow never discounted, the tax shield forgotten in the cost of debt, the
terminal value taken at face value although it sits five years away, net
debt added instead of subtracted, impossible growth accepted, a horizon
hardcoded.

Fixed correctly the answer is 75.61. Against a 62 dollar price, that is
where an investment conversation starts.

---

# Part two: an engine that demands evidence

You get an earnings call transcript. The company is fictional on purpose,
so the model cannot lean on memory. It must work from the document.

Your engine extracts sentiment, themes, risks and guidance, and every claim
must carry a word-for-word quote. Then your own Python checks each quote
against the transcript. A quote that is not in the document is a
fabrication, and your code flags it.

One quote in today's data is planted. Your engine catches it, or it is not
finished.

---

# Your lab · notebook 03 · 30 minutes

Exercises 1 to 4: build the four DCF functions. A test sits under each one,
and the final cell must say 75.61.

Exercise 5: build the quote checker. Then run the full engine and confirm
it flags exactly one fabricated quote.

---

# Remember this one

Green tests and a plausible number. You need both, always.

Tomorrow at 9:00 your code pulls live SEC filings by itself.
