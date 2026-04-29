# 1. Baixa uma imagem leve do Linux com Python 3.10
FROM python:3.10-slim

# 2. Define a pasta onde o projeto vai morar dentro do Docker
WORKDIR /app

# 3. Copia o arquivo de dependências primeiro (para ser mais rápido)
COPY requirements.txt .

# 4. Instala todas as bibliotecas necessárias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o resto do seu código para dentro do container
COPY . .

# 6. Avisa que a API vai rodar na porta 8000
EXPOSE 8000

# 7. Comando para ligar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]