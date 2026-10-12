import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_liquidity_simulations(p50, p95, base_buffer, n_mc_runs=5000, seed=42):
    """
    Executes comprehensive liquidity stress testing and Monte Carlo simulations for Project 3:
    1. Multi-scenario stress tests across 30-day rolling windows
    2. Buffer sizing sensitivity (+/-10%, +/-20%, +30%)
    3. Extended stress duration (10d, 15d, 20d, 30d persistent)
    4. Reverse stress testing (Shortfall threshold discovery)
    5. 5,000-run Monte Carlo Cumulative Outflow Distribution & Buffer Survival Analysis
    """
    os.makedirs("reports", exist_ok=True)
    rng = np.random.default_rng(seed)
    horizon = 30
    n_windows = len(p50) - horizon
    
    # 1. Extended Scenario Suite
    extended_scenarios = {
        "Base (p50)": lambda a, b: a,
        "Mild Stress (+25% 10d)": lambda a, b: np.where(np.arange(len(a)) < 10, a * 1.25, a),
        "Severe Stress (p95 x1.4 10d)": lambda a, b: np.where(np.arange(len(b)) < 10, b * 1.40, b),
        "Extended Stress (p95 x1.25 20d)": lambda a, b: np.where(np.arange(len(b)) < 20, b * 1.25, b),
        "Persistent Elevated (+15% 30d)": lambda a, b: a * 1.15,
        "Capital Market Run (p95 x1.6 15d)": lambda a, b: np.where(np.arange(len(b)) < 15, b * 1.60, b)
    }
    
    scenario_metrics = []
    for name, f in extended_scenarios.items():
        cov_list = []
        surv_list = []
        cum_outflows = []
        for s in range(n_windows):
            path = f(p50[s:s+horizon], p95[s:s+horizon])
            c = np.cumsum(path)
            cov = base_buffer / c[-1]
            cov_list.append(cov)
            surv = int(np.argmax(c > base_buffer)) + 1 if (c > base_buffer).any() else horizon + 1
            surv_list.append(surv)
            cum_outflows.append(c[-1])
            
        scenario_metrics.append({
            "scenario": name,
            "median_cumulative_outflow": round(float(np.median(cum_outflows)), 1),
            "median_coverage": round(float(np.median(cov_list)), 2),
            "worst_coverage": round(float(np.min(cov_list)), 2),
            "breach_rate_pct": round(float(np.mean(np.array(cov_list) < 1.0) * 100), 1),
            "min_survival_days": int(min(surv_list))
        })
        
    df_scenarios = pd.DataFrame(scenario_metrics)
    
    # 2. Buffer Sizing Sensitivities
    buffer_multipliers = [0.80, 0.90, 1.00, 1.10, 1.20, 1.30]
    buffer_sensitivities = []
    
    for mult in buffer_multipliers:
        test_buf = base_buffer * mult
        # Test under severe stress
        f_sev = extended_scenarios["Severe Stress (p95 x1.4 10d)"]
        covs = []
        for s in range(n_windows):
            path = f_sev(p50[s:s+horizon], p95[s:s+horizon])
            covs.append(test_buf / np.sum(path))
            
        breach_rate = float(np.mean(np.array(covs) < 1.0) * 100)
        buffer_sensitivities.append({
            "buffer_multiplier": mult,
            "buffer_amount": round(test_buf, 1),
            "severe_stress_median_coverage": round(float(np.median(covs)), 2),
            "severe_stress_breach_rate_pct": round(breach_rate, 1)
        })
        
    # 3. Reverse Stress Testing: Find required buffer for 0% breach under Severe Stress
    # Find max cumulative outflow in severe stress
    max_severe_cum = max([np.sum(extended_scenarios["Severe Stress (p95 x1.4 10d)"](p50[s:s+horizon], p95[s:s+horizon])) for s in range(n_windows)])
    required_buffer_zero_breach = round(float(max_severe_cum * 1.02), 1) # 2% safety margin
    buffer_shortfall_m = round(float(required_buffer_zero_breach - base_buffer), 1)
    
    # 4. 5,000-Run Monte Carlo Simulation
    # Generate 5,000 stochastic 30-day outflow paths modeling daily residual variance and stress clustering
    mc_cum_base = []
    mc_cum_stressed = []
    daily_vol = 5.8 # Empirical daily standard error
    
    for i in range(n_mc_runs):
        # Pick random starting window
        s_idx = rng.integers(0, n_windows)
        base_path = p50[s_idx:s_idx+horizon]
        p95_path = p95[s_idx:s_idx+horizon]
        
        # Base stochastic path
        rand_noise = rng.normal(0, daily_vol, horizon)
        sim_path_base = np.maximum(base_path + rand_noise, 5.0)
        mc_cum_base.append(np.sum(sim_path_base))
        
        # Stressed stochastic path (severe stress + fat-tailed shock)
        stress_mult = rng.uniform(1.25, 1.55)
        sim_path_stress = np.where(np.arange(horizon) < 10, p95_path * stress_mult, base_path) + rng.normal(0, daily_vol * 1.5, horizon)
        mc_cum_stressed.append(np.sum(np.maximum(sim_path_stress, 5.0)))
        
    mc_cum_base = np.array(mc_cum_base)
    mc_cum_stressed = np.array(mc_cum_stressed)
    
    mc_summary = {
        "runs": n_mc_runs,
        "base_buffer": round(base_buffer, 1),
        "base_median_outflow": round(float(np.median(mc_cum_base)), 1),
        "base_p95_outflow": round(float(np.percentile(mc_cum_base, 95)), 1),
        "base_breach_probability_pct": round(float(np.mean(mc_cum_base > base_buffer) * 100), 2),
        "stressed_median_outflow": round(float(np.median(mc_cum_stressed)), 1),
        "stressed_p95_outflow": round(float(np.percentile(mc_cum_stressed, 95)), 1),
        "stressed_breach_probability_pct": round(float(np.mean(mc_cum_stressed > base_buffer) * 100), 2),
        "reverse_stress": {
            "required_buffer_zero_breach": required_buffer_zero_breach,
            "buffer_shortfall_m": buffer_shortfall_m
        }
    }
    
    # 5. Plot Simulation & Stress Chart
    plt.figure(figsize=(10, 5))
    plt.hist(mc_cum_base, bins=45, color="#1E3A8A", alpha=0.6, label="Baseline 30-Day Outflow MC", density=True)
    plt.hist(mc_cum_stressed, bins=45, color="#DC2626", alpha=0.6, label="Stressed 30-Day Outflow MC", density=True)
    plt.axvline(base_buffer, color="#D97706", linestyle="--", linewidth=2.5, label=f"Current Buffer ({base_buffer:.1f})")
    plt.axvline(required_buffer_zero_breach, color="#059669", linestyle=":", linewidth=2.5, label=f"Zero-Breach Buffer ({required_buffer_zero_breach:.1f})")
    plt.title(f"Liquidity Buffer Coverage: 30-Day Cumulative Outflows (N={n_mc_runs:,})", fontsize=13, fontweight="bold")
    plt.xlabel("Cumulative 30-Day Cash Outflows ($M Index)", fontsize=11)
    plt.ylabel("Probability Density", fontsize=11)
    plt.legend(frameon=True)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("reports/liquidity_stress_simulation.png", dpi=140)
    plt.close()
    
    return {
        "scenarios": scenario_metrics,
        "buffer_sensitivities": buffer_sensitivities,
        "monte_carlo": mc_summary
    }
