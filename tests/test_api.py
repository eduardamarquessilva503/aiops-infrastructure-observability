from fastapi.testclient import TestClient
import sys
import os

# Adiciona o diretório raiz ao path para conseguir importar o main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_docs_respondem_200():
    """
    Testa se a página de documentação (Swagger UI) está online.
    """
    response = client.get("/docs")
    assert response.status_code == 200

def test_rota_testar_email():
    """
    Testa a rota de teste de e-mail (que não exige banco de dados).
    Garante que o retorno é o esperado.
    """
    response = client.post("/testar_email")
    assert response.status_code == 200
    assert "msg" in response.json()
    assert response.json()["msg"] == "Comando de envio acionado em segundo plano! Olhe o terminal do Uvicorn."
