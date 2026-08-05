# Assumptions Register — Modelling Assumptions Log

> All assumptions underlying the unit economics model in `04-analysis/models/simulation.py`.  
> Last updated: August 2026 | Validated against: Swiggy DRHP 2024, RedSeer, Bernstein Research.

---

## Revenue Assumptions

| # | Assumption | Value | Source | Strategic Sensitivity |
|:-:|:-----------|:-----:|:------:|:---------------------:|
| R1 | Grocery commission rate | 8.5% of GMV | Swiggy DRHP 2024 | 🔴 HIGH — ±1pp = ±₹5.2/order CM |
| R2 | Convenience fee (platform retained) | ₹22/order avg. | DRHP + industry avg. | 🟡 MEDIUM — consumer price sensitive |
| R3 | Ad/banner revenue per order | 5.5% of AOV | DRHP revenue breakdown est. | 🟡 MEDIUM — scales with GMV |
| R4 | Blended effective take rate | 18.5% | Derived: R1+R2+R3 | 🔴 HIGH — master revenue lever |
| R5 | Base Case AOV | ₹520 | RedSeer Q-Commerce India 2024 | 🔴 HIGH — ±₹100 = ±₹99,900/mo EBITDA |
| R6 | Conservative AOV | ₹420 | Lower bound (grocery-only basket) | 🟡 MEDIUM |
| R7 | Optimistic AOV | ₹610 | Upper bound (cross-category basket) | 🟢 LOW |

---

## Cost Assumptions

| # | Assumption | Value | Source | Strategic Sensitivity |
|:-:|:-----------|:-----:|:------:|:---------------------:|
| C1 | Delivery cost — Conservative | ₹42/order | Avg. 3.5km radius, 1 run/hr | 🔴 HIGH |
| C2 | Delivery cost — Base | ₹35/order | 2km radius, 2 runs/hr | 🔴 HIGH |
| C3 | Delivery cost — Optimistic | ₹29.5/order | 1.5km radius, 3 runs/hr | 🔴 HIGH |
| C4 | Rider cost per km (fuel + time) | ₹7/km | Industry average FY2025 | 🟡 MEDIUM |
| C5 | Rider base cost (fixed per delivery) | ₹18/delivery | Floor for sub-1km deliveries | 🟡 MEDIUM |
| C6 | Picking & packing cost | ₹12/order | Warehouse ops (RedSeer) | 🟢 LOW — relatively fixed |
| C7 | Marketing/CAC per order | ₹4/order | Blended (lower for subscribers) | 🟢 LOW |

---

## Fixed Cost Assumptions

| # | Assumption | Value | Source | Strategic Sensitivity |
|:-:|:-----------|:-----:|:------:|:---------------------:|
| F1 | Dark store rent — Conservative | ₹1,20,000/month | Tier-1 peripheral zone, 1,200 sq.ft | 🔴 HIGH |
| F2 | Dark store rent — Base | ₹1,00,000/month | Residential hub location | 🔴 HIGH |
| F3 | Dark store rent — Optimistic | ₹90,000/month | Multi-store lease negotiated | 🟡 MEDIUM |
| F4 | Tech overhead (POS + routing) | ₹15,000/month | Platform cost allocation | 🟢 LOW |
| F5 | Dark store capex (fit-out) | ₹2,50,000 one-time | Industry average | 🟢 LOW |
| F6 | Capex amortization period | 36 months | Standard accounting | 🟢 LOW |
| F7 | Monthly capex amortization | ₹6,944/month | F5 ÷ F6 | 🟢 LOW |

---

## Simulation Assumptions

| # | Assumption | Value | Rationale |
|:-:|:-----------|:-----:|:---------|
| S1 | Monte Carlo iterations | 10,000 | Sufficient for P5–P95 stability |
| S2 | Random seed | 42 | Reproducibility |
| S3 | Order volume distribution | Poisson(λ=310) | Demand is count data with variance |
| S4 | AOV distribution | Normal(μ=505, σ=48) | Central limit theorem on basket composition |
| S5 | Delivery cost distribution | Normal(μ=36, σ=5) | Reflects rider efficiency variance |
| S6 | Rent distribution | Uniform(85K, 120K) | Negotiation uncertainty |
| S7 | AOV floor (simulation clip) | ₹250 | Minimum realistic basket |
| S8 | Delivery cost floor (clip) | ₹18 | Sub-1km minimum rider payout |
| S9 | Orders/day floor (clip) | 50 | Dark store minimum viable operations |

---

## Key Assumption Dependencies

```
Break-Even Density ← f(Fixed Costs, CM/Order)
CM/Order ← f(Take Rate, AOV, Delivery Cost, Pick Cost, Marketing)
Take Rate ← f(Commission %, Convenience Fee, Ad Revenue)
Delivery Cost ← f(Distance, Rider Base, Km Rate, Utilization)
```

> **Most Sensitive Assumption:** AOV (₹100 change → ₹99,900/month EBITDA impact at 180 orders/day)  
> **Most Controllable Lever:** Delivery radius (policy decision, immediate implementation)
