import telebot
import requests

# 1. Conexión a Telegram
TOKEN = "8738068138:AAF6SVVp239yicOdJJG773Zs2lKFxgwB33U"
bot = telebot.TeleBot(TOKEN)

# 2. Conexión al cerebro de Rasa (REST API)
RASA_API = "http://127.0.0.1:5005/webhooks/rest/webhook"

@bot.message_handler(func=lambda message: True)
def enviar_a_rasa(message):
    user_id = str(message.chat.id)
    texto = message.text

    try:
        # Enviamos lo que dijiste a Rasa
        respuesta_rasa = requests.post(RASA_API, json={"sender": user_id, "message": texto})
        
        # Rasa nos devuelve la respuesta de la IA y la mandamos a tu celular
        if respuesta_rasa.status_code == 200:
            for resp in respuesta_rasa.json():
                if "text" in resp:
                    bot.send_message(user_id, resp["text"])
    except Exception as e:
        bot.send_message(user_id, "El servidor de IA está pensando... intenta de nuevo en unos segundos.")
        print(f"Error: {e}")

print("🤖 Puente de Telegram activado y blindado. Escuchando...")
bot.infinity_polling()
