from flask import Flask, request, jsonify
import subprocess
import sys
import re

app = Flask(__name__)

def extract_videoid(url):
    """Sibnet URL'sinden videoid çıkar"""
    match = re.search(r'videoid=(\d+)', url)
    return match.group(1) if match else None

def get_real_sibnet_link(videoid):
    """Playwright scriptini çalıştır ve gerçek MP4 linkini döndür"""
    try:
        # test.py'yi çalıştır: python test.py https://video.sibnet.ru/shell.php?videoid=123456
        result = subprocess.run(
            [sys.executable, "test.py", f"https://video.sibnet.ru/shell.php?videoid={videoid}"],
            capture_output=True,
            text=True,
            timeout=40
        )
        # Konsol çıktısından mp4 linkini al
        match = re.search(r'https://dv\d+\.sibnet\.ru.+\.mp4\?st=[^&]+&e=\d+', result.stdout)
        return match.group(0) if match else None
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/api/sibnet', methods=['GET'])
def api_sibnet():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL gerekli"}), 400

    videoid = extract_videoid(url)
    if not videoid:
        return jsonify({"error": "Geçersiz Sibnet URL"}), 400

    video_url = get_real_sibnet_link(videoid)
    if video_url:
        return jsonify({"video_url": video_url})
    else:
        return jsonify({"error": "Video linki alınamadı"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)