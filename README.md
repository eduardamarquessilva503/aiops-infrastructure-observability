# 🚀 Projeto AIOps: Monitoramento Inteligente e Telemetria

Bem-vindo à documentação completa do projeto **AIOps (Inteligência Artificial para Operações de TI)**. Este material foi criado para te ajudar a estudar e entender a fundo cada peça dessa arquitetura.

---

## 🏛️ Arquitetura do Projeto

O projeto é dividido em quatro componentes principais que trabalham juntos para formar um ecossistema de observabilidade inteligente:

1. **Agente de Monitoramento (Python Edge)**
2. **API Backend (FastAPI)**
3. **Banco de Dados (PostgreSQL)**
4. **Visualização (Grafana)**

### Fluxo de Dados (Pipeline)
1. O `agente_monitor.py` roda na máquina cliente, captura os recursos (CPU e RAM) e envia um pacote JSON via requisição HTTP (POST) para a API.
2. O `main.py` (API) recebe a requisição.
3. A API envia os dados para a classe `analyzer.py`, que se comunica com a IA do Google (Gemini) pedindo um diagnóstico ("Tudo bem?" ou "[ALERTA]").
4. A API salva a telemetria e o diagnóstico no banco de dados **PostgreSQL**.
5. Se a IA responder com um `[ALERTA]`, a API dispara silenciosamente uma `BackgroundTask` que envia um e-mail via protocolo SMTP avisando a equipe de SRE.
6. O **Grafana** consome diretamente a tabela do PostgreSQL de segundo em segundo, atualizando seus gráficos dinamicamente para o usuário visualizar.

---

## 📂 Estrutura de Arquivos e Suas Responsabilidades

### 1. `agente_monitor.py` (O Coletor)
* **Objetivo:** Atuar como os "olhos" do sistema na máquina do cliente.
* **Bibliotecas chave:** `psutil` (para ler o hardware do PC), `requests` (para fazer o POST HTTP).
* **Funcionamento:** Fica em um loop infinito (`while True`) lendo os dados de segundo a segundo e disparando-os para a rota da API (configurada no arquivo `.env` como `URL_API`).

### 2. `main.py` (O Cérebro Roteador / API)
* **Objetivo:** Receber, processar e armazenar os dados.
* **Framework:** `FastAPI` (servidor assíncrono extremamente rápido em Python).
* **Destaques de Código:** 
  * Possui a rota `@app.post("/telemetria")` para onde o agente manda os dados.
  * Usa injenção de dependência (`BackgroundTasks`) para enviar e-mails de alerta sem travar a resposta do servidor (envio assíncrono).
  * Conecta com o SQLite e Postgres usando SQLAlchemy (ORM) para salvar registros.

### 3. `ai_model/analyzer.py` (A Inteligência)
* **Objetivo:** Avaliar criticamente os dados através de IA Generativa.
* **Funcionamento:** Recebe uma *string* montada (ex: "CPU a 90% e RAM a 80%") e usa a API Key do Google configurada no `.env` para pedir que o Gemini avalie se a máquina está em risco iminente, respondendo de forma padronizada.

### 4. `docker-compose.yml` (A Infraestrutura)
* **Objetivo:** Orquestrar e rodar todos os serviços isoladamente, porém na mesma rede.
* **Serviços (Containers):**
  * `api-aiops`: Constrói a imagem baseada no seu `Dockerfile`, executando a API na porta `8001`.
  * `db`: Levanta uma imagem limpa do PostgreSQL (versão 15) com as credenciais criadas para que os outros serviços possam gravar.
  * `grafana`: Levanta a interface web de observabilidade na porta `3001`.

### 5. `init.sql` (O Arquiteto de Dados)
* **Objetivo:** Preparar as fundações.
* **Funcionamento:** Assim que o container do Postgres liga pela primeira vez, este script é lido e executado automaticamente, criando a tabela `metricas_infra` (com as colunas de CPU, RAM, data/hora) para que ela já esteja pronta quando a API tentar gravar os primeiros dados.

### 6. `grafana/` (Configurações Visuais)
Aqui é onde aplicamos o conceito de *"Configuration as Code"* (Configuração como Código):
* `provisioning/datasources/datasource.yml`: Ensina o Grafana (assim que ele liga) a como encontrar o container do banco de dados, qual a senha e o usuário do Postgres, sem que você precise preencher manualmente pela interface web.
* `provisioning/dashboards/dashboard.yml`: Ensina ao Grafana a pasta onde deve procurar as telas (Dashboards).
* `dashboards/aiops_dashboard.json`: É a tela em si! Um documento gigante que diz as posições exatas dos gráficos (Painéis de CPU e RAM) e a consulta SQL que eles devem rodar (`SELECT ... FROM metricas_infra`).

---

## 🛠️ Tecnologias e Conceitos (Para Estudo)

* **SRE (Site Reliability Engineering):** Disciplina que incorpora aspectos de engenharia de software e os aplica a problemas de infraestrutura e operações. O projeto inteiro é um caso de uso prático disso.
* **REST API & JSON:** Paradigma usado na comunicação entre o Agente e o Backend.
* **SMTP (Simple Mail Transfer Protocol):** Usado nativamente pelo Python via `smtplib` para disparar os e-mails usando os servidores do Google.
* **Conteinerização (Docker):** Prática que empacotou o ambiente para rodar de forma isolada, prevenindo aquele clássico problema "na minha máquina funciona, na do servidor não".