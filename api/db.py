import psycopg2
import os
from dotenv import load_dotenv

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv()
            cls._instance.conn = psycopg2.connect(
                dbname='rinha',
                user='myuser',
                password='mypassword',
                host=os.getenv('HOST'),
                port=os.getenv('PORT')
            )
        return cls._instance

    def __init__(self):
        self._cursor = None

    def _get_cursor(self):
        if self._cursor is None or self._cursor.closed:
            self._cursor = self.conn.cursor()
        return self._cursor

    def execute_query_commited(self, query, params=None, operation=''):
        cursor = self._get_cursor()
        try:
            cursor.execute(query, params)
            if operation == 'insert':
                self.conn.commit()
            result = True
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            result = False
        return result

    def execute_query_fetch_all(self, query, params=None):
        cursor = self._get_cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            result = None
        return result

    def execute_query_fetch_one(self, query, params=None):
        cursor = self._get_cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            result = None
        return result
