CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    limite NUMERIC(10, 2) NOT NULL,
    saldo_inicial NUMERIC(10, 2) NOT NULL DEFAULT 0,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transacoes (
    id SERIAL PRIMARY KEY,
    transacao TEXT NOT NULL,
    abreviation CHAR(1) NULL
);

CREATE TABLE IF NOT EXISTS transacoes_cliente (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    transacao_id INT REFERENCES transacoes(id),
    data_operacao TIMESTAMP DEFAULT now()
);


INSERT INTO transacoes (transacao, abreviation) VALUES ('Crédito', 'c');
INSERT INTO transacoes (transacao, abreviation) VALUES ('Débito',  'd');

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