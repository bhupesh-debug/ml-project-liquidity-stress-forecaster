import pytest
import numpy as np
import pandas as pd
from src.data_pipeline import make_data
from src.feature_engineering import build_features, FEATS
from src.model import median_model, upper_model
from src.evaluate import wape
from src.business_case import compute_business_case

def test_data_generation():
    df = make_data(days=365, seed=42)
    assert len(df) == 365
    assert "date" in df.columns
    assert "net_outflow" in df.columns
    assert "market_stress" in df.columns
    assert df["net_outflow"].min() > 0

def test_feature_engineering():
    df = make_data(days=100, seed=42)
    f = build_features(df)
    for col in FEATS:
        assert col in f.columns
    assert len(f) > 0
    assert f.isna().sum().sum() == 0

def test_quantile_and_calibration():
    df = make_data(days=200, seed=42)
    f = build_features(df)
    m = median_model().fit(f[FEATS], f.net_outflow)
    u = upper_model(0.95).fit(f[FEATS], f.net_outflow)
    p50 = m.predict(f[FEATS])
    p95 = u.predict(f[FEATS])
    assert len(p50) == len(f)
    assert np.mean(p95 >= p50) > 0.85

def test_business_case_calculation():
    bc = compute_business_case()
    assert len(bc) == 3
    for row in bc:
        assert "Year1_Net_Benefit" in row
        assert "Three_Year_NPV" in row
