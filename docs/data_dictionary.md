# Data Dictionary: Liquidity Stress Forecaster

## 1. Overview
This data dictionary details the schema, operational definitions, data lineage, and statistical characteristics for the daily net liquidity outflow time-series dataset (`data/synthetic/daily_outflow.csv`).

## 2. Dataset Architecture
- **Temporal Span**: 3 Calendar Years (`2023-01-02` to `2025-12-31`).
- **Total Records**: 1,095 consecutive daily observations.
- **Grain**: One record per calendar day representing aggregate net liquidity outflows.
- **Denomination**: Synthetic Index Units ($M index).

---

## 3. Schema & Feature Specifications

| Field Name | Type | Nullable | Source | Business Definition | Range |
|---|---|---|---|---|---|
| `date` | Timestamp | No | Treasury Core | Calendar observation date. | 2023-01-02 to 2025-12-31 |
| `net_outflow` | Float | No | Cash Ledger / Fedwire | Net daily cash outflow disbursements minus cash receipts ($M index). | 5.0 to 198.4 |
| `market_stress` | Float | No | Bloomberg / Market Risk | Autoregressive financial market liquidity stress index. | -0.85 to +3.92 |
| `dow` | Integer | No | Calendar | Day-of-week index (0 = Monday, 6 = Sunday). | 0 to 6 |
| `dom` | Integer | No | Calendar | Day-of-month calendar integer. | 1 to 31 |
| `month_end` | Binary (0/1) | No | Calendar | Flag indicating final business day of month or immediately preceding day. | 0 or 1 |
| `lag1` | Float | No | Derived | Net cash outflow from prior business day ($t-1$). | 5.0 to 198.4 |
| `lag7` | Float | No | Derived | Net cash outflow from same weekday in prior week ($t-7$). | 5.0 to 198.4 |
| `lag14` | Float | No | Derived | Net cash outflow two weeks prior ($t-14$). | 5.0 to 198.4 |
| `roll7` | Float | No | Derived | 7-day trailing moving average of cash outflows. | 15.2 to 142.1 |
| `roll28` | Float | No | Derived | 28-day trailing moving average of cash outflows. | 45.0 to 125.6 |
