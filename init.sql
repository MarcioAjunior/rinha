CREATE DATABASE IF NOT EXISTS rinha_banco;

CREATE TABLE IF NOT EXISTS lb_clientes (
    id SERIAL PRIMARY KEY,
    limite NUMERIC(10, 2) NOT NULL,
    saldo_inicial NUMERIC(10, 2) NOT NULL DEFAULT 0,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lb_transacoes (
    id SERIAL PRIMARY KEY,
    transacao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lb_transacoes_cliente (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES lb_clientes(id),
    transacao_id INT REFERENCES lb_transacoes(id),
    data_operacao TIMESTAMP DEFAULT now()
);


INSERT INTO lb_clientes (id, limite, saldo_inicial, nome) VALUES
(1, 100000.00, 0, 'João da Silva'),
(2, 80000.00, 0, 'Maria Oliveira'),
(3, 1000000.00, 0, 'Pedro Souza'),
(4, 10000000.00, 0, 'Ana Santos'),
(5, 500000.00, 0, 'Carlos Pereira');


INSERT INTO lb_transacoes (transacao) VALUES ('Crédito');
INSERT INTO lb_transacoes (transacao) VALUES ('Débito');
