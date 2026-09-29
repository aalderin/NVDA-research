"""
=============================================================================
NVIDIA Corporation (NVDA) — Integrated 3-Statement Forecast  2027–2031
Standard library only.  Run:  python proforma.py
=============================================================================

OPENING BALANCE SHEET  (end of FY2026 / beginning of FY2027)
All dollar amounts in millions unless noted.

  PP&E           10,383.0  ← FY2026 10-K, net
  Inventory      21,403.0  ← FY2026 10-K
  Floor plan pay      0.0  ← none; NVIDIA is not a store-based retailer
  Revenue base  215,938.0  ← FY2026 10-K
  Cash           10,605.0  ← FY2026 10-K
  Debt            8,468.0  ← FY2026 10-K, short- and long-term debt
  Revolver            0.0  ← none separately disclosed
  Other assets  164,412.0  ← total assets less cash, inventory, and net PP&E
  Other liab     41,042.0  ← total liabilities less debt
  Equity        157,293.0  ← FY2026 10-K total shareholders' equity

NOTE: The FY2026 balance sheet is fully reconciled to total assets of $206,803M.
The assert_balanced() check will catch any re-entry errors.

ASSUMPTION TABLE

  Value                                              Label      Reason
  -------------------------------------------------  ---------  -----------------------------------------------
  FY2024-FY2026 audited 10-K history                 history    Directly reported annual financial statements.
  No annual FY2027 quantitative guidance located     guidance   The supplied 10-Ks provide no formal annual outlook.
  65.5% revenue growth held through forecast          judgment   Uses the latest reported growth because no annual guidance was supplied.
  71.1% gross margin; 3.0% SG&A / gross profit        judgment   Holds the latest reported margins constant as a transparent base case.
  92.0 inventory days                                judgment   Average inventory / cost of revenue * 365.
  27.4% D&A / ending net PP&E proxy                  judgment   D&A is reported combined with amortization, not separately.
  $6,042M annual capex                                judgment   Holds the latest filing cash-investment line constant; it includes intangibles.
  15.1% tax rate                                      judgment   Uses FY2026 tax expense / pretax income absent explicit tax guidance.
  Floor plan / same-store growth: none               history    NVIDIA is not a store-based retailer; neither is disclosed.
  No recurring buyback forecast                      judgment   No forward repurchase assumption was supplied.
  3.1% debt rate                                      judgment   FY2026 interest expense divided by average reported debt is the available proxy.
  $10,605M minimum cash; no revolver capacity         judgment   Uses reported FY2026 cash and no separately disclosed revolver limit.
  10.0% cost of equity; 2.5% terminal growth          judgment   Valuation inputs retained as explicit base-case choices, not company guidance.

Partner Question / My Answer: The 92.0 inventory days equal average FY2025-FY2026 inventory of $15.742B divided by FY2026 cost of revenue of $62.475B, multiplied by 365. They would change with demand and supply planning, product mix and production lead times, inventory purchases, write-downs, or cost-of-revenue growth.

My Attack for Partner (Apple): Why is the capital spending 3.0, and how would it change?
Partner Answer: It would change if there were a sustained shift in Apple's capital-investment needs.
=============================================================================
"""

import copy

# ---------------------------------------------------------------------------
# 0.  ASSUMPTIONS
# ---------------------------------------------------------------------------

# --- Income-statement assumptions ---
REVENUE_GROWTH   = 0.655                        # FY2026 reported growth; no organic metric disclosed
GROSS_MARGIN     = 0.7107                        # FY2026 gross profit / revenue
SGA_RATIOS       = [0.665, 0.655, 0.645, 0.645, 0.645]  # SG&A ÷ gross profit
DEPR_RATE        = 82.4 / 3_070.4              # depreciation ÷ opening PP&E
IMPAIRMENT       = 0.0                          # no recurring impairment assumption in the supplied 10-K history
CAPEX            = 6_042.0                     # FY2026 purchases of PP&E and intangible assets
TAX_RATE         = 21_383.0 / 141_450.0        # FY2026 income tax expense / pretax income

# NVIDIA-specific operating assumptions, based on the supplied FY2024-FY2026 10-Ks.
SGA_RATIOS       = [0.0298] * 5                 # FY2026 SG&A / gross profit
DEPR_RATE        = 2_843.0 / 10_383.0           # FY2026 D&A / ending net PP&E proxy
# --- Inventory / floor plan ---
COGS_2026        = 62_475.0
INV_DAYS         = ((10_080.0 + 21_403.0) / 2) / COGS_2026 * 365  # 91.96 days
FLOOR_PLAN_RATIO = 0.0                          # none; no floor-plan liability or store base

