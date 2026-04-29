import google.generativeai as genai

CHAVE_API ="AIzaSyDpn_PRcBHmPg7ooCvJ8Qbo5mCANATeLgo"

genai.configure(api_key=CHAVE_API)

def analisar_sentimento(texto: str) -> str:
    try:
        # Carregamos o modelo de IA
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # O "Prompt de Sistema": Aqui nós damos a profissão e as regras para a IA
        prompt = f"""
        Você é um Engenheiro de Infraestrutura (SRE) Sênior analisando mensagens e logs de um sistema.
        Leia o texto abaixo e classifique o status da infraestrutura em apenas UMA das três palavras:
        
        - [ESTÁVEL]: Se a mensagem indicar que tudo está funcionando bem ou rápido.
        - [ALERTA]: Se houver menção de lentidão, alto uso de CPU, ou comportamentos estranhos.
        - [CRÍTICO]: Se houver menção de erro, falha, queda de banco de dados ou indisponibilidade.
        
        Não explique. Apenas responda com a palavra entre colchetes.
        
        Texto a ser analisado: "{texto}"
        """
        
        # Enviamos a requisição para o Google
        resposta = model.generate_content(prompt)
        
        # Retornamos o texto gerado pela IA, tirando espaços em branco extras
        return resposta.text.strip()
    
    except Exception as e:
        return f"Erro crítico na comunicação com a IA: {e}"