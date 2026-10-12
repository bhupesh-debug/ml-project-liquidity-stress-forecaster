import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def wape(y,p): return float(np.abs(y-p).sum()/np.abs(y).sum())
def stress_table(p50,p95,buffer,horizon=30):
    """Rolling 30-day windows: coverage = buffer / cumulative stressed outflow. <1.0 means buffer is exhausted."""
    scen={"Base (p50)":lambda a,b:a,
          "Mild stress (+25% first 10d)":lambda a,b:np.where(np.arange(len(a))<10,a*1.25,a),
          "Severe stress (p95, x1.4 first 10d)":lambda a,b:np.where(np.arange(len(b))<10,b*1.4,b)}
    rows=[]
    for name,f in scen.items():
        cov=[];surv=[]
        for s in range(0,len(p50)-horizon):
            path=f(p50[s:s+horizon],p95[s:s+horizon]); c=np.cumsum(path)
            cov.append(buffer/c[-1]); surv.append(int(np.argmax(c>buffer))+1 if (c>buffer).any() else horizon+1)
        rows.append({"scenario":name,"median_coverage":round(float(np.median(cov)),2),"worst_coverage":round(float(np.min(cov)),2),
                     "share_of_windows_buffer_breached":round(float(np.mean(np.array(cov)<1)),3),"min_survival_days":int(min(surv))})
    return pd.DataFrame(rows)
def forecast_chart(dates,y,p50,p95,path):
    plt.figure(figsize=(8,3.6)); plt.plot(dates,y,color="#1F3864",lw=1,label="Actual"); plt.plot(dates,p50,color="#C9A227",lw=1,label="Forecast p50")
    plt.plot(dates,p95,color="#B03A2E",lw=.8,ls="--",label="Forecast p95"); plt.legend(); plt.title("Daily net outflow: actual vs forecast (test period)")
    plt.tight_layout(); plt.savefig(path,dpi=130); plt.close()
