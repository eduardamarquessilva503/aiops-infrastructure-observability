import psutil
import requests
import time
import os
import socket
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# URL da nossa API de IA
URL_API = os.getenv("URL_API", "http://127.0.0.1:8001/telemetria")
TOKEN_TEMPORARIO = os.getenv("TOKEN_TEMPORARIO")

def coletar_metricas_e_enviar():
    print("🤖 Iniciando Agente de Monitoramento SRE...")
    print("Pressione Ctrl+C para parar.\n")
    
    # Extrair hostname (Edge configuration)
    machine_id = socket.gethostname()
    
    while True:
        try:
            # 1. Os "Olhos": Lendo os recursos do seu PC
            uso_cpu = psutil.cpu_percent(interval=1)
            uso_memoria = psutil.virtual_memory().percent
            hora_atual = datetime.now().strftime("%H:%M:%S")
            
            # 2. Montando o payload JSON estruturado
            dados = {
                "machine_id": machine_id,
                "cpu_percent": uso_cpu,
                "ram_percent": uso_memoria
            }
            print(f"📡 Enviando telemetria: {dados}")
            
            # 3. Enviando a requisição POST para a nossa API
            headers = {"Authorization": f"Bearer {TOKEN_TEMPORARIO}"}
            
            resposta = requests.post(URL_API, json=dados, headers=headers)
            
            # 4. Lendo o que a IA respondeu
            if resposta.status_code == 200:
                diagnostico = resposta.json().get('diagnostico_ia')
                print(f"🧠 Diagnóstico da IA: {diagnostico}")
                print("-" * 50)
            else:
                print(f"❌ Erro na API: {resposta.status_code} - {resposta.text}")
                
        except Exception as e:
            print(f"Erro no agente: {e}")
            
        # O agente dorme por 1 segundo antes de olhar de novo
        time.sleep(1)

if __name__ == "__main__":
    coletar_metricas_e_enviar()
