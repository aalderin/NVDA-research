# NVIDIA Corporation (NASDAQ: NVDA) — Corporate Finance Valuation Application

**Course:** FIN 43900 — AI and Finance (Fall 2026)  
**Target Security:** NVIDIA Corporation (NASDAQ: NVDA)  
**Valuation Date:** September 1 / Fall 2026  
**Decision Horizon:** 3–5 Year Buy-Side Investment Horizon  
**Share Basis:** 24,304.0M common shares (FY2026 balance sheet) / 24,514.0M diluted shares (FY2026 income statement)  
**Currency:** USD ($ Millions except per-share values)  
**Dependency Policy:** **Python 3.x Standard Library Only** (No `pandas`, `numpy`, `scipy`, or pip packages required)  

---

## 1. Executive Summary & Investment Decision

* **Committee Recommendation:** **WATCH — DEFER**
* **Valuation Range:** **$119.17 – $613.71 / share** (Observed market price: ~$217.44 – $219.35)
* **Rationale:**
  - **Base-Case FCFF DCF Value ($119.17/share):** Built on a conservative fade model (30% down to 10% explicit growth, 10.0% WACC, 3.0% terminal growth). At current market prices (~$218/share), the stock trades at a ~83% premium to fundamental base-case FCFF value.
  - **Pro-Forma Compound Growth Model ($613.71/share):** Sustaining FY2026's hyper-growth rate (65.5% constant growth) yields a pro-forma value of $613.71, illustrating that current market pricing (~$218) implies a market-expected revenue growth rate of ~47.0% (solved via reverse DCF).
  - **Action Trigger:** Defer position initiation. Initiate a buy position only if NVIDIA trades at or below **$119.17/share** or if quarterly 10-Q evidence proves hyperscaler CapEx acceleration that justifies maintaining >50% revenue growth beyond FY2027.

---

## 2. Quick Execution Guide (Grader Reproducibility)

To run the full valuation application suite end-to-end on Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

Or run individual model components directly with Python:

```powershell
# 1. Run 3-Statement Integrated Pro-Forma & Sensitivity Engine
python nvda_proforma.py

# 2. Run Standalone FCFF DCF Engine & Reverse DCF
python dcf.py

# 3. Run Peer Multiples (P/E & EV) Comps Engine
python pe_comps.py
```

---

## 3. Workspace File Inventory & Architecture

