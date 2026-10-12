# Executive Summary: Liquidity Stress Forecaster

## 1. Executive Context & Treasury Mandate
Corporate treasury desks operate under dual pressures: maintain adequate liquid assets to survive systemic liquidity shocks, while minimizing the cost of carry from parking cash in low-yielding short-term instruments.

This project delivers an automated, high-precision liquidity forecasting engine and stress testing simulator:
- **Champion Forecasting Model**: Gradient Boosting Regressor (p50) delivers an out-of-sample **0.073 WAPE**, outperforming the 28-day rolling mean (0.379 WAPE) and seasonal naive lag-7 baseline (0.105 WAPE) by **80.7% and 30.5%** respectively.
- **Conformal Uncertainty Calibration**: Uncalibrated quantile regression achieves only 87.8% empirical test coverage. Adding a conformal offset (+7.03 units) lifts out-of-sample coverage to **94.4%**, providing a statistically defensible upper tail.
- **Stress Testing Reality**: Under baseline conditions, current buffer (2,886.2) provides 1.06 median coverage (0% breach rate). However, under Severe Stress (+40% on p95 for 10 days), the buffer is exhausted by **Day 22 with 100% of rolling test windows breached**.
- **Reverse Stress Sizing**: To guarantee zero breaches during Severe Stress, Treasury must maintain a buffer of **3,914.8 units**, revealing an operational buffer shortfall of **1,028.6 units**.

---

## 2. Corporate Treasury Business Case & ROI
- **Buffer Optimization & Carry Savings**: By predicting cash outflows with high precision, Treasury safely redeploys surplus idle balances into higher-yielding term instruments (150 bps carry advantage), generating **$2.40M in annualized interest optimization** (Base Case).
- **Avoided Emergency Borrowing Surcharges**: Prevents **$850k annually** in emergency bank facility draw fees and secondary market liquidation haircuts.
- **Quant Labor Efficiency**: Automates **900 hours annually** of manual liquidity modeling ($112.5k value).
- **Financial Return**: Base Case yields a **Year-1 Net Benefit of $3.04M**, a **0.9-month payback period**, and a **3-year NPV of $7.94M** on an initial implementation investment of $260k.
