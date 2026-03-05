import streamlit as st
import requests

# Configuración visual de la página
st.set_page_config(page_title="KrisBot IA", page_icon="🎓")
st.title("🤖 KrisBot - Asistente IA")
st.caption("Resolviendo Cualquier duda, en cualquier momento")

# Inicializar el historial de chat en la memoria
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar lo que escribe el usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Mostrar el mensaje del usuario en pantalla
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Enviar el mensaje a tu servidor Rasa mediante REST (Sin WebSockets)
    rasa_url = "https://krisbot-uis.duckdns.org/webhooks/rest/webhook"
    payload = {"sender": "usuario_streamlit", "message": prompt}

    try:
        response = requests.post(rasa_url, json=payload)

        # Procesar la respuesta de la IA
        if response.status_code == 200:
            rasa_responses = response.json()
            for r in rasa_responses:
                if "text" in r:
                    bot_text = r["text"]
                    with st.chat_message("assistant"):
                        st.markdown(bot_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": bot_text})
        else:
            st.error(f"Error del servidor: {response.status_code}")

    except Exception as e:
        st.error(f"No se pudo conectar con el servidor: {e}")