| File Name | Purpose & Description |
| :--- | :--- |
| [`run.ps1`](file:///c:/Users/liald/finance-ai-course/run.ps1) | PowerShell entry script running all 3 valuation models sequentially with exit code verification. |
| [`nvda_proforma.py`](file:///c:/Users/liald/finance-ai-course/nvda_proforma.py) | **Primary Pro-Forma Model:** Fully linked 5-year 3-statement model (FY2027–FY2031) with automated balance sheet articulation checks (`assert_balanced()`), FCFE valuation engine, and operating-driver sensitivity runs (including wide ±1000 bps and conservative ±200 bps growth ranges). |
| [`dcf.py`](file:///c:/Users/liald/finance-ai-course/dcf.py) | **FCFF DCF Engine:** Standalone FCFF DCF model with WACC–terminal growth sensitivity matrix and reverse-DCF solver. |
| [`pe_comps.py`](file:///c:/Users/liald/finance-ai-course/pe_comps.py) | **Peer Comps Model:** P/E and EV multiple valuation comparing NVIDIA against peer group (AMD, Broadcom) with leave-one-out sensitivity. |
| [`nvda_peer_policy.md`](file:///c:/Users/liald/finance-ai-course/nvda_peer_policy.md) | Formally defined Peer Selection Policy established prior to peer selection. |
| [`partner_questions.md`](file:///c:/Users/liald/finance-ai-course/partner_questions.md) | Peer review defense record containing NVIDIA presenter defense, 10-K evidence citations, and reviewer feedback integration. |
| [`Locked_Changed_Input_Record.md`](file:///c:/Users/liald/finance-ai-course/Locked_Changed_Input_Record.md) | Precommitted directional changed-input verification record (Inventory Days test) with AI-off prediction and actual output trace. |
| [`project-1-edition-a.md`](file:///c:/Users/liald/finance-ai-course/project-1-edition-a.md) | Week 2 Edition A Checkpoint admission memo & target selection baseline. |
| [`sources.md`](file:///c:/Users/liald/finance-ai-course/sources.md) | Complete source catalog tracing all historical facts to SEC Form 10-K disclosures (Accession `0001045810-26-000021`). |
| [`NVDA_2026-09-03_report.md`](file:///c:/Users/liald/finance-ai-course/NVDA_2026-09-03_report.md) | Comprehensive Analyst Memo summarizing research evolution, DCF bounds, comps, and monitoring triggers. |

---

## 4. Key Financial Model Architecture & Accounting Rules

### A. Integrated 3-Statement Articulation Checks
The pro-forma model (`nvda_proforma.py`) enforces strict accounting identities across all forecast years (FY2027–FY2031):
* **Balance Sheet Identity:**  
  $$\text{Total Assets} = \text{Total Liabilities} + \text{Shareholders' Equity}$$
* **Cash Flow Linking:** Cash on the balance sheet is calculated as:  
  $$\text{Cash}_{t} = \text{Cash}_{t-1} + \text{FCFE}_{t} - \text{Buybacks}_{t}$$  
* **Articulation Assert:** Automated check fails loudly (`Gap >= $0.05M`) if the balance sheet fails to close. All projected years pass with $\text{Gap} = 0.0000$.

### B. Valuation Engines
1. **Free Cash Flow to Equity (FCFE) Engine:**
   $$\text{FCFE} = \text{Net Income} + \text{D\&A} + \text{Impairment} - \text{CapEx} - \Delta\text{Inventory} - \Delta\text{Other WC} + \Delta\text{FloorPlan} - \text{Debt Repayment}$$
   Discounted at $10.0\%$ Cost of Equity with $2.5\%$ Terminal Growth.
2. **Free Cash Flow to Firm (FCFF) Engine:**
   $$\text{FCFF} = \text{EBIT}(1 - t) + \text{D\&A} - \text{CapEx} - \Delta\text{NWC}$$
   Bridge from Enterprise Value to Equity Value:
   $$\text{Equity Value} = \text{Enterprise Value} + \text{Cash} - \text{Total Debt}$$

---

## 5. Sensitivity & Peer Review Findings

* **Range-Conditional Sensitivity:**
  - Testing revenue growth over a wide $\pm 1,000\text{ bps}$ range ($55.5\% \text{ to } 75.5\%$) yields a value/share span of **$353.47** ($457.32 \text{ to } 810.79$).
  - Testing revenue growth over a conservative $\pm 200\text{ bps}$ range ($63.5\% \text{ to } 67.5\%$) yields a value/share span of **$70.24**.
  - Testing gross margin over a $\pm 300\text{ bps}$ range ($68.07\% \text{ to } 74.07\%$) yields a value/share span of **$61.83**.
  - **Takeaway:** Revenue growth's perceived dominance is range-dependent due to 5-year compounding. Under tighter growth bounds ($\pm 200\text{ bps}$), gross margin and revenue growth operate in the same impact tier.

---

## 6. Sourced Filings & Authoritative Evidence

* **Primary SEC Filing:** NVIDIA Corporation Form 10-K for the fiscal year ended January 25, 2026 (SEC Accession No. `0001045810-26-000021`).
* **Segment Revenue:** Compute & Networking revenue of $193,479M out of $215,938M total revenue (~89.6%) cited from MD&A (Page 40) and Note 17 (Segment Information).
* **Opening Balance Sheet:** Reconciled to $206,803M Total Assets (PP&E: $10,383M, Cash: $10,605M, Inventory: $21,403M, Debt: $8,468M, Equity: $157,293M).

