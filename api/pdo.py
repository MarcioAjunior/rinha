from datetime import datetime

class PDO:
    def __init__(self, db):
        self.db = db

    def get_cliente(self, id):
        if not id in self.db.custumers:
            return None
        return id

    def get_transacoes(self, id):
        query = "SELECT valor, transacao_tipo, descricao, realizado_em FROM transacoes_cliente WHERE cliente_id = %s ORDER BY realizado_em DESC LIMIT 10"
        result = self.db.execute_query_fetch_all(query, (id,))
        return result

    def insert_credito(self, id_cliente, valor, descricao):
        query = "select credito(%s, %s, %s)"
        results = self.db.execute_query_fetch_one(query, (id_cliente, valor, descricao))
        results = eval(results[0].replace("t", "True").replace("f", "False")) 
        return results
        
    def insert_debito(self, id_cliente, valor, descricao):
        query = "select debito(%s, %s, %s)"
        results = self.db.execute_query_fetch_one(query, (id_cliente, valor, descricao))
        results = eval(results[0].replace("t", "True").replace("f", "False")) 
        return results
    

    def get_extrato(self, id):
        cliente = self.get_cliente(id)
        
        if not cliente:
            return None
        
        saldo, limite = cliente
                
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