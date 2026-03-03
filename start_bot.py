import nest_asyncio
nest_asyncio.apply()
import subprocess
import os

# Esto fuerza a Rasa a correr ignorando el error de Loop
print("Iniciando KrisBot con parche de asincronía...")
os.system('rasa run --enable-api --cors "*" --port 5005')
