import os
import pandas as pd

def compute_business_case():
    """
    Computes rigorous corporate treasury business case for Liquidity Stress Forecaster:
    - 3 Scenarios: Conservative, Base, Upside
    - Buffer drag reduction (avoided yield penalty on excess idle liquidity buffer)
    - Avoided emergency borrowing and repo facility commitment fees
    - Treasury quantitative analyst labor automation hours
    - Implementation costs, annual maintenance, Year-1 Net Benefit, 3-Year NPV, Payback Period
    """
    os.makedirs("reports", exist_ok=True)
    
    scenarios = {
        "Conservative": {
            "buffer_optimization_savings": 1200000,
            "avoided_emergency_borrowing": 400000,
            "treasury_hours_saved": 650,
            "hourly_rate": 125,
            "implementation_cost": 280000,
            "annual_maintenance_cost": 70000
        },
        "Base": {
            "buffer_optimization_savings": 2400000,
            "avoided_emergency_borrowing": 850000,
            "treasury_hours_saved": 900,
            "hourly_rate": 125,
            "implementation_cost": 260000,
            "annual_maintenance_cost": 65000
        },
        "Upside": {
            "buffer_optimization_savings": 3800000,
            "avoided_emergency_borrowing": 1600000,
            "treasury_hours_saved": 1200,
            "hourly_rate": 125,
            "implementation_cost": 240000,
            "annual_maintenance_cost": 60000
        }
    }
    
    rows = []
    discount_rate = 0.10
    
    for name, s in scenarios.items():
        labor_benefit = s["treasury_hours_saved"] * s["hourly_rate"]
        total_annual_benefit = s["buffer_optimization_savings"] + s["avoided_emergency_borrowing"] + labor_benefit
        capex = s["implementation_cost"]
        opex = s["annual_maintenance_cost"]
        
        net_yr1 = total_annual_benefit - capex - opex
        net_yr2 = total_annual_benefit - opex
        net_yr3 = total_annual_benefit - opex
        
        npv_3yr = -capex + (net_yr1 + capex)/(1 + discount_rate) + net_yr2/((1 + discount_rate)**2) + net_yr3/((1 + discount_rate)**3)
        payback_months = (capex / (total_annual_benefit - opex)) * 12
        roi_3yr = (npv_3yr / capex) * 100
        
        rows.append({
            "Scenario": name,
            "Buffer_Carry_Optimization": f"${s['buffer_optimization_savings']:,.0f}",
            "Avoided_Emergency_Borrowing": f"${s['avoided_emergency_borrowing']:,.0f}",
            "Treasury_Labor_Savings": f"${labor_benefit:,.0f}",
            "Total_Annual_Benefit": f"${total_annual_benefit:,.0f}",
            "Implementation_Cost": f"${capex:,.0f}",
            "Annual_Maintenance_Cost": f"${opex:,.0f}",
            "Year1_Net_Benefit": f"${net_yr1:,.0f}",
            "Payback_Period_Months": round(payback_months, 1),
            "Three_Year_NPV": f"${npv_3yr:,.0f}",
            "ROI_3Year_Pct": f"{round(roi_3yr, 0)}%"
        })
        
    df_bc = pd.DataFrame(rows)
    df_bc.to_csv("reports/business_case_table.csv", index=False)
    return df_bc.to_dict(orient="records")
