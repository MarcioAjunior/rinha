import psycopg2

class Db():
    _intance = None
      
    def __new__(cls, db_name, db_user, db_password, db_host):
        if cls._intance is None:
            cls._intance = super().__new__(cls)
            cls._intance.db_name = db_name
            cls._intance.db_user = db_user
            cls._intance.db_password = db_password
            cls._intance.db_host = db_host
            
            cls._intance.conn = None
        return cls._intance
    
    def connect(self):
        try:
            self._intance.conn  = psycopg2.connect(
            dbname=self._intance.db_name,
            user=self._intance.db_user,
            password=self._intance.db_password,
            host= self._intance.db_host
        )
            return self._intance.conn
        except Exception as error:
            raise Exception(f'NÃO FOI POSSÍVEL ESTABELECER CONEXÃO COM O BANCO ! - {error}')
        
    
    def query(self, sql = 'SELECT version()', fetchall = False):
        with self.connect().cursor() as cur:
            try:
                cur.execute(sql)
                if fetchall:
                    rows = cur.fetchall()
                    self._intance.conn.close()
                    return rows
                row = cur.fetchone()
                self._intance.conn.close()
                return row
            except (Exception, psycopg2.DatabaseError) as error:
                print(f'ERRO AO EXECUTAR A QUERY {error}')
            
