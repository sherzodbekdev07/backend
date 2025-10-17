from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Token va chat id - productionda ENV ga qo'ying
TOKEN = os.environ.get('7867472873:AAGKwgCnMIvqtZEP8inHidPNa9LqtRuy_H4')
CHAT_ID = os.environ.get('7757348190')

@app.route('/send-location', methods=['POST'])
def send_location():
    data = request.get_json(force=True)

    first = data.get('firstName', '').strip()
    last  = data.get('lastName', '').strip()
    lat   = data.get('lat')
    lon   = data.get('lon')
    acc   = data.get('accuracy')
    ts    = data.get('timestamp')

    # oddiy validatsiya
    if not first or not last or lat is None or lon is None:
        return jsonify({"ok": False, "error": "Missing required fields"}), 400

    # Telegramga yuboriladigan xabar (text)
    message_text = (
        f"📥 Yangi kirish:\n"
        f"Ism: {first} {last}\n"
        f"Vaqt: {ts or '—'}\n"
        f"Koordinatalar: {lat}, {lon}\n"
        f"Aniqlik: {acc if acc is not None else '—'} m"
    )

    # 1) send message (text)
    send_message_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    msg_payload = {
        "chat_id": CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(send_message_url, json=msg_payload, timeout=8)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

    # 2) send location so map pin chiqadi
    send_loc_url = f"https://api.telegram.org/bot{TOKEN}/sendLocation"
    loc_payload = {
        "chat_id": CHAT_ID,
        "latitude": lat,
        "longitude": lon
    }
    try:
        requests.post(send_loc_url, json=loc_payload, timeout=8)
    except Exception:
        pass  # location yuborilmasa ham xabar jo'natildi

    return jsonify({"ok": True, "message": "Sent to telegram"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