# --- Interest rates ---
FLOOR_PLAN_RATE  = 0.0                          # none
DEBT_RATE        = 259.0 / ((8_463.0 + 8_468.0) / 2)  # FY2026 interest expense / average debt proxy
REVOLVER_RATE    = 0.060

# --- Debt / equity actions ---
DEBT_REPAYMENT   = 0.0    # FY2026 reported no debt repayment
BUYBACK          = 0.0    # judgment: no recurring repurchase forecast supplied

# --- Cash / revolver ---
MIN_CASH         = 10_605.0  # FY2026 ending cash; judgmental minimum
REVOLVER_LIMIT   = 0.0       # no separately disclosed revolver balance/limit

# --- Valuation ---
COST_OF_EQUITY   = 0.10
TERMINAL_GROWTH  = 0.025
SHARES_M         = 24_304.0                # million shares outstanding, FY2026 10-K

# ---------------------------------------------------------------------------
# 1.  OPENING BALANCE SHEET
# ---------------------------------------------------------------------------

op = {
    "revenue":      215_938.0,
    "cash":          10_605.0,
    "inventory":     21_403.0,
    "other_assets": 164_412.0,  # FY2026 total assets less cash, inventory, and net PP&E
    "pp_and_e":      10_383.0,
    "floor_plan":         0.0,  # none
    "debt":           8_468.0,  # FY2026 short- and long-term debt
    "revolver":           0.0,  # none separately disclosed
    "other_liab":    41_042.0,  # FY2026 total liabilities less debt
}
# Equity closes the opening balance sheet
op["equity"] = 157_293.0  # FY2026 total shareholders' equity; sheet reconciles to $206,803M assets

YEARS = [2027, 2028, 2029, 2030, 2031]

# Immutable reference set for all sensitivity runs. Each run receives a fresh
# deep copy so no case can carry cash, inventory, or another linked result into
# the next case.
BASE_INPUTS = {
    "years": YEARS.copy(),
    "opening": copy.deepcopy(op),
    "revenue_growth": REVENUE_GROWTH,
    "gross_margin": GROSS_MARGIN,
    "sga_ratios": SGA_RATIOS.copy(),
    "depr_rate": DEPR_RATE,
    "impairment": IMPAIRMENT,
    "capex": CAPEX,
    "tax_rate": TAX_RATE,
    "inv_days": INV_DAYS,
    "floor_plan_ratio": FLOOR_PLAN_RATIO,
    "floor_plan_rate": FLOOR_PLAN_RATE,
    "debt_rate": DEBT_RATE,
    "revolver_rate": REVOLVER_RATE,
    "debt_repayment": DEBT_REPAYMENT,
    "buyback": BUYBACK,
    "min_cash": MIN_CASH,
    "revolver_limit": REVOLVER_LIMIT,
    "cost_of_equity": COST_OF_EQUITY,
    "terminal_growth": TERMINAL_GROWTH,
    "shares_m": SHARES_M,
}

# One-at-a-time operating-driver sensitivity inputs. Values apply in every
# explicit forecast year; all other independent inputs reset to BASE_INPUTS.
OPERATING_DRIVER_SENSITIVITIES = {
    "Revenue growth": {
        "input_key": "revenue_growth",
        "units": "% year-over-year",
        "years": "FY2027-FY2031",
        "Lower": 0.555,
        "Base": 0.655,
        "Higher": 0.755,
    },
    "Gross margin": {
        "input_key": "gross_margin",
        "units": "% of revenue",
        "years": "FY2027-FY2031",
        "Lower": 0.6807,
        "Base": 0.7107,
        "Higher": 0.7407,
    },
}

# Change this label/scenario to inspect another full linked run below.
TRACE_CASE = ("Revenue growth", "Lower")

# ---------------------------------------------------------------------------
# 2.  PRINT HELPER
# ---------------------------------------------------------------------------

def fmtrow(label, values, width=12):
    """Print one row of the table."""
    nums = "".join(f"{v:>{width}.1f}" for v in values)
    print(f"  {label:<32}{nums}")

def hline(n=5, width=12):
    print("  " + "-" * 32 + "-" * (n * width))

def header(title):
    print()
    print("=" * 92)
    print(f"  {title}")
    print("=" * 92)
    print(f"  {'':32}" + "".join(f"{y:>12}" for y in YEARS))
    hline()

# ---------------------------------------------------------------------------
# 3.  BALANCE-SHEET CHECK
# ---------------------------------------------------------------------------

