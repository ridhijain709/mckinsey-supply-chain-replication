"""
=============================================================================
Swiggy Instamart — Q-Commerce EBITDA Simulation & Sensitivity Engine
=============================================================================
Case Study: Dark Store Unit Economics under Demand Volatility
Author    : Ridhi Jain | BBA '26 | McKinsey Forward Alumna | CAT'26 Aspirant
Repository: github.com/ridhijain709/swiggy-qcommerce-strategy-analysis
Date      : August 2026

METHODOLOGY:
  1. Three-Tier Scenario Analysis (Conservative / Base / Optimistic)
  2. Monte Carlo Simulation (10,000 iterations, seed=42)
  3. Dark-Store Order-Density Sensitivity (Fixed-Cost Absorption Crossover)
  4. Rider Cost Sensitivity vs Delivery Distance
  5. Outputs: CSV + PNG charts saved to ../outputs/

MARKET BENCHMARKS (Public Sources):
  - Swiggy DRHP 2024 (GOV filing) — Instamart avg. gross take rate ~8–9%
  - RedSeer Q-Commerce Report 2024 — India AOV ₹480–₹540 for grocery
  - Bernstein Research "India E-Grocery" 2024 — Dark store density target 350–500 orders/day
  - Euromonitor India Quick Commerce Market Report 2024
=============================================================================
"""

import sys, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server/CI use
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────────────────────────
# OUTPUT DIRECTORY
# ─────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────────────────────────────
SWIGGY_ORANGE = '#FC8019'
SWIGGY_DARK   = '#1C1C1C'
SWIGGY_LIGHT  = '#FFFFFF'
COLOR_PROFIT  = '#2ECC71'
COLOR_LOSS    = '#E74C3C'
COLOR_NEUTRAL = '#3498DB'

plt.rcParams.update({
    'figure.facecolor': SWIGGY_DARK,
    'axes.facecolor':   '#252525',
    'axes.edgecolor':   '#444444',
    'axes.labelcolor':  '#CCCCCC',
    'text.color':       '#CCCCCC',
    'xtick.color':      '#AAAAAA',
    'ytick.color':      '#AAAAAA',
    'grid.color':       '#333333',
    'grid.linestyle':   '--',
    'grid.alpha':       0.5,
    'font.family':      'sans-serif',
    'font.size':        11,
})

# ─────────────────────────────────────────────────────────────────
# MODEL CONSTANTS (market-grounded)
# ─────────────────────────────────────────────────────────────────
TAKE_RATE         = 0.185          # 18.5% effective revenue rate (commission 8.5% + convenience fee avg ₹25 + ad revenue ₹12/order per DRHP 2024)
PICKING_PACKING   = 12.0           # ₹12/order (warehouse ops, per RedSeer 2024)
DARK_STORE_CAPEX  = 250_000        # ₹2.5L one-time fit-out amortized over 36 months
TECH_OVERHEAD     = 15_000         # ₹15K/month — POS, routing algorithms, data infra
MARKETING_PER_ORD = 4.0            # ₹4/order blended (Swiggy One subscribers = lower CAC)

# ─────────────────────────────────────────────────────────────────
# SCENARIO DEFINITIONS
# ─────────────────────────────────────────────────────────────────
SCENARIOS = {
    'Conservative': {
        'orders_per_day':  180,
        'aov_inr':        420.0,
        'delivery_cost':   42.0,    # ₹42 — low density, longer last-mile (1 rider = 1 run/hr)
        'rent_per_month': 120_000,  # Tier-1 city peripheral zone, 1,200 sq.ft dark store
        'picker_headcount':  4,
        'rider_pool':        12,
        'colour': COLOR_LOSS
    },
    'Base': {
        'orders_per_day':  320,
        'aov_inr':        520.0,
        'delivery_cost':   35.0,    # ₹35 — moderate density, 2km radius
        'rent_per_month': 100_000,  # Residential hub, prime location
        'picker_headcount':  7,
        'rider_pool':        20,
        'colour': COLOR_NEUTRAL
    },
    'Optimistic': {
        'orders_per_day':  480,
        'aov_inr':        610.0,
        'delivery_cost':   29.5,    # ₹29.5 — dense urban, riders do ≥3 runs/hr
        'rent_per_month':  90_000,  # Negotiated multi-store lease
        'picker_headcount': 10,
        'rider_pool':        28,
        'colour': COLOR_PROFIT
    },
}

