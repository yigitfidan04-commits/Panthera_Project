import sqlite3
import pandas as pd

# Define database and Excel file names
db_name = 'Panthera_Factory.db'
excel_file = 'Master Spec.xlsx'

print(f"[{excel_file}] is being read and transferred to the factory...")

# Establish connection to the SQLite database
db_connection = sqlite3.connect(db_name)

try:
    # Read all sheets from the Excel file into memory
    excel_data = pd.read_excel(excel_file, sheet_name=None)
    
    # Convert each sheet into a separate SQL table
    for sheet_name, data_table in excel_data.items():
        print(f"-> Processing '{sheet_name}' into SQL...")
        # Save to SQL, replacing if it already exists
        data_table.to_sql(sheet_name, db_connection, if_exists='replace', index=False)
        
    print("✅ SUCCESS: All Excel sheets have been successfully imported into the SQL database!")
    
except Exception as error:
    print(f"SYSTEM ERROR: {error}")

finally:
    # Close the database doors
    db_connection.close()