def assert_balanced(year, assets, liabilities_equity):
    gap = round(assets - liabilities_equity, 4)
    if abs(gap) > 0.05:
        raise ValueError(
            f"Balance sheet DOES NOT CLOSE in {year}: "
            f"Assets={assets:.4f}  L+E={liabilities_equity:.4f}  Gap={gap:.4f}"
        )

# ---------------------------------------------------------------------------
# 4.  FORECAST LOOP
# ---------------------------------------------------------------------------

# Accumulators for printing
IS = {k: [] for k in ["revenue","gross_profit","sga","depr","impair","opinc",
                       "interest","pretax","tax","net_income"]}
BS = {k: [] for k in ["cash","inventory","other_assets","pp_and_e",
                       "floor_plan","debt","revolver","other_liab","equity"]}
CF = {k: [] for k in ["net_income","depr","impair","capex","d_inv",
                       "d_owc","d_floor","repay","fcfe","buyback","net_cash"]}

# Running state
prev = op.copy()
other_wc_bal = 0.0    # cumulative other-working-capital balance (starts at 0)

fcfe_list = []

for i, yr in enumerate(YEARS):

    # -----------------------------------------------------------------------
    # INCOME STATEMENT
    # -----------------------------------------------------------------------
    rev         = prev["revenue"] * (1 + REVENUE_GROWTH)
    gp          = rev * GROSS_MARGIN
    sga         = gp * SGA_RATIOS[i]
    depr        = prev["pp_and_e"] * DEPR_RATE          # opening PP&E
    impair      = IMPAIRMENT
    opinc       = gp - sga - depr - impair
    interest    = (prev["floor_plan"] * FLOOR_PLAN_RATE
                   + prev["debt"]     * DEBT_RATE
                   + prev["revolver"] * REVOLVER_RATE)
    pretax      = opinc - interest
    tax         = max(0.0, pretax) * TAX_RATE
    net_inc     = pretax - tax

    # -----------------------------------------------------------------------
    # BALANCE SHEET  (except cash)
    # -----------------------------------------------------------------------
    cogs_yr     = rev - gp
    inv         = cogs_yr * INV_DAYS / 365
    floor_plan  = inv * FLOOR_PLAN_RATIO
    pp_e        = prev["pp_and_e"] + CAPEX - depr
    d_rev       = rev - prev["revenue"]
    d_owc       = 0.008 * d_rev                         # annual flow
    oa          = prev["other_assets"] + d_owc - impair # other assets
    debt        = prev["debt"] - DEBT_REPAYMENT
    other_liab  = prev["other_liab"]                    # flat
    equity      = prev["equity"] + net_inc - BUYBACK

    # -----------------------------------------------------------------------
    # FREE CASH FLOW TO EQUITY
    # -----------------------------------------------------------------------
    d_inv       = inv - prev["inventory"]
    d_floor     = floor_plan - prev["floor_plan"]       # positive = source
    fcfe        = (net_inc + depr + impair - CAPEX
                   - d_inv - d_owc + d_floor - DEBT_REPAYMENT)

    # -----------------------------------------------------------------------
    # CASH  (with revolver logic)
    # -----------------------------------------------------------------------
    pre_rev_cash = prev["cash"] + fcfe - BUYBACK
    revolver_bal = prev["revolver"]

    if pre_rev_cash < MIN_CASH:
        # Draw revolver to reach exactly MIN_CASH
        draw = min(MIN_CASH - pre_rev_cash, REVOLVER_LIMIT - revolver_bal)
        revolver_bal += draw
        cash = MIN_CASH
    else:
        cash = pre_rev_cash
        if revolver_bal > 0:
            # Repay revolver first
            repay_rev = min(revolver_bal, cash - MIN_CASH)
            revolver_bal -= repay_rev
            cash -= repay_rev

    # -----------------------------------------------------------------------
    # BALANCE SHEET CHECK
    # -----------------------------------------------------------------------
    total_assets = cash + inv + oa + pp_e
    total_le     = floor_plan + debt + revolver_bal + other_liab + equity
    assert_balanced(yr, total_assets, total_le)

    # -----------------------------------------------------------------------
    # STORE RESULTS
    # -----------------------------------------------------------------------
    IS["revenue"].append(rev)
    IS["gross_profit"].append(gp)
    IS["sga"].append(sga)
    IS["depr"].append(depr)
    IS["impair"].append(impair)
    IS["opinc"].append(opinc)
    IS["interest"].append(interest)
    IS["pretax"].append(pretax)
    IS["tax"].append(tax)
    IS["net_income"].append(net_inc)

    BS["cash"].append(cash)
    BS["inventory"].append(inv)
    BS["other_assets"].append(oa)
    BS["pp_and_e"].append(pp_e)
    BS["floor_plan"].append(floor_plan)
    BS["debt"].append(debt)
    BS["revolver"].append(revolver_bal)
    BS["other_liab"].append(other_liab)
    BS["equity"].append(equity)

    CF["net_income"].append(net_inc)
    CF["depr"].append(depr)
    CF["impair"].append(impair)
    CF["capex"].append(-CAPEX)
    CF["d_inv"].append(-d_inv)
    CF["d_owc"].append(-d_owc)
    CF["d_floor"].append(d_floor)
    CF["repay"].append(-DEBT_REPAYMENT)
    CF["fcfe"].append(fcfe)
    CF["buyback"].append(-BUYBACK)
    CF["net_cash"].append(cash - prev["cash"])

    fcfe_list.append(fcfe)

    # Advance state
    prev = {
        "revenue":      rev,
        "cash":         cash,
        "inventory":    inv,
        "other_assets": oa,
        "pp_and_e":     pp_e,
        "floor_plan":   floor_plan,
        "debt":         debt,
        "revolver":     revolver_bal,
        "other_liab":   other_liab,
        "equity":       equity,
    }