# ─────────────────────────────────────────────────────────────────
# CORE CALCULATION ENGINE
# ─────────────────────────────────────────────────────────────────
def calculate_unit_economics(aov, delivery_cost, orders_per_day, rent_per_month):
    """Full per-order P&L and monthly EBITDA calculation.
    
    Revenue model (per Swiggy DRHP 2024 & RedSeer benchmarks):
      - Take rate 8.5% commission on GMV (restaurant/grocery margin)
      - Convenience fee: ₹20–₹35 charged; platform nets ~₹20 after support
      - Ad/banner revenue: ~₹8–15/order from brand partners listed on dark store
      - TAKE_RATE = 18.5% blended effective rate encapsulates all three streams
    """
    # Revenue side
    gross_revenue   = aov * TAKE_RATE  # blended commission + fees + ad revenue

    # Cost side  
    variable_costs  = delivery_cost + PICKING_PACKING + MARKETING_PER_ORD
    contribution_margin = gross_revenue - variable_costs

    # Monthly
    monthly_orders  = orders_per_day * 30
    monthly_cm      = contribution_margin * monthly_orders
    # Fixed costs
    capex_amort     = DARK_STORE_CAPEX / 36           # ~₹6,944/month
    total_fixed     = rent_per_month + TECH_OVERHEAD + capex_amort
    monthly_ebitda  = monthly_cm - total_fixed
    ebitda_margin   = (monthly_ebitda / (aov * monthly_orders)) * 100

    return {
        'gross_revenue_inr':    round(gross_revenue, 2),
        'variable_costs_inr':   round(variable_costs, 2),
        'contribution_margin':  round(contribution_margin, 2),
        'monthly_orders':       monthly_orders,
        'monthly_cm_inr':       round(monthly_cm, 2),
        'total_fixed_inr':      round(total_fixed, 2),
        'monthly_ebitda_inr':   round(monthly_ebitda, 2),
        'ebitda_margin_pct':    round(ebitda_margin, 3),
    }

# ─────────────────────────────────────────────────────────────────
# 1. SCENARIO ANALYSIS TABLE
# ─────────────────────────────────────────────────────────────────
def run_scenario_analysis():
    print("\n" + "="*70)
    print("  SECTION 1: THREE-TIER SCENARIO ANALYSIS")
    print("="*70)

    rows = []
    for name, params in SCENARIOS.items():
        ec = calculate_unit_economics(
            params['aov_inr'],
            params['delivery_cost'],
            params['orders_per_day'],
            params['rent_per_month']
        )
        rows.append({
            'Scenario':           name,
            'Orders/Day':         params['orders_per_day'],
            'AOV (INR)':          params['aov_inr'],
            'Delivery Cost':      params['delivery_cost'],
            'Contribution/Order': ec['contribution_margin'],
            'Monthly CM (INR)':   ec['monthly_cm_inr'],
            'Fixed Costs (INR)':  ec['total_fixed_inr'],
            'Monthly EBITDA':     ec['monthly_ebitda_inr'],
            'EBITDA Margin %':    ec['ebitda_margin_pct'],
            'Breakeven?':         'YES ✅' if ec['monthly_ebitda_inr'] > 0 else 'NO ❌',
        })

    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    csv_path = os.path.join(OUTPUT_DIR, 'scenario_analysis.csv')
    df.to_csv(csv_path, index=False)
    print(f"\n  Saved → {csv_path}")
    return df

