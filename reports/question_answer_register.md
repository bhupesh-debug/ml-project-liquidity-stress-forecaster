# Question-and-Answer Register: Liquidity Stress Forecaster

## Overview
This register records every explicit treasury, econometric, and risk-management question formulated for Project 3, supported by empirical metrics, simulation outcomes, and verified calculations.

---

### Q-LIQ-001: Which forecasting method performs best?
- **Direct Answer**: The Gradient Boosting Regressor (p50) performs best, achieving an out-of-sample **0.073 WAPE** (MAE 6.62). It outperforms the 28-day rolling mean (0.379 WAPE) by 80.7% and the lag-7 seasonal naive baseline (0.105 WAPE) by 30.5%.
- **Supporting Analysis**: 180-day chronological holdout test.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/model_report.md` Section 2.

---

### Q-LIQ-002: Is the uncertainty band adequately calibrated?
- **Direct Answer**: Uncalibrated quantile regression underperforms, achieving only 87.8% coverage. However, applying an out-of-fold conformal calibration offset of **+7.03 units** lifts out-of-sample test coverage to **94.4%**, which is well-calibrated to the 95% target.
- **Supporting Analysis**: Conformal calibration calculation on a 20% validation split.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/results.json`.

---

### Q-LIQ-003: How does the buffer perform under each stress scenario?
- **Direct Answer**:
  - **Base Case**: 1.06 median coverage, 0% window breach rate, 31-day minimum survival runway.
  - **Mild Stress (+25% 10d)**: 0.97 median coverage, 79.3% breach rate, 29-day minimum survival.
  - **Severe Stress (p95 x1.4 10d)**: 0.78 median coverage, 100% breach rate, buffer exhausted by Day 22.
  - **Extended Stress (p95 x1.25 20d)**: 0.76 median coverage, 100% breach rate, buffer exhausted by Day 21.
- **Supporting Analysis**: Multi-scenario rolling 30-day simulations.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/simulation_report.md` Section 2.

---

### Q-LIQ-004: How much additional buffer would be required to meet a specified coverage objective?
- **Direct Answer**: To achieve a 0% breach rate under Severe Stress, the buffer must be increased from **2,886.2 units to 3,914.8 units**, representing an incremental shortfall of **1,028.6 units (+35.6%)**.
- **Supporting Analysis**: Reverse stress testing across rolling test windows.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/simulation_report.md` Section 3.

---

### Q-LIQ-005: Which assumptions have the greatest influence on buffer exhaustion?
- **Direct Answer**: The duration of the stress period and the coincidence of stress with month-end settlements. Month-end calendar dates add +31.92 units of daily outflow; if stress coincides with month-end, survival days drops from 22 days to 16 days.
- **Supporting Analysis**: OLS regression coefficients ($month\_end$ $t=20.70$) and Capital Market Run scenario.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/regression_analysis.md` Section 2.

---

### Q-LIQ-006: What conditions cause the earliest shortfall?
- **Direct Answer**: A prolonged capital markets run (p95 outflows multiplied by 1.6 for 15 days) overlapping with a month-end payroll and vendor clearing cycle causes buffer exhaustion on **Day 16**.
- **Supporting Analysis**: Capital Market Run simulation scenario.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/simulation_report.md` Section 2.

---

### Q-LIQ-007: Which monitoring indicators should Treasury prioritize?
- **Direct Answer**:
  1. The latent `market_stress` indicator (crossing 1.50).
  2. Rolling 30-day coverage ratio (dropping below 1.10).
  3. Conformal p95 band breaches over rolling 14-day windows.
- **Supporting Analysis**: Econometric elasticity analysis and Treasury trigger rules.
- **Status**: Answered with verified evidence.
- **Report Section**: `docs/governance_controls.md` Section 2.

---

### Q-LIQ-008: What additional real-world data is required?
- **Direct Answer**:
  1. Granular counterparty-level cash flows (separating operational client deposits from wholesale flight-prone funding).
  2. Actual credit facility draw and repayment histories.
  3. Intraday RTGS settlement timings.
  4. Real-world HQLA market valuation and haircut schedules.
- **Supporting Analysis**: Synthetic data limitations audit.
- **Status**: Answered with verified evidence.
- **Report Section**: `reports/limitations.md`.
