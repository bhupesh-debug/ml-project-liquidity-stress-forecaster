# Liquidity Stress Testing, Buffer Sizing & Monte Carlo Report: Project 3

## 1. Stress Testing Framework & Sizing Context
To evaluate whether an available liquidity buffer of **2,886.2 units** provides adequate survival runway, we executed multi-scenario rolling 30-day simulations and a 5,000-run stochastic Monte Carlo model.

---

## 2. Multi-Scenario 30-Day Stress Results

| Scenario Specification | Median Cumulative Outflow | Median Coverage Ratio | Worst Coverage Ratio | Share of Windows Breached | Minimum Survival Days |
|---|---|---|---|---|---|
| **Base Case (p50 Forecast)** | 2,732.8 | **1.06** | 1.01 | **0.0%** | **31 Days (Full Survival)** |
| **Mild Stress (+25% for 10d)** | 2,969.1 | **0.97** | 0.93 | **79.3%** | **29 Days** |
| **Severe Stress (p95 x1.4 for 10d)** | 3,715.1 | **0.78** | 0.75 | **100.0%** | **22 Days** |
| **Extended Stress (p95 x1.25 for 20d)** | 3,813.5 | **0.76** | 0.74 | **100.0%** | **21 Days** |
| **Persistent Elevated (+15% for 30d)** | 3,142.7 | **0.92** | 0.88 | **100.0%** | **26 Days** |
| **Capital Market Run (p95 x1.6 for 15d)**| 4,258.1 | **0.68** | 0.66 | **100.0%** | **16 Days** |

*Key Takeaway*: In normal environments, the buffer covers cumulative outflows with a 6% surplus margin. Under Severe Stress, cumulative outflows reach 3,715.1 units, breaching the buffer by Day 22.

---

## 3. Buffer Sizing Sensitivities & Reverse Stress Testing

| Tested Buffer Level | Sized Buffer Amount | Severe Stress Median Coverage | Breach Rate under Severe Stress |
|---|---|---|---|
| 0.80x Current Buffer | 2,309.0 | 0.62 | 100.0% |
| 0.90x Current Buffer | 2,597.6 | 0.70 | 100.0% |
| **1.00x Current Buffer** | **2,886.2** | **0.78** | **100.0%** |
| 1.10x Current Buffer | 3,174.9 | 0.85 | 100.0% |
| 1.20x Current Buffer | 3,463.5 | 0.93 | 100.0% |
| **1.30x Current Buffer** | **3,752.1** | **1.01** | **32.7%** |

### Reverse Stress Discovery
- **Required Buffer for 0% Breaches**: **3,914.8 units** (including 2% safety buffer).
- **Buffer Shortfall**: **1,028.6 units** (+35.6% expansion required to fully immunize against Severe Stress).

---

## 4. 5,000-Run Monte Carlo Simulation

![Liquidity Simulation Chart](liquidity_stress_simulation.png)

- **Baseline Outflow Distribution**:
  - Median Cumulative 30-Day Outflow: **2,734.5 units**
  - 95th Percentile: **2,856.1 units**
  - Empirical Breach Probability: **1.2%**
- **Stressed Outflow Distribution**:
  - Median Cumulative Stressed Outflow: **3,335.1 units**
  - 95th Percentile: **3,571.5 units**
  - Empirical Breach Probability: **100.0%**
- **Treasury Recommendation**: Implement a dynamic buffer target of **3,250 units**, which covers 90% of mild-to-moderate stress states without incurring the full negative carry of a 3,914-unit buffer.
