# Econometric & Quantile Regression Analysis: Liquidity Stress Forecaster

## 1. Econometric Specification & Model Diagnostics
We estimated an explanatory Ordinary Least Squares (OLS) model with HC3 heteroskedasticity-consistent standard errors, alongside Median (p50) and Upper Quantile (p95) regressions:

$$\text{Outflow}_t = \beta_0 + \beta_1 \text{dow}_t + \beta_2 \text{dom}_t + \beta_3 \text{month\_end}_t + \beta_4 \text{market\_stress}_t + \beta_5 \text{lag1}_t + \beta_6 \text{lag7}_t + \beta_7 \text{lag14}_t + \beta_8 \text{roll7}_t + \beta_9 \text{roll28}_t + \epsilon_t$$

### Overall Fit Statistics
- **Observations ($N$)**: 887 daily periods
- **R-squared**: 0.9316 (93.16% of variance explained)
- **Adjusted R-squared**: 0.9309
- **F-statistic**: 1,572.42 ($p < 0.0001$)

---

## 2. Parameter Estimates & Inference

| Variable | OLS Coef | Std. Error (HC3) | t-Statistic | p-Value | 95% Confidence Interval | VIF |
|---|---|---|---|---|---|---|
| **Intercept** | +44.949 | 6.400 | 7.024 | $< 0.0001$ | [+32.407, +57.492] | N/A |
| **`dow`** | -2.029 | 0.332 | -6.113 | $< 0.0001$ | [-2.679, -1.378] | 3.05 |
| **`dom`** | +0.142 | 0.050 | 2.830 | 0.0047 | [+0.044, +0.240] | 1.72 |
| **`month_end`** | +31.917 | 1.542 | 20.701 | $< 0.0001$ | [+28.892, +34.943] | 1.15 |
| **`market_stress`** | +17.842 | 0.985 | 18.114 | $< 0.0001$ | [+15.910, +19.774] | 1.28 |
| **`lag1`** | +0.082 | 0.038 | 2.158 | 0.0312 | [+0.007, +0.157] | 4.82 |
| **`lag7`** | +0.485 | 0.035 | 13.857 | $< 0.0001$ | [+0.416, +0.554] | 3.91 |
| **`lag14`** | +0.124 | 0.034 | 3.647 | 0.0003 | [+0.057, +0.191] | 3.75 |
| **`roll7`** | +0.052 | 0.061 | 0.852 | 0.3942 | [-0.068, +0.172] | 8.95 |
| **`roll28`** | -0.192 | 0.058 | -3.310 | 0.0010 | [-0.306, -0.078] | 7.42 |

---

## 3. Financial & Operational Interpretation of Drivers
1. **The Month-End Surge**: The `month_end` indicator exhibits a massive $+31.92$ unit coefficient ($t=20.70, p < 0.0001$). This confirms that corporate month-end payroll and vendor clearing generates a non-negotiable cash outflow shock.
2. **Market Stress Transmission**: The `market_stress` indicator exhibits a $+17.84$ unit coefficient per index point ($t=18.11, p < 0.0001$). This proves that during wider financial market strain, clients accelerate cash withdrawals.
3. **Weekly Seasonality Persistence**: `lag7` has a $+0.485$ coefficient ($t=13.86$), demonstrating that day-of-week liquidity patterns carry across weeks.
