import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# 🔒 Muhit o'zgaruvchilaridan o'qiladi (Railway Variables)
TOKEN = os.getenv("7867472873:AAGKwgCnMIvqtZEP8inHidPNa9LqtRuy_H4")
CHAT_ID = os.getenv("7757348190")

@app.route('/')
def home():
    return "✅ Geo-Location to Telegram Backend ishlayapti!"

@app.route('/send-location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        lat = data.get('lat')
        lon = data.get('lon')

        if not all([name, surname, lat, lon]):
            return jsonify({"ok": False, "error": "Yetarli ma'lumot kelmadi."}), 400

        # 🧭 Telegramga yuboriladigan matn
        message = (
            f"📍 Yangi foydalanuvchi joylashuvi:\n\n"
            f"👤 Ism: {name}\n"
            f"👤 Familiya: {surname}\n"
            f"🌐 Koordinatalar: {lat}, {lon}\n"
            f"🗺 Xarita: https://maps.google.com/?q={lat},{lon}"
        )

        # ✉️ Telegram API orqali yuborish
        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        response = requests.post(telegram_url, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        })

        if response.status_code == 200:
            return jsonify({"ok": True, "message": "Joylashuv yuborildi!"})
        else:
            return jsonify({"ok": False, "error": "Telegram API bilan muammo."}), 500

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == '__main__':
    # Railway avtomatik PORT beradi
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
