"""Session 5 demo — Mini Investment Analyst Agent.

    python session-05-agents/demo/mini_analyst_agent.py \
        "Analyze Apple (AAPL) and compare it with Sony (SONY)."

    python session-05-agents/demo/mini_analyst_agent.py --preflight   # no API key:
                                                        # show system prompt + tools

WORKFLOW vs AGENT — the one-slide version:
    Session 4's workflow had a fixed plan written by us; the model filled in
    one step. An AGENT gets a goal and TOOLS, and decides for itself which
    tool to call next, in a loop, until it judges the goal met.

The loop below IS the agent. Everything else is tools and guardrails:
    - the model only sees data returned by tools (SEC EDGAR via toolkit.edgar)
    - code does the arithmetic (compare_metrics), the model does the judgment
    - hard limits: max steps, token budget
    - it must finish by calling record_recommendation (machine-readable output)
    - a human approves before anything is written to disk

Watch the trace when it runs on AAPL vs SONY: Sony files in JAPANESE YEN.
A naive agent compares 13 trillion to 416 billion and calls Sony 30x bigger.
The system prompt forces a currency check — that's governance in one line.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / ".env")
except ImportError:
    pass

from toolkit import edgar, llm  # noqa: E402

OUT_DIR = REPO_ROOT / "outputs"
MAX_STEPS = 12
TOKEN_BUDGET = 300_000  # hard stop — an agent without a budget is an incident report

SYSTEM = """You are an investment research agent for an educational exercise.

Operating rules:
1. PLAN first: say briefly which tools you will call and why.
2. Gather financials for EVERY company involved before comparing anything.
3. ALWAYS check the 'unit' field. Foreign filers report in local currency
   (JPY, DKK, EUR...). Never compare absolute amounts across different currencies —
   compare unitless measures (growth, margins) and say so explicitly.
4. Use compare_metrics for arithmetic. Do not compute numbers yourself.
5. Every figure you state must come from a tool result in this conversation.
6. If data is missing or ambiguous, say so — 'insufficient_data' is an
   acceptable stance and better than a confident guess.
7. Finish by calling record_recommendation EXACTLY ONCE. This is an analytical
   comparison for coursework, not investment advice.
