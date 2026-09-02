from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Bibliotecas para o envio de e-mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database.config import get_db, UsuarioDB, HistoricoAnaliseDB, MetricaInfra
from auth.security import criptografar_senha, verificar_senha, criar_token_jwt
from ai_model.analyzer import analisar_sentimento
from models.schemas import UsuarioCreate, Token, TextoRequisicao, MetricaRequisicao

app = FastAPI(title="API com IA e Autenticação")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ==========================================
# CONFIGURAÇÕES DE ALERTA (EMAIL)
# ==========================================
MEU_EMAIL = os.getenv("MEU_EMAIL")
SENHA_DE_APP = os.getenv("SENHA_DE_APP")

def disparar_email(diagnostico, log_sistema):
    msg = MIMEMultipart()
    msg['From'] = MEU_EMAIL
    msg['To'] = MEU_EMAIL 
    msg['Subject'] = f"🚨 AIOps: Incidente detectado - {diagnostico}"

    corpo = f"Alerta de Infraestrutura!\n\nDiagnóstico: {diagnostico}\nLog: {log_sistema}"
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MEU_EMAIL, SENHA_DE_APP)
        server.send_message(msg)
        server.quit()
        print("📧 E-mail de alerta enviado!")
    except Exception as e:
        print(f"❌ Falha ao enviar e-mail: {e}")

# ==========================================
# ROTAS
# ==========================================

@app.post("/register", tags=["Usuários"])
def registrar(user: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existe = db.query(UsuarioDB).filter(UsuarioDB.username == user.username).first()
    if usuario_existe:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    novo_usuario = UsuarioDB(
        username=user.username,
        senha_criptografada=criptografar_senha(user.password)
    )
    db.add(novo_usuario)
    db.commit()
    return {"msg": "Usuário criado! Agora faça login."}

@app.post("/login", response_model=Token, tags=["Segurança"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.username == form_data.username).first()
    if not user or not verificar_senha(form_data.password, user.senha_criptografada):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    token = criar_token_jwt({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/analisar_texto", tags=["Inteligência Artificial"])
def usar_ia(requisicao: TextoRequisicao, background_tasks: BackgroundTasks, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 1. A IA analisa o texto
    resultado = analisar_sentimento(requisicao.texto)
    
    # 2. Salva o resultado no banco de dados
    novo_historico = HistoricoAnaliseDB(
        texto_analisado=requisicao.texto,
        diagnostico=resultado
    )
    db.add(novo_historico)
    db.commit()

    # 3. Dispara o e-mail se a IA detectar problemas (EM SEGUNDO PLANO)
    if "[ALERTA]" in resultado or "[CRÍTICO]" in resultado:
        background_tasks.add_task(disparar_email, resultado, requisicao.texto)
    
    return {
        "texto_enviado": requisicao.texto,
        "diagnostico_ia": resultado,
        "status": "Salvo no Banco e Alerta Processado"
    }

@app.post("/telemetria", tags=["Inteligência Artificial"])
def receber_telemetria(requisicao: MetricaRequisicao, background_tasks: BackgroundTasks, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 1. Monta o texto para a IA analisar (similar ao que o agente fazia)
    texto_log = f"Relatório: O uso da CPU está em {requisicao.cpu_percent}% e a Memória RAM em {requisicao.ram_percent}% na máquina {requisicao.machine_id}."
    resultado_ia = analisar_sentimento(texto_log)
    
    # 2. Salva a métrica estruturada no banco de dados (novo modelo)
    nova_metrica = MetricaInfra(
        machine_id=requisicao.machine_id,
        cpu_percent=requisicao.cpu_percent,
        ram_percent=requisicao.ram_percent,
        log_alerta=resultado_ia if "[ALERTA]" in resultado_ia or "[CRÍTICO]" in resultado_ia else None
    )
    db.add(nova_metrica)
    db.commit()

    # 3. Dispara e-mail se necessário (EM SEGUNDO PLANO)
    if "[ALERTA]" in resultado_ia or "[CRÍTICO]" in resultado_ia:
        background_tasks.add_task(disparar_email, resultado_ia, texto_log)
    
    return {
        "status": "Métrica recebida com sucesso",
        "machine_id": requisicao.machine_id,
        "diagnostico_ia": resultado_ia
    }
@app.post("/testar_email", tags=["Testes SRE"])
def testar_email_direto(background_tasks: BackgroundTasks):
    print("Iniciando teste forçado de e-mail...")
    try:
        # Chama a função de e-mail ignorando a IA (EM SEGUNDO PLANO)
        background_tasks.add_task(disparar_email, "[CRÍTICO] Teste Manual de Sistema", "Log de teste: Validando se o carteiro está acordado.")
        return {"msg": "Comando de envio acionado em segundo plano! Olhe o terminal do Uvicorn."}
    except Exception as e:
        return {"erro_critico": str(e)}