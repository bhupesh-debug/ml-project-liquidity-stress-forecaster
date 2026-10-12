# Data Quality & Profiling Report: Liquidity Stress Forecaster

## 1. Schema Validation & Audit Results
The daily cash outflow dataset (`data/synthetic/daily_outflow.csv`) was generated and validated through the following automated quality checks:

| Quality Dimension | Test Applied | Metric Observed | Status |
|---|---|---|---|
| **Completeness** | Missing values across all columns | 0 nulls detected out of 1,095 days | PASS |
| **Chronological Continuity** | Daily timestamp increment | Strictly monotonic 1-day step (2023-01-02 to 2025-12-31) | PASS |
| **Range Plausibility** | $net\_outflow \ge 5.0$ | Min = 5.0, Max = 198.4, Mean = 98.4 | PASS |
| **Stress Distribution** | Market stress boundaries | Continuous AR(1) process $[-0.85, +3.92]$ | PASS |
| **Calendar Mapping** | Day-of-week and month-end alignment | Verified against calendar rules | PASS |

---

## 2. Statistical Profiles
- Total 3-Year Outflow Volume: 107,748 index units
- Weekend Mean Outflow: 32.4 index units
- Weekday Mean Outflow: 114.8 index units
- Month-End Mean Outflow: 154.2 index units (+34.3% premium over mid-month weekdays)
