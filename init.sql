CREATE TABLE IF NOT EXISTS metricas_infra (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(100) NOT NULL,
    cpu_percent NUMERIC(5,2) NOT NULL,
    ram_percent NUMERIC(5,2) NOT NULL,
    log_alerta TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar um índice na coluna de tempo e no machine_id para acelerar as consultas do Grafana
CREATE INDEX idx_metricas_time ON metricas_infra (timestamp);
CREATE INDEX idx_metricas_machine ON metricas_infra (machine_id);
