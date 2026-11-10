CREATE TABLE IF NOT EXISTS perguntas (
    id TEXT PRIMARY KEY,
    era TEXT NOT NULL,
    dados_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_perguntas_era ON perguntas(era);
