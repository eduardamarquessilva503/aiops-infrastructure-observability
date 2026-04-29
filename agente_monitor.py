import psutil
import requests
import time
from datetime import datetime

# URL da nossa API de IA que criamos
URL_API = "http://127.0.0.1:8000/analisar_texto"

# Token de mentirinha só para passar pela segurança da API por enquanto
# (No mundo real, esse script faria o login primeiro)
TOKEN_TEMPORARIO = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc3NzQyMDE5M30.RmFHN7ANZV3KNUKwWy8KOOLp8gYLJyFfQW8XYeWJXSg"

def coletar_metricas_e_enviar():
    print("🤖 Iniciando Agente de Monitoramento SRE...")
    print("Pressione Ctrl+C para parar.\n")
    
    while True:
        try:
            # 1. Os "Olhos": Lendo os recursos do seu PC
            uso_cpu = psutil.cpu_percent(interval=1)
            uso_memoria = psutil.virtual_memory().percent
            hora_atual = datetime.now().strftime("%H:%M:%S")
            
            # 2. Montando o texto (o log) que será enviado para a IA
            log_texto = f"Relatório das {hora_atual}: O uso da CPU está em {uso_cpu}% e a Memória RAM em {uso_memoria}%."
            print(f"📡 Enviando log: {log_texto}")
            
            # 3. Enviando a requisição POST para a nossa API
            headers = {"Authorization": f"Bearer {TOKEN_TEMPORARIO}"}
            dados = {"texto": log_texto}
            
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
            
        # O agente dorme por 10 segundos antes de olhar de novo
        time.sleep  (600)

if __name__ == "__main__":
    coletar_metricas_e_enviar()