"""

RECOMMENDATION_SCHEMA = {
    "type": "object",
    "required": ["headline", "stance", "key_points", "risks", "confidence",
                 "what_would_change_my_mind"],
    "properties": {
        "headline": {"type": "string"},
        "stance": {
            "type": "string",
            "enum": ["prefer_first", "prefer_second", "balanced", "insufficient_data"],
        },
        "key_points": {"type": "array", "minItems": 3, "items": {"type": "string"}},
        "risks": {"type": "array", "minItems": 2, "items": {"type": "string"}},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "what_would_change_my_mind": {"type": "string"},
    },
}

TOOLS = [
    {
        "name": "get_financials",
        "description": "Annual revenue, operating income and net income (last 4 "
                       "fiscal years) plus balance-sheet basics for a ticker, "
                       "from SEC EDGAR XBRL. Note the 'unit' field: foreign "
                       "filers report in local currency.",
        "input_schema": {
            "type": "object",
            "required": ["ticker"],
            "properties": {"ticker": {"type": "string", "description": "e.g. SONY"}},
        },
    },
    {
        "name": "list_recent_filings",
        "description": "Most recent SEC filings for a ticker (form, dates, URL).",
        "input_schema": {
            "type": "object",
            "required": ["ticker"],
            "properties": {
                "ticker": {"type": "string"},
                "forms": {"type": "array", "items": {"type": "string"},
                          "description": "e.g. ['10-K','20-F','8-K']; omit for all"},
            },
        },
    },
    {
        "name": "compare_metrics",
        "description": "Compute growth and margins side-by-side for several "
                       "tickers IN CODE. Returns per-company unit, revenue "
                       "growth, CAGR and margins. Use this for all arithmetic.",
        "input_schema": {
            "type": "object",
            "required": ["tickers"],
            "properties": {
                "tickers": {"type": "array", "minItems": 2,
                            "items": {"type": "string"}},
            },
        },
    },
    {
        "name": "record_recommendation",
        "description": "Record the final structured recommendation. Call exactly "
                       "once, when the analysis is complete.",
        "input_schema": RECOMMENDATION_SCHEMA,
    },
]


# ---------------------------------------------------------- tool implementations

def _metrics_row(ticker: str) -> dict:
    fin = edgar.annual_financials(ticker, n=4)
    rev = fin["revenue"]
    op = {v["fy_end"]: v["val"] for v in fin["operating_income"]}
    ni = {v["fy_end"]: v["val"] for v in fin["net_income"]}
    years = []
    for i, r in enumerate(rev):
        y = {"fy_end": r["fy_end"], "revenue": r["val"]}
        if i:
            y["revenue_growth"] = round(r["val"] / rev[i - 1]["val"] - 1, 4)
        if (o := op.get(r["fy_end"])) is not None:
            y["op_margin"] = round(o / r["val"], 4)
        if (n := ni.get(r["fy_end"])) is not None:
            y["net_margin"] = round(n / r["val"], 4)
        years.append(y)
    cagr = None
    if len(rev) >= 3:
        n_yrs = len(rev) - 1
        cagr = round((rev[-1]["val"] / rev[0]["val"]) ** (1 / n_yrs) - 1, 4)
    return {"ticker": fin["ticker"], "company": fin["company"], "unit": fin["unit"],
            "revenue_cagr": cagr, "years": years}


def tool_get_financials(args: dict) -> str:
    fin = edgar.annual_financials(args["ticker"], n=4)
    return json.dumps(fin, indent=1)


def tool_list_recent_filings(args: dict) -> str:
    filings = edgar.recent_filings(args["ticker"], forms=args.get("forms"), limit=8)
    return json.dumps(filings, indent=1)


def tool_compare_metrics(args: dict) -> str:
    rows = [_metrics_row(t) for t in args["tickers"]]
    units = {r["unit"] for r in rows}
    out = {"companies": rows}
    if len(units) > 1:
        out["warning"] = (
            f"UNITS DIFFER ({', '.join(sorted(units))}): absolute amounts are NOT "
            "comparable. Compare growth and margins only, or convert currency first."
        )
        print(f"⚠️  compare_metrics: UNITS DIFFER ({', '.join(sorted(units))}) — "
              "flagged to the agent")
    return json.dumps(out, indent=1)


TOOL_IMPLS = {
    "get_financials": tool_get_financials,
    "list_recent_filings": tool_list_recent_filings,
    "compare_metrics": tool_compare_metrics,
}


# ------------------------------------------------------------------ agent loop

def run_agent(task: str, max_steps: int = MAX_STEPS) -> tuple[dict | None, list[str]]:
    """The agent: a loop around (model decides) -> (code executes) -> repeat."""
    messages = [{"role": "user", "content": task}]
    trace: list[str] = []
    recommendation: dict | None = None

    for step in range(1, max_steps + 1):
        if llm.USAGE["input_tokens"] + llm.USAGE["output_tokens"] > TOKEN_BUDGET:
            trace.append(f"step {step}: TOKEN BUDGET EXCEEDED — aborting")
            print("🛑 token budget exceeded — stopping the agent")
            break

        resp = llm.client().messages.create(
            model=llm.default_model(), max_tokens=4096, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        llm._record_usage(resp)

        thinking = " ".join(b.text for b in resp.content if b.type == "text").strip()
        if thinking:
            print(f"🤖 step {step}: {thinking[:300]}{'…' if len(thinking) > 300 else ''}")

        tool_calls = [b for b in resp.content if b.type == "tool_use"]
        if not tool_calls:
            trace.append(f"step {step}: model stopped without record_recommendation")
            print("⚠️  agent ended without recording a recommendation")
            break

        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for call in tool_calls:
            print(f"🔧 step {step}: {call.name}({json.dumps(call.input)[:120]})")
            trace.append(f"step {step}: {call.name}({json.dumps(call.input)})")
            if call.name == "record_recommendation":
                # Trust the schema; verify anyway — malformed tool inputs are
                # rejected and sent back for correction, never rendered.
                errors = llm.validate(call.input, RECOMMENDATION_SCHEMA)
                if errors:
                    print(f"⚠️  step {step}: recommendation failed validation "
                          f"({len(errors)} error(s)) — sent back for correction")
                    trace.append(f"step {step}: record_recommendation REJECTED ({errors[:2]})")
                    results.append({
                        "type": "tool_result", "tool_use_id": call.id,
                        "content": "Validation failed:\n- " + "\n- ".join(errors)
                        + "\nCall record_recommendation again with input matching "
                        "the schema EXACTLY (key_points and risks are JSON arrays of strings).",
                    })
                    continue
                recommendation = call.input
                results.append({"type": "tool_result", "tool_use_id": call.id,
                                "content": "Recommendation recorded. You are done."})
                continue
            impl = TOOL_IMPLS.get(call.name)
            try:
                output = impl(call.input) if impl else f"ERROR: unknown tool {call.name}"
            except Exception as exc:  # tool errors go BACK to the model — it can adapt
                output = f"ERROR: {exc}"
            results.append({"type": "tool_result", "tool_use_id": call.id,
                            "content": output[:20_000]})
        messages.append({"role": "user", "content": results})

        if recommendation is not None:
            break
    else:
        print(f"🛑 hit max_steps={max_steps} — stopping the agent")

    return recommendation, trace


# ------------------------------------------------------------------ reporting

def render_memo(task: str, rec: dict, trace: list[str]) -> str:
    lines = [
        "# Agent research memo",
        "",
        f"**Task:** {task}",
        "",
        f"## {rec['headline']}",
        "",
        f"**Stance:** {rec['stance'].replace('_', ' ')} | **Confidence:** {rec['confidence']}",
        "",
        "## Key points", "",
        *[f"- {p}" for p in rec["key_points"]],
        "", "## Risks", "",
        *[f"- {r}" for r in rec["risks"]],
        "", "## What would change this view", "",
        rec["what_would_change_my_mind"],
        "", "## Audit trail (every tool call the agent made)", "",
        *[f"- {t}" for t in trace],
        "", "---",
        "*Coursework artifact (IESE AI-Finance bootcamp) — data: SEC EDGAR. "
        "Not investment advice.*", "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("task", nargs="?", default=(
        "Analyze Apple (ticker AAPL) and compare it with Sony (ticker SONY): "
        "which is better positioned on growth and profitability?"
    ))
    ap.add_argument("--preflight", "--dry-run", action="store_true",
                    help="print the agent's system prompt and tool catalog, then exit")
    ap.add_argument("--yes", action="store_true", help="skip the human save gate")
    ap.add_argument("--max-steps", type=int, default=MAX_STEPS)
    args = ap.parse_args()

    if args.preflight:
        print("SYSTEM PROMPT:\n" + SYSTEM)
        print("TOOLS:")
        for t in TOOLS:
            print(f"  - {t['name']}: {t['description'][:90]}")
        print(f"\nGuardrails: max_steps={args.max_steps}, token_budget={TOKEN_BUDGET:,}")
        return

    print(f"TASK: {args.task}\n")
    recommendation, trace = run_agent(args.task, args.max_steps)
    if recommendation is None:
        print("\nNo recommendation recorded — see trace above. (This is a finding, "
              "not a crash: agents must be allowed to fail visibly.)")
        return

    print("\n" + "=" * 70)
    print(f"RECOMMENDATION: {recommendation['headline']}")
    print(f"stance={recommendation['stance']}  confidence={recommendation['confidence']}")
    for p in recommendation["key_points"]:
        print(f"  • {p}")
    print(f"\nAgent made {len(trace)} tool call(s). Token usage: {llm.usage_summary()}")

    if not args.yes:
        answer = input("\nHuman gate — save this memo to outputs/? [y/N] ").strip().lower()
        if answer != "y":
            print("Not saved.")
            return
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / "agent_memo.md"
    path.write_text(render_memo(args.task, recommendation, trace), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
