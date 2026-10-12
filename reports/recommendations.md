# Treasury Recommendations & Action Plan: Liquidity Stress Forecaster

## 1. Prioritized Treasury Action Plan

### Action 1: Deploy Dual-Quantile ML into Morning Funding Operations
- **Rationale**: HistGBM cuts forecast error by 30.5% over seasonal naive and 80.7% over 28-day rolling means, eliminating multi-million-dollar funding mismatches.
- **Action**: Embed the p50 model and calibrated p95 band into the morning 07:30 EST money-market desk routine.

### Action 2: Establish a Dynamic Two-Tier Buffer Sizing Policy
- **Rationale**: Holding a static 3,914-unit buffer to immunize against severe stress costs $2.4M+ in negative carry. Current 2,886-unit buffer breaches 100% under Severe Stress.
- **Action**: Set a dynamic baseline buffer at **3,250 units** (+12.6% over current), paired with committed, contingent bank revolving credit facilities to cover the 665-unit tail gap during stress.

### Action 3: Automate Red/Amber/Green ALCO Contingency Triggers
- **Rationale**: Clear quantitative thresholds prevent emotional overreaction during market turbulence.
- **Action**: Implement automated alerts: Amber at coverage $< 1.10$, Red at coverage $< 1.00$.

---

## 2. 12-Week Implementation Roadmap
- **Weeks 1-4**: Production ingestion of SWIFT cash logs and ERP treasury ledgers.
- **Weeks 5-8**: Shadow running against current spreadsheet liquidity ladder; tracking coverage and bias.
- **Weeks 9-12**: ALCO formal sign-off, API integration into treasury workstation, and executive dashboard release.
