"""Five-year FCFF discounted cash flow calculator (USD millions)."""

# Editable inputs
STARTING_FCFF = 96896.0  # USD millions
GROWTH_RATES = [0.30, 0.25, 0.20, 0.15, 0.10]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 62556.0  # USD millions
DEBT = 8468.0  # USD millions
DILUTED_SHARES = 24514.0  # millions

# Editable sensitivity and reverse-DCF inputs
SENSITIVITY_WACC_VALUES = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 218.06


def value_per_share(wacc, terminal_growth, growth_rates):
    """Return the DCF value per diluted share for one set of assumptions."""
    if terminal_growth >= wacc:
        return None

    current_fcff = STARTING_FCFF
    pv_explicit_fcff = 0.0
    for year, growth in enumerate(growth_rates, start=1):
        current_fcff *= 1 + growth
        pv_explicit_fcff += current_fcff / (1 + wacc) ** year

    terminal_value = current_fcff * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / (1 + wacc) ** len(growth_rates)
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    return (enterprise_value + NON_OPERATING_CASH - DEBT) / DILUTED_SHARES


def print_sensitivity_grid():
    """Print value per diluted share for WACC and terminal-growth combinations."""
    print("\nSensitivity: Value per Diluted Share")
    header = "WACC \\ Terminal Growth | " + " | ".join(
        f"{growth:.1%}" for growth in SENSITIVITY_TERMINAL_GROWTH_VALUES
    )
    print(header)
    print("-" * len(header))

    for wacc in SENSITIVITY_WACC_VALUES:
        cells = []
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTH_VALUES:
            result = value_per_share(wacc, terminal_growth, GROWTH_RATES)
            cells.append("invalid" if result is None else f"${result:,.2f}")
        print(f"{wacc:.1%}".ljust(23) + " | " + " | ".join(cells))


def solve_uniform_growth_shift(target_share_price):
    """Solve for the common additive shift to all explicit growth rates."""
    minimum_shift = -min(GROWTH_RATES) + 1e-12
    lower_bound = minimum_shift
    upper_bound = 0.10

    def price_for_shift(shift):
        shifted_growth_rates = [growth + shift for growth in GROWTH_RATES]
        return value_per_share(WACC, TERMINAL_GROWTH, shifted_growth_rates)

    while price_for_shift(upper_bound) < target_share_price:
        upper_bound *= 2
        if upper_bound > 100:
            raise ValueError("Unable to bracket a reverse-DCF solution.")

    for _ in range(100):
        midpoint = (lower_bound + upper_bound) / 2
        if price_for_shift(midpoint) < target_share_price:
            lower_bound = midpoint
        else:
            upper_bound = midpoint

    return (lower_bound + upper_bound) / 2


def print_reverse_dcf():
    """Print the growth-rate shift required to reach the target share price."""
    shift = solve_uniform_growth_shift(TARGET_SHARE_PRICE)
    shifted_growth_rates = [growth + shift for growth in GROWTH_RATES]

    print("\nReverse DCF: Uniform Explicit-Growth-Rate Shift")
    print(f"Target share price: ${TARGET_SHARE_PRICE:,.2f}")
    print(f"Solved uniform shift: {shift:+.4%}")
    print("Implied growth rates: " + ", ".join(f"{growth:.4%}" for growth in shifted_growth_rates))
    print(
        "Inputs held fixed: "
        f"STARTING_FCFF={STARTING_FCFF:.1f}, WACC={WACC:.2%}, "
        f"TERMINAL_GROWTH={TERMINAL_GROWTH:.2%}, "
        f"NON_OPERATING_CASH={NON_OPERATING_CASH:.1f}, DEBT={DEBT:.1f}, "
        f"DILUTED_SHARES={DILUTED_SHARES:.1f}"
    )


def print_conditional_call():
    """Print the model-linked conditional investment call."""
    base_case_value = value_per_share(WACC, TERMINAL_GROWTH, GROWTH_RATES)
    print("\nConditional Investment Call")
    print(
        "Watch—defer. Initiate if NVIDIA trades at or below approximately "
        f"${base_case_value:,.2f} per share, the current base-case DCF value, "
        "or if sourced evidence supports increasing each of the five explicit "
        "FCFF growth assumptions by 2 percentage points. Otherwise, defer "
        f"initiation because the observed ${TARGET_SHARE_PRICE:,.2f} price "
        "requires growth above the current forecast path."
    )
    print("Monitor: next-quarter operating margin, using NVIDIA's quarterly earnings release and Form 10-Q.")


def main():
    if TERMINAL_GROWTH >= WACC:
        raise SystemExit(
            "Error: terminal growth must be less than WACC for the Gordon-growth formula."
        )

    if len(GROWTH_RATES) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")

    fcff = []
    current_fcff = STARTING_FCFF
    for growth in GROWTH_RATES:
        current_fcff *= 1 + growth
        fcff.append(current_fcff)

    pv_explicit_fcff = sum(
        cash_flow / (1 + WACC) ** year
        for year, cash_flow in enumerate(fcff, start=1)
    )
    terminal_value_year_5 = fcff[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value_year_5 / (1 + WACC) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share_of_ev = pv_terminal_value / enterprise_value

    for year, cash_flow in enumerate(fcff, start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"Present Value of Five Explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"Present Value of Terminal Value: {pv_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(f"PV Terminal Value as Share of Enterprise Value: {terminal_value_share_of_ev:.4f}")
    print_sensitivity_grid()
    print_reverse_dcf()
    print_conditional_call()


if __name__ == "__main__":
    main()
