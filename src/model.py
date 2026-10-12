from sklearn.ensemble import HistGradientBoostingRegressor as H
def median_model(): return H(loss="absolute_error",max_depth=4,learning_rate=0.05,max_iter=300,random_state=11)
def upper_model(q=0.95): return H(loss="quantile",quantile=q,max_depth=4,learning_rate=0.05,max_iter=300,random_state=11)
