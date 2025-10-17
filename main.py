import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = os.getenv("7867472873:AAGKwgCnMIvqtZEP8inHidPNa9LqtRuy_H4")
CHAT_ID = os.getenv("7757348190")

@app.route('/send-location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        lat = data.get('lat')
        lon = data.get('lon')

        text = f"📍 Foydalanuvchi: {first_name} {last_name}\n🌍 Joylashuv: https://www.google.com/maps?q={lat},{lon}"

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}
        response = requests.post(telegram_url, json=payload)

        print("Telegram javobi:", response.text)
        return jsonify({"ok": True, "telegram_response": response.json()}), 200

    except Exception as e:
        print("Xato:", e)
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)