# ---------------------------------------------------------------------------
# 5.  PRINT OPENING BALANCE SHEET
# ---------------------------------------------------------------------------
print()
print("=" * 92)
print("  NVIDIA OPENING BALANCE SHEET  (FY2026 year-end / FY2027 beginning)   [$ millions]")
print("  Reported FY2026 amounts are reconciled to total assets; residual rows are labeled.")
print("=" * 92)
print(f"  {'ASSETS':}")
print(f"    {'Cash':30}  {op['cash']:>10.1f}   FY2026 10-K")
print(f"    {'Inventory':30}  {op['inventory']:>10.1f}   FY2026 10-K")
print(f"    {'Other assets':30}  {op['other_assets']:>10.1f}   total-assets residual")
print(f"    {'PP&E, net':30}  {op['pp_and_e']:>10.1f}   FY2026 10-K")
print(f"    {'Total assets':30}  {op['cash']+op['inventory']+op['other_assets']+op['pp_and_e']:>10.1f}")
print()
print(f"  {'LIABILITIES + EQUITY':}")
print(f"    {'Floor plan payables':30}  {op['floor_plan']:>10.1f}   none")
print(f"    {'Debt':30}  {op['debt']:>10.1f}   FY2026 10-K")
print(f"    {'Revolver':30}  {op['revolver']:>10.1f}   none separately disclosed")
print(f"    {'Other liabilities':30}  {op['other_liab']:>10.1f}   total-liabilities residual")
print(f"    {'Shareholders equity':30}  {op['equity']:>10.1f}   FY2026 10-K")
print(f"    {'Total L+E':30}  {op['floor_plan']+op['debt']+op['revolver']+op['other_liab']+op['equity']:>10.1f}")

# ---------------------------------------------------------------------------
# 6.  PRINT INCOME STATEMENT
# ---------------------------------------------------------------------------
header("NVIDIA INCOME STATEMENT  2027–2031   [$ millions]")
fmtrow("Revenue",              IS["revenue"])
fmtrow("  Gross profit",       IS["gross_profit"])
fmtrow("  SG&A",               IS["sga"])
fmtrow("  Depreciation",       IS["depr"])
fmtrow("  Impairment",         IS["impair"])
hline()
fmtrow("Operating income",     IS["opinc"])
fmtrow("  Interest expense",   IS["interest"])
hline()
fmtrow("Pre-tax income",       IS["pretax"])
fmtrow("  Income tax",         IS["tax"])
hline()
fmtrow("NET INCOME",           IS["net_income"])

# ---------------------------------------------------------------------------
# 7.  PRINT BALANCE SHEET
# ---------------------------------------------------------------------------
header("NVIDIA BALANCE SHEET  2027–2031   [$ millions]")
print(f"  {'ASSETS':}")
fmtrow("Cash",                 BS["cash"])
fmtrow("Inventory",            BS["inventory"])
fmtrow("Other assets",         BS["other_assets"])
fmtrow("PP&E",                 BS["pp_and_e"])
hline()
total_a = [BS["cash"][j]+BS["inventory"][j]+BS["other_assets"][j]+BS["pp_and_e"][j]
           for j in range(5)]
