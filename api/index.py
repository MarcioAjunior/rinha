from bottle import run, get, post, error, request, BaseResponse, response
from helpers.db import Db
import os, json
from dotenv import load_dotenv


@post('/clientes/<id:int>/transacoes')
def post_operation(id:int = None):
    """Rota que cadastra uma operação para o id do cliente indicado como parâmetro"""
    required = set(('valor','tipo','descricao')) 
    body = request.json
    if not set(body.keys()) == required:
        response.status = 422
        response.body = 'Requisição imcompleta !'
        return response
    
    user = db.query(type_query='R', args={"campos":'id, limite, saldo_inicial', "tabela":'clientes', "condicao":f'id = {id}' })

    if user is None:
        response.status = 404
        response.body = 'Usuario Não encontrado !'
        return response
    
    user = dict(zip(('id','limite','saldo_inicial'),user))
    
    if body.get('tipo') == 'd':
        if user.get('saldo_inicial') - body.get('valor') < user.get('limite') * -1:
            response.status = 422
            response.body = 'Operaçõe inconsiste com limite desse usuario !'
            return response
        
        user["saldo_inicial"] -= body.get('valor')
        print(user.get('saldo_inicial'))
        db.query(type_query='U', args={"tabela": 'clientes', "set": f'saldo_inicial = {user.get("saldo_inicial")}', "condicao": f'id = {user.get("id")}'})
        db.query(type_query='C', args={"tabela": 'transacoes_cliente', "colunas": 'cliente_id, transacao_id, valor', "values": f'{user.get("id")}, {2}, {body.get("valor")}'})
    else:
        user["saldo_inicial"] += body.get('valor')
        print(user.get('saldo_inicial'))
        db.query(type_query='U', args={"tabela": 'clientes', "set": f'saldo_inicial = {user.get("saldo_inicial")}', "condicao": f'id = {user.get("id")}'})
        db.query(type_query='C', args={"tabela": 'transacoes_cliente', "colunas": 'cliente_id, transacao_id, valor', "values": f'{user.get("id")}, {1},  {body.get("valor")}'})

    return user

@get('/clientes/<id:int>/extrato')
def get_extract(id:int = None):
    """Rota que retorna o extrato do cliente indicado como parâmetro"""
    aa = db.query()
    print(f'AAAA {db.conn.closed}')
    return str(db.conn.closed)

@error(404)
def error404(error):
    print(error)
    return "Não há nada aqui ! (´。＿。｀) (。﹏。*)"

if __name__ == '__main__':
    load_dotenv()
    db = Db(
        db_host= 'localhost',
        db_name='rinha',
        db_password='mypassword',
        db_user='myuser'
        )
    run(host= '127.0.0.1', port=80, debug=True, reloader=True) #os.environ.get('HOST') os.environ.get('PORT_HTTP')
