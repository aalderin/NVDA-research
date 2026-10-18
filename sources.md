# Sources — NVIDIA Company Research Report

This file lists the source cited in [NVDA_2026-09-03_report.md](NVDA_2026-09-03_report.md).

## Primary and Regulatory Filings

1. **NVIDIA Corporation, Form 10-K for the fiscal year ended January 25, 2026.** Filed February 25, 2026. SEC accession number 0001045810-26-000021.  
   Direct filing: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm

   Report and model sections used:
   - Cover — registrant identity, fiscal year, filing date, and shares outstanding (24,304 million common shares).
   - Item 1, *Business*, pp. 4–11 — company description, reportable segments, products, platform, markets, customers, and Rubin platform.
   - Item 7, *Management’s Discussion and Analysis of Financial Condition and Results of Operations*, pp. 36–43 — fiscal-2026 performance, Compute & Networking revenue ($193,479M / 89.6% of total), gross-margin change, operating expenses, customer concentration, liquidity, CapEx ($6,042M), and outlook statements.
   - Item 8, *Consolidated Financial Statements*:
     - Balance Sheets (p. 53) — opening assets ($206,803M), cash ($10,605M), inventory ($21,403M), net PP&E ($10,383M), debt ($8,468M), and equity ($157,293M).
     - Statements of Income (p. 51) — revenue ($215,938M), cost of revenue ($62,475M), SG&A ($4,574M), D&A ($2,843M), tax expense ($21,383M), and diluted share count (24,514M shares).
   - Item 1A, *Risk Factors*, pp. 12–31 — background risk context referenced by the MD&A.

2. **NVIDIA Corporation, Form 10-K for the fiscal year ended January 26, 2025 (and comparative FY2024 disclosures).** Filed February 26, 2025. SEC accession number 0001045810-25-000023.  
   Direct filing: https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm

   Report and model sections used:
   - Comparative Balance Sheet & Notes — FY2025 ending inventory ($10,080M) used alongside FY2026 inventory to compute the 2-year average inventory ($15,741.5M) for the 91.96 inventory days calculation (`INV_DAYS`).
   - Comparative Debt Disclosures (Note 11) — FY2025 total debt ($8,463M) used to establish average debt ($8,465.5M) for the 3.06% effective debt interest rate (`DEBT_RATE`).
   - Segment Information (Note 17) — FY2025 Compute & Networking revenue ($116,193M) used to calculate the 66.5% (~67%) year-over-year hyper-growth baseline.
   - Audited 3-year history (FY2024–FY2026) for SG&A to gross profit trend and depreciation rate baselining.

3. **NVIDIA Corporation, Form 10-Q for the quarterly period ended July 26, 2026 (Q2 FY2027).** Filed August 27, 2026.  
   Direct filing: https://investor.nvidia.com/files/doc_financials/2027/NVDA-2027-Q2-10Q-Final-including-exhibits.pdf

   Report and model sections used:
   - Balance Sheet as of July 26, 2026 used in `project-1-edition-a.md` for the market-implied enterprise-to-equity bridge as of the September 1, 2026 valuation date ($217.44 closing price reconciliation).
   - Cash and marketable debt securities ($56,586M), total debt claims ($33,366M), and common shares outstanding (24,147M shares).

## Supplemental sources

4. **NVIDIA Corporation, “NVIDIA Announces Financial Results for Second Quarter Fiscal 2027.”** August 26, 2026.  
   Direct release: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/default.aspx

   Report uses:

   - Updated financial context after the fiscal-2026 10-K: Q2 FY2027 revenue of $96.2 billion, Data Center revenue of $89.0 billion, and GAAP gross margin of 75.0%.
   - Management’s Q3 FY2027 outlook: revenue of $108.0 billion, plus or minus 2%, and no assumed Data Center compute revenue from China.
   - CEO Jensen Huang’s assessment that AI demand is accelerating. This is management commentary, not an independently verified forecast.

5. **Associated Press, “U.S. will get a 15% cut of Nvidia and AMD chip sales to China under a new, unusual agreement.”** August 11, 2025.  
   Direct article: https://apnews.com/article/c06e20d9c3418f1d0b1292891c4610c6

   Report uses:

   - Independent context for the H20 situation: the April 2025 halt in sales of certain advanced chips to China and the later resumption framework for H20 sales subject to export licenses.
   - This source provides policy and market context; NVIDIA’s Form 10-K remains the source for the company’s reported H20 charge and revenue.

## Citation convention used in the report

- `[Source: NVIDIA Form 10-K, Item 1—Business, p. X]` identifies a company-description or business-model statement.
- `[Source: NVIDIA Form 10-K, Item 7—MD&A, p. X]` identifies a financial-performance, management-commentary, risk, or outlook statement.
- `[Source: NVIDIA Q2 FY2027 earnings release, Aug. 26, 2026]` identifies a post-10-K result, outlook, or management statement.
- `[Source: Associated Press, Aug. 11, 2025]` identifies independent H20/export-control context.
- Page numbers refer to the numbered pages in the filed Form 10-K, not browser page numbers.
