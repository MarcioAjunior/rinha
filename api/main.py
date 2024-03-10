from bottle import Bottle, request, HTTPResponse
from pdo import PDO
from db import Database
from validate_transaction import validate_transaction_data

app = Bottle()
db = Database()
db.get_custumers()
pdo = PDO(db)

@app.post('/clientes/<id:int>/transacoes')
def realizar_transacao(id):
    cliente = pdo.get_cliente(id)
    if not cliente:
        return HTTPResponse(status=404, body='Cliente não encontrado!')
    try:
        data = request.json
    except:
        return HTTPResponse(status=422, body='Corpo da requisição inválido!')

    valid, error_message = validate_transaction_data(data)
    if not valid:
        return HTTPResponse(status=422, body=error_message)

    tipo = data['tipo']
    valor = data['valor']
    descricao = data['descricao']
    
    if tipo == 'c':
        saldo_inicial, limite, success = pdo.insert_credito(cliente,valor,descricao)
        if success:
            return HTTPResponse({'limite': limite, 'saldo': saldo_inicial})
    else:
        #d
        saldo_inicial, limite, success = pdo.insert_debito(cliente,valor,descricao)
        if success:
            return HTTPResponse({'limite': limite, 'saldo': saldo_inicial})
        
        return HTTPResponse(status=422, body='Operação incosistente para o cliente !')
        

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




