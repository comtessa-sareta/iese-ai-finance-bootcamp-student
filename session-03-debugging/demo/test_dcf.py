"""Sanity tests for the DCF model — the financial logic, written as code.

Run from the repo root:

    python -m pytest session-03-debugging/demo/ -q

Against broken_dcf.py these tests FAIL. That is the point: each failure names
a specific piece of financial logic the model violates. Fix broken_dcf.py in
place until everything is green.

The most important test is the last one: it checks the whole model against a
case simple enough to compute by hand. If you can't hand-check your model on
SOME input, you don't have a model — you have a rumour.
"""
from __future__ import annotations

import pytest

from broken_dcf import dcf_value, project_fcf, terminal_value, wacc


def test_project_fcf_handles_any_horizon():
    """One growth rate per year — 3 rates in, 3 flows out (no hardcoded 5)."""
    flows = project_fcf(100.0, [0.10, 0.10, 0.10])
    assert len(flows) == 3
    assert flows[0] == pytest.approx(110.0)
    assert flows[2] == pytest.approx(133.1)


def test_wacc_uses_after_tax_cost_of_debt():
    """100% debt at 5% with 21% tax -> 3.95%, not 5%."""
    assert wacc(0.0, 1.0, 0.10, 0.05, 0.21) == pytest.approx(0.05 * 0.79)


def test_first_year_flow_is_discounted():
    """Money in a year is worth less than money now: PV(year 1) < FCF(year 1)."""
    result = dcf_value(
        base_fcf=100.0, growth_rates=[0.0], discount_rate=0.10,
        terminal_growth=0.0, net_debt=0.0, shares_outstanding=1.0,
    )
    assert result["pv_explicit"] == pytest.approx(100.0 / 1.10)


def test_terminal_value_is_discounted():
    """TV sits N years away — it must be brought back at (1+r)^N."""
    result = dcf_value(
        base_fcf=100.0, growth_rates=[0.0, 0.0], discount_rate=0.10,
        terminal_growth=0.0, net_debt=0.0, shares_outstanding=1.0,
    )
    undiscounted_tv = 100.0 / 0.10
    assert result["pv_terminal"] == pytest.approx(undiscounted_tv / 1.10**2)


def test_equity_value_subtracts_net_debt():
    """Debt holders get paid first: equity = EV - net debt."""
    with_debt = dcf_value(100.0, [0.0], 0.10, 0.0, net_debt=50.0, shares_outstanding=1.0)
    no_debt = dcf_value(100.0, [0.0], 0.10, 0.0, net_debt=0.0, shares_outstanding=1.0)
    assert with_debt["equity_value"] == pytest.approx(no_debt["equity_value"] - 50.0)


def test_rejects_terminal_growth_above_discount_rate():
    """g >= r means infinite value. The model must refuse, not divide."""
    with pytest.raises(ValueError):
        terminal_value(100.0, terminal_growth=0.12, discount_rate=0.10)


def test_matches_hand_calculation():
    """Flat FCF of 100, r = 10%, g = 0, 2 years — checkable on a napkin:
    PV explicit  = 100/1.1 + 100/1.21          = 173.55
    TV           = 100/0.10 = 1000, PV(TV)     = 1000/1.21 = 826.45
    EV           = 1000.00 exactly. Net debt 200 -> equity 800, 10 shares -> 80.
    """
    result = dcf_value(
        base_fcf=100.0, growth_rates=[0.0, 0.0], discount_rate=0.10,
        terminal_growth=0.0, net_debt=200.0, shares_outstanding=10.0,
    )
    assert result["enterprise_value"] == pytest.approx(1000.0, abs=0.01)
    assert result["equity_value"] == pytest.approx(800.0, abs=0.01)
    assert result["per_share"] == pytest.approx(80.0, abs=0.001)
