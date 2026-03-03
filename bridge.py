from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8738068138:AAF6SVVp239yicOdJJG773Zs2lKFxgwB33U"
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"].get("text", "")

        # Enviar a Rasa
        response = requests.post(RASA_URL, json={"sender": str(chat_id), "message": user_msg})
        rasa_answers = response.json()

        # Enviar respuestas de Rasa a Telegram
        for ans in rasa_answers:
            if "text" in ans:
                payload = {"chat_id": chat_id, "text": ans["text"]}
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)

    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