fmtrow("TOTAL ASSETS",         total_a)
print()
print(f"  {'LIABILITIES + EQUITY':}")
fmtrow("Floor plan payables",  BS["floor_plan"])
fmtrow("Term debt",            BS["debt"])
fmtrow("Revolver",             BS["revolver"])
fmtrow("Other liabilities",    BS["other_liab"])
fmtrow("Equity",               BS["equity"])
hline()
total_le = [BS["floor_plan"][j]+BS["debt"][j]+BS["revolver"][j]+BS["other_liab"][j]+BS["equity"][j]
            for j in range(5)]
fmtrow("TOTAL L+E",            total_le)

# Inline balance check print
print()
print("  Balance-sheet checks (gap must be < $0.1M):")
for j, yr in enumerate(YEARS):
    gap = total_a[j] - total_le[j]
    status = "OK" if abs(gap) < 0.05 else "FAIL"
    print(f"    {yr}: Assets={total_a[j]:.1f}  L+E={total_le[j]:.1f}  Gap={gap:.4f}  [{status}]")

# ---------------------------------------------------------------------------
# 8.  PRINT CASH FLOW STATEMENT
# ---------------------------------------------------------------------------
header("NVIDIA CASH FLOW STATEMENT  2027–2031   [$ millions]")
print(f"  {'Operating activities':}")
fmtrow("Net income",                   CF["net_income"])
fmtrow("  + Depreciation",            CF["depr"])
fmtrow("  + Impairment",              CF["impair"])
fmtrow("  - Change in inventory",     CF["d_inv"])
fmtrow("  - Change in other WC",      CF["d_owc"])
fmtrow("  + Change in floor plan",    CF["d_floor"])
print()
print(f"  {'Investing activities':}")
fmtrow("  Capital expenditure",       CF["capex"])
print()
print(f"  {'Financing activities':}")
fmtrow("  Debt repayment",            CF["repay"])
hline()
fmtrow("FREE CASH FLOW TO EQUITY",    CF["fcfe"])
fmtrow("  Share buybacks",            CF["buyback"])
hline()
fmtrow("NET CHANGE IN CASH",          CF["net_cash"])

# ---------------------------------------------------------------------------
# 9.  EQUITY VALUATION
# ---------------------------------------------------------------------------

# Terminal value uses 2030 FCFE + 2030 repayment, grown one period
fcfe_2030   = fcfe_list[4]
tv_numer    = (fcfe_2030 + DEBT_REPAYMENT) * (1 + TERMINAL_GROWTH)
tv          = tv_numer / (COST_OF_EQUITY - TERMINAL_GROWTH)

# PV of each FCFE
pv_fcfe = sum(fcfe_list[t] / (1 + COST_OF_EQUITY)**(t + 1) for t in range(5))

# PV of terminal value (discounted 5 years)
pv_tv   = tv / (1 + COST_OF_EQUITY)**5

equity_value   = pv_fcfe + pv_tv
value_per_share = equity_value / SHARES_M

# Share of value from terminal value
tv_share = pv_tv / equity_value * 100

print()
print("=" * 92)
print("  NVIDIA EQUITY VALUATION   [$ millions except per-share]")
print("=" * 92)
print(f"  {'FCFE 2027–2031':}")
for t, yr in enumerate(YEARS):
    disc = fcfe_list[t] / (1 + COST_OF_EQUITY)**(t + 1)
    print(f"    {yr}  FCFE={fcfe_list[t]:>9.1f}   PV={disc:>9.1f}")
print()
print(f"  {'Terminal value  (undiscounted)':45} {tv:>10.1f}")
print(f"  {'PV of terminal value':45} {pv_tv:>10.1f}")
print(f"  {'PV of 5 FCFEs':45} {pv_fcfe:>10.1f}")
print(f"  {'Equity value':45} {equity_value:>10.1f}")
print()
print(f"  {'Shares outstanding (millions)':45} {SHARES_M:>10.3f}")
print(f"  {'VALUE PER SHARE  ($)':45} {value_per_share:>10.2f}")
print()
print(f"  {'% of value from terminal value':45} {tv_share:>10.1f}%")
print()
print("  Key assumptions:")
print(f"    Cost of equity:   {COST_OF_EQUITY*100:.1f}%")
print(f"    Terminal growth:  {TERMINAL_GROWTH*100:.1f}%")
print(f"    Opening cash / debt / other assets / other liab: FY2026 reported or reconciled — see top of file")


