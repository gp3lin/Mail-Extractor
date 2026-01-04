import msal
import os
from dotenv import load_dotenv

# .env dosyasından environment variables'ları yükle
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
if not CLIENT_ID:
    raise ValueError("❌ CLIENT_ID bulunamadı! .env dosyasını oluşturup CLIENT_ID değerini ekleyin.")

TENANT_ID = os.getenv("TENANT_ID", "consumers")
SCOPES = ["https://graph.microsoft.com/Mail.Read"]

def test_authentication():
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )

    print("[*] Tarayici acilacak, lutfen Microsoft hesabina giris yap.")

    result = app.acquire_token_interactive(scopes=SCOPES)

    if "access_token" in result:
        print("[+] Token alindi.")
        return result["access_token"]
    else:
        print("[-] Hata:", result.get("error_description"))
        return None

if __name__ == "__main__":
    test_authentication()
