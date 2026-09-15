# Comparable Company Valuation (P/E Comps) — Summary & Theoretical Guide

**Target Company:** Asbury Automotive Group, Inc. (NYSE: ABG)  
**Peer Candidates:** AutoNation, Inc. (NYSE: AN), Group 1 Automotive, Inc. (NYSE: GPI)  
**Valuation Date / Data Basis:** December 31, 2024 Closing Prices & FY2024 Total GAAP Diluted EPS  
**Script Reference:** [`pe_comps.py`](pe_comps.py)  
**Run Command:** `python pe_comps.py`

---

## 1. Valuation Data & Calculations Summary

### A. Raw Input Data
| Company | Ticker | Role | Dec 31, 2024 Price | FY2024 GAAP Diluted EPS |
| :--- | :---: | :---: | :---: | :---: |
| **Asbury Automotive Group** | **ABG** | **Target** | **$243.03** | **$21.50** |
| **AutoNation, Inc.** | **AN** | Candidate Peer | **$169.84** | **$16.92** |
| **Group 1 Automotive, Inc.** | **GPI** | Qualified Candidate Peer | **$421.48** | **$36.81** |

---

### B. Peer P/E Multiples & Summary Statistics
$$\text{P/E Multiple} = \frac{\text{Market Price per Share}}{\text{Diluted EPS}}$$

* **AutoNation (AN) P/E:** $\frac{\$169.84}{\$16.92} = \mathbf{10.037825x}$
* **Group 1 Automotive (GPI) P/E:** $\frac{\$421.48}{\$36.81} = \mathbf{11.450149x}$
* **Asbury Automotive (ABG) Target P/E:** $\frac{\$243.03}{\$21.50} = \mathbf{11.303721x}$

**Peer Group Statistics ($N=2$):**
* **Minimum Peer P/E:** **10.037825x** (AutoNation)
* **Median Peer P/E:** $\frac{10.037825 + 11.450149}{2} = \mathbf{10.743987x}$
* **Maximum Peer P/E:** **11.450149x** (Group 1 Automotive)

---

### C. Implied Target Valuations for Asbury Automotive (ABG)
$$\text{Implied Share Price} = \text{Peer P/E Multiple} \times \text{Target Diluted EPS (\$21.50)}$$

| Metric | Peer Multiple | Implied Target Price | Calculation (Unrounded) |
| :--- | :---: | :---: | :--- |
| **Minimum Implied Price** | 10.037825x | **$215.81** | $10.037825059 \times \$21.50 = \$215.8132\dots$ |
| **Median Implied Price (Baseline)** | 10.743987x | **$231.00** | $10.743987238 \times \$21.50 = \$230.9957\dots$ |
| **Maximum Implied Price** | 11.450149x | **$246.18** | $11.450149416 \times \$21.50 = \$246.1782\dots$ |

---

## 2. Leave-One-Out (Sensitivity) Analysis

### A. Results Table
| Removed Peer | Remaining Peer(s) | Remaining Median Multiple | Remaining Implied Price | Dollar Change vs. Baseline |
| :--- | :--- | :---: | :---: | :---: |
| **AutoNation (AN)** | GPI *(1 remaining)* | 11.450149x | **$246.18** | **+$15.18** |
| **Group 1 Automotive (GPI)** | AN *(1 remaining)* | 10.037825x | **$215.81** | **-$15.18** |

