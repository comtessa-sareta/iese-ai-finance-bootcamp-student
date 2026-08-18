"""Session 5 lab — AI Financial Research Agent (STARTER).

Build your own analyst agent for a company pair YOU choose (pharma, banking or
tech — any two SEC filers). The agent loop is given; you build what makes it
an analyst: the tools and the rules.

Check the skeleton without an API key:

    python session-05-agents/lab/research_agent_starter.py --preflight

Your work:
  TODO 1 — implement tool_get_financials() (toolkit.edgar does the heavy lifting)
  TODO 2 — implement tool_compare_metrics() with the units-differ warning
  TODO 3 — write the SYSTEM rules (plan, currency check, grounding,
           record_recommendation exactly once, insufficient_data allowed)
  TODO 4 — human gate: ask before saving the memo

Stretch:
  5 — add a save_note tool that appends to outputs/agent_notes.md (memory!)
  6 — add a token budget guard in the loop (see the demo)
  7 — add list_recent_filings and make the agent cite the latest 10-K date
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

# ---------------------------------------------------------------- TODO 3
SYSTEM = """You are an investment research agent for an educational exercise.
TODO: your operating rules here. Don't forget the currency check.
"""

RECOMMENDATION_SCHEMA = {
    "type": "object",
    "required": ["headline", "stance", "key_points", "risks", "confidence",
                 "what_would_change_my_mind"],
    "properties": {
        "headline": {"type": "string"},
        "stance": {"type": "string",
                   "enum": ["prefer_first", "prefer_second", "balanced", "insufficient_data"]},
        "key_points": {"type": "array", "minItems": 3, "items": {"type": "string"}},
        "risks": {"type": "array", "minItems": 2, "items": {"type": "string"}},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "what_would_change_my_mind": {"type": "string"},
    },
}

TOOLS = [
    {
        "name": "get_financials",
        "description": "Annual revenue, operating and net income (last 4 FYs) for "
                       "a ticker from SEC EDGAR. Mind the 'unit' field.",
        "input_schema": {
            "type": "object", "required": ["ticker"],
            "properties": {"ticker": {"type": "string"}},
        },
    },
    {
        "name": "compare_metrics",
        "description": "Growth and margins side-by-side, computed in code. "
                       "Use for ALL arithmetic.",
        "input_schema": {
            "type": "object", "required": ["tickers"],
            "properties": {"tickers": {"type": "array", "minItems": 2,
                                       "items": {"type": "string"}}},
        },
    },
    {
        "name": "record_recommendation",
        "description": "Record the final structured recommendation. Call exactly once.",
        "input_schema": RECOMMENDATION_SCHEMA,
    },
]


# ---------------------------------------------------------- tool implementations

def _metrics_row(ticker: str) -> dict:
    """Per-company metrics block (given — you did this math in Session 4)."""
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
    return {"ticker": fin["ticker"], "company": fin["company"],
            "unit": fin["unit"], "years": years}


def tool_get_financials(args: dict) -> str:
    """TODO 1 — call edgar.annual_financials(args['ticker'], n=4) and return it
    as a JSON string (the model reads strings, not dicts)."""
    raise NotImplementedError("TODO 1")


def tool_compare_metrics(args: dict) -> str:
    """TODO 2 — build [_metrics_row(t) for t in args['tickers']]; if the
    companies' units differ, add a loud 'warning' key telling the model that
    absolute amounts are not comparable — and print() the warning too, so the
    human watching the trace sees the trap being caught. Return JSON string."""
    raise NotImplementedError("TODO 2")


TOOL_IMPLS = {
    "get_financials": tool_get_financials,
    "compare_metrics": tool_compare_metrics,
}


# ------------------------------------------------------------------ agent loop
# (given — read it once, carefully: THIS is what "agent" means)

def run_agent(task: str, max_steps: int = MAX_STEPS) -> tuple[dict | None, list[str]]:
    messages = [{"role": "user", "content": task}]
    trace: list[str] = []
    recommendation: dict | None = None

    for step in range(1, max_steps + 1):
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
            print("⚠️  agent ended without recording a recommendation")
            break

        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for call in tool_calls:
            print(f"🔧 step {step}: {call.name}({json.dumps(call.input)[:120]})")
            trace.append(f"step {step}: {call.name}({json.dumps(call.input)})")
            if call.name == "record_recommendation":
                # Trust the schema; verify anyway — malformed tool inputs go
                # back to the model for correction, never into your memo.
                errors = llm.validate(call.input, RECOMMENDATION_SCHEMA)
                if errors:
                    print(f"⚠️  step {step}: recommendation failed validation — sent back")
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
            except Exception as exc:
                output = f"ERROR: {exc}"
            results.append({"type": "tool_result", "tool_use_id": call.id,
                            "content": output[:20_000]})
        messages.append({"role": "user", "content": results})
        if recommendation is not None:
            break
    return recommendation, trace


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("task", nargs="?", default=(
        "Analyze <COMPANY A> (ticker A) and compare it with <COMPANY B> "
        "(ticker B): which is better positioned on growth and profitability?"
    ))
    ap.add_argument("--preflight", action="store_true")
    args = ap.parse_args()

    if args.preflight:
        print("SYSTEM PROMPT:\n" + SYSTEM)
        print("TOOLS:")
        for t in TOOLS:
            print(f"  - {t['name']}: {t['description'][:90]}")
        return

    print(f"TASK: {args.task}\n")
    recommendation, trace = run_agent(args.task)
    if recommendation is None:
        return
    print(f"\nRECOMMENDATION: {recommendation['headline']}")
    print(f"stance={recommendation['stance']}  confidence={recommendation['confidence']}")
    print(f"Tool calls: {len(trace)} | Token usage: {llm.usage_summary()}")

    # TODO 4 — human gate: ask before writing outputs/agent_memo.md
    # (render however you like — see the demo's render_memo for one pattern)


if __name__ == "__main__":
    main()
