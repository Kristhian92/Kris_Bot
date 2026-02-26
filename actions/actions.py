# import google.generativeai as genai
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# # Configura tu clave secreta de Gemini
# genai.configure(api_key="AIzaSyCXrvGlneH4u_5qCFugYOqW37XFgFomtqo")
# # Usamos el modelo más rápido y eficiente
# modelo = genai.GenerativeModel('gemini-2.5-flash')


# class ActionRespuestaGemini(Action):
#     def name(self) -> Text:
#         # Este es el nombre que Rasa usará para llamar a este script
#         return "action_respuesta_gemini"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # 1. Capturamos lo último que el usuario escribió
#         mensaje_usuario = tracker.latest_message.get('text')

#         # 2. Le damos un contexto a Gemini para que sepa quién es
#         # 2. Le damos un contexto y personalidad a Gemini
#         prompt = f"""
#         Eres un asistente virtual avanzado llamado KrisBot. 
#         Si el usuario te hace una pregunta técnica o compleja, respóndele de forma clara y estructurada.
#         Si el usuario te dice algo informal, jerga o una charla casual, respóndele de forma muy natural, amigable y breve.
#         Mensaje del usuario: {mensaje_usuario}
#         """
#         try:
#             # 3. Enviamos el mensaje a Gemini
#             respuesta = modelo.generate_content(prompt)
#             texto_ia = respuesta.text

#             # 4. Le devolvemos la respuesta al usuario en el chat de Rasa
#             dispatcher.utter_message(text=texto_ia)

#         except Exception as e:
#             dispatcher.utter_message(
#                 text=f"Lo siento, mis circuitos cuánticos fallaron: {str(e)}")

#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from groq import Groq

# Configuración de Groq
# Reemplaza con la clave que acabas de crear
client = Groq(
    api_key="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")


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
