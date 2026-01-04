# config.py
# Bu dosya ETL sisteminin tüm ayarlarını merkezi olarak yönetir
# Tüm parametreleri buradan değiştirebilirsin

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# .env dosyasından environment variables'ları yükle
load_dotenv()

# ========================
# 🔐 AZURE AD AYARLARI
# ========================
CLIENT_ID = os.getenv("CLIENT_ID")
if not CLIENT_ID:
    raise ValueError("❌ CLIENT_ID bulunamadı! .env dosyasını oluşturup CLIENT_ID değerini ekleyin.")

TENANT_ID = os.getenv("TENANT_ID", "consumers")
SCOPES = ["https://graph.microsoft.com/Mail.Read"]

# ========================
# 📧 EMAIL FİLTRE AYARLARI
# ========================
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
if not SENDER_EMAIL:
    raise ValueError("❌ SENDER_EMAIL bulunamadı! .env dosyasında SENDER_EMAIL değerini ekleyin.")

MAX_RESULTS = 20  # Kaç mesaj kontrol edilsin (güvenlik için fazla alıyoruz)

# ========================
# 📊 RAPOR AYARLARI
# ========================
# Her rapor türü için ayarlar: (Mesaj_Konusu, Hedef_Klasör, Yeni_Dosya_İsmi)
RAPOR_AYARLARI = {
    "RAPOR1": {
        "mesaj_konusu": "Konu1",     # Mesaj konusunda bu kelime aranacak
        "rapor_adi": "Rapor1",       # Açıklama için rapor ismi  
        "klasor": "Klasör1",         # Hangi klasöre kaydedilsin
        "dosya_ismi": "X"            # X.xlsx olarak kaydedilsin
    },
    "RAPOR2": {
        "mesaj_konusu": "Konu2",     # Gerçek mesaj konunuzu buraya yazın
        "rapor_adi": "Rapor2", 
        "klasor": "Klasör2",
        "dosya_ismi": "Y"            # Y.xlsx olarak kaydedilsin
    }
}

# 💡 KULLANIM: 
# - "mesaj_konusu": Email'de gelen gerçek konu başlığındaki anahtar kelime
# - "rapor_adi": Sadece açıklama/log için kullanılır
# - Örnek: Email konusu "Haftalık Satış Raporu - Ocak 2024" ise
#          mesaj_konusu = "Satış Raporu" yazabilirsiniz

# ========================
# 📁 KLASÖR AYARLARI
# ========================
MASAUSTU_PATH = os.getenv("MASAUSTU_PATH")
if not MASAUSTU_PATH:
    raise ValueError("❌ MASAUSTU_PATH bulunamadı! .env dosyasında MASAUSTU_PATH değerini ekleyin.")

MASTER_KLASOR = "MasterKlasor"  # İsteğe bağlı: tüm dosyalar buraya da kopyalanabilir

# Klasör yollarını otomatik oluştur
KLASOR_YOLLARI = {}
for rapor_id, ayar in RAPOR_AYARLARI.items():
    klasor_adi = ayar["klasor"]
    KLASOR_YOLLARI[rapor_id] = os.path.join(MASAUSTU_PATH, klasor_adi)

MASTER_KLASOR_PATH = os.path.join(MASAUSTU_PATH, MASTER_KLASOR)

# ========================
# ⏰ TARİH FİLTRE AYARLARI
# ========================

# 🔄 OTOMATIK PAZARTESI MOD (Cron job ile kullanım için)
# def get_last_monday():
#     """Son pazartesi gününün tarihini döndürür"""
#     today = datetime.now().date()
#     days_since_monday = today.weekday()  # 0=Pazartesi, 6=Pazar
#     last_monday = today - timedelta(days=days_since_monday)
#     return last_monday.strftime("%Y-%m-%dT00:00:00Z")
# TARIH_FILTRESI = get_last_monday()  # Her pazartesi otomatik çekimde kullan

# ========================
# ⏰ TARİH FİLTRE AYARLARI
# ========================

# 🗓️ MANUEL TARİH AYARI (Şu anda aktif)
# İstediğin tarihi elle ayarlayabilirsin:
MANUAL_DATE = os.getenv("MANUAL_DATE", "2025-08-13")  # YYYY-MM-DD formatında istediğin tarihi yaz
TARIH_FILTRESI = f"{MANUAL_DATE}T00:00:00Z"

# 💡 MANUEL TARİH DEĞİŞTİRME:
# Yukarıdaki MANUAL_DATE'i değiştir, örnek:
# - "2025-08-07" → Bugünkü mesajları çek
# - "2025-08-01" → 1 Ağustos'tan itibaren çek
# - "2025-07-29" → Geçen haftadan itibaren çek

# 🔄 OTOMATİK PAZARTESI MOD (Gelecekte otomasyon için)
# def get_last_monday():
#     """Son pazartesi gününün tarihini döndürür"""
#     today = datetime.now().date()
#     days_since_monday = today.weekday()  # 0=Pazartesi, 6=Pazar
#     last_monday = today - timedelta(days=days_since_monday)
#     return last_monday.strftime("%Y-%m-%dT00:00:00Z")
# TARIH_FILTRESI = get_last_monday()  # Otomasyon için bunu aktif et

# 🧪 ESNEKTARİH MOD (Test için)
# def get_recent_days(days=7):
#     """Son X günün tarihini döndürür"""  
#     today = datetime.now().date()
#     target_date = today - timedelta(days=days)
#     return target_date.strftime("%Y-%m-%dT00:00:00Z")
# TARIH_FILTRESI = get_recent_days(30)  # Son 30 günü çek

# ========================
# 🎯 EXCEL FİLTRE AYARLARI
# ========================
EXCEL_UZANTILARI = ['.xlsx', '.xls', '.csv']

# ========================
# 🔧 OTOMASYON AYARLARI
# ========================
# Cron job veya Task Scheduler ile otomatikleştirme için:
# - Linux/Mac: crontab -e → "0 9 * * 1 /path/to/python /path/to/main.py" (Her pazartesi 09:00)
# - Windows: Task Scheduler ile haftalık tetikleyici ayarla
# - Bu durumda yukarıdaki get_last_monday() fonksiyonunu aktif et

AUTO_MODE = False  # True: Otomasyon modu, False: Manuel test modu
# ========================
MASTER_KLASORE_KOPYALA = True  # True: MasterKlasör'e de kopyala, False: sadece hedef klasörlere kaydet

try:
    print("⚙️ Config dosyası yüklendi:")
    print(f"📧 Gönderen: {SENDER_EMAIL}")
    print(f"📅 Tarih filtresi: {TARIH_FILTRESI}")
    print(f"📁 Masaüstü: {MASAUSTU_PATH}")
    print(f"🎯 {len(RAPOR_AYARLARI)} rapor türü tanımlı")
except UnicodeEncodeError:
    print("Config dosyasi yuklendi:")
    print(f"Gonderen: {SENDER_EMAIL}")
    print(f"Tarih filtresi: {TARIH_FILTRESI}")
    print(f"Masaustu: {MASAUSTU_PATH}")
    print(f"{len(RAPOR_AYARLARI)} rapor turu tanimli")