### B. Predicting & Explaining the Removal of Group 1 (GPI)
1. **Prediction:** Group 1 is the higher-multiple peer ($11.45x$ vs. AN's $10.04x$). Removing GPI removes the upper anchor, collapsing the median multiple down to AutoNation’s $10.037825x$. Consequently, the implied target price is predicted to fall sharply.
2. **Step-by-Step Price Change Breakdown:**
   * Baseline 2-peer median multiple: **$10.743987x$**
   * Multiple after removing GPI: **$10.037825x$**
   * Multiple contraction ($\Delta \text{Multiple}$): $10.037825 - 10.743987 = \mathbf{-0.706162x}$
   * Dollar impact on ABG:
     $$\Delta \text{Price} = -0.706162357 \times \$21.50 = \mathbf{-\$15.18249\dots \approx -\$15.18}$$
   * Target implied price drops from **\$231.00** to **\$215.81**.

---

## 3. Theoretical & Conceptual Questions Answered

### Q1: What does the P/E multiple fundamentally measure?
The Price-to-Earnings (P/E) ratio is an **equity-value multiple**:
$$\text{P/E} = \frac{\text{Price per Share}}{\text{Diluted EPS}} = \frac{\text{Market Capitalization}}{\text{Net Income}}$$
It measures how many dollars investors are willing to pay today for every **\$1.00 of annual after-tax earnings** generated for common shareholders.

Analytically, derived from the Gordon Growth dividend discount model:
$$\frac{P_0}{E_1} = \frac{\text{Payout Ratio}}{r_e - g}$$
P/E is driven by three core fundamentals:
1. **Earnings Growth Expectations ($g$):** Higher expected earnings growth expands the multiple.
2. **Cost of Equity / Risk ($r_e$):** Higher business or financial risk increases required return, compressing the multiple.
3. **Reinvestment Efficiency / Return on Equity (ROE):** Firms that generate more profit per dollar of reinvested capital support higher payout ratios and higher multiples.

> **Methodological Rule:** Never bridge P/E with cash or debt. P/E is already an equity-level metric; multiplying P/E by EPS yields equity price per share directly.

---

### Q2: Why does each peer belong, and what qualifications are needed?

* **AutoNation, Inc. (AN):**
  * *Why it belongs:* Largest pure-play U.S. automotive dealership group with identical primary revenue streams: new/used vehicle sales, customer-pay parts & service, and high-margin Finance & Insurance (F&I).
  * *Qualifications:* AutoNation has a substantially larger national scale, operates standalone *AutoNation USA* used-car retail stores, owns an internal captive financing company (*AutoNation Financial Services*), and executes heavy share repurchases that affect EPS dynamics differently.
* **Group 1 Automotive, Inc. (GPI):**
  * *Why it belongs:* Direct franchised dealership operator sharing identical dealership unit economics, gross profit mix, and acquisition-driven consolidation strategies.
  * *Qualifications:* Unlike Asbury (100% domestic U.S.), Group 1 has significant **international operations in the United Kingdom / Europe**. This exposes GPI to foreign exchange rate volatility (GBP/USD), distinct European regulatory mandates, and different interest rate/macro cycles.

---

### Q3: Why does one remaining peer give a reference estimate rather than a range?
* **Mathematical Reason:** A valuation **range** (Min, Median, Max) requires cross-sectional dispersion across multiple observations ($N \ge 2$). When only one peer remains ($N = 1$), the minimum, median, and maximum are mathematically identical ($\min = \text{median} = \max = 10.037825\text{x}$). The variance and spread are exactly zero.
* **Valuation Reason:** A single peer's multiple reflects that specific company's idiosyncratic capital structure, geographic mix, and operational anomalies. It serves only as a **single point-in-time reference estimate**, not an industry valuation range.

---

### Q4: Why does this peer comparison NOT prove Asbury is fairly valued?
Trading at **\$243.03** ($11.30\text{x}$) versus the peer median of **\$231.00** ($10.74\text{x}$) does not prove Asbury is mispriced or fairly valued due to four key limitations:

1. **Relative Pricing $\neq$ Intrinsic Fair Value:** Multiples only describe relative valuation across peers at one moment in time. If the automotive retail sector as a whole is overvalued or undervalued due to cyclical macro trends, comps will reproduce that mispricing.
2. **Capital Structure & Debt Differences:** P/E does not adjust for differences in balance sheet debt, floorplan financing, or lease structures. A peer with higher leverage will have higher financial risk and a lower P/E multiple.
3. **Small Sample Size ($N = 2$):** Two companies cannot form a statistically robust peer group. The median is simply an average of two numbers, making the benchmark highly vulnerable to single-peer noise.
4. **Operating & Margin Quality Differences:** Asbury’s modest valuation premium may be fully justified by higher Parts & Service gross margin mix, superior ROIC, or better capital allocation. Comps assume all peer earnings dollars are of identical quality.

---

### Q5: Final Peer Decision
**Retain both AutoNation (AN) and Group 1 Automotive (GPI) in the peer group.**
* Both companies share the exact same core business model.
* Excluding GPI drops the sample to $N=1$, introducing severe single-peer idiosyncratic bias.
* Retaining both provides a balanced two-peer median of **10.743987x** and an implied valuation range of **\$215.81 – \$246.18** around the **\$231.00** median.

