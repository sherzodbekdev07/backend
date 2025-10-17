from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ To'g'ri usul
TOKEN = "7867472873:AAGKwgCnMIvqtZEP8inHidPNa9LqtRuy_H4"
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

        res = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text}
        )

        if not res.ok:
            print("Telegram javobi:", res.text)
            return jsonify({"error": "Telegram API bilan muammo.", "details": res.text}), 500

        return jsonify({"ok": True})

    except Exception as e:
        print("Server xatosi:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Backend ishlayapti ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)