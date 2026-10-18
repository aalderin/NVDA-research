# Locked Changed-Input Record: NVIDIA (NVDA) Integrated Pro-Forma Model

**Target Company:** NVIDIA Corporation (NASDAQ: NVDA)  
**Valuation Engine:** `nvda_proforma.py` (5-Year 3-Statement Forecast + FCFF DCF)  
**Record Status:** FROZEN & PRECOMMITTED  
**Precommit Timestamp:** 2026-10-08 13:52:00 EDT  

---

## 1. Test Specification & Input Parameters

| Parameter | Value / Description |
| :--- | :--- |
| **Tested Input Driver** | `INV_DAYS` (Inventory Holding Period) |
| **Original Input (Base Case)** | `91.96 days` (calculated as average FY25–FY26 inventory / FY26 COGS × 365) |
| **Changed Input (Test Case)** | `110.00 days` (+18.04 days inventory expansion) |
| **Units** | Days of COGS |
| **Affected Forecast Years** | FY2027 – FY2031 (applied across all 5 pro-forma years) |
| **Non-Tested Inputs** | Held strictly constant at `BASE_INPUTS` (Revenue Growth = 65.5%, Gross Margin = 71.07%, WACC = 10.0%, Terminal Growth = 2.5%) |

---

## 2. Human-Authored Pre-Run Prediction (AI-Off)

> **Prediction Statement:**  
> "Increasing inventory holding days from 91.96 days to 110.0 days increases the required inventory dollar balance on the balance sheet for any given level of sales and COGS. In the linked statement model, higher inventory balance increases working capital investment each year ($\Delta\text{Inventory}$ cash outflow on the Statement of Cash Flows), directly reducing Free Cash Flow to Equity (FCFE) across all forecast years (FY2027–FY2031). Because DCF equity value is the present value of FCFE plus terminal value, higher inventory days must **decrease** value per share. Income statement metrics (Revenue, Gross Profit, Operating Profit, Tax) should remain completely unchanged because inventory holding period affects cash conversion and balance sheet asset balances, not operating margins or revenue."

---

## 3. Directional Execution & Output Comparison

| Output Metric | Base Case (91.96 days) | Changed Run (110.00 days) | Actual Change | Expected Direction | Match? |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **FY2031 Revenue** | $1,963,274.6M | $1,963,274.6M | $0.0M | No change | ✅ YES |
| **FY2031 Operating Profit** | $1,843,548.5M | $1,843,548.5M | $0.0M | No change | ✅ YES |
| **FY2031 Inventory Balance** | $143,184.2M | $171,263.2M | +$28,079.0M | Increase | ✅ YES |
| **FY2031 FCFE** | $1,477,912.5M | $1,472,999.5M | -$4,913.0M | Decrease | ✅ YES |
| **Value per Share** | **$613.71** | **$607.29** | **-$6.42** (-1.05%) | Decrease | ✅ YES |
| **Balance Sheet Articulation** | 5/5 Years Gap < $0.05M | 5/5 Years Gap < $0.05M | Gap = 0.0000 | Pass | ✅ YES |

---

## 4. Statement Causal Transmission Trace

1. **Balance Sheet Asset Accumulation:**  
   $$\text{Inventory}_{t} = \frac{\text{COGS}_{t} \times \text{INV\_DAYS}}{365}$$  
   At 110.0 days, inventory required to support FY2031 revenue rises from $143,184.2M to $171,263.2M (+ $28,079.0M).

2. **Cash Flow Statement Drag:**  
   The annual inventory increase ($\Delta\text{Inventory} = \text{Inventory}_{t} - \text{Inventory}_{t-1}$) increases cash outflow in operating activities. In FY2031 alone, $\Delta\text{Inventory}$ drag increases from $57,001.3M to $68,172.9M.

3. **FCFE & Valuation Impact:**  
   $$\text{FCFE} = \text{Net Income} + \text{D\&A} - \text{CapEx} - \Delta\text{Inventory} - \Delta\text{Other WC} + \Delta\text{FloorPlan} - \text{Debt Repayment}$$  
   The cumulative reduction in discounted FCFE and terminal value reduces total equity value by **$156,031.7M**, resulting in a **-$6.42 per share drop** (from $613.71 to $607.29).

---

## 5. Decision Effect & Verification Summary

* **Directional Test Result:** PASS (100% match between human prediction and model execution).
* **Accounting Identity Verification:** The balance sheet balanced perfectly in all 5 projected years ($\text{Gap} = 0.0000$), confirming that the cash reduction exactly offset the inventory asset increase.
* **Investment Decision Impact:** A 18.04-day inventory blowout reduces equity value by ~$6.42/share (-1.05%). While not enough on its own to flip the long-term investment stance, it demonstrates that supply chain congestion and inventory aging create non-trivial working capital drag for fabless semiconductor leaders.

