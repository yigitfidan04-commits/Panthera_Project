import sqlite3
import pandas as pd

# Define database name
db_name = 'Panthera_Factory.db'

# Establish connection to the SQLite database
db_connection = sqlite3.connect(db_name)

print("--- PANTHERA VARIANT ENGINEERING SYSTEM ---\n")

try:
    # Get table list
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(tables_query, db_connection)
    
    # 1. Calculate Base (VZ) Cost from the main BOM
    bom_table = [name for name in tables['name'] if 'BOM' in name and 'Upgrade' not in name][0]
    base_query = f"""
        SELECT Item, [TotalCost_Num] FROM [{bom_table}] 
        WHERE Item NOT LIKE '%Total%' AND Item NOT LIKE '%Sum%' AND [TotalCost_Num] IS NOT NULL
    """
    base_data = pd.read_sql_query(base_query, db_connection)
    base_cost = base_data['TotalCost_Num'].sum()
    
    # 2. Extract Performance Add-ons from Upgrade BOM
    upgrade_table = [name for name in tables['name'] if 'Upgrade' in name][0]
    upgrade_query = f"""
        SELECT Item, [Unit Cost (€)], [TotalCost_Num] FROM [{upgrade_table}]
        WHERE Item NOT LIKE '%Total%' AND Item NOT LIKE '%Sum%' AND [TotalCost_Num] IS NOT NULL
    """
    upgrade_data = pd.read_sql_query(upgrade_query, db_connection)
    upgrade_cost = upgrade_data['TotalCost_Num'].sum()
    
    # 3. Calculate VZ+ Total Cost
    vz_plus_cost = base_cost + upgrade_cost
    
    # --- REPORTING ---
    print(f"⚡ VZ (BASE VARIANT) COST: {base_cost:,.2f} €\n")
    
    print(f"[{upgrade_table}] - Performance Add-ons:")
    print(upgrade_data.to_string(index=False))
    print("-" * 50)
    print(f"Total Upgrade Premium: +{upgrade_cost:,.2f} €\n")
    
    print(f"🔥 VZ+ (HIGH-PERFORMANCE) TOTAL PRODUCTION COST: {vz_plus_cost:,.2f} €")

except Exception as error:
    print(f"System Error: {error}")

finally:
    db_connection.close()