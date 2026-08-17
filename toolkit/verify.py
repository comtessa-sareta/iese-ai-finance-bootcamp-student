"""Grounding checks: is the model inventing numbers?

Schema validation (llm.validate) proves the SHAPE is right. These helpers
check the SUBSTANCE: any figure appearing in model-written prose must trace
back to a number we actually supplied. Used in Sessions 4-5.
"""
from __future__ import annotations

import re

# Small counts and years read as narrative, not data — don't flag them.
_IGNORE_INTS = set(range(0, 11)) | set(range(1990, 2041))


def numbers_in_text(text: str) -> list[float]:
    """Every numeric literal in a piece of prose ('58.3%', '2,410', '1.9bn')."""
    out = []
    for m in re.findall(r"\d[\d,]*(?:\.\d+)?", text):
        try:
            out.append(float(m.replace(",", "")))
        except ValueError:
            continue
    return out


def allowed_set(values: list[float]) -> list[float]:
    """Expand source values into the representations prose legitimately uses:
    raw, thousands/millions/billions rescalings, percentage form, and rounded."""
    allowed: set[float] = set()
    for v in values:
        if v is None:
            continue
        for scaled in (v, v / 1e3, v / 1e6, v / 1e9, v * 100, abs(v), abs(v) * 100):
            allowed.add(round(scaled, 2))
            allowed.add(round(scaled, 1))
            allowed.add(round(scaled))
    return sorted(allowed)


def novel_numbers(text: str, source_values: list[float], rel_tol: float = 0.015) -> list[float]:
    """Numbers in `text` that do NOT correspond to any supplied source value.

    A number passes if it is within rel_tol of some allowed representation
    (covers the model rounding 38.4% to 'about 38%'). Returns the offenders —
    an empty list means the prose is numerically grounded.
    """
    allowed = allowed_set(source_values)
    offenders = []
    for n in numbers_in_text(text):
        if n in _IGNORE_INTS:
            continue
        ok = any(
            abs(n - a) <= rel_tol * max(abs(a), 1e-9) or abs(n - a) < 0.05
            for a in allowed
        )
        if not ok:
            offenders.append(n)
    return offenders
