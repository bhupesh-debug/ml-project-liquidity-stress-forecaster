# Model Benchmark & Evaluation Report: Liquidity Stress Forecaster

## 1. Evaluation Methodology & Holdout Split
To ensure zero lookahead leakage, the model was evaluated chronologically on the final 180 days of the 3-year time series ($t=915$ to $1094$). The training history ($N=887$) was split into an 80% model fitting partition and a 20% validation partition for conformal quantile calibration.

---

## 2. Model Comparative Benchmark Table

| Model Architecture | WAPE | MAE ($M index) | RMSE ($M index) | Forecast Bias | 95% Tail Coverage |
|---|---|---|---|---|---|
| **28-Day Rolling Mean** | 0.379 | 36.05 | 41.42 | -0.8% | N/A |
| **Seasonal Naive (Lag 7)** | 0.105 | 10.00 | 14.64 | -0.8% | N/A |
| **OLS Linear Model** | 0.087 | 8.29 | 10.43 | -3.6% | N/A |
| **Quantile Regression (p50)** | 0.083 | 7.88 | 10.11 | -2.1% | 87.8% (Uncalibrated) |
| **Gradient Boosting (p50)** | **0.073** | **6.62** | **8.85** | **-1.5%** | N/A |
| **Calibrated Upper Bound (p95)** | N/A | N/A | N/A | N/A | **94.4% (Calibrated)** |

---

## 3. Analysis of Baseline Deficiencies
1. **28-Day Rolling Mean Failure**: The 28-day rolling average completely smooths out weekly liquidity spikes (Monday settlements and Friday sweeps) and month-end cash disbursement walls, resulting in a severe 0.379 WAPE.
2. **Lag-7 Naive Failure during Month-End & Stress**: While lag-7 captures recurring weekday rhythm, it lags by 7 days whenever month-end falls mid-week, and fails entirely during market stress shocks.
3. **Value of Conformal Calibration**: Raw parametric quantile regression captured only 87.8% of test realisations. Calculating the 95th percentile residual offset ($\Delta = +7.03$) on the held-out calibration split lifted coverage to **94.4%**, successfully bounding test volatility.
