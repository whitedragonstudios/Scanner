import psycopg2, os


class Handler:
    def __init__(self,user="postgres",password="",dbname="postgres",port=5000,host="localhost",filename=None,query=None,cmd=None,info=False,autorun=True):
        self.user = user or "postgres"
        self.password = password or ""
        self.dbname = dbname or "postgres"
        self.port = port or 5000 #5432
        self.host = host or "localhost"
        self.filename = filename
        self.query = query
        self.cmd = cmd
        self.info = info
        self.autorun = autorun
        if self.autorun == True:
            self.run()
    def connect(self):
        if self.info == True:
            print(f"""Connecting...
                ---Database: {self.dbname}
                ---User: {self.user}
                ---Port: {self.port}
                ---Host: {self.host}""")
        try:
            conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
            conn.autocommit = True
            return conn
        except Exception as e:
            print(f"Failed: Handler.connect - {e}")
            return None
    
    
    def open_file(self):
        if not os.path.exists(self.filename):
            print(f"Cannot locate file: {self.filename}")
            return
        conn=self.connect()
        if not conn:
            print("Could not connect to psql")
            return
        with conn.cursor() as cur:
            try:
                with open(self.filename, 'r') as f:
                    sql_script = f.read()
                for stmt in sql_script.split(";"):
                    stmt = stmt.strip()
                    if stmt:
                        cur.execute(stmt)
                print(f"^^^Executed SQL file: {self.filename}")
            except psycopg2.Error as e:
                print(f"Failed executing SQL file: {e}")
            finally:
                conn.close()


    def send_command(self):
            self.cur.execute(self.cmd)
            print(f"^^^Executed command: {self.cmd}")


    def send_query(self):
        try:
            self.cur.execute(self.query)
            print(f"^^^Executed Query: {self.query}")
            for row in self.cur.fetchall():
                print(row)
        except psycopg2.Error as e:
            self.print_pg_error("Query error", e)

    def request_config(self):
            conn = self.connect()
            if not conn:
                return {}
            cur = conn.cursor()
            config = {}
            try:
                cur.execute("SELECT * FROM config_database;")
                for row in cur.fetchall():
                    config[row[0]] = row[1]
            except psycopg2.Error as e:
                print("Database error:", e)
            finally:
                cur.close()
                conn.close()
            return config
    

    def update_config(self, key, value):
        try:  
            db = self.connect()
            with db.cursor() as cursor:
                cursor.execute("UPDATE config_table SET value = %s WHERE key = %s;", (value, key))
        except psycopg2.Error as e:
            print("Database error:", e)
        finally: 
            db.close()


    def run(self):
        conn = self.connect()
        if not conn:
            print("Error: Handler_Run" )
            return
        self.conn = conn
        try:
            self.cur = conn.cursor()
            #if self.filename is not None:
                #self.open_file()
            if self.query is not None:
                self.send_query()
            if self.cmd is not None:
                self.send_command()
            for notice in conn.notices:
                print("NOTICE:", notice)

        except psycopg2.Error as e:
            print("Message:", e.pgerror)
            print("Details:", e.diag.message_detail)
            print("Context:", e.diag.context)
            print("SQLSTATE:", e.pgcode)
        finally:
            if hasattr(self, "cur"):
                self.cur.close()
            if conn:
                conn.close()


#if __name__ == "__main__":
    #Handler(dbname="scanner", user="marcus", password = "stoic", info=True, query= "SELECT * FROM config_database;")