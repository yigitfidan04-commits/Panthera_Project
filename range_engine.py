import sqlite3
import pandas as pd

# Define database name
db_name = 'Panthera_Factory.db'
db_connection = sqlite3.connect(db_name)

print("--- PANTHERA EFFICIENCY & RANGE ENGINE (REAL-WORLD EDITION) ---")
print("Target: Calculating Dynamic WLTP and Street-Legal Range Constraints\n")

try:
    # 1. Temel Parametreler 
    net_battery_kwh = 79.0  # VAG MEB Evo Yeni Nesil Performans Bataryası
    
    # Sürtünme ve Aerodinamik Kısıtlar 
    cd = 0.24
    frontal_area = 2.2
    air_density = 1.225
    gravity = 9.81
    crr = 0.008 # Premium EV-Specific Low Rolling Resistance Tires
    drivetrain_efficiency = 0.90 # Motor verimliliği
    regen_efficiency = 0.75      # Rejeneratif frenlemenin (geri kazanım) verim kaybı
    aux_power_kw = 1.5           # Klima, koltuk ısıtma, ekranlar

    vz_weight = 1850
    vz_plus_weight = 1916.5

    print(f"🔋 BATTERY: {net_battery_kwh} kWh Net")
    print(f"📐 AERO: Cd = {cd} | Frontal Area = {frontal_area} m^2")
    print("⚠️ DYNAMIC PENALTY ENABLED: Simulating Stop-and-Go & Acceleration Losses\n")

    def calculate_consumption(weight, speed_kmh, dynamic_penalty, is_awd=False):
        """Gerçek hayat dinamiklerini (dur-kalk) hesaba katan fizik motoru"""
        speed_ms = speed_kmh / 3.6
        
        # 1. Yuvarlanma Direnci
        rolling_resistance_force = weight * gravity * crr
        if is_awd:
            rolling_resistance_force *= 1.05 # AWD ekstra sürtünme
            
        # 2. Rüzgar Direnci
        aero_drag_force = 0.5 * air_density * cd * frontal_area * (speed_ms ** 2)
        
        # 3. Saf İtme Gücü
        total_force = rolling_resistance_force + aero_drag_force
        base_power_at_wheels_kw = (total_force * speed_ms) / 1000
        
        # --- İŞTE GERÇEKLİK MÜDAHALESİ ---
        # Sabit hıza, dur-kalk ve ivmelenme kayıplarını (Dynamic Penalty) ekliyoruz
        real_power_at_wheels_kw = base_power_at_wheels_kw * dynamic_penalty
        
        # Bataryadan Çekilen Toplam Güç (Motor Kaybı + Klima Eklentisi)
        power_from_battery_kw = (real_power_at_wheels_kw / drivetrain_efficiency) + aux_power_kw
        
        # Tüketim (kWh/100km)
        consumption_100km = (power_from_battery_kw / speed_kmh) * 100
        
        return consumption_100km

    # --- GERÇEKÇİ SİMÜLASYON SENARYOLARI ---
    # Dynamic_Penalty: Sabit hıza göre eklenecek "gerçek hayat" zorluk katsayısı
    scenarios = [
        # Şehir İçi: Ortalama hız düşük ama çok fazla dur-kalk, kırmızı ışık ve atalet kaybı var. (Yük %40 arttırıldı)
        {"Env": "City (Real Stop & Go)", "Speed": 40, "Dynamic_Penalty": 1.40},
        
        # WLTP Döngüsü: Sert hızlanmalar ve yavaşlamalar barındıran homologasyon testi. (Yük %25 arttırıldı)
        {"Env": "Mixed (True WLTP Cycle)", "Speed": 70, "Dynamic_Penalty": 1.25}, 
        
        # Otoban: Hız sabit, dur-kalk çok az. Sadece ara sıra şerit değiştirme/sollama rüzgarı. (Yük %5 arttırıldı)
        {"Env": "Highway (120 km/h Autobahn)", "Speed": 120, "Dynamic_Penalty": 1.05}
    ]

    results = []

    for s in scenarios:
        env = s["Env"]
        speed = s["Speed"]
        penalty = s["Dynamic_Penalty"]
        
        # VZ Hesaplama
        vz_cons = calculate_consumption(vz_weight, speed, penalty, is_awd=False)
        vz_range = net_battery_kwh / (vz_cons / 100)
        
        # VZ+ Hesaplama
        vz_plus_cons = calculate_consumption(vz_plus_weight, speed, penalty, is_awd=True)
        vz_plus_range = net_battery_kwh / (vz_plus_cons / 100)
        
        results.append({
            "Scenario": env,
            "VZ Cons.": f"{vz_cons:.1f} kWh",
            "VZ Range": f"{int(vz_range)} km",
            "VZ+ Cons.": f"{vz_plus_cons:.1f} kWh",
            "VZ+ Range": f"{int(vz_plus_range)} km"
        })

    # Raporlama
    report_df = pd.DataFrame(results)
    print("📊 PANTHERA ENERGY CONSUMPTION & RANGE REPORT:")
    print("-" * 75)
    print(report_df.to_string(index=False))
    print("-" * 75)
    
    # Karar Mekanizması (Gerçekçi WLTP)
    wltp_vz_range_str = results[1]["VZ Range"]
    wltp_vz_range = int(wltp_vz_range_str.split()[0])
    
    if wltp_vz_range >= 580:
        print("\n✅ VERDICT: PASSED (STREET LEGAL).")
        print(f"Rationale: Real-world WLTP Range stands at {wltp_vz_range} km. Perfectly competitive against Ioniq 6 and Model 3.")
    else:
        print("\n❌ VERDICT: FAILED.")
        print("Rationale: Range fell below competitive benchmarks in real-world testing.")

except Exception as error:
    print(f"System Error: {error}")

finally:
    db_connection.close()