# Model Card: Liquidity Stress Forecaster & Conformal Uncertainty Engine

## 1. Model Details
- **Model Name**: Dual Quantile & Conformal Liquidity Stress Engine
- **Architecture**:
  - Central Tendency: `HistGradientBoostingRegressor(loss="absolute_error", max_depth=4, learning_rate=0.05, max_iter=300)`
  - Upper Quantile: `HistGradientBoostingRegressor(loss="quantile", quantile=0.95, max_depth=4, learning_rate=0.05, max_iter=300)`
  - Conformal Calibration: Additive quantile residual offset ($\Delta = +7.03$ units) calculated on an out-of-fold calibration slice.
- **Developer**: Bhupesh Chandra Dimri (`bhupesh7cd@gmail.com`).
- **Regulatory Status**: Prototype and analytical benchmark. **Not a replacement for statutory Basel III LCR, NSFR, or FR 2052a filings.**

---

## 2. Intended Domain & Use Cases
- **Intended Use**: Operational liquidity management, forward 30-day cash ladder forecasting, stress testing for Asset-Liability Committees (ALCO), and buffer sizing optimization.
- **Out of Scope**: Intraday real-time RTGS payments routing, individual payment settlement fraud, or long-term structural balance-sheet ALM (>1 year).

---

## 3. Evaluation & Performance Summary
Evaluated chronologically on the final 180 calendar days held out:
- **Baseline Rolling 28-day Mean**: WAPE = 0.379 (MAE 36.05)
- **Seasonal Naive (Lag 7)**: WAPE = 0.105 (MAE 10.00)
- **OLS Linear Model**: WAPE = 0.087 (MAE 8.29)
- **Quantile Regression (p50)**: WAPE = 0.083 (MAE 7.88)
- **Gradient Boosting (p50)**: **WAPE = 0.073 (MAE 6.62)** — **Champion central forecast**
- **Calibrated p95 Band Coverage**: **94.4% empirical test coverage** (Target: 95.0%).
