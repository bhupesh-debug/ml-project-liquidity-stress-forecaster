import numpy as np, pandas as pd
def make_data(days=1095, seed=11):
    """Synthetic daily net cash outflow ($M index) for a treasury desk, with month-end spikes and market stress."""
    r=np.random.default_rng(seed); idx=pd.date_range("2023-01-02",periods=days,freq="D")
    dow=np.array([1.15,1.05,1.0,1.0,1.1,.35,.25])[idx.dayofweek]
    me=1+0.35*(idx.is_month_end|((idx+pd.Timedelta(days=1)).is_month_end))
    stress=np.zeros(days)
    for i in range(1,days): stress[i]=0.97*stress[i-1]+r.normal(0,.15)+(1.2 if r.random()<.006 else 0)
    stress=np.clip(stress,-1,4)
    trend=np.linspace(95,110,days)
    out=trend*dow*me*(1+0.18*np.maximum(stress,0))+r.normal(0,6,days)
    return pd.DataFrame({"date":idx,"net_outflow":np.clip(out,5,None).round(2),"market_stress":stress.round(3)})
