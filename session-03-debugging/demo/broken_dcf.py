"""Session 3 demo — a DCF model that is WRONG ON PURPOSE.

This values Meridian Semiconductor (MSH), the fictional company whose earnings
call you'll analyze in the lab. Meridian trades around $62. This model will
first crash, and once it runs, it will produce a confidently wrong valuation.

Your job (with Claude as copilot):
  1. Run it. Read the traceback. Fix the crash.
  2. Run the sanity tests:  python -m pytest session-03-debugging/demo/ -q
  3. Fix bugs until every test passes — fix THIS file in place.
  4. Only then look at the number and ask: does it make sense?

The docstrings describe the INTENDED behaviour — they are the spec.
Do not trust the code; trust the spec and the tests.
"""
from __future__ import annotations


def wacc(
    equity_weight: float,
    debt_weight: float,
    cost_of_equity: float,
    cost_of_debt: float,
    tax_rate: float,
) -> float:
    """Weighted average cost of capital.

    WACC = w_e * k_e  +  w_d * k_d * (1 - tax_rate)
    Debt is cheaper than it looks: interest is tax-deductible.
    """
    return equity_weight * cost_of_equity + debt_weight * cost_of_debt


def project_fcf(base_fcf: float, growth_rates: list[float]) -> list[float]:
    """Project free cash flow forward, one growth rate per projection year.

    project_fcf(100, [0.10, 0.10]) -> [110.0, 121.0]
    """
    flows = []
    fcf = base_fcf
    for year in range(5):
        fcf = fcf * (1 + growth_rates[year])
        flows.append(fcf)
    return flows


def terminal_value(final_fcf: float, terminal_growth: float, discount_rate: float) -> float:
    """Gordon growth terminal value, as of the END of the projection period.

    TV = FCF_final * (1 + g) / (r - g)
    Must reject g >= r: a company growing faster than its discount rate
    forever would be worth infinity (it isn't).
    """
    return final_fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)


def dcf_value(
    base_fcf: float,
    growth_rates: list[float],
    discount_rate: float,
    terminal_growth: float,
    net_debt: float,
    shares_outstanding: float,
) -> dict:
    """Full DCF: discount explicit flows and terminal value, bridge to equity.

    - Year t cash flow is discounted by (1 + r)^t with t = 1 for the FIRST year.
    - Terminal value sits at the end of year N: discount it by (1 + r)^N.
    - Equity value = enterprise value MINUS net debt.
    Returns enterprise_value, equity_value, per_share, pv_explicit, pv_terminal.
    """
    flows = project_fcf(base_fcf, growth_rates)

    pv_explicit = 0.0
    for t, fcf in enumerate(flows):
        pv_explicit += fcf / (1 + discount_rate) ** t

    tv = terminal_value(flows[-1], terminal_growth, discount_rate)
    pv_terminal = tv

    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + net_debt
    per_share = equity_value / shares_outstanding

    return {
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "per_share": per_share,
        "pv_explicit": pv_explicit,
        "pv_terminal": pv_terminal,
    }


# ----------------------------------------------------------------- inputs
# Meridian Semiconductor (fictional) — all figures in $ billions except shares.
MERIDIAN = {
    "base_fcf": 1.35,                       # last-twelve-months free cash flow
    "growth_rates": [0.30, 0.25, 0.20, 0.15],   # analyst FCF growth, years 1-5
    "terminal_growth": 0.025,
    "net_debt": 0.85,                       # total debt 1.5 - cash 0.65
    "shares_outstanding": 0.46,             # billions of shares
}
WACC_INPUTS = {
    "equity_weight": 0.85,
    "debt_weight": 0.15,
    "cost_of_equity": 0.115,
    "cost_of_debt": 0.055,
    "tax_rate": 0.21,
}
MARKET_PRICE = 62.00


if __name__ == "__main__":
    r = wacc(**WACC_INPUTS)
    result = dcf_value(discount_rate=r, **MERIDIAN)
    print(f"WACC:              {r:.2%}")
    print(f"PV explicit FCFs:  ${result['pv_explicit']:.2f}bn")
    print(f"PV terminal value: ${result['pv_terminal']:.2f}bn")
    print(f"Enterprise value:  ${result['enterprise_value']:.2f}bn")
    print(f"Equity value:      ${result['equity_value']:.2f}bn")
    print(f"Value per share:   ${result['per_share']:.2f}   (market: ${MARKET_PRICE:.2f})")
