# Graph API Email Extractor

Microsoft Graph API kullanarak belirli kriterlerdeki email mesajlarından Excel dosyalarını otomatik olarak indiren ETL (Extract, Transform, Load) sistemi.

## Proje Amacı

Bu proje, düzenli olarak email yoluyla gelen raporları (Excel dosyaları) otomatik olarak indirip organize etmek için geliştirilmiştir. Özellikle:

- Belirli bir gönderenden gelen mesajları filtreler
- Belirli tarih aralığındaki mesajları kontrol eder
- Mesaj konularına göre rapor türlerini ayırt eder
- Excel dosyalarını otomatik olarak indirir ve yeniden adlandırır
- Dosyaları belirlenen klasörlere organize eder

## Özellikler

- Microsoft Graph API entegrasyonu
- Otomatik kimlik doğrulama (OAuth 2.0)
- Esnek tarih filtreleme (manuel veya otomatik)
- Çoklu rapor türü desteği
- Otomatik klasör organizasyonu
- Master klasör yedekleme özelliği
- Detaylı log ve hata yönetimi
- Güvenli credential yönetimi (.env dosyası)

## Gereksinimler

- Python 3.7+
- Microsoft hesabı (Outlook/Hotmail veya kişisel Microsoft hesabı)
- Azure AD'de kayıtlı bir uygulama (Client ID)

## Kurulum

### 1. Projeyi İndirin

```bash
git clone https://github.com/gp3lin/graph-api-extractor.git
cd graph-api-extractor
```

### 2. Virtual Environment Oluşturun

```bash
# Windows
python -m venv mail_extractor_venv
mail_extractor_venv\Scripts\activate

# macOS/Linux
python3 -m venv mail_extractor_venv
source mail_extractor_venv/bin/activate
```

### 3. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Azure AD Uygulaması Oluşturun

1. [Azure Portal](https://portal.azure.com/) > Azure Active Directory > App registrations
2. "New registration" butonuna tıklayın
3. Uygulama adını girin (örn: "Mail Extractor")
4. Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
5. Redirect URI: Public client/native (mobile & desktop) - `http://localhost`
6. "Register" butonuna tıklayın
7. Overview sayfasından **Application (client) ID**'yi kopyalayın

### 5. .env Dosyası Oluşturun

```bash
# .env.example dosyasını kopyalayın
cp .env.example .env

# .env dosyasını düzenleyin
```

`.env` dosyasını açıp aşağıdaki değerleri kendi bilgilerinizle doldurun:

```env
CLIENT_ID=your_azure_client_id_here
TENANT_ID=consumers
SENDER_EMAIL=rapor_gonderen@email.com
MASAUSTU_PATH=C:\Users\YourUsername\Desktop
MANUAL_DATE=2025-01-04
```

### 6. Rapor Ayarlarını Yapılandırın

`config.py` dosyasındaki `RAPOR_AYARLARI` bölümünü düzenleyin:

```python
RAPOR_AYARLARI = {
    "RAPOR1": {
        "mesaj_konusu": "Haftalık Satış",     # Email konusunda aranacak kelime
        "rapor_adi": "Satış Raporu",          # Açıklama
        "klasor": "Satış",                    # Hedef klasör
        "dosya_ismi": "haftalik_satis"        # Kaydedilecek dosya ismi
    },
    "RAPOR2": {
        "mesaj_konusu": "Envanter Raporu",
        "rapor_adi": "Envanter",
        "klasor": "Envanter",
        "dosya_ismi": "envanter_listesi"
    }
}
```

## Kullanım

### Test Modu

Önce test modunda çalıştırarak mesajların doğru filtrelendiğini kontrol edin:

```bash
python main.py test
```

### Normal Kullanım

```bash
python main.py
```

### Kimlik Doğrulama Testi

Sadece Microsoft Graph API bağlantısını test etmek için:

```bash
python test_mail.py
```

## Yapılandırma

### Tarih Filtreleme

`config.py` dosyasında tarih filtreleme modunu değiştirebilirsiniz:

**Manuel Tarih (Varsayılan):**
```python
MANUAL_DATE = "2025-01-04"  # Bu tarihten sonraki mesajlar
```

**Otomatik Pazartesi Modu:**
```python
# Yorumları kaldırarak aktif edin
TARIH_FILTRESI = get_last_monday()
```

### Master Klasör

Tüm dosyaların bir kopyasını master klasörde saklamak için:

```python
MASTER_KLASORE_KOPYALA = True  # config.py içinde
```

## Güvenlik

### Önemli Uyarılar

- `.env` dosyası asla GitHub'a pushlanmamalı (zaten `.gitignore`'da)
- `CLIENT_ID` ve diğer hassas bilgiler sadece `.env` dosyasında olmalı
- Üretim ortamında ek güvenlik önlemleri alın
- Access token'lar geçici olup, her oturumda yenilenir

### Güvenli Kullanım

Detaylı güvenlik talimatları için [README_SECURITY.md](README_SECURITY.md) dosyasına bakın.

## Otomasyon

Düzenli çalıştırma için:

**Windows Task Scheduler:**
1. Task Scheduler'ı açın
2. "Create Basic Task" seçin
3. Trigger: Weekly, Monday, 09:00
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `C:\path\to\main.py`
7. Start in: `C:\path\to\project`

**Linux/macOS crontab:**
```bash
# Her pazartesi 09:00'da çalıştır
0 9 * * 1 /path/to/venv/bin/python /path/to/main.py
```

## Proje Yapısı

```
graph-api-extractor/
├── .env.example          # Environment variables şablonu
├── .gitignore           # Git ignore kuralları
├── config.py            # Ana konfigürasyon dosyası
├── extract.py           # ETL Extract fonksiyonları
├── main.py              # Ana uygulama
├── test_mail.py         # Bağlantı test scripti
├── requirements.txt     # Python bağımlılıkları
├── README.md           # Bu dosya
└── README_SECURITY.md  # Güvenlik dokümantasyonu
```

## Sorun Giderme

### "CLIENT_ID bulunamadı" Hatası

`.env` dosyasının proje kök dizininde olduğundan ve `CLIENT_ID` değerinin doğru girildiğinden emin olun.

### "Token alınamadı" Hatası

1. Azure AD uygulamanızın doğru yapılandırıldığından emin olun
2. Redirect URI'nin `http://localhost` olarak ayarlandığını kontrol edin
3. İnternet bağlantınızı kontrol edin

### "Uygun mesaj bulunamadı" Hatası

1. `SENDER_EMAIL` değerinin doğru olduğunu kontrol edin
2. `MANUAL_DATE` değerinin mesaj tarihlerini kapsadığından emin olun
3. `config.py`'deki `mesaj_konusu` değerlerinin gerçek email konularıyla eşleştiğini kontrol edin

### Unicode Encoding Hatası

Windows'ta emoji'ler sorun çıkarıyorsa:
```bash
set PYTHONIOENCODING=utf-8
python main.py
```

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

## Teşekkürler

- Microsoft Graph API
- MSAL (Microsoft Authentication Library)
- Python Community
