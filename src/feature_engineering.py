import numpy as np, pandas as pd
FEATS=["dow","dom","month_end","market_stress","lag1","lag7","lag14","roll7","roll28"]
def build_features(d):
    x=d.copy(); x["dow"]=x.date.dt.dayofweek; x["dom"]=x.date.dt.day
    x["month_end"]=(x.date.dt.is_month_end|((x.date+pd.Timedelta(days=1)).dt.is_month_end)).astype(int)
    for k in (1,7,14): x[f"lag{k}"]=x.net_outflow.shift(k)
    x["roll7"]=x.net_outflow.shift(1).rolling(7).mean(); x["roll28"]=x.net_outflow.shift(1).rolling(28).mean()
    return x.dropna().reset_index(drop=True)
