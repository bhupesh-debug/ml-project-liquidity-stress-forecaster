# Model Governance, ALCO Controls & Treasury Operating Framework: Project 3

## 1. Governance Classification & Regulatory Boundary
- **Classification**: MRM Tier 2 Model (Liquidity Risk & Cash Management).
- **Compliance Alignment**: Aligns with Federal Reserve SR 11-7 / OCC 2011-12 standards on model risk management and BCBS 238 principles for sound liquidity risk management.
- **Explicit Regulatory Boundary**: This model is an operational forecasting tool. It does **not** generate regulatory Liquidity Coverage Ratio (LCR) or Net Stable Funding Ratio (NSFR) returns, which remain governed by statutory accounting rules.

---

## 2. Treasury Early-Warning Trigger System

| Trigger Level | Metric Condition | Operational Treasury Response |
|---|---|---|
| **Normal (Green)** | 30-Day Coverage $> 1.10$ | Unrestricted short-term money market deployment; yield optimization active. |
| **Warning (Amber)** | $1.00 \le \text{Coverage} \le 1.10$ | Halt discretionary affiliate funding; review bilateral repo lines; daily ALCO briefing. |
| **Critical (Red)** | 30-Day Coverage $< 1.00$ | Convene Emergency ALCO; draw committed revolving credit facilities; suspend capex. |
| **Market Stress Shock** | `market_stress` $> 1.50$ | Automatically switch operational buffer planning from p50 to calibrated p95 trajectory. |

---

## 3. Daily Execution Workflow & Close Controls
1. **06:30 EST**: Automated ETL ingestion of prior-day Fedwire/CHIPS settlement balances and market risk stress indicators.
2. **07:00 EST**: Feature transformation and dual-model execution (median + calibrated p95).
3. **07:30 EST**: Generation of 30-day forward rolling stress table and buffer coverage ratios.
4. **08:00 EST**: Morning Money Market Desk review prior to repo market open.
5. **Ongoing Drift Monitoring**: Monthly audit of p95 empirical coverage; alert triggers if rolling 60-day coverage drops below 92.5%.
