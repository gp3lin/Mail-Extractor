# Güvenlik Talimatları

## GitHub'a Pushlamadan Önce MUTLAKA Yapılması Gerekenler

### ✅ TAMAMLANDI: Proje Güvenli Hale Getirildi

Bu proje artık güvenli bir şekilde yapılandırılmıştır:

1. ✅ Tüm hassas bilgiler environment variables'a taşındı
2. ✅ `.env` dosyası `.gitignore`'a eklendi
3. ✅ `python-dotenv` paketi kuruldu ve requirements.txt'ye eklendi
4. ✅ `config.py` ve `test_mail.py` dosyaları güvenli hale getirildi

### 1. .env Dosyası

Proje çalışması için `.env` dosyası gereklidir. Bu dosya `.gitignore`'da olduğu için GitHub'a pushlanmayacaktır.

**Önemli:** `.env` dosyası asla GitHub'a pushlanmamalı! (Şu anda zaten .gitignore'da)

### 2. Kurulum

```bash
# Gerekli paketleri kur
pip install -r requirements.txt

# .env dosyasını kendi bilgilerinizle güncelleyin
# (Dosya şu anda mevcut bilgilerinizle oluşturulmuş durumda)
```

### 4. .gitignore Kontrolü

Aşağıdaki dosyaların `.gitignore`'da olduğundan emin olun:

```
.env
.env.local
config_local.py
mail_extractor_venv/
__pycache__/
*.pyc
```

### 5. Hassas Bilgileri Temizle

Eğer daha önce config.py'yi commit ettiyseniz:

```bash
# Git geçmişinden dosyayı temizle
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config.py" \
  --prune-empty --tag-name-filter cat -- --all
```

## .env Dosyası Örneği

```env
CLIENT_ID=your_client_id_here
TENANT_ID=consumers
SENDER_EMAIL=sender@example.com
MASAUSTU_PATH=C:\Users\YourUsername\Desktop
MANUAL_DATE=2025-08-13
```

**Not:** Yukarıdaki değerleri kendi gerçek değerlerinizle değiştirin!

## GitHub'a Push Öncesi Kontrol Listesi

- [ ] `.env` dosyası oluşturuldu
- [ ] `.gitignore` dosyası var ve doğru yapılandırıldı
- [ ] `config_secure.py` kullanılıyor veya `config.py` .gitignore'da
- [ ] `python-dotenv` kurulu
- [ ] Virtual environment klasörü .gitignore'da
- [ ] Hassas bilgiler koddan temizlendi

## Güvenlik Uyarısı

Aşağıdaki bilgiler ASLA GitHub'a pushlanmamalı:

- CLIENT_ID
- TENANT_ID (genellikle güvenli ama yine de env'de tutmak iyi)
- Email adresleri
- Kişisel dosya yolları
- Access token'lar
- Şifreler

## Kullanım

Güvenli config kullanırken:

```python
# main.py veya extract.py'de import değişikliği YAPMAYA GEREK YOK
# config.py'yi config_secure.py ile değiştirdiğinizde otomatik çalışır
from config import *
```
