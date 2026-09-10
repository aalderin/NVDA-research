# NVIDIA (NVDA) FCFF DCF Valuation Inputs & Evidence

**Company:** NVIDIA Corporation (NASDAQ: NVDA)  
**Primary Source Filing:** Form 10-K for Fiscal Year Ended January 25, 2026 ([SEC Link](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm))  
**Valuation Model:** 5-Year Unlevered Discounted Cash Flow (FCFF) Model  
**Observation Timestamp:** September 10, 2026 at 1:50 PM EDT  
**Observed Market Share Price:** **$218.06** *(Prior Valuation Benchmark: $217.44 on Sept 1, 2026 Close)*

---

## 1. DCF Model Input Table

| Input Parameter | Value | Units | Source / Methodology |
| :--- | :--- | :--- | :--- |
| **Market Share Price (Observed)** | **$218.06** | USD / Share | Real-time market price as of **September 10, 2026, 1:50 PM EDT** (NASDAQ: NVDA). Implies ~$5.34T market cap. |
| **Starting FCFF (Year 0)** | **$96,896** | USD (Millions) | CFO ($102,718M) + after-tax interest expense ($259M × (1 − 15.1%)) − CapEx ($6,042M), from FY2026 financial statements. |
| **Growth Rates (Years 1–5)** | **30%, 25%, 20%, 15%, 10%** *(Illustrative Baseline)* | % YoY | Reflects high current Data Center / Blackwell demand fading down toward normalized growth over 5 years. |
| **WACC (Discount Rate)** | **10.0%** (Range: 9.0%–11.0%) | % | Cost of Equity (~10.2% via CAPM: Rf ~4.0%, Beta ~1.25, ERP ~5.0%) blended with negligible debt cost. |
| **Terminal Growth Rate ($g$)** | **3.0%** | % | Long-term sustainable macroeconomic / GDP growth rate ($g < \text{WACC}$). |
| **Cash & Non-Operating Assets** | **$62,556** | USD (Millions) | Cash & Cash Equivalents ($10,605M) + Marketable Securities ($51,951M) on Balance Sheet (p. 53). *(Latest Q2 FY27 figures require a separate 10-Q citation.)* |
| **Total Debt** | **$8,468** | USD (Millions) | Short-term debt ($999M) + long-term debt ($7,469M) on Balance Sheet (p. 53; Note 11, p. 69). *(Later-period debt requires a separate 10-Q citation.)* |
| **Diluted Shares** | **24,514** | Millions | FY2026 weighted-average diluted shares from the Income Statement (p. 51; Note 4, p. 62). *(For a point-in-time valuation, cite the relevant period-end shares outstanding.)* |

---

## 2. Step-by-Step Filing Evidence & Derivations

### A. Starting FCFF ($96,896 Million)
From the **Consolidated Statements of Cash Flows (Form 10-K, p. 55)** for the fiscal year ended January 25, 2026:
- **Net cash provided by operating activities:** $\$102,718\text{ million}$
- **Purchases of property and equipment and intangible assets (CapEx):** $(\$6,042)\text{ million}$
- **Interest expense:** $\$259\text{ million}$
- **Effective income tax rate:** $15.1\%$

Because CFO includes interest expense, add back its after-tax amount to express cash flow available to both debt and equity holders:
$$\text{Starting FCFF} = \text{CFO} + \text{Interest Expense}(1-\text{Tax Rate}) - \text{CapEx}$$
$$= \$102,718 + \$259(1-0.151) - \$6,042 = \mathbf{\$96,896\text{ million}}$$

---

### B. Cash and Non-Operating Assets ($62,556 Million)
From the **Consolidated Balance Sheets (Form 10-K, p. 53)** as of January 25, 2026:
- **Cash and cash equivalents:** $\$10,605\text{ million}$
- **Marketable securities:** $\$51,951\text{ million}$
$$\text{Total Cash & Marketable Securities} = \$10,605 + \$51,951 = \mathbf{\$62,556\text{ million}}$$

---

### C. Total Debt ($8,468 Million)
From the **Consolidated Balance Sheets (Form 10-K, p. 53)** and **Note 11 (Debt, p. 69)** as of January 25, 2026:
- **Short-term debt:** $\$999\text{ million}$
- **Long-term debt:** $\$7,469\text{ million}$
$$\text{Total Debt (Carrying Amount)} = \$999 + \$7,469 = \mathbf{\$8,468\text{ million}}$$
*(Note: Principal amount is $\$8,500\text{ million}$ across senior notes maturing between 2026 and 2060).*

---

