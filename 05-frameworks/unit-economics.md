# Unit Economics Framework — Swiggy Instamart Dark Store

> Full P&L structure, lever analysis, and sensitivity matrix. All figures derived from `04-analysis/models/simulation.py` using public benchmark data.

---

## Revenue Architecture (Per Order)

Swiggy earns through three revenue streams per Instamart order:

| Revenue Stream | Rate | On AOV ₹520 | Notes |
|:--------------|:----:|:-----------:|:------|
| **Grocery Commission** | 8.5% | ₹44.2 | Merchant margin share (DRHP 2024) |
| **Convenience Fee** | avg. ₹22 retained | ₹22.0 | ₹25–35 charged; ₹22 net after payment gateway |
| **Ad/Banner Revenue** | 5.5% | ₹28.6 | Brand placement, search ads, in-app promotions |
| **Blended Effective Rate** | **18.5%** | **₹96.2** | Total platform revenue per order |

---

## Cost Architecture (Per Order)

| Cost Item | Conservative | Base | Optimistic | Driver |
|:----------|:------------:|:----:|:----------:|:-------|
| **Delivery Cost** | ₹42.0 | ₹35.0 | ₹29.5 | Distance + rider utilization rate |
| **Picking & Packing** | ₹12.0 | ₹12.0 | ₹12.0 | Warehouse labor (fairly fixed) |
| **Marketing / CAC** | ₹4.0 | ₹4.0 | ₹4.0 | Lower for subscribers |
| **Total Variable Cost** | ₹58.0 | ₹51.0 | ₹45.5 | |

---

## Per-Order P&L Waterfall (Base Scenario, AOV ₹520)

```
Revenue
  ├── Commission (8.5% × ₹520)      = +₹44.2
  ├── Convenience Fee (net)          = +₹22.0
  └── Ad Revenue (5.5% × ₹520)      = +₹28.6
      ─────────────────────────────────────────
      Gross Revenue per Order        = +₹96.2   [18.5% effective rate]

Variable Costs
  ├── Delivery (2km radius)          = –₹35.0
  ├── Picking & Packing              = –₹12.0
  └── Marketing / CAC                = –₹ 4.0
      ─────────────────────────────────────────
      Contribution Margin / Order    = +₹45.2   ✅ Positive

Monthly (320 orders/day × 30 days = 9,600 orders)
  Monthly Contribution Margin       = +₹4,33,920

Fixed Costs
  ├── Dark Store Rent                = –₹1,00,000
  ├── Tech Overhead                  = –₹ 15,000
  └── Capex Amortization (36mo)      = –₹  6,944
      ─────────────────────────────────────────
      Total Monthly Fixed            = –₹1,21,944

Monthly EBITDA (Base)               = +₹3,11,976  ✅
EBITDA Margin (on GMV)              =    6.25%
```

---

## Three-Tier Scenario Summary

| Scenario | Orders/Day | AOV | CM/Order | Monthly EBITDA | EBITDA Margin | Status |
|:---------|:----------:|:---:|:--------:|:--------------:|:-------------:|:------:|
| **Conservative** | 180 | ₹420 | ₹19.7 | **–₹35,564** | –1.57% | ❌ Loss |
| **Base** | 320 | ₹520 | ₹45.2 | **+₹3,11,976** | 6.25% | ✅ Profit |
| **Optimistic** | 480 | ₹610 | ₹67.4 | **+₹8,57,896** | 9.77% | 🚀 Scale |

---

## Break-Even Order Density by AOV Tier

| AOV Tier | AOV (₹) | Break-Even Orders/Day | Monthly Fixed Cost Coverage |
|:---------|:-------:|:---------------------:|:---------------------------:|
| Low | ₹420 | **160 ord/day** | 160 × 30 × ₹19.7 = ₹94,560 |
| Mid | ₹520 | **100 ord/day** | 100 × 30 × ₹45.2 = ₹135,600 |
| High | ₹620 | **70 ord/day** | 70 × 30 × ₹66.7 = ₹140,070 |

> Note: Fixed costs = ₹121,944/month. Break-even = Fixed Costs ÷ (CM/Order × 30)

---

## Sensitivity Matrix: EBITDA at Various Order Volumes & AOV (₹ Thousands/Month)

|               | 100 ord/day | 150 ord/day | 200 ord/day | 280 ord/day | 350 ord/day | 420 ord/day | 500 ord/day |
|:-------------|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|
| **AOV ₹420** | –₹86K | –₹75K | –₹58K | –₹37K | **–₹12K** | **+₹13K** | +₹44K |
| **AOV ₹520** | –₹79K | –₹57K | –₹34K | **+₹1K** | **+₹31K** | **+₹62K** | +₹99K |
| **AOV ₹620** | –₹70K | –₹39K | –₹8K | **+₹41K** | **+₹82K** | **+₹122K** | +₹172K |

🟥 = Loss-making | 🟨 = Near break-even | 🟩 = Profitable

---

## Key Economic Levers Ranked by EBITDA Impact

| Rank | Lever | Impact on Monthly EBITDA | Difficulty |
|:----:|:------|:------------------------:|:----------:|
| 1 | +50 orders/day (demand densification) | +₹67,800 | Medium |
| 2 | AOV uplift ₹100 (bundling/substitution) | +₹99,900 | Low |
| 3 | Delivery radius –1km (2.5→1.5km) | +₹44,400 | Medium |
| 4 | Swiggy One penetration +10pp | +₹38,200 | Medium |
| 5 | Rent renegotiation –₹10,000 | +₹10,000 | Low |
| 6 | Picking cost –₹2/order | +₹5,760 | High |

---

*Source: Simulation output from [`simulation.py`](../04-analysis/models/simulation.py). All benchmarks from Swiggy DRHP 2024, RedSeer Q-Commerce Report 2024, Bernstein India E-Grocery 2024.*
