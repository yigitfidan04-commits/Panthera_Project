import sqlite3
import pandas as pd

# Define database name
db_name = 'Panthera_Factory.db'
db_connection = sqlite3.connect(db_name)

print("--- PANTHERA SMART THERMAL ENGINE (PREDICTIVE BMS) ---")
print("Target: Simulating Software-Driven Thermal Management (0€ Hardware Cost)\n")

try:
    # 1. SQL'den Kısıtları Çek (Zırhlı Sorgu)
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(tables_query, db_connection)
    constraint_table = [name for name in tables['name'] if 'Constraint' in name][0]
    
    query = f"SELECT * FROM [{constraint_table}] WHERE [Constraint] LIKE '%Thermal%'"
    thermal_data = pd.read_sql_query(query, db_connection)
    
    # Başmühendis Notu: Pazar Hedefleri
    print("💰 MARKET TARGET: VZ (52k-55k €) | VZ+ (60k-64k €)")
    print("Strategy: Keeping costs tight. Managing heat strictly through BMS Software.\n")
    print("="*75)

    # Başlangıç Parametreleri
    pack_temp = 30.0       

    # Sürüş Fazları (Aynı Müşteri, Aynı Yol)
    driving_phases = [
        {"Phase": "City & Suburbs (Şehir İçi)", "Time_min": 20, "Heat_rate": 0.2, "Cool_rate": 0.5},
        {"Phase": "Highway Cruise (130 km/h)", "Time_min": 45, "Heat_rate": 0.4, "Cool_rate": 0.5},
        {"Phase": "Autobahn Unrestricted (180 km/h)", "Time_min": 15, "Heat_rate": 1.2, "Cool_rate": 0.5},
        {"Phase": "Aggressive Overtakes (Tam Gaz)", "Time_min": 5, "Heat_rate": 3.5, "Cool_rate": 0.5},
        {"Phase": "Alpine Mountain Pass (Dik Yokuş)", "Time_min": 15, "Heat_rate": 1.8, "Cool_rate": 0.5},
        {"Phase": "Traffic Jam / Cooldown", "Time_min": 20, "Heat_rate": 0.1, "Cool_rate": 0.8}
    ]

    results = []

    for phase in driving_phases:
        name = phase["Phase"]
        duration = phase["Time_min"]
        base_heat_rate = phase["Heat_rate"]
        cool_rate = phase["Cool_rate"]
        
        # --- İŞTE MÜHENDİSLİK: PRE-CONDITIONING (Ön Soğutma) ---
        if "Alpine" in name:
            print(f"❄️ [BMS INTELLIGENCE] GPS detected 'Mountain Pass' approach!")
            print(f"   -> Routing A/C Compressor to Battery. Pre-cooling from {round(pack_temp, 1)}°C down to 15.0°C...\n")
            pack_temp = 15.0 # Müşteri dağa girmeden bataryayı derin dondurucuya aldık!

        status = "✅ OPTIMAL"
        min_power_state = "100% (340 HP)"

        # --- DAKİKA DAKİKA TERMAL SİMÜLASYON VE SOFT-LIMITER ---
        for minute in range(duration):
            current_heat_rate = base_heat_rate
            
            # Batarya sınırları zorlamaya başladığında gücü çaktırmadan tıraşlıyoruz
            if pack_temp >= 60.0:
                current_heat_rate = base_heat_rate * 0.4 # Limp Mode (Kaplumbağa)
                status = "❌ HARD THROTTLE"
                min_power_state = "40% (136 HP)"
            elif pack_temp >= 56.0:
                current_heat_rate = base_heat_rate * 0.8 # Sürücü hissetmez ama ısı düşer
                if status != "❌ HARD THROTTLE":
                    status = "🟡 SOFT LIMIT"
                    min_power_state = "80% (272 HP)"
            elif pack_temp >= 52.0:
                current_heat_rate = base_heat_rate * 0.9 # Ufak bir törpüleme
                if status not in ["❌ HARD THROTTLE", "🟡 SOFT LIMIT"]:
                    status = "🟢 PREDICTIVE COOLING"
                    min_power_state = "90% (306 HP)"

            # O dakikadaki net ısı değişimi
            pack_temp += (current_heat_rate - cool_rate)

        results.append({
            "Driving Phase": name,
            "End Temp (°C)": round(pack_temp, 1),
            "Lowest Power": min_power_state,
            "BMS Status": status
        })

    # Raporlama
    report_df = pd.DataFrame(results)
    print(report_df.to_string(index=False))
    print("\n" + "="*75)
    
    # Başmühendis Yargı Kararı
    hard_throttles = sum(1 for r in results if 'HARD THROTTLE' in r['BMS Status'])
    if hard_throttles == 0:
        print("🏁 HOMOLOGATION VERDICT: PASSED.")
        print("Rationale: Added 0€ in hardware costs. The predictive BMS successfully created a thermal buffer and avoided total power loss. Series production approved.")
    else:
        print("❌ HOMOLOGATION VERDICT: FAILED.")

except Exception as error:
    print(f"System Error: {error}")

finally:
    db_connection.close()