### D. Diluted Shares (24,514 Million Shares)
From the **Consolidated Statements of Income (Form 10-K, p. 51)** and **Note 4 (Net Income Per Share, p. 62)**:
- **Weighted-average shares used in computing diluted net income per share:** $\mathbf{24,514\text{ million}}$
- *(Common shares outstanding as of January 25, 2026: $24,304\text{ million}$. A later-period share count requires a separate 10-Q citation.)*

---

### E. WACC & Terminal Growth Rationale
- **WACC (10.0%):** NVIDIA’s capital structure is over 98% equity funded. Using CAPM ($r_e = R_f + \beta \times \text{ERP}$):
  - Risk-free rate ($R_f$): $4.0\%$
  - Estimated Equity Beta ($\beta$): $1.20 - 1.30$
  - Equity Risk Premium ($\text{ERP}$): $5.0\%$
  - Cost of Equity ($r_e$): $4.0\% + 1.25 \times 5.0\% \approx 10.25\%$
  - A round **10.0%** discount rate is a sound valuation standard for NVIDIA.
- **Terminal Growth ($g = 3.0\%$):** 
  - Aligns with expected long-term global nominal GDP growth.
  - Satisfies the required boundary condition: $g < \text{WACC}$ ($3\% < 10\%$).

---

## 3. Illustrative DCF Output (Python `dcf.py` Alignment)

Plugging these exact inputs into `dcf.py`:
- `STARTING_FCFF = 96896.0`
- `GROWTH_RATES = [0.30, 0.25, 0.20, 0.15, 0.10]`
- `WACC = 0.10`
- `TERMINAL_GROWTH = 0.03`
- `NON_OPERATING_CASH = 62556.0`
- `DEBT = 8468.0`
- `DILUTED_SHARES = 24514.0`

### Projected Cash Flows:
- **Year 1 FCFF (30%):** $\$125,964.80\text{M}$ $\to$ $\text{PV} = \$114,513.45\text{M}$
- **Year 2 FCFF (25%):** $\$157,456.00\text{M}$ $\to$ $\text{PV} = \$130,128.93\text{M}$
- **Year 3 FCFF (20%):** $\$188,947.20\text{M}$ $\to$ $\text{PV} = \$141,958.83\text{M}$
- **Year 4 FCFF (15%):** $\$217,289.28\text{M}$ $\to$ $\text{PV} = \$148,411.50\text{M}$
- **Year 5 FCFF (10%):** $\$239,018.21\text{M}$ $\to$ $\text{PV} = \$148,411.50\text{M}$
- **Sum of PV (Years 1–5):** $\mathbf{\$683,424.21\text{ million}}$

### Terminal Value & Bridge:
- **Terminal Value at Year 5:** $\frac{\$239,018.21 \times 1.03}{0.10 - 0.03} = \$3,516,982.20\text{ million}$
- **PV of Terminal Value:** $\mathbf{\$2,183,769.24\text{ million}}$
- **Enterprise Value (EV):** $\$683,424.21 + \$2,183,769.24 = \mathbf{\$2,867,193.45\text{ million}}$ (~$2.87 Trillion)
- **Equity Value:** $\$2,867,193.45 + \$62,556 - \$8,468 = \mathbf{\$2,921,281.45\text{ million}}$ (~$2.92 Trillion)
- **Value Per Diluted Share:** $\frac{\$2,921,281.45\text{M}}{24,514\text{M shares}} = \mathbf{\$119.17\text{ per share}}$

---

## 4. What Today's Market Price ($218.06) Implies (Reverse DCF)

- **Observed Market Price:** **$218.06** (September 10, 2026, 1:50 PM EDT)
- **Market Implied Equity Value:** $\approx \$5.35\text{ Trillion}$
- **Model DCF Value (30% $\to$ 10% Fade):** **$119.17**
- **Interpretation:**
  - Today's market price of **$218.06** embeds significantly higher growth expectations than a 30% $\to$ 10% fade.
  - To justify ~$218/share at a 10% WACC and 3% terminal growth, NVIDIA's FCFF would need to compound at ~**38%–40% annually** across all 5 explicit forecast years (reaching >$500B in annual FCFF by Year 5), or the market is pricing in a lower cost of capital / higher long-term terminal return.

---

## 5. Conditional Investment Call

**Watch—defer.** Initiate if NVIDIA trades at or below approximately **$119.17 per share**, the current base-case DCF value, or if sourced evidence supports increasing each of the five explicit FCFF growth assumptions by **2 percentage points**. Otherwise, defer initiation because the observed $218.06 price requires growth above the current forecast path.

**Monitor:** next-quarter operating margin, using NVIDIA's quarterly earnings release and Form 10-Q.
