from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TextoRequisicao(BaseModel):
    texto: str


class HistoricoAnalise(BaseModel):
    texto_analisado: str
    diagnostico: str
    data_hora: str

class MetricaRequisicao(BaseModel):
    machine_id: str
    cpu_percent: float
    ram_percent: float