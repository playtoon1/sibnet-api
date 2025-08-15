import sys
from playwright.sync_api import sync_playwright

def get_sibnet_video(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--disable-plugins-discovery',
                '--window-position=800,100',
                '--window-size=1024,768',
                '--lang=ru-RU,ru'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1024, 'height': 768},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
            extra_http_headers={
                'Referer': 'https://video.sibnet.ru/',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
            }
        )
        page = context.new_page()

        # Bot tespitini engelle
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru'] });
        """)

        video_url = None

        # ⚠️ Sadece dv alt domaininden gelen gerçek mp4'leri yakala
        def handle_response(response):
            nonlocal video_url
            if response.url.startswith("https://dv") and "sibnet.ru" in response.url and ".mp4" in response.url:
                print(f"🎯✅ GERÇEK MP4 BULUNDU: {response.url}")
                if video_url is None:
                    video_url = response.url

        page.on("response", handle_response)

        try:
            print("🌐 Sayfa yükleniyor... Bekleyin.")
            page.goto(url, wait_until="networkidle", timeout=30000)

            print("▶️ 'Play' butonu aranıyor ve tıklanıyor...")
            page.wait_for_selector("button[title='Play'], .play-button, #play-btn, .video-play", timeout=10000)
            page.click("button[title='Play'], .play-button, #play-btn, .video-play")

            print("⏳ Gerçek video yükleniyor... 20 saniye bekleniyor (dv linki için)")
            page.wait_for_timeout(20000)  # dv linki gelmesi için daha uzun bekle

        except Exception as e:
            print(f"❌ Hata: {e}")

        browser.close()
        return video_url

# === ANA KOD ===
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python test.py <sibnet_url>")
        print("Örnek: python test.py https://video.sibnet.ru/shell.php?videoid=4702979")
        sys.exit(1)

    url = sys.argv[1]
    result = get_sibnet_video(url)

    if result:
        print("\n\n🎥✅ BAŞARILI! GERÇEK VE GEÇERLİ MP4 LİNKİ:")
        print(result)
        print("\nBu linki kopyala ve mobil uygulamada kullanabilirsin.")
        print("Not: Bu link yaklaşık 24 saat geçerlidir.")
    else:
        print("\n\n❌ Maalesef, gerçek dv linki alınamadı.")
        print("Tarayıcıda video oynadı mı? Gerçekten oynadıysa, bana söyle, başka yol deneriz.")