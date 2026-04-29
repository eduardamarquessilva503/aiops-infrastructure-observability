# 🛡️ AIOps Sentinel: API de Monitoramento Inteligente

![AIOps Sentinel Banner](./aiops_banner_1777424801716.png)

## 🚀 Sobre o Projeto

O **AIOps Sentinel** é uma solução avançada de monitoramento de infraestrutura baseada em Inteligência Artificial. Utilizando o framework **FastAPI**, o sistema coleta métricas de desempenho em tempo real e utiliza modelos de IA (Google Gemini) para diagnosticar anomalias e prever incidentes antes que eles afetem a operação.

Este projeto foi desenvolvido com foco em **SRE (Site Reliability Engineering)**, garantindo que logs e métricas de hardware sejam analisados com precisão cirúrgica.

---

## ✨ Principais Funcionalidades

- 🧠 **Diagnóstico Inteligente**: Análise de logs e métricas via IA para identificar estados críticos.
- 📉 **Monitoramento de Hardware**: Agente integrado que monitora CPU e RAM continuamente.
- 🚨 **Alertas em Tempo Real**: Disparo automático de e-mails para a equipe de SRE ao detectar incidentes.
- 🔐 **Segurança Robusta**: Autenticação via JWT (JSON Web Tokens) e criptografia de senhas com bcrypt.
- 🐳 **Pronto para Docker**: Configuração completa com Docker e Docker Compose para implantação rápida.
- 📂 **Histórico de Análises**: Armazenamento persistente de todos os diagnósticos realizados pela IA.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.x
- **Framework Web**: FastAPI (Uvicorn)
- **Inteligência Artificial**: Google Generative AI (Gemini Pro)
- **Banco de Dados**: SQLAlchemy (SQLite)
- **Segurança**: JWT, Passlib, Bcrypt
- **Monitoramento**: Psutil
- **Infraestrutura**: Docker & Docker Compose

## 📂 Estrutura do Projeto

```text
├── api_ia_profissional/
│   ├── ai_model/         # Módulo de integração com IA
│   ├── auth/             # Regras de segurança e JWT
│   ├── database/         # Configurações do banco SQLite
│   ├── models/           # Schemas de validação de dados
│   ├── main.py           # Ponto de entrada da API
│   ├── Dockerfile        # Receita de construção do container
│   └── requirements.txt  # Dependências do sistema
├── docker-compose.yml    # Orquestração do ambiente
├── agente_monitor.py     # Script de coleta (roda no host)
└── .gitignore            # Proteção de arquivos sensíveis



## ⚙️ Como Executar

### 1. Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/api_ia_profissional.git
cd api_ia_profissional
```

### 2. Configurar o Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
Crie um arquivo `.env` ou edite as configurações no `main.py` com suas credenciais de e-mail e chave da API do Google Gemini.

### 4. Rodar a API
```bash
uvicorn main:app --reload
```

### 5. Rodar o Agente de Monitoramento
Em outro terminal:
```bash
python agente_monitor.py
```

---

## 🐳 Docker (Opcional)

Para rodar o projeto em containers:
```bash
docker-compose up --build
```

---

<p align="center"> Desenvolvido por Maria Eduarda Marques </p>
