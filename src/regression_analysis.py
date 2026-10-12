import os
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from src.feature_engineering import build_features, FEATS
from src.evaluate import wape

def run_regression_analysis(df_outflow):
    """
    Performs econometric regression and benchmark comparative evaluation for Project 3:
    - OLS Linear Model with HC3 robust standard errors
    - Quantile Regression at median (p50) and upper bound (p95)
    - Multicollinearity diagnostics (VIF)
    - Out-of-sample benchmark comparison (Rolling 28d, Lag 7, OLS, QuantReg, GBM)
    """
    os.makedirs("reports", exist_ok=True)
    
    f = build_features(df_outflow)
    cut = len(f) - 180
    tr = f.iloc[:cut].copy()
    te = f.iloc[cut:].copy()
    
    X_tr = tr[FEATS].copy()
    y_tr = tr["net_outflow"].values
    X_te = te[FEATS].copy()
    y_te = te["net_outflow"].values
    
    # Add constant
    X_tr_const = sm.add_constant(X_tr)
    X_te_const = sm.add_constant(X_te)
    
    # 1. OLS with HC3 robust standard errors
    ols_model = sm.OLS(y_tr, X_tr_const).fit(cov_type='HC3')
    p_ols = ols_model.predict(X_te_const)
    
    # 2. Quantile Regression (p50)
    qr_p50 = sm.QuantReg(y_tr, X_tr_const).fit(q=0.50)
    p_qr50 = qr_p50.predict(X_te_const)
    
    # 3. Quantile Regression (p95)
    qr_p95 = sm.QuantReg(y_tr, X_tr_const).fit(q=0.95)
    p_qr95 = qr_p95.predict(X_te_const)
    
    # Extract OLS Coefficients & Inference
    coef_df = pd.DataFrame({
        "Variable": X_tr_const.columns,
        "Coefficient": ols_model.params.values,
        "Std_Error": ols_model.bse.values,
        "t_Statistic": ols_model.tvalues.values,
        "p_Value": ols_model.pvalues.values,
        "CI_Lower_95": ols_model.conf_int()[0].values,
        "CI_Upper_95": ols_model.conf_int()[1].values
    })
    
    # VIF calculations
    vif_data = []
    for i, col in enumerate(X_tr.columns):
        v = variance_inflation_factor(X_tr.values, i)
        vif_data.append({"Variable": col, "VIF": round(v, 2)})
    vif_df = pd.DataFrame(vif_data)
    coef_df = coef_df.merge(vif_df, on="Variable", how="left")
    coef_df.to_csv("reports/regression_coefficients.csv", index=False)
    
    # Benchmarks on test set
    p_lag7 = te["lag7"].values
    p_roll28 = te["roll28"].values
    
    def calc_metrics(y_true, y_pred):
        err = y_pred - y_true
        return {
            "wape": round(wape(y_true, y_pred), 3),
            "mae": round(float(np.mean(np.abs(err))), 2),
            "rmse": round(float(np.sqrt(np.mean(err**2))), 2),
            "bias": round(float(np.sum(err) / np.sum(y_true)), 3)
        }
        
    benchmarks = {
        "rolling_28d_mean": calc_metrics(y_te, p_roll28),
        "seasonal_naive_lag7": calc_metrics(y_te, p_lag7),
        "ols_regression": calc_metrics(y_te, p_ols),
        "quantile_reg_p50": calc_metrics(y_te, p_qr50)
    }
    
    # Coverage of parametric QuantReg p95
    qr95_cov = float(np.mean(y_te <= p_qr95))
    qr95_width = float(np.mean(p_qr95 - p_qr50))
    
    summary = {
        "r_squared": round(ols_model.rsquared, 4),
        "adj_r_squared": round(ols_model.rsquared_adj, 4),
        "f_stat": round(ols_model.fvalue, 2),
        "f_pvalue": float(ols_model.f_pvalue),
        "n_obs": int(ols_model.nobs),
        "benchmarks": benchmarks,
        "quantreg_p95_coverage": round(qr95_cov, 3),
        "quantreg_mean_interval_width": round(qr95_width, 2),
        "coefficients": coef_df.to_dict(orient="records")
    }
    
    return summary
