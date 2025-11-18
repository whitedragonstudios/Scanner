import psycopg2, os
from psycopg2 import sql

class Handler:
    def __init__(self, profile="marcus", dbname="scanner", info=False):
        # Set user and database properly
        if profile == "admin":
            self.user = "postgres"
            self.dbname = dbname or "postgres"
        elif profile == "superuser":
            self.user = "postgres"
            self.dbname = dbname or "scanner"
        else:
            self.user = "marcus"
            self.dbname = dbname or "scanner"

        self.password = "stoic"
        self.port = 5000
        self.host = "localhost"
        self.info = info
        self._shared_conn = None

    def connect(self):
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
            conn.autocommit = True
            # Ensure public schema is used in this session
            with conn.cursor() as cur:
                cur.execute("SET search_path TO public;")
            return conn
        except Exception as e:
            print("Failed to connect:", e)
            raise

    def report_error(self, e):
        print("!!! PostgreSQL Error !!!")
        msg = e.pgerror.strip() if e.pgerror else str(e)
        print(f"Message: {msg}")
        if hasattr(e, 'diag') and e.diag:
            print(f"SQLSTATE: {e.pgcode}")
            if getattr(e.diag, 'message_detail', None):
                print(f"Details: {e.diag.message_detail.strip()}")
            if getattr(e.diag, 'context', None):
                print(f"Context: {e.diag.context.strip()}")
        print("\n")

    def send_command(self, cmd):
        conn = cur = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            print("<<< Executing command >>>")
            print(cmd)
            cur.execute(cmd)
            conn.commit()
            print(">>> Executed command <<<")
            for notice in conn.notices:
                print("NOTICE:", notice)
        except psycopg2.Error as e:
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def send_query(self, query):
        conn = cur = None
        results = []
        try:
            conn = self.connect()
            cur = conn.cursor()
            print("<<< Executing Query >>>")
            print(query)
            cur.execute(query)
            results = cur.fetchall()
            print("--- Query Results ---")
            for row in results:
                print(row)
            print("--- End Results ---")
            for notice in conn.notices:
                print("NOTICE:", notice)
            return results
        except psycopg2.Error as e:
            self.report_error(e)
            raise
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def update_database(self, database, kname, vname, key, value, keep_open=False):
        conn = cur = None
        try:
            if keep_open:
                if not hasattr(self, "_shared_conn") or self._shared_conn is None or self._shared_conn.closed:
                    self._shared_conn = self.connect()
                conn = self._shared_conn
            else:
                conn = self.connect()

            cur = conn.cursor()
            cur.execute(
                sql.SQL("""
                    INSERT INTO {table} ({col_key}, {col_value})
                    VALUES (%s, %s)
                    ON CONFLICT ({col_key})
                    DO UPDATE SET {col_value} = EXCLUDED.{col_value};
                """).format(
                    table=sql.Identifier(database),
                    col_key=sql.Identifier(kname),
                    col_value=sql.Identifier(vname)
                ),
                (key, value)
            )
            conn.commit()
            print(f"Configuration key '{key}' updated to {value}")
        except psycopg2.Error as e:
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise
        finally:
            if cur: cur.close()
            if not keep_open and conn and not conn.closed:
                conn.close()

    # ADDED: Missing update_people method
    def update_people(self, employee_id, fields):
        """Insert or update a person in people_database"""
        conn = cur = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            
            # Build the INSERT statement dynamically
            columns = ['employee_id'] + list(fields.keys())
            values = [employee_id] + list(fields.values())
            
            # Build conflict resolution for all fields except employee_id
            update_clause = sql.SQL(', ').join([
                sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(k), sql.Identifier(k))
                for k in fields.keys()
            ])
            
            query = sql.SQL("""
                INSERT INTO people_database ({columns})
                VALUES ({placeholders})
                ON CONFLICT (employee_id)
                DO UPDATE SET {updates};
            """).format(
                columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
                placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values)),
                updates=update_clause
            )
            
            cur.execute(query, values)
            conn.commit()
            print(f"Employee {employee_id} updated successfully")
            
        except psycopg2.Error as e:
            if conn and not conn.closed:
                conn.rollback()
            self.report_error(e)
            raise
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def disconnect(self):
        if hasattr(self, "_shared_conn") and self._shared_conn and not self._shared_conn.closed:
            self._shared_conn.close()
            self._shared_conn = None