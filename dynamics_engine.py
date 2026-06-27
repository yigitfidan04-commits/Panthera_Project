import sqlite3
import pandas as pd

# Define database name
db_name = 'Panthera_Factory.db'
db_connection = sqlite3.connect(db_name)

print("--- PANTHERA ADVANCED PHYSICS ENGINE ---")
print("Target: Calculating Real-World 0-100 km/h with Exact MEB Evo Limits\n")

try:
    # 1. Departmanları keşfet ve Performans tablosunu bul
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(tables_query, db_connection)
    perf_table = [name for name in tables['name'] if 'Performance' in name][0]
    
    # 2. Ağırlığı veritabanından çek (Excel'deki ağırlığımız 1850 kg olarak doğruydu)
    query = f"SELECT Parameter, Value FROM [{perf_table}] WHERE Value IS NOT NULL"
    perf_data = pd.read_sql_query(query, db_connection)
    vz_weight = perf_data.loc[perf_data['Parameter'] == 'VZ_Curb_Weight', 'Value'].values[0]
    
    # --- İŞTE BURASI: MEB EVO GERÇEKLİK MÜDAHALESİ ---
    # Excel'deki hayali 240 kW gücü çöpe atıyoruz. VW Grubu'nun gerçek donanım limitlerini sisteme çiviliyoruz:
    vz_power_kw = 210        # VZ Base: Sadece arkada APP550 Motor (286 HP)
    vz_plus_power_kw = 250   # VZ+: APP550 + Önde AKA150 Motor. BMS'in izin verdiği maksimum sınır! (340 HP)
    
    # Kinetik Enerji Sabiti (100 km/h = 27.78 m/s)
    v_target_ms = 27.78 
    drivetrain_eff = 0.90    # MEB Platformu aktarma organı verimliliği
    
    print("⚙️ INITIALIZING REAL-WORLD PHYSICS PARAMETERS...")
    print(f"- Drivetrain Efficiency: %{int(drivetrain_eff*100)} (MEB Platform Standard)")
    print("- Traction Control Limitation: Applied to prevent wheelspin\n")
    
    # --- VZ (BASE RWD) REALITY CALCULATION ---
    vz_traction_factor = 0.70  # Arkadan itişli (RWD) araç, patinajı önlemek için gücün ancak %70'ini yere basabilir.
    
    vz_usable_power = (vz_power_kw * 1000) * drivetrain_eff * vz_traction_factor 
    vz_ke = 0.5 * vz_weight * (v_target_ms ** 2)
    vz_real_time = vz_ke / vz_usable_power
    
    print(f"⚖️ VZ (Base) Specs: {vz_weight} kg | {int(vz_power_kw * 1.341)} HP (RWD)")
    print(f"🏎️ VZ (Base) REAL 0-100 km/h: {vz_real_time:.2f} seconds\n")
    
    # --- VZ+ (HIGH-PERFORMANCE AWD) REALITY CALCULATION ---
    vz_plus_weight = vz_weight + 50 # Ekstra ön motor ve kalın soğutucuların ağırlığı eklendi
    vz_plus_traction_factor = 0.78  # Dört Çeker (AWD) olduğu için tutunma artar, gücü daha erken yere basar!
    
    vz_plus_usable_power = (vz_plus_power_kw * 1000) * drivetrain_eff * vz_plus_traction_factor
    vz_plus_ke = 0.5 * vz_plus_weight * (v_target_ms ** 2)
    vz_plus_real_time = vz_plus_ke / vz_plus_usable_power
    
    print("-" * 50)
    print(f"🔥 VZ+ PROJECTED SPECS: {vz_plus_weight} kg | {int(vz_plus_power_kw * 1.341)} HP (Dual-Motor AWD - MEB Evo MAX LIMIT)")
    print(f"🔥 VZ+ REAL 0-100 km/h: {vz_plus_real_time:.2f} seconds")
    print("-" * 50)

except Exception as error:
    print(f"System Error: {error}")

finally:
    db_connection.close()