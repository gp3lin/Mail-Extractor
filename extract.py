# extract.py
# Bu script Microsoft Graph API'si kullanarak:
# 1. Microsoft hesabına giriş yapar
# 2. Belirli tarihten sonraki mesajları filtreler
# 3. Belirli kişiden gelen mesajları bulur
# 4. Excel dosyalarını tespit eder ve indirir
# 5. Rapor türüne göre doğru klasörlere kaydeder

import msal
import requests
import json
import os
from datetime import datetime
from config import *

def test_authentication():
    """
    🔐 Microsoft Graph API için token alır
    Tarayıcıda Microsoft hesap girişi yapar
    """
    print("🔐 Microsoft hesabına giriş yapılıyor...")
    
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )
    
    result = app.acquire_token_interactive(scopes=SCOPES)
    
    if "access_token" in result:
        print("✅ Token başarıyla alındı.")
        print(f"🕒 Token süresi: {result.get('expires_in', 0)} saniye")
        return result["access_token"]
    else:
        print("❌ Token alınamadı:", result.get("error_description"))
        return None

def create_folders():
    """
    📁 Gerekli klasörleri masaüstünde oluşturur
    """
    print("📁 Klasörler kontrol ediliyor...")
    
    created_folders = []
    
    # Her rapor için klasör oluştur
    for rapor_id, klasor_path in KLASOR_YOLLARI.items():
        if not os.path.exists(klasor_path):
            os.makedirs(klasor_path)
            created_folders.append(RAPOR_AYARLARI[rapor_id]["klasor"])
            print(f"✅ Klasör oluşturuldu: {RAPOR_AYARLARI[rapor_id]['klasor']}")
    
    # Master klasör oluştur (isteğe bağlı)
    if MASTER_KLASORE_KOPYALA and not os.path.exists(MASTER_KLASOR_PATH):
        os.makedirs(MASTER_KLASOR_PATH)
        created_folders.append(MASTER_KLASOR)
        print(f"✅ Master klasör oluşturuldu: {MASTER_KLASOR}")
    
    if not created_folders:
        print("📁 Tüm klasörler zaten mevcut.")
    
    return True

def get_filtered_messages(access_token):
    """
    📧 Filtrelenmiş mesajları getirir:
    - Belirli kişiden gelen
    - Belirli tarihten sonraki
    - Excel attachment içeren
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    # API URL'sini oluştur - attachment'larla birlikte
    base_url = 'https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages'
    
    # Filtreler
    filters = []
    filters.append(f"from/emailAddress/address eq '{SENDER_EMAIL}'")
    filters.append(f"receivedDateTime ge {TARIH_FILTRESI}")
    
    params = [
        f'$top={MAX_RESULTS}',
        '$expand=attachments',
        f"$filter={' and '.join(filters)}"
    ]
    
    url = base_url + '?' + '&'.join(params)
    
    print(f"📡 API çağrısı yapılıyor...")
    print(f"🔍 Filtreler: {SENDER_EMAIL} + {TARIH_FILTRESI[:10]} sonrası")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📊 API Durumu: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get('value', [])
            print(f"📧 Toplam {len(messages)} mesaj bulundu")
            
            # Excel içeren mesajları filtrele
            excel_messages = []
            
            for msg in messages:
                subject = msg.get('subject', '')
                attachments = msg.get('attachments', [])
                
                # Excel dosyalarını bul
                excel_attachments = []
                for att in attachments:
                    name = att.get('name', '').lower()
                    if any(name.endswith(ext) for ext in EXCEL_UZANTILARI):
                        excel_attachments.append(att)
                
                # Rapor türünü belirle (mesaj konusuna göre)
                rapor_turu = None
                matched_keyword = None
                
                for rapor_id, ayar in RAPOR_AYARLARI.items():
                    mesaj_konusu = ayar["mesaj_konusu"]
                    if mesaj_konusu.lower() in subject.lower():
                        rapor_turu = rapor_id
                        matched_keyword = mesaj_konusu
                        break
                
                if excel_attachments and rapor_turu:
                    msg['excel_attachments'] = excel_attachments
                    msg['rapor_turu'] = rapor_turu
                    excel_messages.append(msg)
                    rapor_adi = RAPOR_AYARLARI[rapor_turu]["rapor_adi"]
                    print(f"🎯 {rapor_adi}: '{subject}' - {len(excel_attachments)} Excel dosyası")
                    print(f"   └─ Eşleşen anahtar: '{matched_keyword}'")
                elif excel_attachments:
                    # Excel var ama rapor türü eşleşmiyor
                    print(f"⚠️ Excel var ama tür belirsiz: '{subject}' - {len(excel_attachments)} dosya")
                    print("   └─ Kontrol: Mesaj konusu config.py'daki anahtar kelimelerle eşleşiyor mu?")
                    
            print(f"\n📊 Mesaj analizi:")
            print(f"   • Toplam mesaj: {len(messages)}")
            print(f"   • Excel içeren: {sum(1 for msg in messages if msg.get('attachments'))}")
            print(f"   • İşlenecek: {len(excel_messages)}")
            
            if len(excel_messages) == 0 and len(messages) > 0:
                print(f"\n🔍 Bulunan mesaj konuları:")
                for i, msg in enumerate(messages[:3], 1):
                    print(f"   {i}. '{msg.get('subject', 'Konu yok')}'")
                print("\n💡 Bu konulardan hiçbiri config.py'daki anahtar kelimelerle eşleşmiyor.")
                print("💡 config.py'da 'mesaj_konusu' değerlerini kontrol et.")
            
            print(f"📈 İşlenecek mesaj sayısı: {len(excel_messages)}")
            return excel_messages
            
        else:
            print(f"❌ API hatası: {response.status_code}")
            print(f"❌ Detay: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return None

def download_excel_file(access_token, message_id, attachment_id, save_path):
    """
    💾 Excel dosyasını indirir ve belirtilen yola kaydeder
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    # Attachment indirme URL'si
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}/$value'
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return True
        else:
            print(f"❌ Dosya indirilemedi: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ İndirme hatası: {e}")
        return False

