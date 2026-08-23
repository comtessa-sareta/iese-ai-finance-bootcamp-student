"""Claude API helpers for the bootcamp.

Three ways to call Claude, in increasing order of reliability:

1. ask()            — plain text in, plain text out (Session 1 style, via API)
2. ask_json()       — prompt-enforced JSON + validation + self-repair retries (Session 3)
3. ask_structured() — tool-forced JSON: the model MUST return arguments matching
                      your schema. The production pattern. (Sessions 4-5)

All functions read ANTHROPIC_API_KEY and ANTHROPIC_MODEL from the environment
(.env is loaded by the calling scripts). Token usage is accumulated in
USAGE so scripts can print what a run cost in tokens.
"""
from __future__ import annotations

import json
import os
import re

DEFAULT_MODEL_FALLBACK = "claude-sonnet-5"

_client = None
USAGE = {"input_tokens": 0, "output_tokens": 0, "calls": 0}


class LLMError(RuntimeError):
    pass


def default_model() -> str:
    return os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL_FALLBACK)


def _in_notebook() -> bool:
    try:
        from IPython import get_ipython

        shell = get_ipython()
        return shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"
    except Exception:  # noqa: BLE001 — IPython absent or not running
        return False


def show(text: str, title: str | None = None, width: int = 100) -> None:
    """Display model output in full, readably.

    Never truncate model output when a human is meant to judge it. In a notebook
    this renders the model's markdown (headings, tables, bullets) wrapped to the
    cell width; in a plain terminal it wraps to `width` characters. Either way you
    see the whole answer without scrolling sideways.
    """
    if _in_notebook():
        from IPython.display import Markdown, display

        display(Markdown(f"**{title}**\n\n{text}" if title else text))
        return
    import textwrap

    if title:
        print(f"\n=== {title} ===")
    for para in text.split("\n"):
        print(textwrap.fill(para, width=width) if para.strip() else "")


def client():
    """Lazy Anthropic client with a friendly error if the key is missing."""
    global _client
    if _client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise LLMError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env, add your "
                "key, and re-run. (Scripts also accept --dry-run to skip API calls.)"
            )
        from anthropic import Anthropic

        _client = Anthropic()
    return _client


def _friendly(exc: Exception) -> Exception:
    """Translate the most common API errors into instructions students can act on."""
    msg = str(exc)
    if "reached your specified API usage limits" in msg:
        return LLMError(
            "Your Anthropic Console account has hit its configured monthly usage "
            "limit, so the API refused the call. Fix: console.anthropic.com -> "
            "Settings -> Limits -> raise the monthly limit (or wait for the reset "
            "date in the original message). Then re-run this cell."
        )
    if "credit balance is too low" in msg:
        return LLMError(
            "Your Anthropic Console account has no credit, so the API refused the "
            "call. Fix (1 minute): console.anthropic.com -> Billing -> add $5 "
            "(the whole course uses about 1-2 euros). If you have another key with "
            "credit, put that one in .env instead. Then re-run this cell."
        )
    if "authentication" in msg.lower() or "invalid x-api-key" in msg.lower():
        return LLMError(
            "The API key in your .env was rejected. Create a fresh key at "
            "console.anthropic.com -> API Keys (30 seconds, free), paste it into "
            ".env, save, and re-run this cell."
        )
    return exc


def _record_usage(resp) -> None:
    try:
        USAGE["input_tokens"] += resp.usage.input_tokens
        USAGE["output_tokens"] += resp.usage.output_tokens
        USAGE["calls"] += 1
    except AttributeError:
        pass


def usage_summary() -> str:
    return (
        f"{USAGE['calls']} API call(s), "
        f"{USAGE['input_tokens']:,} input / {USAGE['output_tokens']:,} output tokens"
    )


def ask(
    prompt: str,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int = 2048,
) -> str:
    """Single-turn text completion.

    Note: no `temperature` knob — Claude 5-generation models reject the
    parameter (HTTP 400, 'temperature is deprecated for this model').
    Output discipline comes from schemas and verification, not sampling.
    """
    kwargs: dict = {
        "model": model or default_model(),
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    try:
        resp = client().messages.create(**kwargs)
    except Exception as exc:  # noqa: BLE001 - translate, then re-raise
        raise _friendly(exc) from exc
    _record_usage(resp)
    text = "".join(b.text for b in resp.content if b.type == "text")
    if not text.strip():
        # Current models reason before answering; that reasoning counts against
        # max_tokens. A tight cap can therefore be spent entirely on reasoning,
        # leaving no visible answer. Say so plainly instead of returning "".
        return (f"[no visible answer: the response reached max_tokens={max_tokens} "
                f"before producing text (stop_reason={resp.stop_reason}). "
                "Raise max_tokens and run the cell again.]")
    return text


# ------------------------------------------------------------ JSON handling

def extract_json(text: str) -> str:
    """Pull a JSON object out of a model reply (handles ```json fences and prose)."""
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        return fence.group(1)
    start = text.find("{")
    if start == -1:
        raise LLMError("No JSON object found in model reply")
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise LLMError("Unbalanced JSON object in model reply")


def validate(obj, schema: dict, path: str = "$") -> list[str]:
    """Tiny JSON-Schema-subset validator (type, required, properties, items, enum).

    Returns a list of human-readable errors — empty list means valid. Deliberately
    small so students can read every line: this is what 'validate the output'
    actually means in code.
    """
    errors: list[str] = []
    expected = schema.get("type")
    type_map = {
        "object": dict, "array": list, "string": str,
        "number": (int, float), "integer": int, "boolean": bool,
    }
    if expected:
        py = type_map.get(expected)
        if py and not isinstance(obj, py) or (expected == "number" and isinstance(obj, bool)):
            errors.append(f"{path}: expected {expected}, got {type(obj).__name__}")
            return errors
    if "enum" in schema and obj not in schema["enum"]:
        errors.append(f"{path}: {obj!r} not in allowed values {schema['enum']}")
    if expected == "object":
        for key in schema.get("required", []):
            if key not in obj:
                errors.append(f"{path}: missing required key '{key}'")
        for key, sub in schema.get("properties", {}).items():
            if key in obj:
                errors.extend(validate(obj[key], sub, f"{path}.{key}"))
    if expected == "array":
        if "minItems" in schema and len(obj) < schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} items, got {len(obj)}")
        items = schema.get("items")
        if items:
            for i, item in enumerate(obj):
                errors.extend(validate(item, items, f"{path}[{i}]"))
    return errors


