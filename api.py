from flask import Flask, request, jsonify
import subprocess
import sys
import re
import os  # eksik olabilir, ekleyelim

app = Flask(__name__)

def extract_videoid(url):
    match = re.search(r'videoid=(\d+)', url)
    return match.group(1) if match else None

@app.route('/api/sibnet', methods=['GET'])
def get_video():
    url = request.args.get('url')
    if not url or "sibnet.ru" not in url:
        return jsonify({"error": "Geçersiz URL"}), 400

    videoid = extract_videoid(url)
    if not videoid:
        return jsonify({"error": "videoid bulunamadı"}), 400

    final_url = f"https://video.sibnet.ru/shell.php?videoid={videoid}"

    try:
        # test.py çalıştır
        result = subprocess.run(
            [sys.executable, "test.py", final_url],
            capture_output=True,
            text=True,
            timeout=40
        )
        output = result.stdout

        # Gerçek dv linkini çıkar
        match = re.search(r'https://dv\d+\.sibnet\.ru.+\.mp4\?st=[^&]+&e=\d+', output)
        if match:
            return jsonify({"video_url": match.group(0)})
        else:
            return jsonify({"error": "Video linki alınamadı", "output": output}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ ROOT ROUTE (test için)
@app.route('/')
def home():
    return "✅ API çalışıyor! Kullanım: /api/sibnet?url=..."

if __name__ == '__main__':
    # PORT ortam değişkenine göre ayarla
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