def process_excel_messages(access_token, messages):
    """
    🏭 Excel mesajlarını işler:
    - Her mesajdaki Excel dosyalarını indirir
    - Doğru klasörlere doğru isimlerle kaydeder
    - Master klasöre de kopyalar (isteğe bağlı)
    """
    if not messages:
        print("❌ İşlenecek mesaj bulunamadı.")
        return False
    
    print(f"\n🏭 {len(messages)} mesaj işleniyor...")
    
    basarili_indirmeler = 0
    toplam_dosya = 0
    
    for msg in messages:
        subject = msg.get('subject', 'Konu yok')
        message_id = msg.get('id')
        rapor_turu = msg.get('rapor_turu')
        excel_attachments = msg.get('excel_attachments', [])
        
        print(f"\n📧 İşleniyor: '{subject}'")
        print(f"🎯 Rapor türü: {rapor_turu}")
        
        for att in excel_attachments:
            toplam_dosya += 1
            att_id = att.get('id')
            original_name = att.get('name', f'dosya_{toplam_dosya}.xlsx')
            
            # Yeni dosya ismini belirle
            rapor_ayar = RAPOR_AYARLARI[rapor_turu]
            file_extension = os.path.splitext(original_name)[1]
            new_filename = f"{rapor_ayar['dosya_ismi']}{file_extension}"
            
            # Hedef klasör yolu
            target_folder = KLASOR_YOLLARI[rapor_turu]
            target_path = os.path.join(target_folder, new_filename)
            
            print(f"💾 İndiriliyor: {original_name} → {new_filename}")
            
            # Dosyayı indir
            if download_excel_file(access_token, message_id, att_id, target_path):
                print(f"✅ Kaydedildi: {rapor_ayar['klasor']}/{new_filename}")
                basarili_indirmeler += 1
                
                # Master klasöre de kopyala
                if MASTER_KLASORE_KOPYALA:
                    master_path = os.path.join(MASTER_KLASOR_PATH, f"{rapor_ayar['dosya_ismi']}_{datetime.now().strftime('%Y%m%d')}{file_extension}")
                    try:
                        import shutil
                        shutil.copy2(target_path, master_path)
                        print(f"📋 Master'a kopyalandı: {os.path.basename(master_path)}")
                    except Exception as e:
                        print(f"⚠️ Master kopyalama hatası: {e}")
            else:
                print(f"❌ İndirilemedi: {original_name}")
    
    print(f"\n🎉 İşlem tamamlandı!")
    print(f"✅ Başarılı: {basarili_indirmeler}/{toplam_dosya} dosya")
    return basarili_indirmeler > 0