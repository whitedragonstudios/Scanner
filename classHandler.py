import psycopg2, os
from psycopg2 import sql

# 
class Handler:
    def __init__(self, profile="marcus", dbname="postgres", info=False):
        # attributes for Handler admin is the default PostgreSQL admin user
        if profile == "admin":
            self.dbname = "postgres" or dbname
        # attributes for Handler superuser use the scanner database
        elif profile == "superuser":
            self.user = "postgres"
            self.dbname = "scanner" or dbname
        # attributes for Handler user is the default application user
        else:
            self.user = "marcus"
            self.dbname = "scanner" or dbname
        # These attributes are constant for all profiles
        self.password = "stoic"
        self.port = 5000
        self.host = "localhost"
        self.info = info


    # Connect handles connections to database
    def connect(self):
        # info flag is for debugging it shows which settings where used for connecting.
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

    
    # this method reports errors from the server and sends them to python.
    def report_error(self, e):
        print("\n\n!!! PostgreSQL Error !!!")
        # Capture the error message if it exists.
        msg = e.pgerror.strip() if e.pgerror else str(e)
        print(f"Message: {msg}")
        # Handles different types of messages
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
        # Try making the connection
        try:
            conn = self.connect()
            cur = conn.cursor()
            print(f"<<< Executing command >>>")
            print(cmd)
            # Exacutes the command
            cur.execute(cmd)
            # Commmt explicit
            conn.commit()
            print(f">>> Executed command <<<")
            # Print feedback
            for notice in conn.notices:
                print("NOTICE:", notice)
        except psycopg2.Error as e:
            # Close and roll back the connection attempt
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise e
        # Close the connection after each command
        finally:
            if cur: cur.close()
            if conn: conn.close()
        # Adding a parameter to keep the connection open may be better for scale but UX and large scale testing required


    # Open file (not working 11/12/25 permissions error) allows the use of sql scripts for sending complex commands to the server
    def open_file(self, filename):
        # check the path to the file
        if not os.path.exists(filename):
            print(f"Cannot locate file: {filename}")
            return
        conn = None
        cur = None
        # Try to establish connection
        try:
            conn = self.connect()
            cur = conn.cursor()
            print(f"<<< Processing SQL script >>>\n{filename}")
            # Open the file and read into memory
            with open(filename, 'r') as f:
                sql_script = f.read()
            # Seperate multiple SQL commands based on ;
            statements = sql_script.split(";")
            clean_statements = []
            # Cleans out SQL comments
            for stmt in statements:
                stmt = stmt.strip()
                if stmt and not stmt.startswith("--"):
                    clean_statements.append(stmt)
            # Exacutes each command
            for stmt in clean_statements:
                print(stmt)
                cur.execute(stmt)
            # Explicit Commmit
            conn.commit()
            print(f">>> Executed SQL file <<<")
        except psycopg2.Error as e:
            # Close and roll back the connection attempt
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise e
        # Close the connection after all commands have completed.
        finally:
            if cur: cur.close()
            if conn: conn.close()


    # Send query sends a single query and returns a structured tuple
    def send_query(self, query):
        conn = None
        cur = None
        results = []
        # Attemps connection
        try:
            conn = self.connect()
            cur = conn.cursor()
            print(f"<<< Executing Query >>>")
            print(query)
            # Excecute query
            cur.execute(query)
            # Fetch the results of the query returns a tuple
            results = cur.fetchall()
            print("--- Query Results ---")
            # Print each row as a list of tuples
            for row in results:
                print(row)
            print("--- End Results ---")
            print(f">>> Query Exacuted <<<")
            # Capture feedback
            for notice in conn.notices:
                print("NOTICE:", notice)
            return results
        except psycopg2.Error as e:
            # Roll back and release if connection fails.
            self.report_error(e)
            raise e
        # Close the connection after each command
        finally:
            if cur: cur.close()
            if conn: conn.close()
    

    # request_config(self)
    # Query looks like: Handler instance .send_query("SELECT key, value FROM config_database;")
    

    from psycopg2 import sql

    # Modify in next sprint ADD database parameter.
def update_database(self, database, key, value, keep_open=False):
    # Prepare connection + cursor holders
    conn = None
    cur = None
    try:
        # If keeping open, reuse or create a shared connection
        if keep_open:
            if not hasattr(self, "_shared_conn") or self._shared_conn is None or self._shared_conn.closed:
                self._shared_conn = self.connect()
            conn = self._shared_conn
        else:
            conn = self.connect()
        cur = conn.cursor()
        # SAFE PARAMETERIZED QUERY — prevents SQL injection
        cur.execute(
            f"""
            INSERT INTO {database} (key, value)
            VALUES (%s, %s)
            ON CONFLICT (key)
            DO UPDATE SET value = EXCLUDED.value;
            """,
            (key, value)
        )
        conn.commit()
        print(f"Configuration key '{key}' updated successfully.")
    except psycopg2.Error as e:
        print(f"Database error during config update: {e}")
        if conn and not conn.closed:
            conn.rollback()
        self.report_error(e)
        raise e
    finally:
        # Always close cursor
        if cur:
            cur.close()
        # If NOT keeping the connection open, close it normally
        if not keep_open and conn and not conn.closed:
            conn.close()

    def disconnect(self):
        if hasattr(self, "_shared_conn") and self._shared_conn and not self._shared_conn.closed:
            self._shared_conn.close()
            self._shared_conn = None