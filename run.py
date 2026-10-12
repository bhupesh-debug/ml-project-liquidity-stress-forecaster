import os
import json
import joblib
import numpy as np
import pandas as pd
from src.data_pipeline import make_data
from src.feature_engineering import build_features, FEATS
from src.model import median_model, upper_model
from src.evaluate import wape, stress_table, forecast_chart
from src.regression_analysis import run_regression_analysis
from src.simulation import run_liquidity_simulations
from src.business_case import compute_business_case
from slides.generate_deck import create_presentation

def main():
    os.makedirs("data/synthetic", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("slides", exist_ok=True)

    # 1. Data generation
    d = make_data()
    d.to_csv("data/synthetic/daily_outflow.csv", index=False)
    f = build_features(d)

    # 2. Time-based split: last 180 days held out
    cut = len(f) - 180
    tr, te = f.iloc[:cut], f.iloc[cut:]
    fit, cal = tr.iloc[:int(len(tr) * 0.8)], tr.iloc[int(len(tr) * 0.8):]

    # 3. Train GBM Models
    m = median_model().fit(fit[FEATS], fit.net_outflow)
    u = upper_model().fit(fit[FEATS], fit.net_outflow)

    # Conformal calibration offset on validation slice
    off = max(0.0, float(np.quantile(cal.net_outflow.values - u.predict(cal[FEATS]), 0.95)))
    p50 = m.predict(te[FEATS])
    p95 = u.predict(te[FEATS]) + off
    y = te.net_outflow.values

    # 4. Illustrative HQLA-style buffer
    buffer = float(np.percentile(np.convolve(y, np.ones(30), "valid"), 70))
    tab = stress_table(p50, p95, buffer)

    # 5. Regression Analysis
    reg_res = run_regression_analysis(d)

    # 6. Stress Simulations & 5,000-run Monte Carlo
    sim_res = run_liquidity_simulations(p50, p95, buffer, n_mc_runs=5000, seed=42)

    # 7. Financial Business Case
    bc_res = compute_business_case()

    # 8. Charts and Models
    forecast_chart(te.date, y, p50, p95, "reports/forecast_vs_actual.png")
    joblib.dump(m, "models/best_model.pkl")

    # 9. Slide Presentation
    create_presentation()

    # 10. Compile Results JSON
    res = {
        "calibration_offset": round(off, 2),
        "train_days": len(tr),
        "test_days": len(te),
        "wape_seasonal_naive_lag7": round(wape(y, te.lag7.values), 3),
        "wape_rolling28": round(wape(y, te.roll28.values), 3),
        "wape_gbm_p50": round(wape(y, p50), 3),
        "p95_coverage": round(float((y <= p95).mean()), 3),
        "buffer_index": round(buffer, 1),
        "stress_table": tab.to_dict("records"),
        "regression": reg_res,
        "simulations": sim_res,
        "business_case": bc_res
    }

    with open("reports/results.json", "w") as f_out:
        json.dump(res, f_out, indent=2)

    print("Project 3 pipeline executed successfully.")
    print("Results written to reports/results.json")

if __name__ == "__main__":
    main()
