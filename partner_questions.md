# Peer Review & Partner Defense Exchange: NVIDIA vs. UiPath (PATH)

**Course:** FIN 43900 — AI and Finance  
**Target Analyzed:** NVIDIA Corporation (NASDAQ: NVDA)  
**Partner Target:** UiPath Inc. (NYSE: PATH)  
**Valuation Date:** Fall 2026  

---

## 1. Questions Asked to Partner (UiPath) & Responses

### Question 1: Revenue Mix
> **"Where does your revenue mix come from — how much is renewable license/ARR revenue versus subscription and cloud ARR versus professional services, and which piece is growing?"**

* **Context & What to Look For:** UiPath reports revenue across three streams with different economics: (1) licenses, which are primarily renewable term licenses that contribute to ARR; (2) subscription services and cloud ARR, the faster-growing recurring component; and (3) professional services and other revenue, which has lower margin. Check whether the model separates these streams or uses a single blended top-line growth rate. The key question is whether the fast-growing subscription/cloud component is modeled explicitly, since it drives revenue durability and margin pressure from hosting costs.
* **Partner's Response:**
  * **FY2026 revenue mix:** Licenses were **$606M** (up 3%), subscription services were **$954M** (up 19%), and professional services and other were **$50M** (up 23%), for total revenue of **$1,611M** (up 13%). This is approximately **38% licenses / 59% subscription services / 3% professional services and other**. [SEC Form 10-K](https://www.sec.gov/Archives/edgar/data/1734722/000173472226000012/path-20260131.htm)
  * **Important qualification:** “Licenses” are primarily renewable term licenses that contribute to ARR; UiPath is not primarily a one-time perpetual-license business. Subscription services are the principal growth engine.
  * **ARR evidence:** Cloud ARR exceeded **$1.3B**, up more than 19% year over year; total ARR rose 12% to **$1.938B**. [Quartr Q2 FY2027 event](https://quartr.com/events/uipath-inc-path-q2-2027_332pAUxO), [MarketBeat Q2 FY2027 call summary](https://www.marketbeat.com/instant-alerts/transcript-uipath-q2-earnings-call-highlights-2026-09-03/)
  * **Source of growth:** Existing customers generated 85% of FY2026 revenue growth, versus 15% from new customers. [SEC Form 10-K](https://www.sec.gov/Archives/edgar/data/1734722/000173472226000012/path-20260131.htm)

---

### Question 2: Gross Margin Trajectory
> **"Why is your gross margin where it is, and does it improve as the mix shifts toward cloud? Are you modeling services gross margin separately from software gross margin?"**

* **Context & What to Look For:** UiPath's economics are split between two very different cost structures:
  1. *Software/Subscription Gross Margin:* ~85%+ — this is the scalable core of the business.
  2. *Professional Services Gross Margin:* Often near breakeven or slightly negative — implementation and training are cost centers, not profit centers.
  If services revenue shrinks as a share of total (as customers self-implement or use partners), blended gross margin should naturally rise. Check whether their model captures this mix shift or holds a flat consolidated margin. Also check: does their model account for growing cloud hosting costs (Azure/AWS infrastructure) as UiPath migrates on-prem customers to the cloud?
* **Partner's Response:**
  * **Margin level:** Blended gross margin is in the low 80s because software has very high margins while professional services dilute the consolidated rate. In Q2 FY2027, non-GAAP gross margin was **82%**, GAAP gross margin was **80%**, and software gross margin was **90%**. [Quartr Q2 FY2027 event](https://quartr.com/events/uipath-inc-path-q2-2027_332pAUxO)
  * **Cloud-mix effect:** The cloud shift is a mild gross-margin headwind, rather than a tailwind, because SaaS hosting costs do not apply to term licenses in the same way. FY2025 gross margin fell to 83% from 85%, partly due to increased subscription-services hosting and personnel costs. [QZ earnings coverage](https://qz.com/uipath-inc-class-a-path-reports-earnings-1851772073)
  * **Forecast treatment:** Management guided to approximately 84% full-year non-GAAP gross margin, so the model holds consolidated margin roughly flat. [MarketBeat Q2 FY2027 call summary](https://www.marketbeat.com/instant-alerts/transcript-uipath-q2-earnings-call-highlights-2026-09-03/)
  * **Separate-services treatment:** Professional services are modeled separately at a much lower margin. The segment is sufficiently small that it has limited effect on the blended gross-margin result.

---

### Question 3: Treatment of Stock-Based Compensation
> **"UiPath pays a huge share of employee comp in stock — how did you treat stock-based compensation? Is it a real expense in your income statement, and does your share count grow each year from dilution?"**

* **Context & What to Look For:** UiPath has historically spent 20%–25% of revenue on stock-based compensation. This matters in three places:
  1. *Income Statement:* Is SBC included as an operating expense (GAAP treatment), or did they use non-GAAP adjusted numbers that exclude it? Excluding SBC overstates true profitability.
  2. *Balance Sheet:* SBC should credit equity (additional paid-in capital) as shares are issued to employees.
  3. *Share Count / Dilution:* Equity grants create gross dilution, but repurchases can offset some or all of it. The key test is whether the model supports a flat **net** share count with documented buybacks; if buybacks slow or stop while grants continue, value per share is overstated because the equity pie is divided by too few shares.
* **Partner's Response:**
  * **GAAP treatment:** Stock-based compensation is treated as a real operating expense. The model uses GAAP operating income, not a non-GAAP measure that adds SBC back. SBC was **$291M in FY2026**, down from **$358M in FY2025** and **$372M in FY2024**, and was roughly 18% of FY2026 revenue; excluding it would materially overstate margins. [EDGAR company data](https://app.edgar.tools/companies/PATH)
  * **Share-count treatment:** Gross RSU dilution is assumed to be offset by repurchases, producing a roughly flat net share count. UiPath repurchased **$329M** of stock in FY2026 and **$391M** in FY2025, and announced a new **$500M** authorization after completing its prior $1B program. [EDGAR company data](https://app.edgar.tools/companies/PATH), [Business Wire authorization announcement](https://www.businesswire.com/news/home/20260311599358/en)
  * **Sensitivity / limitation:** If repurchases cease while equity grants continue, the diluted share count would increase and the model’s per-share valuation would be overstated under the flat-share-count assumption.

---

## 2. Presenter Defense Record (Your NVIDIA Defense)

### Question 1 Received
> **"Why did you choose NVIDIA, and which 10-K source supports your claim that data-center demand is its main revenue driver?"**

**Answer:** I chose NVIDIA because its Compute & Networking segment grew 67% in FY2026, making the durability of AI-driven demand the single most consequential question for its enterprise value. The source is NVIDIA's Form 10-K for the fiscal year ended January 25, 2026 (SEC Accession No. `0001045810-26-000021`), specifically the MD&A Revenue by Reportable Segments disclosure on page 40: Compute & Networking revenue was $193,479 million out of $215,938 million total revenue (~90% of the top line). The segment breakdown is also cross-referenced in Note 17 (Segment Information). Data Center GPU and networking platform sales are the dominant sub-driver within that segment.

---

### Question 2 Received
> **"How does your AI/data-center revenue-growth assumption move through revenue, gross margin, cash flow, and finally value per share?"**

**Answer:** The causal chain through the linked 3-statement model works as follows:
1. **Revenue:** Each year's revenue = prior year × (1 + 65.5% growth), compounding the base across all five forecast years (FY2027–FY2031).
2. **Gross Profit:** Revenue × 71.07% gross margin = gross profit. Because NVIDIA is fabless (TSMC manufactures chips), the margin is high and relatively stable, so revenue growth flows almost one-for-one into gross profit growth.
3. **Operating Profit:** Gross profit minus SG&A (held at ~3.0% of gross profit) minus D&A. SG&A is small relative to gross profit, so operating leverage is strong — most incremental gross profit drops to operating income.
4. **Net Income:** Operating income minus interest expense minus taxes (at the 15.1% effective rate). Interest is minimal because NVIDIA's debt is small relative to its cash generation.
5. **FCFE:** Net income + D&A − CapEx − change in inventory − change in other working capital. The working capital drag (inventory buildup at 92 days of COGS) partially offsets earnings, but D&A addback and low capex ($6B vs. $100B+ in operating cash flow) mean most of net income converts to free cash.
6. **Value per Share:** The five annual FCFEs are discounted at 10%, then the Year 5 FCFE is capitalized into a terminal value at (10% − 2.5%) and discounted back. The sum is divided by 24,304 million shares. Because the terminal value is 84% of total equity value, the compounding effect of revenue growth on the Year 5 FCFE is the dominant transmission mechanism to value per share.

---

### Question 3 Received
> **"Could your main-driver ranking change if you used a different growth or gross-margin range, especially if AI spending slows down?"**

**Answer:** Yes — the ranking is strictly conditional on the tested ranges. In our sensitivity analysis, we tested revenue growth at ±1,000 bps (55.5%–75.5%) and gross margin at ±300 bps (68.07%–74.07%). Revenue growth produced the larger value-per-share span ($353.47 vs. $61.83) primarily because:
* Revenue growth **compounds** across all five years — a 10-percentage-point change in Year 1 cascades into a much larger absolute dollar difference by Year 5.
* The tested revenue range was proportionally wider than the gross margin range.

If AI spending slowed significantly and we narrowed the revenue range to ±200 bps while simultaneously widening the gross margin range to ±500 bps (simulating pricing pressure from custom ASICs like Google TPU or AWS Trainium), gross margin could overtake revenue growth as the top-ranked driver. The sensitivity table establishes which driver matters more *over these specific ranges* — it does not prove universal dominance. This is explicitly noted in the model output: "The comparison is range-specific; its wider tested range can contribute to the larger span."

---

### Feedback Received
* **Strength:** “Your causal chain was very clear—from revenue to gross profit, operating profit, FCFE, and value per share.”
* **Improvement:** “I would add a second, more conservative sensitivity range for revenue growth, because the wide ±1,000-basis-point range makes revenue appear especially important.”
* **Response / next revision:** Retain the existing ±1,000-basis-point stress case, but add a narrower revenue-growth range as a second sensitivity. Compare the output spans under both ranges and state whether revenue remains the leading driver when the range-width advantage is reduced.

### Actions Taken Post-Feedback
* **Keep:** The fully integrated 3-statement forecast model, the automated `assert_balanced()` audit check, and the conservative 10% WACC / 2.5% terminal growth DCF bounds.
* **Revise:** Formally label the sensitivity ranking as "range-conditional" rather than universally dominant. Added explicit language in the locked record that narrower revenue or wider margin ranges could reverse the finding.
* **Investigate Next:** Review the upcoming Form 10-Q for segment-level Compute & Networking gross margins and hyperscaler customer concentration trends.

---

## 3. Reviewer Audit Record (Your Critique of Partner's UiPath Model)

### Summary of Audit Check Performed
* **Check Performed:** Verified the partner's sensitivity run by checking that non-tested inputs were reset to base and that the changed-minus-base output moved in the predicted direction through the linked statements.
* **10-K Source Verified:** Cross-referenced UiPath's reported ARR (Annual Recurring Revenue) and revenue breakdown (subscription vs. services) against the assumptions used in their pro-forma model.
* **Check Result:** Balance-sheet checks confirmed formula linkages were intact; the accounting identity held across all projected years.

### Explanation Back & Feedback
* **Conclusion & Drivers:** Partner concluded UiPath is a high-growth enterprise software company transitioning from on-premise licenses to cloud subscriptions, with equity value driven primarily by ARR growth and the path to sustained GAAP profitability.
* **Identified Strength:** The model correctly captured UiPath's subscription-driven recurring revenue base and recognized that software gross margins (~85%+) are structurally higher than blended margins, giving the business significant operating leverage as it scales. The linked model also properly showed that UiPath's capital-light model (minimal PP&E, no inventory) means almost all operating profit converts directly to free cash flow once the company reaches profitability.
* **Identified Improvement:** The model correctly treats SBC as a GAAP operating expense and assumes that repurchases offset gross RSU dilution, producing a roughly flat **net** share count. That assumption should be made conditional: UiPath repurchased $329M in FY2026, but per-share value would be overstated if buybacks slow or stop while equity grants continue. A more complete model would show annual gross shares issued, shares repurchased, and resulting net diluted shares, then include a no-buyback dilution sensitivity.

---

## 4. UiPath Company Summary

* **Business and revenue base:** UiPath is an enterprise automation-software company. FY2026 revenue was **$1,611M**, consisting of licenses of **$606M** (38%), subscription services of **$954M** (59%), and professional services/other of **$50M** (3%). Although licenses are separately reported, they are largely renewable term licenses that contribute to ARR rather than a traditional one-time perpetual-license business.
* **Growth engine:** Subscription and cloud adoption are the principal sources of growth. Subscription-services revenue grew 19% in FY2026, Cloud ARR exceeded $1.3B, and total ARR reached $1.938B. Existing customers accounted for 85% of FY2026 revenue growth.
* **Margins:** UiPath's software business is highly scalable, with a 90% Q2 FY2027 software gross margin, but consolidated margins are lower because professional services have weaker economics and cloud delivery requires hosting and support costs. Q2 FY2027 GAAP gross margin was 80%, versus 82% non-GAAP.
* **Cloud-mix implication:** Cloud delivery supports recurring revenue, but it is not automatically margin-accretive. Hosting and subscription-services personnel costs contributed to gross-margin decline from 85% in FY2024 to 83% in FY2025; therefore, a roughly flat consolidated-margin forecast is reasonable unless management demonstrates hosting-cost leverage.
* **SBC and per-share value:** SBC was $291M in FY2026, roughly 18% of revenue, and remains a real GAAP operating expense. FY2026 repurchases of $329M can offset RSU dilution and support a flat net share-count assumption, but if buybacks stop while grants continue, diluted shares would rise and per-share value would fall.
* **Overall analytical takeaway:** UiPath has a recurring-revenue, high-software-margin model with installed-base expansion potential. The key valuation questions are whether subscription/cloud growth can outpace hosting-cost pressure, whether services remain immaterial to blended margins, and whether ongoing buybacks continue to neutralize SBC dilution.