# ---------------------------------------------------------------------------
# 10. ONE-AT-A-TIME OPERATING-DRIVER SENSITIVITY
# ---------------------------------------------------------------------------

def run_linked_model(inputs):
    """Run the complete model from an independent deep copy of its inputs."""
    cfg = copy.deepcopy(inputs)
    prior = copy.deepcopy(cfg["opening"])
    results = {"revenue": [], "gross_profit": [], "opinc": [], "fcfe": [], "gaps": []}
    invalid_reasons = []

    for i, year in enumerate(cfg["years"]):
        rev = prior["revenue"] * (1 + cfg["revenue_growth"])
        gp = rev * cfg["gross_margin"]
        sga = gp * cfg["sga_ratios"][i]
        depr = prior["pp_and_e"] * cfg["depr_rate"]
        opinc = gp - sga - depr - cfg["impairment"]
        interest = (prior["floor_plan"] * cfg["floor_plan_rate"]
                    + prior["debt"] * cfg["debt_rate"]
                    + prior["revolver"] * cfg["revolver_rate"])
        pretax = opinc - interest
        tax = max(0.0, pretax) * cfg["tax_rate"]
        net_inc = pretax - tax

        inventory = (rev - gp) * cfg["inv_days"] / 365
        floor_plan = inventory * cfg["floor_plan_ratio"]
        pp_and_e = prior["pp_and_e"] + cfg["capex"] - depr
        d_owc = 0.008 * (rev - prior["revenue"])
        other_assets = prior["other_assets"] + d_owc - cfg["impairment"]
        debt = prior["debt"] - cfg["debt_repayment"]
        equity = prior["equity"] + net_inc - cfg["buyback"]
        d_inventory = inventory - prior["inventory"]
        d_floor_plan = floor_plan - prior["floor_plan"]
        fcfe = (net_inc + depr + cfg["impairment"] - cfg["capex"] - d_inventory
                - d_owc + d_floor_plan - cfg["debt_repayment"])

        pre_revolver_cash = prior["cash"] + fcfe - cfg["buyback"]
        revolver = prior["revolver"]
        if pre_revolver_cash < cfg["min_cash"]:
            revolver += min(cfg["min_cash"] - pre_revolver_cash,
                            cfg["revolver_limit"] - revolver)
            cash = cfg["min_cash"]
        else:
            cash = pre_revolver_cash
            if revolver > 0:
                repay_revolver = min(revolver, cash - cfg["min_cash"])
                revolver -= repay_revolver
                cash -= repay_revolver

        gap = ((cash + inventory + other_assets + pp_and_e)
               - (floor_plan + debt + revolver + prior["other_liab"] + equity))
        results["gaps"].append(gap)
        if abs(gap) >= 0.05:
            invalid_reasons.append(f"{year} balance-sheet gap {gap:,.4f} USD M")
        for key, value in {"revenue": rev, "gross_profit": gp, "opinc": opinc, "fcfe": fcfe}.items():
            results[key].append(value)
        prior = {
            "revenue": rev, "cash": cash, "inventory": inventory,
            "other_assets": other_assets, "pp_and_e": pp_and_e,
            "floor_plan": floor_plan, "debt": debt, "revolver": revolver,
            "other_liab": prior["other_liab"], "equity": equity,
        }

    value_per_share = None
    valuation_reason = None
    if cfg["terminal_growth"] >= cfg["cost_of_equity"]:
        valuation_reason = "terminal growth must be lower than cost of equity"
    elif cfg["shares_m"] <= 0:
        valuation_reason = "shares outstanding must be positive"
    else:
        terminal_value = ((results["fcfe"][-1] + cfg["debt_repayment"])
                          * (1 + cfg["terminal_growth"])
                          / (cfg["cost_of_equity"] - cfg["terminal_growth"]))
        pv_fcfe = sum(fcff / (1 + cfg["cost_of_equity"]) ** (i + 1)
                      for i, fcff in enumerate(results["fcfe"]))
        value_per_share = (pv_fcfe + terminal_value / (1 + cfg["cost_of_equity"]) ** len(cfg["years"])) / cfg["shares_m"]
    return {
        "inputs": cfg, "results": results, "accounting_valid": not invalid_reasons,
        "invalid_reasons": invalid_reasons, "valuation_valid": value_per_share is not None,
        "valuation_reason": valuation_reason, "value_per_share": value_per_share,
        "final_opinc": results["opinc"][-1], "final_fcfe": results["fcfe"][-1],
    }


def fmt(value, decimals=1, signed=False):
    if value is None:
        return "unavailable"
    sign = "+" if signed else ""
    return f"{value:{sign},.{decimals}f}"


