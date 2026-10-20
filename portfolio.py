"""Portfolio comparison using editable capital-market assumptions.

Standard library only. All results are calculated from the inputs below.
"""

from math import sqrt


# ---------------------------------------------------------------------------
# EDITABLE INPUTS
# ---------------------------------------------------------------------------

# Expected returns and volatilities are annual percentages.
SLEEVES = {
    "Treasury bills": {"expected_return": 3.5, "volatility": 0.5},
    "Treasury 10-year note": {"expected_return": 4.3, "volatility": 7.0},
    "Investment-grade bond fund": {"expected_return": 5.0, "volatility": 6.0},
    "Global equity index fund": {"expected_return": 8.0, "volatility": 16.0},
}

# Correlations are unitless. Every sleeve must have a row and column.
CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00,
        "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05,
        "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10,
        "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80,
        "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05,
        "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00,
        "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00,
        "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25,
        "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 6.5
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


# ---------------------------------------------------------------------------
# REUSABLE CALCULATIONS
# ---------------------------------------------------------------------------

def validate_inputs(sleeves, correlations):
    """Raise ValueError when inputs cannot form a valid correlation matrix."""
    assets = set(sleeves)
    if set(correlations) != assets:
        raise ValueError("Correlation table must contain exactly one row for every sleeve.")

    for asset, assumptions in sleeves.items():
        volatility = assumptions["volatility"]
        if volatility <= 0:
            raise ValueError(f"Volatility for {asset!r} must be greater than zero.")

    for left in sleeves:
        if set(correlations[left]) != assets:
            raise ValueError(
                f"Correlation row for {left!r} must contain exactly one value for every sleeve."
            )
        for right in sleeves:
            correlation = correlations[left][right]
            if not -1.0 <= correlation <= 1.0:
                raise ValueError(
                    f"Correlation for {left!r} and {right!r} is {correlation}; it must be between -1 and 1."
                )
            if correlation != correlations[right][left]:
                raise ValueError(
                    f"Correlation table is not symmetric: {left!r}/{right!r} does not match "
                    f"{right!r}/{left!r}."
                )


def covariance_matrix(sleeves, correlations):
    """Return covariance entries, in percentage-squared units, by sleeve pair."""
    return {
        left: {
            right: (
                correlations[left][right]
                * sleeves[left]["volatility"]
                * sleeves[right]["volatility"]
            )
            for right in sleeves
        }
        for left in sleeves
    }


def benchmark_weights(sleeves):
    """Return the 40% investment-grade bond / 60% equity benchmark."""
    weights = {asset: 0.0 for asset in sleeves}
    weights["Investment-grade bond fund"] = 40.0
    weights["Global equity index fund"] = 60.0
    return weights


def equal_weight_weights(sleeves):
    """Return weights equally split across every sleeve."""
    return {asset: 100.0 / len(sleeves) for asset in sleeves}


def inverse_volatility_weights(sleeves):
    """Return weights proportional to one divided by volatility."""
    inverse_volatility = {
        asset: 1.0 / assumptions["volatility"]
        for asset, assumptions in sleeves.items()
    }
    total = sum(inverse_volatility.values())
    return {asset: value / total * 100.0 for asset, value in inverse_volatility.items()}


def expected_return(weights, sleeves):
    """Return the portfolio's annual expected return as a percentage."""
    return sum(
        weights[asset] / 100.0 * sleeves[asset]["expected_return"]
        for asset in sleeves
    )


def portfolio_volatility(weights, covariances):
    """Return portfolio annual volatility as a percentage."""
    variance = sum(
        weights[left] / 100.0 * weights[right] / 100.0 * covariances[left][right]
        for left in weights
        for right in weights
    )
    return sqrt(variance)


def reserve_eligible_weight(weights, reserve_eligible):
    """Return the combined percent weight in reserve-eligible sleeves."""
    return sum(weights[asset] for asset in reserve_eligible)


def meets_objective(portfolio_expected_return, objective_return):
    """Return whether expected return is at least the stated objective."""
    return portfolio_expected_return >= objective_return


def print_portfolio(name, weights, sleeves, covariances, objective_return, reserve_eligible):
    """Print all requested metrics for one portfolio."""
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariances)
    reserve_weight = reserve_eligible_weight(weights, reserve_eligible)
    weights_text = ", ".join(f"{asset}: {weight:.1f}%" for asset, weight in weights.items())
    objective_result = "Yes" if meets_objective(result_return, objective_return) else "No"

    print(name)
    print(f"  Weights: {weights_text}")
    print(f"  Expected return: {result_return:.2f}%")
    print(f"  Volatility: {result_volatility:.2f}%")
    print(f"  Reserve-eligible weight: {reserve_weight:.1f}%")
    print(f"  Meets {objective_return:.1f}% objective: {objective_result}")


def main():
    """Validate inputs, build covariance, and compare the three portfolios."""
    try:
        validate_inputs(SLEEVES, CORRELATIONS)
    except ValueError as error:
        raise SystemExit(f"Input error: refusing to run. {error}")

    covariances = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark (40% IG bonds / 60% equity)": benchmark_weights(SLEEVES),
        "Equal weight": equal_weight_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }

    for name, weights in portfolios.items():
        print_portfolio(
            name, weights, SLEEVES, covariances, OBJECTIVE_RETURN, RESERVE_ELIGIBLE
        )
        print()


if __name__ == "__main__":
    main()
