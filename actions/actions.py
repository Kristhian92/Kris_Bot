from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from groq import Groq

# Configuración de Groq
# Reemplaza con la clave que acabas de crear
client = Groq(
    api_key="SECRET_KEY")


class ActionRespuestaGemini(Action):
    def name(self) -> Text:
        return "action_respuesta_gemini"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mensaje_usuario = tracker.latest_message.get('text')

        prompt = f"""
        Eres un asistente virtual avanzado llamado KrisBot. 
        Si el usuario te hace una pregunta técnica o compleja, respóndele de forma clara y estructurada.
        Si el usuario te dice algo informal, jerga o una charla casual, respóndele de forma muy natural, amigable y breve.
        Mensaje del usuario: {mensaje_usuario}
        """

        try:
            # Llamada a Groq (Usando Llama 3.3 de 70 billones de parámetros)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=512
            )

            texto_ia = completion.choices[0].message.content
            dispatcher.utter_message(text=texto_ia)

        except Exception as e:
            dispatcher.utter_message(
                text=f"Lo siento, mis circuitos fallaron: {str(e)}")

        return []
