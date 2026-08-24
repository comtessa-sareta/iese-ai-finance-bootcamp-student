"""Grounding checks: is the model inventing numbers?

Schema validation (llm.validate) proves the SHAPE is right. These helpers
check the SUBSTANCE: any figure appearing in model-written prose must trace
back to a number we actually supplied. Used in Sessions 4-5.
"""
from __future__ import annotations

import re

# Small counts and years read as narrative, not data — don't flag them.
_IGNORE_INTS = set(range(0, 11)) | set(range(1990, 2041))

# Dates and fiscal-year labels are context, not financial claims — strip them
# before extraction so '2024-01-28' doesn't flag as 28 and 'FY25' as 25.
_ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_FY_LABEL = re.compile(r"\bFY\s?\d{2,4}\b", re.IGNORECASE)


def numbers_in_text(text: str) -> list[float]:
    """Every numeric literal in a piece of prose ('58.3%', '-11.7bn', '2,410')."""
    text = _FY_LABEL.sub(" ", _ISO_DATE.sub(" ", text))
    out = []
    # (?<!\w) keeps a hyphen glued to a word from reading as a minus sign:
    # 'mid-2026' and the '2026' in '2025-2026' are years, not negative numbers.
    for m in re.findall(r"(?<!\w)-?\d[\d,]*(?:\.\d+)?", text):
        try:
            out.append(float(m.replace(",", "")))
        except ValueError:
            continue
    return out


def allowed_set(values: list[float]) -> list[float]:
    """Expand source values into the representations prose legitimately uses:
    raw, thousands/millions/billions rescalings, percentage form, either sign
    (prose may quote a loss as 11.7 or -11.7), and rounded."""
    allowed: set[float] = set()
    for v in values:
        if v is None:
            continue
        for base in (v, v / 1e3, v / 1e6, v / 1e9, v * 100):
            for scaled in (base, -base):
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