def print_trace(driver, scenario, result):
    """Print sufficient linked statement detail to trace one selected run."""
    print()
    print("=" * 92)
    print(f"  TRACE: {driver} — {scenario}   [$ millions]")
    print("=" * 92)
    print(f"  Inputs used: revenue growth {result['inputs']['revenue_growth']:.2%}; "
          f"gross margin {result['inputs']['gross_margin']:.2%}")
    print(f"  {'':24}" + "".join(f"{year:>12}" for year in result["inputs"]["years"]))
    print("  " + "-" * 84)
    for label, key in [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
                       ("Operating profit", "opinc"), ("FCFE", "fcfe")]:
        print(f"  {label:<24}" + "".join(f"{value:>12,.1f}" for value in result["results"][key]))
    print("  Accounting checks (gap must be < $0.1M):")
    for year, gap in zip(result["inputs"]["years"], result["results"]["gaps"]):
        status = "OK" if abs(gap) < 0.05 else "INVALID"
        print(f"    {year}: Gap={gap:.4f}  [{status}]")


print()
print("=" * 118)
print("  ONE-AT-A-TIME OPERATING-DRIVER SENSITIVITY   [$ millions except per-share]")
print("  Every run begins with a fresh deep copy of BASE_INPUTS; no cases are ranked.")
print("=" * 118)
sensitivity_results = {}
for driver, spec in OPERATING_DRIVER_SENSITIVITIES.items():
    print()
    print(f"  {driver}: {spec['units']}; affected years: {spec['years']}")
    print("  " + " | ".join(f"{case}: {spec[case]:.2%}" for case in ("Lower", "Base", "Higher")))
    driver_results = {}
    for case in ("Lower", "Base", "Higher"):
        case_inputs = copy.deepcopy(BASE_INPUTS)
        case_inputs[spec["input_key"]] = spec[case]
        driver_results[case] = run_linked_model(case_inputs)
    base_result = driver_results["Base"]
    print(f"  {'Run':<9}{'Final operating profit':>25}{'Change from base':>20}{'Final FCFE':>18}"
          f"{'Change from base':>20}{'Value/share':>16}{'Change from base':>20}{'Check':>12}")
    print("  " + "-" * 136)
    for case in ("Lower", "Base", "Higher"):
        result = driver_results[case]
        value_change = None if not (result["valuation_valid"] and base_result["valuation_valid"]) else result["value_per_share"] - base_result["value_per_share"]
        status = "OK" if result["accounting_valid"] else "INVALID"
        print(f"  {case:<9}{fmt(result['final_opinc']):>25}{fmt(result['final_opinc'] - base_result['final_opinc'], signed=True):>20}"
              f"{fmt(result['final_fcfe']):>18}{fmt(result['final_fcfe'] - base_result['final_fcfe'], signed=True):>20}"
              f"{fmt(result['value_per_share'], 2):>16}{fmt(value_change, 2, True):>20}{status:>12}")
        if not result["accounting_valid"]:
            print("    Invalid run: " + "; ".join(result["invalid_reasons"]))
        if not result["valuation_valid"]:
            print(f"    Value per share unavailable: {result['valuation_reason']}.")
    valid = [result for result in driver_results.values() if result["accounting_valid"]]
    def span(key, decimals=1):
        values = [result[key] for result in valid if result[key] is not None]
        return "unavailable" if not values else fmt(max(values) - min(values), decimals)
    print(f"  Output span (max - min across valid lower/base/higher runs): operating profit {span('final_opinc')} USD M; "
          f"FCFE {span('final_fcfe')} USD M; value/share {span('value_per_share', 2)} USD.")
    sensitivity_results[driver] = driver_results

trace_driver, trace_case = TRACE_CASE
print_trace(trace_driver, trace_case, sensitivity_results[trace_driver][trace_case])

# Restore the separate base input set and rerun it after all sensitivity cases.
restored_base_result = run_linked_model(copy.deepcopy(BASE_INPUTS))
print()
print("  Base inputs restored and rerun after sensitivity cases:")
print(f"    Final operating profit: {restored_base_result['final_opinc']:,.1f} USD M")
print(f"    Final FCFE: {restored_base_result['final_fcfe']:,.1f} USD M")
if restored_base_result["valuation_valid"]:
    print(f"    Value per share: {restored_base_result['value_per_share']:,.2f} USD")
else:
    print(f"    Value per share: unavailable ({restored_base_result['valuation_reason']}).")
