import psycopg2, os

class Handler:
    def __init__(self, user="postgres", password="", dbname="postgres", port=5000, host="localhost", info=False):
        # Default attributes for Handler are for postgre default account
        self.user = user or "postgres"
        self.password = password or ""
        self.dbname = dbname or "postgres"
        self.port = port or 5000 
        self.host = host or "localhost"
        self.info = info


    # Connect handles connections to database
    def connect(self):
        # info flag is for debugging it shows which settings where used for connect.
        if self.info:
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
            # Usually commit is used explicitly, autocommit is just a precaution.
            conn.autocommit = True 
            return conn
        except Exception:
            raise

    
    # this method reports errors from the server and reports them to python.
    def report_error(self, e):
        print("\n\n!!! PostgreSQL Error !!!")
        msg = e.pgerror.strip() if e.pgerror else str(e)
        print(f"Message: {msg}")
        if hasattr(e, 'diag') and e.diag:
            print(f"SQLSTATE: {e.pgcode}")
            if getattr(e.diag, 'message_detail', None):
                print(f"Details: {e.diag.message_detail.strip()}")
            if getattr(e.diag, 'context', None):
                print(f"Context: {e.diag.context.strip()}")
        print("\n\n")

    
    # send command allows single commands to be sent to the server
    def send_command(self, cmd):
        conn = None
        cur = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            print(f"<<< Executing command >>>")
            print(cmd)
            cur.execute(cmd)
            conn.commit()
            print(f">>> Executed command <<<")
            for notice in conn.notices:
                print("NOTICE:", notice)
        except psycopg2.Error as e:
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()


    # Open file (not working permissions error) allows the use of sql scripts for sending complex commands to the server
    def open_file(self, filename):
        if not os.path.exists(filename):
            print(f"Cannot locate file: {filename}")
            return
        conn = None
        cur = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            print(f"<<< Processing SQL script >>>\n{filename}")
            with open(filename, 'r') as f:
                sql_script = f.read()
            statements = sql_script.split(";")
            clean_statements = []
            for stmt in statements:
                stmt = stmt.strip()
                if stmt and not stmt.startswith("--"):
                    clean_statements.append(stmt)
            for stmt in clean_statements:
                print(stmt)
                cur.execute(stmt)
            conn.commit()
            print(f">>> Executed SQL file <<<")
        except psycopg2.Error as e:
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()


    # Send query sends a single query and returns a structured tuple
    def send_query(self, query):
        conn = None
        cur = None
        results = []
        try:
            conn = self.connect()
            cur = conn.cursor()
            print(f"<<< Executing Query >>>")
            print(query)
            cur.execute(query)
            results = cur.fetchall()
            print("--- Query Results ---")
            for row in results:
                print(row)
            print("--- End Results ---")
            print(f">>> Query Exacuted <<<")
            for notice in conn.notices:
                print("NOTICE:", notice)
            return results
        except psycopg2.Error as e:
            self.report_error(e)
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()
    

    # Request config is a specific case for loading the config files. May be replaced by send_query as they are almost the same.
    def request_config(self):
        conn = None
        cur = None
        config = {}
        try: 
            conn = self.connect()
            cur = conn.cursor()
            print("<<< Loading configuration >>>")
            # query is hard coded
            cur.execute("SELECT key, value FROM config_database;") 
            for row in cur.fetchall():
                config[row[0]] = row[1]
            print(">>> Configuration loaded <<<")
            #print(config)
            return config
        except psycopg2.Error as e:
            self.report_error(e)
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()
    

    # update config (untested) is a method to update specific config setting from the menu.html page.
    def update_config(self, key, value):
        conn = None
        cur = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("UPDATE config_database SET value = %s WHERE key = %s;", (value, key)) 
            conn.commit() 
            print(f"Configuration key '{key}' updated successfully.")
        except psycopg2.Error as e:
            print(f"Database error during config update: {e}")
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise e
        finally: 
            if cur: cur.close()
            if conn: conn.close()



print("Connecting to database:", "scanner", "host:", "localhost", "port:", 5000)
h = Handler("marcus", "stoic", "scanner", 5000, "localhost")
rows = h.send_query("SELECT * FROM people_database;")
print("Rows in database:", rows)
