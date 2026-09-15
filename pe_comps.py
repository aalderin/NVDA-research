"""P/E Comps Valuation Model (Standard Library Only).

Computes peer P/E multiples, summary statistics, target implied prices,
and leave-one-out sensitivity analysis.
"""

import statistics
from typing import Any, Dict, List, Optional

# ==============================================================================
# EDITABLE INPUTS (December 31, 2024 / FY2024 GAAP Diluted Data)
# ==============================================================================

TARGET: Dict[str, Any] = {
    "name": "Asbury Automotive",
    "ticker": "ABG",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS: List[Dict[str, Any]] = [
    {
        "name": "AutoNation",
        "ticker": "AN",
        "price": 169.84,
        "diluted_eps": 16.92,
    },
    {
        "name": "Group 1 Automotive",
        "ticker": "GPI",
        "price": 421.48,
        "diluted_eps": 36.81,
    },
]

# ==============================================================================
# CALCULATION & VALUATION ENGINE
# ==============================================================================


def is_positive_number(val: Any) -> bool:
    """Check if value is a valid numeric float/int greater than zero."""
    if val is None:
        return False
    try:
        return float(val) > 0.0
    except (ValueError, TypeError):
        return False


def format_multiple(multiple: Optional[float]) -> str:
    """Format multiple to 6 decimal places or mark not meaningful."""
    if multiple is None:
        return "not meaningful"
    return f"{multiple:.6f}x"


def format_price(price: Optional[float]) -> str:
    """Format price to cents ($XX.XX) or mark not meaningful."""
    if price is None:
        return "not meaningful"
    return f"${price:,.2f}"


def format_change(change: Optional[float]) -> str:
    """Format price change to cents with explicit sign."""
    if change is None:
        return "no estimate"
    sign = "+" if change > 0 else ("-" if change < 0 else " ")
    return f"{sign}${abs(change):,.2f}"


def deduplicate_and_filter_peers(
    peers: List[Dict[str, Any]], target: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Deduplicates peer entries and excludes the target company."""
    target_ticker = str(target.get("ticker", "")).strip().upper()
    target_name = str(target.get("name", "")).strip().upper()

    seen_keys = set()
    cleaned_peers = []

    for peer in peers:
        ticker = str(peer.get("ticker", "")).strip().upper()
        name = str(peer.get("name", "")).strip().upper()

        # Exclude target
        if (ticker and ticker == target_ticker) or (name and name == target_name):
            continue

        # Deduplicate
        key = ticker if ticker else name
        if not key or key in seen_keys:
            continue

        seen_keys.add(key)
        cleaned_peers.append(peer)

    return cleaned_peers


def main() -> None:
    print("=" * 72)
    print("PEER P/E COMPARABLE VALUATION ANALYSIS")
    print("=" * 72)

    # 1. Target Validation & Information
    target_name = TARGET.get("name", "Target")
    target_ticker = TARGET.get("ticker", "TARGET")
    target_price = TARGET.get("price")
    target_eps = TARGET.get("diluted_eps")

    target_price_valid = is_positive_number(target_price)
    target_eps_valid = is_positive_number(target_eps)

    target_pe = (
        (float(target_price) / float(target_eps))
        if (target_price_valid and target_eps_valid)
        else None
    )

    print(f"\nTarget Company: {target_name} ({target_ticker})")
    print(f"  Current Market Price : {format_price(target_price if target_price_valid else None)}")
    print(f"  FY2024 Diluted EPS   : {format_price(target_eps if target_eps_valid else None).replace('$', '$') if target_eps_valid else 'not meaningful'}")
    print(f"  Target Current P/E   : {format_multiple(target_pe)}")

    # 2. Peer Deduplication & Multiple Computation
    unique_peers = deduplicate_and_filter_peers(PEERS, TARGET)

    valid_peers: List[Dict[str, Any]] = []
    print("\n" + "-" * 72)
    print("PEER GROUP MULTIPLES")
    print("-" * 72)
    print(f"{'Peer Company':<28} {'Price':<12} {'Diluted EPS':<14} {'P/E Multiple':<16}")
    print("-" * 72)

    for peer in unique_peers:
        p_name = peer.get("name", "Peer")
        p_ticker = peer.get("ticker", "")
        display_label = f"{p_name} ({p_ticker})" if p_ticker else p_name
        p_price = peer.get("price")
        p_eps = peer.get("diluted_eps")

        p_price_valid = is_positive_number(p_price)
        p_eps_valid = is_positive_number(p_eps)

        if p_price_valid and p_eps_valid:
            pe_multiple = float(p_price) / float(p_eps)
            valid_peers.append(
                {
                    "label": display_label,
                    "ticker": p_ticker,
                    "price": float(p_price),
                    "eps": float(p_eps),
                    "pe": pe_multiple,
                }
            )
            print(
                f"{display_label:<28} {format_price(float(p_price)):<12} "
                f"{f'${float(p_eps):,.2f}':<14} {format_multiple(pe_multiple):<16}"
            )
        else:
            price_disp = format_price(float(p_price)) if p_price_valid else "not meaningful"
            eps_disp = f"${float(p_eps):,.2f}" if p_eps_valid else "not meaningful"
            print(f"{display_label:<28} {price_disp:<12} {eps_disp:<14} {'not meaningful':<16}")

    num_valid = len(valid_peers)
    print("-" * 72)
    print(f"Valid usable peers: {num_valid}")

    # 3. Implied Valuation Calculations
    print("\n" + "=" * 72)
    print("VALUATION RESULTS")
    print("=" * 72)

    if num_valid == 0:
        print("Result: no usable peers.")
        return

    peer_pes = [p["pe"] for p in valid_peers]
    min_pe = min(peer_pes)
    median_pe = statistics.median(peer_pes)
    max_pe = max(peer_pes)

    if not target_eps_valid:
        print("Target EPS is missing or nonpositive: implied prices are not meaningful.")
        print(f"Peer P/E Summary Multiples:")
        print(f"  Minimum P/E : {format_multiple(min_pe)}")
        print(f"  Median P/E  : {format_multiple(median_pe)}")
        print(f"  Maximum P/E : {format_multiple(max_pe)}")
        return

    target_eps_float = float(target_eps)
    full_median_price = median_pe * target_eps_float
    min_price = min_pe * target_eps_float
    max_price = max_pe * target_eps_float

    if num_valid == 1:
        print("Note: exactly one valid peer available (reference estimate, no range).\n")
        print(f"  Peer P/E Multiple      : {format_multiple(median_pe)}")
        print(f"  Implied Price per Share: {format_price(full_median_price)}")
    else:
        print(f"Peer P/E Summary Multiples & Implied Target Prices:")
        print(f"  {'Metric':<12} {'Peer P/E Multiple':<22} {'Implied Target Price':<20}")
        print(f"  {'-'*12} {'-'*22} {'-'*20}")
        print(f"  {'Minimum':<12} {format_multiple(min_pe):<22} {format_price(min_price):<20}")
        print(f"  {'Median':<12} {format_multiple(median_pe):<22} {format_price(full_median_price):<20}")
        print(f"  {'Maximum':<12} {format_multiple(max_pe):<22} {format_price(max_price):<20}")

    # 4. Leave-One-Out Sensitivity Analysis
    print("\n" + "=" * 72)
    print("LEAVE-ONE-OUT SENSITIVITY ANALYSIS")
    print("=" * 72)
    print(f"Full-peer baseline median-implied price: {format_price(full_median_price)}\n")
    print(f"{'Removed Peer':<28} {'Remaining Peers':<18} {'Remaining Implied Price':<25} {'Dollar Change':<15}")
    print("-" * 88)

    for i, removed in enumerate(valid_peers):
        remaining = [p["pe"] for j, p in enumerate(valid_peers) if j != i]
        removed_label = removed["label"]

        if not remaining:
            print(f"{removed_label:<28} {'0 remaining':<18} {'no estimate':<25} {'no estimate':<15}")
        else:
            rem_median_pe = statistics.median(remaining)
            rem_implied_price = rem_median_pe * target_eps_float
            dollar_change = rem_implied_price - full_median_price
            print(
                f"{removed_label:<28} {f'{len(remaining)} remaining':<18} "
                f"{format_price(rem_implied_price):<25} "
                f"{format_change(dollar_change):<15}"
            )

    print("=" * 88)
    print("Methodological Note: P/E multiplies target diluted EPS directly to arrive at")
    print("equity value per share. Cash and debt are never bridged with P/E multiples.")
    print("=" * 88)


if __name__ == "__main__":
    main()

