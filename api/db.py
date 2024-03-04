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
                port = os.getenv('PORT')
            )
        return cls._instance

    def execute_query(self, query, params=None, operation = 'select'):       
        cursor = self.conn.cursor()
        if operation in ("insert", "update"):
            try:
                cursor.execute(query, params)
                self.conn.commit()
                #print(f"{operation.capitalize()} realizada com sucesso.")
                result = True
            except:
                result = False
        else :
            cursor.execute(query, params)
            result = cursor.fetchall()     
        cursor.close()
        return result
