"""
=============================================================================
Asbury Automotive Group (ABG) — Integrated 3-Statement Forecast  2026–2030
Standard library only.  Run:  python abg_3statement.py
=============================================================================

OPENING BALANCE SHEET  (end of FY2025 / beginning of FY2026)
All dollar amounts in millions unless noted.

  PP&E            3,070.4   ← given (FY2025 year-end)
  Inventory       2,135.8   ← given (FY2025)
  Floor plan pay  2,027.0   ← given (FY2025)
  Revenue base   17,999.0   ← given (FY2025 total revenue)
  Cash               40.4   ← ABG FY2025 10-K
  Term debt       3,572.0   ← ABG FY2025 10-K (long-term debt incl. current portion)
  Revolver            0.0   ← clean at start
  Other assets      500.0   ← [ASSUMED] placeholder; replace with 10-K actual
  Other liab        300.0   ← [ASSUMED] placeholder; replace with 10-K actual
  Equity           =  Assets − Liabilities  (plug to close)

NOTE: Replace [ASSUMED] items with actual 10-K figures when available.
The assert_balanced() check will catch any re-entry errors.
=============================================================================
"""

# ---------------------------------------------------------------------------
# 0.  ASSUMPTIONS
# ---------------------------------------------------------------------------

# --- Income-statement assumptions ---
REVENUE_GROWTH   = 0.018                        # 1.8% organic
GROSS_MARGIN     = 0.1705                        # 17.05%
SGA_RATIOS       = [0.665, 0.655, 0.645, 0.645, 0.645]  # SG&A ÷ gross profit
DEPR_RATE        = 82.4 / 3_070.4              # depreciation ÷ opening PP&E
IMPAIRMENT       = 120.0                        # non-cash, per year
CAPEX            = 250.0                        # per year
TAX_RATE         = 0.255

# --- Inventory / floor plan ---
COGS_2025        = 17_999.0 - 3_071.7          # = 14,927.3
INV_DAYS         = 2_135.8 / COGS_2025 * 365   # ≈ 52.24 days
FLOOR_PLAN_RATIO = 2_027.0 / 2_135.8           # ≈ 0.9491

# --- Interest rates ---
FLOOR_PLAN_RATE  = 0.0467
DEBT_RATE        = 0.0544
REVOLVER_RATE    = 0.060

# --- Debt / equity actions ---
DEBT_REPAYMENT   = 150.0  # per year
BUYBACK          = 150.0  # per year

# --- Cash / revolver ---
MIN_CASH         = 25.0
REVOLVER_LIMIT   = 850.0

# --- Valuation ---
COST_OF_EQUITY   = 0.10
TERMINAL_GROWTH  = 0.025
SHARES_M         = 17.951349               # million shares (10-Q 30 Jun 2026)

# ---------------------------------------------------------------------------
# 1.  OPENING BALANCE SHEET
# ---------------------------------------------------------------------------

op = {
    "revenue":      17_999.0,
    "cash":             40.4,   # ABG FY2025 10-K
    "inventory":     2_135.8,
    "other_assets":    500.0,   # [ASSUMED] placeholder
    "pp_and_e":      3_070.4,
    "floor_plan":    2_027.0,
    "debt":          3_572.0,   # ABG FY2025 10-K (long-term debt incl. current)
    "revolver":          0.0,
    "other_liab":      300.0,   # [ASSUMED] placeholder
}
# Equity closes the opening balance sheet
op["equity"] = (op["cash"] + op["inventory"] + op["other_assets"] + op["pp_and_e"]
                - op["floor_plan"] - op["debt"] - op["revolver"] - op["other_liab"])

# ---------------------------------------------------------------------------
# 2.  PRINT HELPER
# ---------------------------------------------------------------------------

YEARS = [2026, 2027, 2028, 2029, 2030]

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
print("  ABG OPENING BALANCE SHEET  (FY2025 year-end / FY2026 beginning)   [$ millions]")
print("  Items marked [ASSUMED] are placeholders — replace with 10-K actuals.")
print("=" * 92)
print(f"  {'ASSETS':}")
print(f"    {'Cash':30}  {op['cash']:>10.1f}   [ASSUMED] set to minimum cash")
print(f"    {'Inventory':30}  {op['inventory']:>10.1f}   from FY2025 data")
print(f"    {'Other assets':30}  {op['other_assets']:>10.1f}   [ASSUMED]")
print(f"    {'PP&E':30}  {op['pp_and_e']:>10.1f}   from FY2025 data")
print(f"    {'Total assets':30}  {op['cash']+op['inventory']+op['other_assets']+op['pp_and_e']:>10.1f}")
print()
print(f"  {'LIABILITIES + EQUITY':}")
print(f"    {'Floor plan payables':30}  {op['floor_plan']:>10.1f}   from FY2025 data")
print(f"    {'Term debt':30}  {op['debt']:>10.1f}   [ASSUMED]")
print(f"    {'Revolver':30}  {op['revolver']:>10.1f}   [ASSUMED] clean")
print(f"    {'Other liabilities':30}  {op['other_liab']:>10.1f}   [ASSUMED]")
print(f"    {'Equity (plug)':30}  {op['equity']:>10.1f}   closes sheet")
print(f"    {'Total L+E':30}  {op['floor_plan']+op['debt']+op['revolver']+op['other_liab']+op['equity']:>10.1f}")

# ---------------------------------------------------------------------------
# 6.  PRINT INCOME STATEMENT
# ---------------------------------------------------------------------------
header("ABG INCOME STATEMENT  2026–2030   [$ millions]")
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
header("ABG BALANCE SHEET  2026–2030   [$ millions]")
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
header("ABG CASH FLOW STATEMENT  2026–2030   [$ millions]")
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
print("  ABG EQUITY VALUATION   [$ millions except per-share]")
print("=" * 92)
print(f"  {'FCFE 2026–2030':}")
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
print(f"    Opening cash / debt / other assets / other liab: [ASSUMED] — see top of file")

