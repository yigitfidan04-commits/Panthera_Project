import subprocess
import time

print("="*70)
print(" 🚀 PANTHERA MASTER ORCHESTRATOR INITIALIZED")
print(" 🏢 ODTÜ Industrial Engineering & Automotive Systems")
print("="*70)

# Sistemdeki otonom motorların kritik çalışma sırası
# Veritabanı kurulmadan diğerleri çalışamaz, o yüzden sıralama hayati önem taşır.
pipeline = [
    ("🏗️  Departman 1: Fabrika Kurulumu (ETL)", "fabrika_kurulum.py"),
    ("💵  Departman 2: Parça Maliyet Denetimi", "cost.py"),
    ("💰  Departman 3: Finans ve Fiyatlandırma", "finance_engine.py"),
    ("🏎️  Departman 4: MEB Evo Dinamik Motoru", "dynamics_engine.py"),
    ("📐  Departman 5: Aerodinamik Kısıt Yargıcı", "constraints_engine.py"),
    ("🌡️  Departman 6: Otonom BMS Zekası (Termal)", "thermal_engine.py"),
    ("🔋  Departman 7: Verimlilik ve Menzil Hesaplayıcı", "range_engine.py")
]

print("\n⚙️ ÜRETİM BANDI ŞALTERİ İNDİRİLİYOR...\n")
time.sleep(1)

# Üretim Bandı Döngüsü
for name, script in pipeline:
    print(f"⏳ BAŞLATILIYOR: {name}")
    time.sleep(0.5) # Terminaller arası okunabilirlik için ufak bir gecikme
    
    try:
        # Python'a diğer dosyaları alt-işlem (subprocess) olarak çalıştırma emri veriyoruz
        subprocess.run(["python", script], check=True)
        print(f"✅ TAMAMLANDI: {name} başarıyla test edildi.\n")
        print("-" * 70)
        time.sleep(1)
        
    except subprocess.CalledProcessError:
        print(f"\n❌ SİSTEM ÇÖKTÜ: [{script}] modülünde kritik bir hata tespit edildi!")
        print("🚨 Üretim bandı acil durum protokolüyle durduruldu. Sonraki departmanlara geçilemiyor.")
        break # Hata varsa zinciri kır, fabrikayı durdur
        
    except FileNotFoundError:
        print(f"\n❌ DOSYA BULUNAMADI: [{script}] eksik. Klasör yolunu kontrol et.")
        break

else:
    # Eğer döngü hiçbir 'break' yemeden (hatasız) tamamlanırsa burası çalışır
    print("\n" + "="*70)
    print(" 🏁 TÜM SİSTEMLER ONAYLANDI. PANTHERA SERİ ÜRETİME HAZIR.")
    print("="*70)