from bottle import run, get, post, error, request
from helpers.db import Db
import os
from dotenv import load_dotenv

@post('/clientes/<id:int>/transacoes')
def post_operation(id:int = None):
    """Rota que cadastra uma operação para o id do cliente indicado como parâmetro"""
    required = set(('valor','tipo','descricao')) 
    body = request.json
    if not set(body.keys()) == required:
        return 'Erro'
    
    result = db.query(type_query='R', kwargs={"campos":"limite, saldo_inicial", "tabela":"clientes", "condicao":f"id = {id}" })
    print(result)
    return 

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
