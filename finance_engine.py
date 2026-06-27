import sqlite3
import pandas as pd

db_name = 'Panthera_Factory.db'
db_connection = sqlite3.connect(db_name)

print("--- PANTHERA FINANCIAL ENGINEERING & PRICING ---")
print("Target: Calculating Required MSRP for Realistic Profit Margins\n")

try:
    # 1. Get existing tables
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(tables_query, db_connection)
    
    # 2. Recalculate VZ Base Cost
    bom_table = [name for name in tables['name'] if 'BOM' in name and 'Upgrade' not in name][0]
    base_query = f"SELECT [TotalCost_Num] FROM [{bom_table}] WHERE Item NOT LIKE '%Total%' AND Item NOT LIKE '%Sum%' AND [TotalCost_Num] IS NOT NULL"
    base_cost = pd.read_sql_query(base_query, db_connection)['TotalCost_Num'].sum()
    
    # 3. Recalculate VZ+ Cost
    upgrade_table = [name for name in tables['name'] if 'Upgrade' in name][0]
    upgrade_query = f"SELECT [TotalCost_Num] FROM [{upgrade_table}] WHERE Item NOT LIKE '%Total%' AND Item NOT LIKE '%Sum%' AND [TotalCost_Num] IS NOT NULL"
    upgrade_cost = pd.read_sql_query(upgrade_query, db_connection)['TotalCost_Num'].sum()
    vz_plus_cost = base_cost + upgrade_cost

    # 4. PRICING ALGORITHM (Realistic Market Parameters)
    target_margins = [0.17, 0.19, 0.21, 0.22] # 17%, 19%, 21%, 22%
    
    financial_report = []

    for margin in target_margins:
        vz_msrp = base_cost / (1 - margin)
        vz_plus_msrp = vz_plus_cost / (1 - margin)
        
        financial_report.append({
            "Target Margin": f"{int(margin * 100)}%",
            "VZ MSRP (€)": round(vz_msrp, 2),
            "VZ+ MSRP (€)": round(vz_plus_msrp, 2),
            "VZ Profit/Car (€)": round(vz_msrp - base_cost, 2),
            "VZ+ Profit/Car (€)": round(vz_plus_msrp - vz_plus_cost, 2)
        })

    report_df = pd.DataFrame(financial_report)
    
    print("📋 EXECUTIVE PRICING STRATEGY REPORT (REALISTIC):")
    print("-" * 75)
    print(report_df.to_string(index=False))
    print("-" * 75)

except Exception as error:
    print(f"System Error: {error}")

finally:
    db_connection.close()