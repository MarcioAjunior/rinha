def validate_transaction_data(data):
    if not isinstance(data, dict) or 'valor' not in data or 'tipo' not in data or 'descricao' not in data:
        return False, "Requisição incompleta!"
    
    valor = data.get('valor')
    tipo = data.get('tipo')
    descricao = data.get('descricao')

    if not isinstance(valor, (int, float)) or valor < 0 or '.' in str(valor):
        return False, "Informe um valor inteiro positivo!"

    if tipo not in ('c', 'd') or not isinstance(descricao, str) or len(descricao) < 1 or len(descricao) > 10:
        return False, "Dados inválidos na requisição!"

    return True, ""