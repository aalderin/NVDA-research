# NVIDIA (NVDA) Peer Selection & Comparability Policy

**Company:** NVIDIA Corporation (NASDAQ: NVDA)  
**Valuation Subject:** Comparable Company P/E Multiple Analysis & DCF Benchmark  
**Date:** September 17, 2026  
**Status:** Initial Policy Baseline (Visible Policy)

---

## 1. Business Economics That MUST Match (Mandatory Inclusion Criteria)

To be admitted into NVIDIA’s peer valuation set, a candidate company must satisfy three core economic criteria:

1. **High-Performance Silicon & Compute Architecture:**  
   The candidate must design advanced accelerated compute processors (GPUs, custom accelerators/ASICs, high-throughput network fabrics, or data-center CPUs) targeting AI training, AI inference, high-performance computing (HPC), or enterprise graphics.
2. **Data Center & Cloud Infrastructure End-Market Exposure:**  
   A substantial portion of earnings must depend on enterprise, cloud service provider (CSP), and sovereign infrastructure capital expenditures.
3. **Fabless Semiconductor Design Model:**  
   The candidate must operate an asset-light, fabless operating model (outsourcing foundry fabrication and advanced packaging to third-party foundries like TSMC) to share comparable gross margin dynamics, working capital profiles, and R&D-to-revenue reinvestment structures.

---

## 2. Differences That Require Qualification vs. Exclusion

| Category | Characteristic / Criterion | Action & Valuation Policy | Candidate Examples |
| :--- | :--- | :--- | :--- |
| **Qualify (Retain Peer)** | **Direct Chip Competitor (Hardware vs Full Stack)** | **Retain:** Direct competitor in accelerated GPUs/CPUs. **Qualify:** Adjust for CUDA software ecosystem advantage and gross margin differential (~70%+ vs ~50%). | **Advanced Micro Devices (AMD)** |
| **Qualify (Retain Peer)** | **Custom AI Silicon (ASIC) + Enterprise Software** | **Retain:** Dominant AI networking (Ethernet/PCIe) and custom ASIC silicon. **Qualify:** Adjust for non-semi enterprise software mix (e.g., VMware). | **Broadcom (AVGO)** |
| **Qualify (Retain Peer)** | **Edge / Mobile AI & Connectivity Mix** | **Retain:** High-performance fabless design. **Qualify:** Slower-growth smartphone/handset market drag vs. pure Data Center AI growth. | **Qualcomm (QCOM)** |
| **Exclude (Disqualify)** | **Cloud Hyperscalers (Direct Customers)** | **Exclude:** Hyperscalers are NVIDIA’s primary *customers* (representing ~36%+ of FY2026 revenue). Their core business is cloud hosting, advertising, and enterprise SaaS—not chip design. | *Microsoft (MSFT), Alphabet (GOOGL), Amazon (AMZN), Meta (META)* |
| **Exclude (Disqualify)** | **Pure Semiconductor Foundries** | **Exclude:** Capital-intensive contract manufacturing with heavy fab CapEx, cleanroom depreciation, and wafer yield risk rather than merchant chip architecture. | *TSMC (TSM), GlobalFoundries (GFS)* |
| **Exclude (Disqualify)** | **Semiconductor Equipment (Toolmakers)** | **Exclude:** Revenue depends on foundry equipment tool install cycles (lithography, etch, deposition) rather than compute workload demand. | *ASML, Applied Materials (AMAT), Lam Research (LRCX)* |
| **Exclude (Disqualify)** | **Commodity Memory (DRAM / HBM)** | **Exclude:** Subject to extreme commodity memory pricing cycles and lower pricing power than proprietary compute platforms. | *Micron Technology (MU), SK Hynix* |

---

## 3. Initial Peer Selection Policy Summary

| Peer Candidate | Ticker | Initial Policy Status | Rationale / Key Qualification |
| :--- | :---: | :---: | :--- |
| **Advanced Micro Devices** | **AMD** | **Qualified Peer (Include)** | Purest direct GPU/CPU competitor (Instinct MI300/MI350 series); qualifies for software ecosystem gap (ROCm vs CUDA). |
| **Broadcom Inc.** | **AVGO** | **Qualified Peer (Include)** | Critical AI networking (Tomahawk/Jericho) and custom XPUs; qualifies for VMware enterprise software revenue mix. |
| **Qualcomm Inc.** | **QCOM** | **Qualified Peer (Include)** | Leading fabless NPU/mobile architecture; qualifies for handset market exposure and lower margin profile. |
| **TSMC / Foundries** | **TSM** | **Excluded** | Foundry manufacturer, not fabless compute designer. |
| **Microsoft / Hyperscalers**| **MSFT** | **Excluded** | Downstream customer, cloud hosting and enterprise software provider. |

---

## 4. Policy Revision Protocol

1. **Initial Baseline:** The peer comparison set consists of qualified fabless compute and networking peers (**AMD, AVGO, QCOM**).
2. **Revision Rules:**
   - Any peer whose Data Center / AI-related revenue drops below **20%** of total revenue will be disqualified.
   - Any peer transitioning to an integrated device manufacturing (IDM) model with proprietary fab ownership will be excluded.
   - If a peer is removed or added, the specific policy criterion failure will be documented in this log **before** recalculating peer median multiples or implied share prices.

