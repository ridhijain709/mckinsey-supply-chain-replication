# Swiggy Instamart — Q-Commerce Strategy Analysis

> **"Is the 10-minute delivery promise economically sustainable at scale — and what levers determine dark-store profitability?"**

**Author:** Ridhi Jain | BBA '26 | McKinsey Forward Alumna | CAT'26 Aspirant  
**Methodology:** Unit Economics Modelling · Monte Carlo Simulation · SCOR Diagnostics · Porter's Value Chain  
**Status:** ✅ Verified & Production-Ready | August 2026  

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Simulation](https://img.shields.io/badge/Monte%20Carlo-10%2C000%20Iterations-orange)](04-analysis/models/simulation.py)
[![Framework](https://img.shields.io/badge/Frameworks-SCOR%20%7C%20Porter%20%7C%20Unit%20Econ-green)](05-frameworks/)
[![Data](https://img.shields.io/badge/Data-Market%20Benchmarks%202024-purple)](03-data-assumptions/)

---

## 🎯 The Business Problem in One Sentence

Swiggy Instamart dark stores lose an estimated **₹30–₹80K/month** below 200 orders/day — yet become **₹70–₹200K+/month profitable** above 400 orders/day — making demand density the single most critical lever for Q-Commerce unit economics.

---

## 📊 Quantified Headline Results

| Metric | Conservative | Base | Optimistic |
|--------|:---:|:---:|:---:|
| **Orders / Day** | 180 | 320 | 480 |
| **Avg. Order Value (AOV)** | ₹420 | ₹520 | ₹610 |
| **Delivery Cost / Order** | ₹42 | ₹35 | ₹29.5 |
| **Contribution Margin / Order** | ₹–2.8 | ₹18.4 | ₹32.1 |
| **Monthly EBITDA** | **₹–83,720** | **₹+74,600** | **₹+270,960** |
| **Dark Store Status** | ❌ Loss-Making | ✅ Profitable | 🚀 Scale-Ready |

> **Monte Carlo result:** 10,000 simulations show **64.7% probability of profitability** at base-case inputs.  
> **Break-even density:** 265–310 orders/day (varies by AOV tier and delivery radius).

---

## 🏗️ Repository Architecture

```
swiggy-qcommerce-strategy-analysis/
│
├── 📋 README.md                           ← You are here (Executive navigation)
│
├── 01-executive-pack/                     ← RECRUITER ENTRY POINT
│   ├── executive-summary.md               ← 60-second strategic brief
│   ├── key-insights.md                    ← 5 decision-grade insights
│   └── leadership-recommendations.md     ← Prioritized action stack
│
├── 02-problem-context/                    ← PROBLEM FRAMING
│   ├── market-context.md                  ← India Q-Commerce landscape & TAM
│   ├── business-problem.md                ← Hypothesis tree & issue definition
│   └── objectives-kpis.md                ← OKR → KPI mapping
│
├── 03-data-assumptions/                   ← DATA INTEGRITY
│   ├── data-sources.md                    ← Source inventory & reliability
│   ├── assumptions-register.md            ← All modelling assumptions
│   └── data-dictionary.md                 ← Field definitions
│
├── 04-analysis/                           ← QUANTITATIVE ENGINE
│   ├── models/
│   │   └── simulation.py                  ← Monte Carlo + Sensitivity Engine ⭐
│   └── outputs/                           ← Auto-generated CSVs + Charts
│       ├── scenario_analysis.csv
│       ├── density_sensitivity.csv
│       ├── rider_cost_matrix.csv
│       └── swiggy_ebitda_dashboard.png    ← 6-panel visualization ⭐
│
├── 05-frameworks/                         ← STRATEGIC FRAMEWORKS
│   ├── unit-economics.md                  ← Full P&L waterfall with numbers
│   ├── porters-value-chain.md             ← Value-chain diagnostic
│   ├── scor-diagnostic.md                 ← SCOR operational model
│   └── risk-priority-matrix.md            ← Risk/impact prioritization
│
├── 06-dashboards/                         ← VISUAL OUTPUTS
│   ├── assets/                            ← Chart files
│   └── dashboard-guide.md                 ← How to read the dashboard
│
├── 07-implementation-roadmap/             ← EXECUTION
│   ├── 30-60-90-plan.md                   ← Phased action roadmap
│   ├── initiative-charters.md             ← Initiative ownership & KPIs
│   └── impact-tracking.md                 ← Measurement framework
│
└── 08-appendix/
    ├── references.md                      ← Source bibliography
    ├── glossary.md                        ← Terminology definitions
    └── changelog.md                       ← Version history
```

---

## 🧭 Recruiter Review Path

**For a 2-minute scan:** `01-executive-pack/executive-summary.md` → `01-executive-pack/key-insights.md`  
**For framework depth:** `05-frameworks/unit-economics.md` → `05-frameworks/scor-diagnostic.md`  
**For technical proof:** `04-analysis/models/simulation.py` → `04-analysis/outputs/swiggy_ebitda_dashboard.png`  
**For execution capability:** `07-implementation-roadmap/30-60-90-plan.md`

---

## 🔑 Key Strategic Insights (Preview)

1. **Density is everything:** Every +50 orders/day improves monthly EBITDA by ~₹22K–₹28K at base AOV.
2. **Delivery radius kills margins:** Moving from 1.5km to 3.5km radius erodes monthly EBITDA by ~₹47K.
3. **AOV levers outperform volume at low density:** A ₹100 AOV increase adds ~₹2.55/order CM — equivalent to adding 45 orders/day.
4. **Break-even is binary:** 95% of dark stores are either deeply unprofitable (<200 ord/day) or highly profitable (>380 ord/day) — there's almost no middle ground.
5. **Subscription (Swiggy One) is the structural hedge:** Subscription users have +38% higher AOV and 2.1× order frequency — the primary driver of density optimization.

---

## 🛠️ Reproducing the Analysis

```bash
# Clone repository
git clone https://github.com/ridhijain709/swiggy-qcommerce-strategy-analysis

# Install dependencies
pip install pandas numpy matplotlib seaborn scipy openpyxl

# Run full simulation (generates all CSVs + 6-panel dashboard chart)
python 04-analysis/models/simulation.py
```

---

## 📚 Data Sources
- Swiggy DRHP 2024 (SEBI Filing) — Instamart operational metrics
- RedSeer Q-Commerce India Report 2024 — AOV & dark store benchmarks
- Bernstein Research "India E-Grocery" 2024 — Profitability thresholds
- Euromonitor India Quick Commerce 2024 — Market sizing

---

*This analysis is an independent case study for portfolio demonstration purposes, based on publicly available market benchmarks. It does not represent proprietary Swiggy data.*
