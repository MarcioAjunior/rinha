from bottle import Bottle, request, HTTPResponse
from datetime import datetime
from pdo import PDO
from db import Database
import re

app = Bottle()
db = Database()
pdo = PDO(db)

@app.post('/clientes/<id:int>/transacoes')
def realizar_transacao(id):
    cliente = pdo.get_cliente(id)
    if not cliente:
        return HTTPResponse(status=404, body='Cliente não encontrado !')
    try:
        data = request.json
    except Exception as error:
        return HTTPResponse(status=422, body='Corpo da requisição invaída')  
    
    if 'valor' not in data or 'tipo' not in data or 'descricao' not in data:
        return HTTPResponse(status=422, body='Requisição incompleta !')
    
    if data['tipo'] not in ('c', 'd'):
        return HTTPResponse(status=422, body='Tipo de transação inválida !')
 
    if isinstance(data['valor'], str):
        if re.match(r'^\d*\.\d+$', data['valor']):
            return HTTPResponse(status=422, body='Informe um valor inteiro valido !')
        try :
            if int(data['valor']) < 0:
                return HTTPResponse(status=422, body='Informe um valor positivo!')
        except:
            return HTTPResponse(status=422, body='Informe um valor valido')
    elif isinstance(data['valor'], (int, float)):
        if '.' in str(data['valor']):
            return HTTPResponse(status=422, body='Informe um valor inteiro valido !')
        if int(data['valor']) < 0: 
            return HTTPResponse(status=422, body='Informe um valor positivo!')     
    else:
        return HTTPResponse(status=422, body='O Tipo de valor deve ser um inteiro !')          
    
    if len(str(data['descricao'])) > 10 or len(str(data['descricao'])) < 1:
        return HTTPResponse(status=422, body='Informe uma descrição entre 1 e 10 caractéres !')
    
    valor = int(data['valor'])
    tipo = str(data['tipo'])
    descricao = str(data['descricao'])
    
    for saldo_cliente, limite_cliente in cliente:
        saldo = saldo_cliente
        limite = limite_cliente
    
    if tipo == 'd':
        if int(saldo) - valor < -int(limite):
            return HTTPResponse(status=422, body='Transação inconsistente para esse usuario (Sem limite) !')
        novo_saldo = saldo - valor
    else: # c
        novo_saldo = saldo + valor
        
    pdo.update_saldo(id, novo_saldo)
    pdo.insert_transacao(id, valor, tipo, descricao)
    
    return HTTPResponse(status=200, body=dict(zip(('limite', 'saldo'),(limite, novo_saldo)))) 

@app.get('/clientes/<id:int>/extrato')
def obter_extrato(id):
    extrato = pdo.get_extrato(id)
    if not extrato:
        return HTTPResponse(status=404, body='Cliente não encontrado !')
    return extrato

@app.error(404)
def error404(error):
    return "Não há nada aqui ! (´。＿。｀) (。﹏。*)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)