def ask_json(
    prompt: str,
    schema: dict,
    system: str | None = None,
    retries: int = 2,
    **kwargs,
) -> dict:
    """Prompt-enforced JSON with a self-repair loop.

    If the reply isn't valid JSON or fails schema validation, the errors are sent
    back to the model and it gets another try. Raises LLMError when out of retries.
    """
    full_prompt = (
        f"{prompt}\n\n"
        "Respond with ONLY a JSON object (no prose, no markdown fences) that "
        f"matches this JSON schema exactly:\n{json.dumps(schema, indent=2)}"
    )
    messages = [{"role": "user", "content": full_prompt}]
    for attempt in range(retries + 1):
        call: dict = {
            "model": kwargs.get("model") or default_model(),
            "max_tokens": kwargs.get("max_tokens", 4096),
            "messages": messages,
        }
        if system:
            call["system"] = system
        try:
            resp = client().messages.create(**call)
        except Exception as exc:  # noqa: BLE001
            raise _friendly(exc) from exc
        _record_usage(resp)
        text = "".join(b.text for b in resp.content if b.type == "text")
        try:
            obj = json.loads(extract_json(text))
            errors = validate(obj, schema)
        except (json.JSONDecodeError, LLMError) as exc:
            errors = [str(exc)]
            obj = None
        if obj is not None and not errors:
            return obj
        messages.append({"role": "assistant", "content": text})
        messages.append({
            "role": "user",
            "content": (
                "Your previous reply failed validation:\n- "
                + "\n- ".join(errors)
                + "\nReturn ONLY the corrected JSON object."
            ),
        })
    raise LLMError(f"Model output failed validation after {retries + 1} attempts: {errors}")


def ask_pydantic(prompt: str, model_cls, **kwargs):
    """Tool-forced structured output, validated into a Pydantic model.

    Pydantic is the industry-standard validation library (the anthropic SDK
    itself is built on it). This helper derives the JSON schema from your
    model class, forces the tool call through ask_structured, then parses the
    result into a typed instance - so downstream code gets attributes, types
    and validation errors instead of a raw dict.
    """
    schema = model_cls.model_json_schema()
    name = kwargs.pop("name", model_cls.__name__.lower())
    raw = ask_structured(prompt, name=name, schema=schema, **kwargs)
    return model_cls.model_validate(raw)


def ask_structured(
    prompt: str,
    name: str,
    schema: dict,
    description: str = "Record the structured analysis result.",
    system: str | None = None,
    model: str | None = None,
    max_tokens: int = 4096,
    retries: int = 2,
) -> dict:
    """Tool-forced structured output, VERIFIED and self-repairing.

    We define one tool whose input schema IS our desired output schema, then
    force the model to 'call' it. Tool-forcing makes conforming output very
    likely — but not certain (models occasionally return an array of strings
    where objects were required). So we validate the input against the schema
    ourselves and, on failure, send the errors back as the tool result and let
    the model correct itself. Trust the schema; verify anyway.
    """
    messages: list[dict] = [{"role": "user", "content": prompt}]
    errors: list[str] = []
    for _attempt in range(retries + 1):
        kwargs: dict = {
            "model": model or default_model(),
            "max_tokens": max_tokens,
            "messages": messages,
            "tools": [{"name": name, "description": description, "input_schema": schema}],
            "tool_choice": {"type": "tool", "name": name},
        }
        if system:
            kwargs["system"] = system
        try:
            resp = client().messages.create(**kwargs)
        except Exception as exc:  # noqa: BLE001
            raise _friendly(exc) from exc
        _record_usage(resp)
        blocks = [b for b in resp.content if b.type == "tool_use"]
        if not blocks:
            raise LLMError("Model did not return the forced tool call")
        for block in blocks:  # the model may call more than once — take any valid one
            if block.name == name:
                errors = validate(block.input, schema)
                if not errors:
                    return block.input
        # None valid: the API requires a tool_result for EVERY tool_use block
        # in the assistant turn, so answer each of them with the errors.
        feedback = (
            "Your tool input failed validation:\n- " + "\n- ".join(errors)
            + "\nCall the tool again ONCE, with input matching the schema EXACTLY "
            "(arrays must be real JSON arrays of the specified item type)."
        )
        messages.append({"role": "assistant", "content": resp.content})
        messages.append({
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": b.id, "content": feedback}
                for b in blocks
            ],
        })
    raise LLMError(f"Structured output failed validation after {retries + 1} attempts: {errors}")
