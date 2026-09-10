# NVIDIA (NVDA) Reverse DCF Inputs & Results

**Company:** NVIDIA Corporation (NASDAQ: NVDA)  
**Model:** Five-year unlevered DCF (FCFF), USD millions except per-share values  
**Primary financial source:** [NVIDIA Form 10-K for the fiscal year ended January 25, 2026](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)  
**Target market price:** $218.06 per share, observed September 10, 2026 at 1:50 PM EDT  

---

## 1. Fixed DCF Inputs

| Input | Value | Units | Method / source |
| :--- | ---: | :--- | :--- |
| Starting FCFF (Year 0) | $96,896 | USD millions | CFO $102,718M + after-tax interest expense $220M − CapEx $6,042M |
| Base growth rates (Years 1–5) | 30.0%, 25.0%, 20.0%, 15.0%, 10.0% | % | Base-case forecast path |
| WACC | 10.0% | % | Held fixed |
| Terminal growth rate | 3.0% | % | Held fixed; must remain below WACC |
| Cash and marketable securities | $62,556 | USD millions | $10,605M cash and equivalents + $51,951M marketable securities |
| Total debt | $8,468 | USD millions | $999M short-term debt + $7,469M long-term debt |
| Diluted shares | 24,514 | Millions | FY2026 weighted-average diluted shares |

---

## 2. Reverse-DCF Question and Method

**Question:** What common percentage-point shift must be added to all five explicit FCFF growth rates for the model’s value per diluted share to equal the $218.06 target price?

For each candidate shift, s:

\[
g_t^{\text{implied}} = g_t^{\text{base}} + s
\]

\[
\text{FCFF}_t = \text{FCFF}_{t-1}(1+g_t^{\text{implied}})
\]

\[
\text{Terminal Value}_5 =
\frac{\text{FCFF}_5(1+g)}{\text{WACC}-g}
\]

The model discounts the five FCFF forecasts and terminal value at the fixed 10.0% WACC, adds cash, subtracts debt, and divides by 24,514 million diluted shares. The solver uses bisection until the calculated price equals the target price.

---

## 3. Reverse-DCF Result

| Output | Result |
| :--- | ---: |
| Target share price | $218.06 |
| Solved uniform shift to explicit growth rates | **+17.0235 percentage points** |
| Calculated value per diluted share | $218.06 |

### Implied Explicit FCFF Growth Path

| Forecast year | Base growth | Uniform shift | Implied growth |
| :--- | ---: | ---: | ---: |
| Year 1 | 30.0000% | +17.0235 pts | **47.0235%** |
| Year 2 | 25.0000% | +17.0235 pts | **42.0235%** |
| Year 3 | 20.0000% | +17.0235 pts | **37.0235%** |
| Year 4 | 15.0000% | +17.0235 pts | **32.0235%** |
| Year 5 | 10.0000% | +17.0235 pts | **27.0235%** |

---

## 4. Interpretation

At the fixed 10.0% WACC and 3.0% terminal-growth rate, a $218.06 share price requires FCFF growth that is roughly 17 percentage points above the base forecast in every explicit forecast year. This is an implied-growth scenario, not a forecast or recommendation.

## 5. Updating the Analysis

To rerun the reverse DCF, update **TARGET_SHARE_PRICE** in [dcf.py](dcf.py). Keep the fixed inputs synchronized with the input block in that file, then run:

    python dcf.py
