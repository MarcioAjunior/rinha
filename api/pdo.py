from datetime import datetime

class PDO:
    def __init__(self, db):
        self.db = db

    def get_cliente(self, id):
        query = "SELECT saldo_inicial, limite  FROM clientes WHERE id = %s"
        result = self.db.execute_query(query, (id,))
        return result

    def get_transacoes(self, id):
        query = "SELECT valor, transacao_tipo, descricao, realizado_em FROM transacoes_cliente WHERE cliente_id = %s ORDER BY realizado_em DESC LIMIT 10"
        result = self.db.execute_query(query, (id,))
        return result

    def insert_transacao(self, cliente_id, valor, tipo, descricao):
        query = "INSERT INTO transacoes_cliente (cliente_id, transacao_tipo, realizado_em, valor, descricao) VALUES (%s, %s, %s, %s, %s)"
        data = (cliente_id, tipo, datetime.now(), valor, descricao)
        self.db.execute_query(query, data, operation = 'insert')

    def update_saldo(self, cliente_id, novo_saldo):
        query = "UPDATE clientes SET saldo_inicial = %s WHERE id = %s"
        self.db.execute_query(query, (novo_saldo, cliente_id), operation = 'update')

    def get_extrato(self, id):
        cliente = self.get_cliente(id)
        
        if not cliente:
            return None
        
        for saldo_cliente, limite_cliente in cliente:
            saldo = saldo_cliente
            limite = limite_cliente
                
        transacoes = self.get_transacoes(id)

        extrato = {
            "saldo": {
                "total": saldo,
                "data_extrato": datetime.now().isoformat(),
                "limite": limite
            },
            "ultimas_transacoes": []
        }

        for valor, tipo, descricao, realizado_em in transacoes:
            extrato["ultimas_transacoes"].append({
                "valor": valor,
                "tipo": tipo,
                "descricao": descricao,
                "realizada_em": realizado_em.isoformat()
            })

        return extrato
