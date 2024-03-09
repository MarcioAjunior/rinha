from datetime import datetime

class PDO:
    def __init__(self, db):
        self.db = db

    def get_cliente(self, id):
        query = "SELECT saldo_inicial, limite  FROM clientes WHERE id = %s"
        result = self.db.execute_query_fetch_one(query, (id,))
        return result

    def get_transacoes(self, id):
        query = "SELECT valor, transacao_tipo, descricao, realizado_em FROM transacoes_cliente WHERE cliente_id = %s ORDER BY realizado_em DESC LIMIT 10"
        result = self.db.execute_query_fetch_all(query, (id,))
        return result

    def insert_transacao(self, cliente_id, valor, tipo, descricao):
        query = "INSERT INTO transacoes_cliente (cliente_id, transacao_tipo, realizado_em, valor, descricao) VALUES (%s, %s, %s, %s, %s)"
        data = (cliente_id, tipo, datetime.now(), valor, descricao)
        self.db.execute_query_commited(query, data)

    def update_saldo(self, cliente_id, novo_saldo):
        query = "UPDATE clientes SET saldo_inicial = %s WHERE id = %s"
        self.db.execute_query_commited(query, (novo_saldo, cliente_id))

    def get_extrato(self, id):
        query = f"SELECT c.saldo_inicial, c.limite, tc.valor,tc.transacao_tipo,descricao,realizado_em FROM clientes c inner join transacoes_cliente tc on tc.cliente_id = {id} order by tc.realizado_em desc limit 10"
        results = self.db.execute_query_fetch_all(query, (id,))
        
        if not results:
            return None
        
        saldo = {}
        ultimas_transacoes = []
        
        for saldo_inicial, limite, valor, transacao_tipo, descricao, realizado_em in results:
            saldo = {
                "total": saldo_inicial,
                "data_extrato": datetime.now().isoformat(),
                "limite": limite
            }
            ultimas_transacoes.append({
                "valor": valor,
                "tipo": transacao_tipo,
                "descricao": descricao,
                "realizado_em": realizado_em.isoformat()
            })
            
        objetao = {
            "saldo": saldo,
            "ultimas_transacoes": ultimas_transacoes
        }

        return objetao
