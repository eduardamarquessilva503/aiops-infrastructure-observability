import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sre_user:sre_pass@db:5432/aiops")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    senha_criptografada = Column(String)

# --- ADICIONE ESTE NOVO BLOCO ABAIXO ---
class HistoricoAnaliseDB(Base):
    __tablename__ = "historicos_analise"
    id = Column(Integer, primary_key=True, index=True)
    texto_analisado = Column(String)
    diagnostico = Column(String)
    data_hora = Column(DateTime, default=datetime.utcnow)

class MetricaInfra(Base):
    __tablename__ = "metricas_infra"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String(100), index=True, nullable=False)
    cpu_percent = Column(Numeric(5, 2), nullable=False)
    ram_percent = Column(Numeric(5, 2), nullable=False)
    log_alerta = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()