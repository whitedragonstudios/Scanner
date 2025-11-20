import psycopg2
from psycopg2 import sql
from classHandler import Handler

class DBDebugger:
    def __init__(self, handler: "Handler"):
        self.handler = handler

    # --- Quick health check ---
    def check_connection(self):
        try:
            conn = self.handler.connect()
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"✅ Connection OK - PostgreSQL version: {version}")
        except Exception as e:
            self.handler.report_error(e)
            print("❌ Connection failed.")
        finally:
            if cur: cur.close()
            if conn: conn.close()

    # --- List all databases ---
    def list_databases(self):
        try:
            results = self.handler.send_query("SELECT datname FROM pg_database WHERE datistemplate = false;")
            print("📚 Databases:", [r[0] for r in results])
        except Exception as e:
            self.handler.report_error(e)

    # --- List all tables in the current database ---
    def list_tables(self):
        try:
            results = self.handler.send_query("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            print("📋 Tables:", [r[0] for r in results])
        except Exception as e:
            self.handler.report_error(e)

    # --- Describe a table's columns ---
    def describe_table(self, table_name):
        try:
            query = sql.SQL("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = %s;
            """)
            conn = self.handler.connect()
            cur = conn.cursor()
            cur.execute(query, (table_name,))
            rows = cur.fetchall()
            print(f"🧱 Columns in {table_name}:")
            for col, dtype, nullable in rows:
                print(f"   - {col}: {dtype} (nullable: {nullable})")
        except psycopg2.Error as e:
            self.handler.report_error(e)
        finally:
            if cur: cur.close()
            if conn: conn.close()

    # --- Show first N rows of a table ---
    def preview_table(self, table_name, limit=5):
        try:
            query = sql.SQL("SELECT * FROM {} LIMIT %s;").format(sql.Identifier(table_name))
            conn = self.handler.connect()
            cur = conn.cursor()
            cur.execute(query, (limit,))
            rows = cur.fetchall()
            print(f"🔍 Preview of {table_name} (limit {limit}):")
            for r in rows:
                print(r)
        except psycopg2.Error as e:
            self.handler.report_error(e)
        finally:
            if cur: cur.close()
            if conn: conn.close()

    # --- Count total rows in a table ---
    def count_rows(self, table_name):
        try:
            query = sql.SQL("SELECT COUNT(*) FROM {};").format(sql.Identifier(table_name))
            conn = self.handler.connect()
            cur = conn.cursor()
            cur.execute(query)
            count = cur.fetchone()[0]
            print(f"📊 {table_name} has {count} rows.")
            return count
        except psycopg2.Error as e:
            self.handler.report_error(e)
        finally:
            if cur: cur.close()
            if conn: conn.close()

    # --- Run a quick test command ---
    def run_test(self, cmd):
        print("⚙️ Running quick test command:")
        self.handler.send_command(cmd)


user_handle = Handler(profile="user")
debugger = DBDebugger(user_handle)

# Run quick diagnostics
debugger.check_connection()
debugger.list_databases()
debugger.list_tables()
debugger.describe_table("config_database")
debugger.describe_table("email_list")
debugger.count_rows("config_database")
debugger.preview_table("config_database", limit=50)
debugger.preview_table("email_list", limit=4)
debugger.preview_table("people_database", limit=110)
debugger.preview_table("timesheet_database", limit=4)