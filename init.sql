SET timezone = 'America/Sao_Paulo';

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


CREATE TYPE credito_result AS (
  saldo_inicial INTEGER,
  limite INTEGER,
  success BOOLEAN
);

CREATE FUNCTION credito(
  p_cliente_id INTEGER,
  p_valor INTEGER,
  p_descricao VARCHAR(10)
) RETURNS credito_result AS
$$
DECLARE
  r_saldo_inicial INT;
  r_limite INT;
BEGIN
  PERFORM pg_advisory_xact_lock(p_cliente_id);
 
  begin
	  INSERT INTO transacoes_cliente(id, cliente_id,transacao_tipo, realizado_em, valor, descricao)
	  VALUES(DEFAULT, p_cliente_id,'c', CURRENT_TIMESTAMP, p_valor, p_descricao);
	  
	  UPDATE clientes
	  SET saldo_inicial = saldo_inicial + p_valor
	  WHERE id = p_cliente_id
	  RETURNING saldo_inicial, limite
	  INTO r_saldo_inicial, r_limite;
	  
	  RETURN (r_saldo_inicial::INTEGER, r_limite::INTEGER, TRUE::BOOLEAN);
  exception
  	when others then
  		RETURN (0::INTEGER, 0::INTEGER, FALSE::BOOLEAN);
  end;
   
END;
$$ LANGUAGE plpgsql;

CREATE TYPE debito_result AS (
  saldo_inicial INTEGER,
  limite INTEGER,
  success BOOLEAN
);

CREATE FUNCTION debito(
  p_cliente_id INTEGER,
  p_valor INTEGER,
  p_descricao VARCHAR(10)
) RETURNS debito_result AS
$$
DECLARE
  r_saldo_inicial INT;
  r_limite INT;
BEGIN
  PERFORM pg_advisory_xact_lock(p_cliente_id);
  begin
	  
	SELECT saldo_inicial,
           limite
    INTO
        r_saldo_inicial,
        r_limite
    FROM clientes
    WHERE id = p_cliente_id;
	
   IF (r_saldo_inicial - p_valor) >= (r_limite * -1) THEN
   		INSERT INTO transacoes_cliente(id, cliente_id,transacao_tipo, realizado_em, valor, descricao) VALUES(DEFAULT, p_cliente_id,'d', CURRENT_TIMESTAMP, p_valor, p_descricao);
   		
   	  UPDATE clientes
	  SET saldo_inicial = saldo_inicial - p_valor
	  WHERE id = p_cliente_id
	  RETURNING saldo_inicial, limite
	  INTO r_saldo_inicial, r_limite;
	 
	  RETURN (r_saldo_inicial::INTEGER, r_limite::INTEGER, TRUE::BOOLEAN);
   	
   	else
   	   RETURN (0::INTEGER, 0::INTEGER, FALSE::BOOLEAN);
   end if;
  
  exception
  	when others then
  		RETURN (0::INTEGER, 0::INTEGER, FALSE::BOOLEAN);
  end;

END;
$$ LANGUAGE plpgsql;