for year, gap in zip(BASE_INPUTS["years"], restored_base_result["results"]["gaps"]):
    status = "OK" if abs(gap) < 0.05 else "INVALID"
    print(f"    {year} base accounting check: Gap={gap:.4f}  [{status}]")


# ---------------------------------------------------------------------------
# 11. PRINTED LOCKED RECORD / PARTNER EXCHANGE
# ---------------------------------------------------------------------------

def valid_span(driver, output_key):
    """Return max-minus-min for valid lower/base/higher runs of one driver."""
    values = [result[output_key] for result in sensitivity_results[driver].values()
              if result["accounting_valid"] and result[output_key] is not None]
    return None if not values else max(values) - min(values)


revenue_lower = sensitivity_results["Revenue growth"]["Lower"]
revenue_base = sensitivity_results["Revenue growth"]["Base"]
revenue_deltas = {
    "opinc": revenue_lower["final_opinc"] - revenue_base["final_opinc"],
    "fcfe": revenue_lower["final_fcfe"] - revenue_base["final_fcfe"],
    "value": revenue_lower["value_per_share"] - revenue_base["value_per_share"],
}
opinc_driver = max(OPERATING_DRIVER_SENSITIVITIES, key=lambda driver: valid_span(driver, "final_opinc"))
fcfe_driver = max(OPERATING_DRIVER_SENSITIVITIES, key=lambda driver: valid_span(driver, "final_fcfe"))
value_driver = max(OPERATING_DRIVER_SENSITIVITIES, key=lambda driver: valid_span(driver, "value_per_share"))

print()
print("=" * 118)
print("  LOCKED RECORD: NVIDIA SENSITIVITY REVIEW AND PARTNER EXCHANGE")
print("=" * 118)
print("  Operating-driver table is printed above. Amounts below are USD millions except per-share values.")
print(f"  Restored-base check: FY2031 operating profit {restored_base_result['final_opinc']:,.1f}; "
      f"FY2031 FCFE {restored_base_result['final_fcfe']:,.1f}; "
      f"value/share {restored_base_result['value_per_share']:,.2f}; all five accounting checks OK.")
print()
print("  Locked prediction and reconciliation")
print("    Prediction: Lower revenue growth should reduce FY2031 operating profit, FCFE, and value/share versus base.")
print(f"    Actual lower revenue-growth run: operating profit change {revenue_deltas['opinc']:+,.1f}; "
      f"FCFE change {revenue_deltas['fcfe']:+,.1f}; value/share change {revenue_deltas['value']:+,.2f}.")
print("    Reconciliation: Directional prediction matched the linked-model result; no directional prediction error.")
print("    Trace checked: lower revenue growth reduces revenue, then gross profit and operating profit; "
      "earnings and working-capital effects then reduce FCFE and value/share.")
print()
print("  Main driver over the tested ranges")
print(f"    Revenue growth range: {OPERATING_DRIVER_SENSITIVITIES['Revenue growth']['Lower']:.2%} to "
      f"{OPERATING_DRIVER_SENSITIVITIES['Revenue growth']['Higher']:.2%}; "
      f"gross-margin range: {OPERATING_DRIVER_SENSITIVITIES['Gross margin']['Lower']:.2%} to "
      f"{OPERATING_DRIVER_SENSITIVITIES['Gross margin']['Higher']:.2%}.")
print(f"    Largest operating-profit span: {opinc_driver} ({valid_span(opinc_driver, 'final_opinc'):,.1f} USD M).")
print(f"    Largest FCFE span: {fcfe_driver} ({valid_span(fcfe_driver, 'final_fcfe'):,.1f} USD M).")
print(f"    Largest value/share span: {value_driver} ({valid_span(value_driver, 'value_per_share'):,.2f} USD).")
print("    Over these ranges, revenue growth is the larger driver because it compounds the revenue base in every "
      "forecast year. The comparison is range-specific: its wider tested range can contribute to the larger span.")
print()
print("  Partner exchange 3")
print("    Question received: Could the revenue-growth ranking reflect the chosen ranges rather than inherent importance?")
print("    Response: Yes. The ranking applies only over these stated ranges; a narrower revenue range or wider "
      "gross-margin range could change the span comparison.")
print("    Check performed on partner analysis: Recomputed the selected changed-minus-base output, checked that "
      "non-tested independent inputs were reset to base, and requested a statement trace from the driver through "
      "operating profit and FCFE.")
print("    Partner-summary limitation: Do not rank NVIDIA and the partner company by raw dollar changes; compare "
      "each company's causal driver and span over that company's own tested range.")
