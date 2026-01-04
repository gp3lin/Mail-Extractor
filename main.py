# main.py  
# Ana ETL Extract scripti - Tüm süreci koordine eder:
# 1. Sistem ayarlarını kontrol eder
# 2. Microsoft Graph API'sine bağlanır
# 3. Belirli kriterlerdeki mesajları bulur
# 4. Excel dosyalarını indirir ve organize eder
# 5. Transform aşaması için hazırlar

from extract import test_authentication, create_folders, get_filtered_messages, process_excel_messages
from config import RAPOR_AYARLARI, SENDER_EMAIL, TARIH_FILTRESI
import sys

def print_banner():
    """🎨 Başlangıç banner'ını yazdırır"""
    print("=" * 60)
    print("🚀 ETL EXTRACT - EXCEL RAPOR İNDİRİCİ")
    print("=" * 60)
    print(f"📧 Gönderen: {SENDER_EMAIL}")
    print(f"📅 Tarih: {TARIH_FILTRESI[:10]} sonrası")
    print(f"📊 Rapor türleri: {len(RAPOR_AYARLARI)} adet")
    for rapor_id, ayar in RAPOR_AYARLARI.items():
        print(f"   • {ayar['mesaj_konusu']} → {ayar['klasor']}/{ayar['dosya_ismi']}.xlsx")
    print("=" * 60)

def main():
    """🎯 Ana süreç - ETL Extract Pipeline"""
    
    try:
        # Banner göster
        print_banner()
        
        # 1. Klasör hazırlığı
        print("\n1️⃣ KLASÖR HAZIRLIĞI")
        if not create_folders():
            print("❌ Klasör oluşturulamadı, işlem durduruluyor.")
            return False
        
        # 2. Authentication
        print("\n2️⃣ KİMLİK DOĞRULAMA")
        token = test_authentication()
        if not token:
            print("❌ Token alınamadı, işlem durduruluyor.")
            return False
        
        # 3. Mesaj filtreleme
        print("\n3️⃣ MESAJ FİLTRELEME")
        messages = get_filtered_messages(token)
        if not messages:
            print("❌ Uygun mesaj bulunamadı.")
            print("💡 Kontrol edilecekler:")
            print(f"   • Email adresi doğru mu? {SENDER_EMAIL}")
            print(f"   • Tarih doğru mu? {TARIH_FILTRESI[:10]} sonrası")
            print("   • Mesaj konularında anahtar kelimeler var mı?")
            print("   • Excel attachment'ları var mı?")
            print("📝 config.py'da 'mesaj_konusu' değerlerini gerçek email konularıyla karşılaştır")
            return False
        
        # 4. Excel dosyalarını işle
        print("\n4️⃣ EXCEL İŞLEME")
        success = process_excel_messages(token, messages)
        
        if success:
            print("\n🎉 ETL EXTRACT BAŞARIYLA TAMAMLANDI!")
            print("\n📋 SONUÇ ÖZETİ:")
            print(f"✅ {len(messages)} mesaj işlendi")
            print("📁 Dosyalar kaydedildi:")
            for rapor_id, ayar in RAPOR_AYARLARI.items():
                print(f"   • {ayar['klasor']}/{ayar['dosya_ismi']}.xlsx")
            print("\n🔄 Transform aşaması için hazır!")
            return True
        else:
            print("\n❌ Dosya indirme işlemi başarısız!")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️ İşlem kullanıcı tarafından durduruldu.")
        return False
    except Exception as e:
        print(f"\n💥 Beklenmeyen hata: {e}")
        print("🔧 Config dosyasını kontrol edin.")
        return False

def test_mode():
    """🧪 Test modu - sadece mesajları listeler, indirmez"""
    print("🧪 TEST MODU - Sadece mesajları kontrol ediyorum...")
    
    token = test_authentication()
    if token:
        messages = get_filtered_messages(token)
        if messages:
            print(f"\n✅ {len(messages)} uygun mesaj bulundu:")
            for i, msg in enumerate(messages, 1):
                print(f"{i}. {msg.get('subject')} - {msg.get('rapor_turu')}")
        else:
            print("❌ Test modunda mesaj bulunamadı.")

if __name__ == "__main__":
    print("🚀 ETL Extract başlatılıyor...\n")
    
    # Komut satırı argümanını kontrol et
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_mode()
    else:
        main()