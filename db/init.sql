CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    limite INT NOT NULL,
    saldo_inicial INT NOT NULL DEFAULT 0,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transacoes (
    id INT NOT NULL PRIMARY KEY,
    transacao TEXT NOT NULL,
    abreviation CHAR(1) NULL
);

CREATE TABLE IF NOT EXISTS transacoes_cliente (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    transacao_id INT REFERENCES transacoes(id),
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor INT NOT NULL,
    descricao TEXT NULL
);


INSERT INTO transacoes (id, transacao, abreviation) VALUES (1, 'Crédito', 'c');
INSERT INTO transacoes (id, transacao, abreviation) VALUES (2, 'Débito',  'd');

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