# Limitations & Model Risk Register: Liquidity Stress Forecaster

## 1. Regulatory Non-Equivalence Notice
- **Non-Regulatory Prototype**: This model is an operational liquidity forecasting and scenario prototype. It does **not** constitute an implementation of statutory regulatory ratios such as:
  - Basel III Liquidity Coverage Ratio (LCR)
  - Net Stable Funding Ratio (NSFR)
  - Federal Reserve FR 2052a Complex Liquidity Monitoring Report
- Any production use must clearly segregate internal operational liquidity metrics from statutory regulatory reporting.

---

## 2. Synthetic Data Limitations & Environmental Assumptions
- **Synthetic Denomination**: Outflows are expressed in synthetic index units ($M index), not denominated fiat currency.
- **Behavioral Assumptions**: Stressed simulations assume static contractual client outflows without dynamic counterparty behavioral adjustments or active management intervention.
- **Tail Extremes**: While conformal calibration bounds historical 95% tails, severe non-linear systemic credit freezes (e.g. 2008 Lehman crisis, 2023 SVB run) may exceed historical empirical bands.