# ─────────────────────────────────────────────────────────────────
# 2. MONTE CARLO SIMULATION
# ─────────────────────────────────────────────────────────────────
def run_monte_carlo(iterations=10_000, seed=42):
    print("\n" + "="*70)
    print(f"  SECTION 2: MONTE CARLO SIMULATION  ({iterations:,} iterations)")
    print("="*70)

    rng = np.random.default_rng(seed)

    # Stochastic variable distributions (market-calibrated)
    orders_per_day   = rng.poisson(lam=310,       size=iterations)          # Poisson demand
    aovs             = rng.normal(loc=505, scale=48, size=iterations)       # AOV volatility
    delivery_costs   = rng.normal(loc=36,  scale=5,  size=iterations)       # Rider cost variation
    rents            = rng.uniform(low=85_000, high=120_000, size=iterations)

    # Compute monthly EBITDA for each iteration
    commissions  = np.clip(aovs, 250, 800) * TAKE_RATE  # blended 18.5% effective rate
    var_costs    = np.clip(delivery_costs, 18, 65) + PICKING_PACKING + MARKETING_PER_ORD
    cm_per_order = commissions - var_costs
    monthly_cm   = cm_per_order * (np.maximum(orders_per_day, 50) * 30)
    fixed        = rents + TECH_OVERHEAD + (DARK_STORE_CAPEX / 36)
    ebitdas      = monthly_cm - fixed

    break_even_pct = np.mean(ebitdas > 0) * 100
    p5  = np.percentile(ebitdas,  5)
    p25 = np.percentile(ebitdas, 25)
    p50 = np.percentile(ebitdas, 50)
    p75 = np.percentile(ebitdas, 75)
    p95 = np.percentile(ebitdas, 95)
    mean_ebitda = np.mean(ebitdas)
    std_ebitda  = np.std(ebitdas)

    print(f"\n  Break-Even Probability  : {break_even_pct:.1f}%")
    print(f"  Mean Monthly EBITDA     : INR {mean_ebitda:>12,.0f}")
    print(f"  Std Deviation           : INR {std_ebitda:>12,.0f}")
    print(f"  P5  (Downside Tail)     : INR {p5:>12,.0f}")
    print(f"  P25 (Lower Quartile)    : INR {p25:>12,.0f}")
    print(f"  P50 (Median)            : INR {p50:>12,.0f}")
    print(f"  P75 (Upper Quartile)    : INR {p75:>12,.0f}")
    print(f"  P95 (Upside Tail)       : INR {p95:>12,.0f}")

    results = {
        'iterations': iterations, 'break_even_pct': round(break_even_pct, 2),
        'mean': round(mean_ebitda, 2), 'std': round(std_ebitda, 2),
        'p5': round(p5, 2), 'p25': round(p25, 2), 'p50': round(p50, 2),
        'p75': round(p75, 2), 'p95': round(p95, 2),
        'raw_ebitdas': ebitdas
    }
    return results

# ─────────────────────────────────────────────────────────────────
# 3. ORDER DENSITY SENSITIVITY (Fixed-Cost Absorption)
# ─────────────────────────────────────────────────────────────────
def run_density_sensitivity():
    print("\n" + "="*70)
    print("  SECTION 3: ORDER DENSITY SENSITIVITY — FIXED COST ABSORPTION")
    print("="*70)

    order_range = range(50, 601, 10)
    rows = []
    for orders in order_range:
        for aov, label in [(420, 'Low AOV'), (520, 'Mid AOV'), (620, 'High AOV')]:
            ec = calculate_unit_economics(aov, 36.0, orders, 100_000)
            rows.append({
                'orders_per_day': orders,
                'aov_tier': label,
                'aov': aov,
                'monthly_ebitda': ec['monthly_ebitda_inr'],
                'contribution_margin': ec['contribution_margin'],
            })

    df = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, 'density_sensitivity.csv')
    df.to_csv(csv_path, index=False)
    print(f"  Saved → {csv_path}")

    # Find breakeven order density per AOV tier
    for label in ['Low AOV', 'Mid AOV', 'High AOV']:
        tier = df[df['aov_tier'] == label]
        crossover = tier[tier['monthly_ebitda'] > 0]
        if not crossover.empty:
            be = crossover.iloc[0]['orders_per_day']
            print(f"  Break-even density ({label}): {be} orders/day")
    return df

