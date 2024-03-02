from bottle import run, get, post, error, request, BaseResponse, response
from helpers.db import Db
import os, json
from dotenv import load_dotenv
import datetime

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
        success = db.query(type_query='U', args={"tabela": 'clientes', "set": f'saldo_inicial = {user.get("saldo_inicial")}', "condicao": f'id = {user.get("id")}'})
        if success:
            success =db.query(type_query='C', args={"tabela": 'transacoes_cliente', "colunas": 'cliente_id, transacao_id, valor, descricao', "values": f'{user.get("id")}, {2}, {body.get("valor")}, \'{body.get("descricao")}\''})
            if success:
                user.pop("id")
                return user
    else:
        user["saldo_inicial"] += body.get('valor')
        success = db.query(type_query='U', args={"tabela": 'clientes', "set": f'saldo_inicial = {user.get("saldo_inicial")}', "condicao": f'id = {user.get("id")}'})
        if success:
            success = db.query(type_query='C', args={"tabela": 'transacoes_cliente', "colunas": 'cliente_id, transacao_id, valor, descricao', "values": f'{user.get("id")}, {2}, {body.get("valor")}, \'{body.get("descricao")}\'' })
            if success:     
                user.pop("id")
                return user

@get('/clientes/<id:int>/extrato')
def get_extract(id:int = None):
    """Rota que retorna o extrato do cliente indicado como parâmetro"""
    
    user = db.query(type_query='R', args={"campos":'id, limite, saldo_inicial', "tabela":'clientes', "condicao":f'id = {id}' })
    
    if user is None:
        response.status = 404
        response.body = 'Usuario Não encontrado !'
        return response
    
    user = dict(zip(('id','limite','saldo_inicial'),user))
    
    data_formatada = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    saldo = dict(zip(('total','data_extrato', 'limite'),(user.get("saldo_inicial"), data_formatada ,user.get("limite"))))

    user_trasacoes = db.query(type_query='RL', args={"campos":'valor, transacao_id, descricao, data_operacao', "tabela":'transacoes_cliente', "condicao":f' cliente_id = {id}' })

    ultimas_transacoes = []
    for valor, trasacao_id, descricao, data_operacao in user_trasacoes:
        tipo = 'c' if trasacao_id == 1 else 'd'       
        data_operacao = data_operacao.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        ultimas_transacoes.append(dict(zip(('valor', 'tipo', 'descricao', 'realizada_em'),(valor, tipo, descricao, data_operacao))))

    result = dict(zip(('saldo','ultimas_transacoes'),(saldo, ultimas_transacoes)))
    return result
 
@error(404)
def error404(error):
    print(error)
    return "Não há nada aqui ! (´。＿。｀) (。﹏。*)"

if __name__ == '__main__':
    load_dotenv()
    db = Db(
        db_host= 'db',
        db_name='rinha',
        db_password='mypassword',
        db_user='myuser'
        )
    run(host= '0.0.0.0', port=8080, debug=True, reloader=True) #os.environ.get('HOST') os.environ.get('PORT_HTTP')
