from bottle import Bottle, request, HTTPResponse
from pdo import PDO
from db import Database

app = Bottle()
db = Database()
pdo = PDO(db)

@app.post('/clientes/<id:int>/transacoes')
def realizar_transacao(id):
    cliente = pdo.get_cliente(id)
    if not cliente:
        return HTTPResponse(status=404, body='Cliente não encontrado!')

    try:
        data = request.json
    except Exception as error:
        return HTTPResponse(status=422, body='Corpo da requisição inválido!')

    valid, error_message = validate_transaction_data(data)
    if not valid:
        return HTTPResponse(status=422, body=error_message)

    saldo, limite = cliente
    valor = int(data['valor'])
    tipo = data['tipo']
    descricao = data['descricao']

    if tipo == 'd' and saldo - valor < -limite:
        return HTTPResponse(status=422, body='Transação inconsistente para esse usuário (Sem limite)!')

    novo_saldo = saldo - valor if tipo == 'd' else saldo + valor

    pdo.update_saldo(id, novo_saldo)
    pdo.insert_transacao(id, valor, tipo, descricao)

    return HTTPResponse({'limite': limite, 'saldo': novo_saldo})

def validate_transaction_data(data):
    if not isinstance(data, dict) or 'valor' not in data or 'tipo' not in data or 'descricao' not in data:
        return False, "Requisição incompleta!"
    valor = data.get('valor')
    tipo = data.get('tipo')
    descricao = data.get('descricao')
    if not isinstance(valor, (int, float)) or not isinstance(descricao, str) or tipo not in ('c', 'd'):
        return False, "Dados inválidos na requisição!"
    if '.' in str(valor) or valor < 0:
        return False, "Informe um valor inteiro positivo!"
    if len(descricao) < 1 or len(descricao) > 10:
        return False, "A descrição deve ter entre 1 e 10 caracteres!"
    return True, ""

@app.get('/clientes/<id:int>/extrato')
def obter_extrato(id):
    extrato = pdo.get_extrato(id)
    if not extrato:
        return HTTPResponse(status=404, body='Cliente não encontrado !')
    return extrato

@app.error(404)
def error404(error):
    return f"Não há nada aqui ! (´。＿。｀) (。﹏。*), -> {error}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)




