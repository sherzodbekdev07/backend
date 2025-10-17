from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

TOKEN = "8213291727:AAEKf-ayk9IKufQ9Nq9ZuotgQ89c3uP92qc"
CHAT_ID = "7757348190"

@app.route('/send-location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "JSON ma'lumot yo'q"}), 400

        first_name = data.get('firstName')
        last_name = data.get('lastName')
        lat = data.get('lat')
        lon = data.get('lon')

        if not (first_name and last_name and lat and lon):
            return jsonify({"error": "To'liq ma'lumot yuborilmadi"}), 400

        text = f"📍 {first_name} {last_name}\n🌐 Joylashuv: https://maps.google.com/?q={lat},{lon}"
        
        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}

        res = requests.post(telegram_url, json=payload, timeout=10)

        if not res.ok:
            return jsonify({
                "error": "Telegram API xatolik berdi",
                "status": res.status_code,
                "details": res.text
            }), 500

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Backend ishlayapti"

@app.route('/test', methods=['GET'])
def test():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        res = requests.get(url, timeout=5)
        
        return jsonify({
            "status": "ok" if res.ok else "failed",
            "code": res.status_code,
            "response": res.json() if res.ok else res.text
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)