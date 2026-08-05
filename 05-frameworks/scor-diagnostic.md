# SCOR Diagnostic — Swiggy Instamart Q-Commerce Operations

> SCOR (Supply Chain Operations Reference) model applied to dark-store operations. Diagnoses performance gaps across Plan → Source → Make → Deliver → Return → Enable.

---

## SCOR Framework Mapping for Q-Commerce

| SCOR Process | Q-Commerce Equivalent | Primary KPI | Current (Est.) | Target |
|:------------|:----------------------|:-----------:|:--------------:|:------:|
| **Plan** | Demand forecasting, slot allocation, inventory pre-positioning | Forecast Accuracy (%) | 71% | ≥88% |
| **Source** | Supplier procurement, dark store restocking, vendor SLA management | Fill Rate (%) | 84% | ≥95% |
| **Make** | Order picking, packing, quality check, temperature management | Pick Accuracy (%) | 96.2% | ≥98.5% |
| **Deliver** | Rider dispatch, route optimization, last-mile execution | On-Time Delivery (%) | 81% | ≥91% |
| **Return** | Damaged/wrong item returns, refund processing, reverse logistics | Return Rate (%) | 3.8% | ≤2.0% |
| **Enable** | Tech infrastructure, data analytics, partner onboarding | Platform Uptime (%) | 99.1% | ≥99.7% |

---

## Performance Gap Analysis

### 🔴 Critical Gaps (Immediate Action Required)

**1. Demand Forecasting (Plan) — 71% Accuracy → Target 88%**

Current gap: Dark stores overstock 28% of SKUs and stockout 18% of high-velocity items (estimated from RedSeer Q-Commerce Ops Report 2024).

Root cause: Slot-level demand models do not account for:
- Weather-correlated demand spikes (+35% for hot drinks/cold beverages on 35°C+ days)
- Local event-driven demand (nearby cricket match, festive day)
- Substitution cascade effects when primary SKU stockouts

**Solution:** Integrate hyper-local demand signals (weather API, event calendar) into forecasting engine. Implement safety-stock tiering: Tier 1 (top 50 SKUs by velocity) maintain 2-day buffer; Tier 2 (next 200 SKUs) maintain 1-day buffer.

**Financial Impact:** Reducing stockouts from 18% → 8% of items recovers est. 4–6% of lost orders = **+12–18 orders/day** per store.

---

**2. Last-Mile Delivery (Deliver) — 81% On-Time → Target 91%**

Current gap: 19% of orders delivered outside the promised 10-minute window. Primary causes:
- Rider allocation lag at peak demand windows (7–9pm) — 34% of on-time failures
- Multi-order batching failures when zones misalign — 28%
- Dark store picking delays (>3 min per order) — 22%
- Traffic/parking — 16%

**Solution Stack:**
- Pre-position riders 15 minutes ahead of predicted peak surge (ML-based demand signal)
- Limit batching to co-directional orders within 400m delivery endpoint proximity
- Reduce picking time via warehouse slotting optimization (velocity-based shelf placement)

**Financial Impact:** On-time improvement from 81% → 91% reduces refund/credit issuance by ~₹8,500/store/month and improves repeat order rate by est. 6%.

---

### 🟡 Moderate Gaps (30–60 Day Action)

**3. Fill Rate (Source) — 84% → Target 95%**

Driven by vendor SLA inconsistency in Tier 2 cities. Resolution: Dual-vendor sourcing for top-50 velocity SKUs; penalty clauses for fill rate <90% over rolling 7-day window.

**4. Return Rate (Return) — 3.8% → Target 2.0%**

High return rate on fresh produce (expiry, quality). Solution: FIFO enforcement at picking station + daily freshness audit at store open.

---

## SCOR Metrics Dashboard

```
SCOR PERFORMANCE DASHBOARD — Swiggy Instamart (Est. Q1 FY2026)
═══════════════════════════════════════════════════════════════

PLAN         Forecast Accuracy      ████████░░  71%  [Target: 88%]  ⚠️  GAP: 17pp
SOURCE       Fill Rate              █████████░  84%  [Target: 95%]  ⚠️  GAP: 11pp
MAKE         Pick Accuracy          ██████████  96%  [Target: 98%]  ✅  GAP:  2pp
DELIVER      On-Time Delivery       █████████░  81%  [Target: 91%]  🔴  GAP: 10pp
RETURN       Return Rate (inv.)     ██████████  96%  [Target: 98%]  ✅  GAP:  2pp
ENABLE       Platform Uptime        ██████████  99%  [Target: 99.7%]✅  GAP: 0.6pp

Overall SCOR Score: 87.8 / 100  [Industry Best-in-Class: 94+]
Performance vs Target: 4 of 6 process areas require active intervention
```

---

## SCOR Improvement Roadmap

| Phase | Initiative | SCOR Area | Timeline | Owner |
|:------|:-----------|:---------:|:--------:|:-----:|
| 1 | Demand signal API integration (weather + events) | Plan | 0–30d | Data Science |
| 1 | Safety-stock tiering for Top 200 SKUs | Source | 0–30d | Procurement |
| 2 | Rider pre-positioning ML model | Deliver | 30–60d | Ops Tech |
| 2 | Velocity-based shelf slotting | Make | 30–60d | Dark Store Ops |
| 3 | Dual-vendor sourcing for Tier 2 cities | Source | 60–90d | Category |
| 3 | FIFO enforcement + freshness audit protocol | Return | 60–90d | Quality |

---

*SCOR methodology reference: ASCM SCOR Framework v12.0. All current performance figures are estimates based on industry benchmarks from RedSeer Q-Commerce Report 2024 and Swiggy DRHP 2024 disclosures.*
