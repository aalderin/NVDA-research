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
=============================================================================
"""

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

# ---------------------------------------------------------------------------
# 2.  PRINT HELPER
# ---------------------------------------------------------------------------

YEARS = [2027, 2028, 2029, 2030, 2031]

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
