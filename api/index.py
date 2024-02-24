from bottle import run, get, post, error
from helpers.db import Db
import os
from dotenv import load_dotenv

@post('/clientes/<id:int>/transacoes')
def post_operation(id:int = None):
    """Rota que cadastra uma operação para o id do cliente indicado como parâmetro"""
    return None

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
        db_host= os.environ.get('HOST'),
        db_name=os.environ.get('DBNAME'),
        db_password=os.environ.get('PASS'),
        db_user=os.environ.get('USER')
        )
    run(host= os.environ.get('HOST'), port=os.environ.get('PORT_HTTP'), debug=True)