# ─────────────────────────────────────────────────────────────────
# 4. RIDER COST vs DELIVERY DISTANCE MATRIX
# ─────────────────────────────────────────────────────────────────
def run_rider_cost_matrix():
    distances  = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]  # km (dark-store radius)
    order_dens = [200, 280, 350, 420, 500]               # daily orders
    # Cost model: base ₹18 + ₹7/km (fuel parity, 2024 rider economics)
    rows = []
    for d in distances:
        delivery_cost = 18 + (7 * d)
        row = {'Distance (km)': d}
        for od in order_dens:
            ec = calculate_unit_economics(520, delivery_cost, od, 100_000)
            row[f'{od} ord/day'] = round(ec['monthly_ebitda_inr'] / 1000, 1)  # in '000 INR
        rows.append(row)
    df = pd.DataFrame(rows).set_index('Distance (km)')
    print("\n" + "="*70)
    print("  SECTION 4: RIDER COST vs DELIVERY DISTANCE  (Monthly EBITDA '000 INR)")
    print("="*70)
    print(df.to_string())
    csv_path = os.path.join(OUTPUT_DIR, 'rider_cost_matrix.csv')
    df.to_csv(csv_path)
    print(f"\n  Saved → {csv_path}")
    return df

# ─────────────────────────────────────────────────────────────────
# CHART GENERATION
# ─────────────────────────────────────────────────────────────────
def generate_all_charts(scenario_df, mc_results, density_df, rider_df):
    print("\n  Generating charts...")

    fig = plt.figure(figsize=(20, 24), facecolor=SWIGGY_DARK)
    fig.suptitle(
        "Swiggy Instamart — Q-Commerce Unit Economics Dashboard\n"
        "Author: Ridhi Jain | BBA '26 | McKinsey Forward Alumna",
        color=SWIGGY_ORANGE, fontsize=16, fontweight='bold', y=0.99
    )

    gs = fig.add_gridspec(4, 2, hspace=0.45, wspace=0.35)

    # ── Chart 1: Scenario EBITDA Bar ──────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    colours = [SCENARIOS[s]['colour'] for s in scenario_df['Scenario']]
    bars = ax1.bar(scenario_df['Scenario'], scenario_df['Monthly EBITDA'] / 1000,
                   color=colours, alpha=0.85, width=0.5, edgecolor='white', linewidth=0.5)
    ax1.axhline(0, color='white', linewidth=1.0, linestyle='--', alpha=0.6)
    ax1.set_title('Monthly EBITDA by Scenario (₹ Thousands)', color=SWIGGY_ORANGE, fontsize=12, pad=10)
    ax1.set_ylabel('EBITDA (INR \'000)', color='#CCCCCC')
    for bar, val in zip(bars, scenario_df['Monthly EBITDA']):
        label = f"₹{val/1000:.1f}K"
        ypos  = val/1000 + (3 if val > 0 else -8)
        ax1.text(bar.get_x() + bar.get_width()/2, ypos, label,
                 ha='center', va='bottom', fontsize=11, color='white', fontweight='bold')

    # ── Chart 2: Per-Order Waterfall ─────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    base_ec = calculate_unit_economics(520, 35.0, 320, 100_000)
    comm_component   = 520 * 0.085           # Pure restaurant commission
    conv_fee         = 22.0                  # Convenience fee retained
    ad_rev           = 520 * 0.055           # Ad/banner revenue
    waterfall_items = [
        ('Commission\n(8.5%)', round(comm_component,1), COLOR_PROFIT),
        ('Conv Fee\n+Ad Rev', round(conv_fee + ad_rev,1), COLOR_PROFIT),
        ('- Delivery\nCost', -35.0, COLOR_LOSS),
        ('- Pick\n& Pack', -PICKING_PACKING, COLOR_LOSS),
        ('- Marketing', -MARKETING_PER_ORD, COLOR_LOSS),
        ('Net CM\n/Order', base_ec['contribution_margin'], SWIGGY_ORANGE),
    ]
    labels = [x[0] for x in waterfall_items]
    values = [x[1] for x in waterfall_items]
    colors = [x[2] for x in waterfall_items]
    ax2.bar(labels, [abs(v) for v in values], color=colors, alpha=0.85,
            edgecolor='white', linewidth=0.5)
    for i, (label, val) in enumerate(zip(labels, values)):
        ax2.text(i, abs(val) + 0.3, f"₹{val:.1f}", ha='center', fontsize=9.5,
                 color='white', fontweight='bold')
    ax2.set_title('Per-Order P&L Waterfall — Base Scenario (₹)', color=SWIGGY_ORANGE, fontsize=12, pad=10)
    ax2.set_ylabel('INR / Order', color='#CCCCCC')

    # ── Chart 3: Monte Carlo Distribution ────────────────────────
    ax3 = fig.add_subplot(gs[1, :])
    ebitdas_k = mc_results['raw_ebitdas'] / 1000
    ax3.hist(ebitdas_k, bins=120, color=COLOR_NEUTRAL, alpha=0.7, edgecolor='none')
    ax3.axvline(mc_results['p5']/1000,  color=COLOR_LOSS,   lw=2, label=f"P5  = ₹{mc_results['p5']/1000:.1f}K")
    ax3.axvline(mc_results['p50']/1000, color=SWIGGY_ORANGE, lw=2, label=f"P50 = ₹{mc_results['p50']/1000:.1f}K")
    ax3.axvline(mc_results['p95']/1000, color=COLOR_PROFIT,  lw=2, label=f"P95 = ₹{mc_results['p95']/1000:.1f}K")
    ax3.axvline(0, color='white', lw=1.5, linestyle='--', alpha=0.8, label='Break-Even')
    ax3.fill_betweenx([0, ax3.get_ylim()[1] if ax3.get_ylim()[1] > 0 else 500],
                      ebitdas_k.min(), 0, alpha=0.08, color=COLOR_LOSS)
    ax3.set_title(
        f'Monte Carlo Distribution — Monthly EBITDA  |  10,000 Simulations  |  '
        f'Break-Even Probability: {mc_results["break_even_pct"]:.1f}%',
        color=SWIGGY_ORANGE, fontsize=12, pad=10
    )
    ax3.set_xlabel("Monthly EBITDA (₹ Thousands)", color='#CCCCCC')
    ax3.set_ylabel("Frequency", color='#CCCCCC')
    ax3.legend(facecolor='#333333', edgecolor='#555555', labelcolor='white', fontsize=10)

    # ── Chart 4: Density Sensitivity ─────────────────────────────
    ax4 = fig.add_subplot(gs[2, 0])
    palette = {'Low AOV': COLOR_LOSS, 'Mid AOV': COLOR_NEUTRAL, 'High AOV': COLOR_PROFIT}
    for aov_tier, colour in palette.items():
        tier_data = density_df[density_df['aov_tier'] == aov_tier]
        ax4.plot(tier_data['orders_per_day'], tier_data['monthly_ebitda'] / 1000,
                 color=colour, lw=2.5, label=aov_tier)
    ax4.axhline(0, color='white', lw=1, linestyle='--', alpha=0.7)
    ax4.fill_between(density_df['orders_per_day'].unique(), 0,
                     density_df.groupby('orders_per_day')['monthly_ebitda'].min() / 1000,
                     alpha=0.07, color=COLOR_LOSS)
    ax4.set_title('Order Density → EBITDA Crossover (₹ Thousands)', color=SWIGGY_ORANGE, fontsize=12, pad=10)
    ax4.set_xlabel('Orders / Day', color='#CCCCCC')
    ax4.set_ylabel("Monthly EBITDA (₹'000)", color='#CCCCCC')
    ax4.legend(facecolor='#333333', edgecolor='#555555', labelcolor='white', fontsize=10)

    # ── Chart 5: Rider Cost Heatmap ───────────────────────────────
    ax5 = fig.add_subplot(gs[2, 1])
    rider_numeric = rider_df.copy()
    sns.heatmap(rider_numeric, ax=ax5, cmap='RdYlGn', center=0, annot=True,
                fmt='.1f', linewidths=0.5, linecolor='#333333',
                cbar_kws={'label': "EBITDA '000 INR"},
                annot_kws={'size': 9})
    ax5.set_title('EBITDA Heatmap: Distance × Order Volume (₹ Thousands)', color=SWIGGY_ORANGE, fontsize=12, pad=10)
    ax5.set_xlabel('Daily Order Volume', color='#CCCCCC')
    ax5.set_ylabel('Delivery Distance (km)', color='#CCCCCC')
    ax5.tick_params(colors='#CCCCCC')

    # ── Chart 6: Contribution Margin Breakdown ────────────────────
    ax6 = fig.add_subplot(gs[3, :])
    orders_range = np.arange(100, 550, 50)
    for sc_name, params in SCENARIOS.items():
        ebitdas = []
        for ord_count in orders_range:
            ec = calculate_unit_economics(
                params['aov_inr'], params['delivery_cost'], ord_count, params['rent_per_month']
            )
            ebitdas.append(ec['monthly_ebitda_inr'] / 1000)
        ax6.plot(orders_range, ebitdas, color=params['colour'], lw=2.5,
                 label=sc_name, marker='o', markersize=5)
    ax6.axhline(0, color='white', lw=1, linestyle='--', alpha=0.7)
    ax6.set_title('EBITDA Trajectory Across Scenarios: Impact of Order Volume Scaling',
                  color=SWIGGY_ORANGE, fontsize=12, pad=10)
    ax6.set_xlabel('Daily Order Volume', color='#CCCCCC')
    ax6.set_ylabel("Monthly EBITDA (₹'000)", color='#CCCCCC')
    ax6.legend(facecolor='#333333', edgecolor='#555555', labelcolor='white', fontsize=11)
    ax6.annotate(
        'BCG / RedSeer target: 350–500 orders/day for dark-store profitability',
        xy=(380, ax6.get_ylim()[0] if ax6.get_ylim()[0] else -50),
        xytext=(400, -80), color='#AAAAAA', fontsize=9,
        arrowprops=dict(arrowstyle='->', color='#AAAAAA', lw=1.2)
    )

    chart_path = os.path.join(OUTPUT_DIR, 'swiggy_ebitda_dashboard.png')
    plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor=SWIGGY_DARK)
    plt.close()
    print(f"  Chart saved → {chart_path}")
    return chart_path

# ─────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "█"*70)
    print("  SWIGGY INSTAMART — Q-COMMERCE EBITDA SIMULATION ENGINE")
    print("  Author: Ridhi Jain | BBA '26 | McKinsey Forward Alumna")
    print("█"*70)

    scenario_df = run_scenario_analysis()
    mc_results  = run_monte_carlo(iterations=10_000)
    density_df  = run_density_sensitivity()
    rider_df    = run_rider_cost_matrix()
    chart_path  = generate_all_charts(scenario_df, mc_results, density_df, rider_df)

    print("\n" + "="*70)
    print("  SIMULATION COMPLETE — All outputs written to /04-analysis/outputs/")
    print(f"  Dashboard chart: {chart_path}")
    print("="*70 + "\n")
