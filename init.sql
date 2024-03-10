CREATE UNLOGGED TABLE clientes (
    id SERIAL PRIMARY KEY,
    limite INT NOT NULL,
    saldo_inicial INT NOT NULL DEFAULT 0,
    nome TEXT NOT NULL
);

CREATE INDEX idx_saldo_inicial ON clientes (saldo_inicial);

CREATE INDEX idx_limite ON clientes (limite);

CREATE UNLOGGED TABLE transacoes_cliente (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    transacao_tipo TEXT NOT NULL,
    realizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor INT NOT NULL,
    descricao TEXT NULL
);

CREATE INDEX idx_valor ON transacoes_cliente (valor);

CREATE INDEX idx_transacao_tipo ON transacoes_cliente (transacao_tipo);

CREATE INDEX idx_descricao ON transacoes_cliente (descricao);

CREATE INDEX idx_realizado_em ON transacoes_cliente (realizado_em);


DO $$
BEGIN
  INSERT INTO clientes (nome, limite)
  VALUES
    ('o barato sai caro', 1000 * 100),
    ('zan corp ltda', 800 * 100),
    ('les cruders', 10000 * 100),
    ('padaria joia de cocaia', 100000 * 100),
    ('kid mais', 5000 * 100);
END; $$;