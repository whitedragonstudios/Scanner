import psycopg2


class Handler:
    def __init__(self, user, password, dbname, port, host):
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.host = host
        
    def connectDB(self, filename=None, query=None, cmd=None, user=None, password=None, dbname=None, host=None, port=None, return_conn=False, info = False):
            user = user or self.user
            password = password or self.password
            dbname = dbname or self.dbname
            host = host or self.host
            port = port or self.port
            def connection_info():
                if info == True:
                    print(f"Connecting...\n---Database: {dbname}\n---User: {user}\n---Port: {port}\n---Host: {host}")
            connection_info()
            try:
                conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                conn.autocommit = True
                cur = conn.cursor()

                def exec_and_print(sql):
                    cur.execute(sql)
                    for n in conn.notices:
                        print(f"[PostgreSQL Notice] {n.strip()}")
                    
                    try:
                        rows = cur.fetchall()
                        if rows:
                            print("\nQuery Result:")
                            for row in rows:
                                print("   ", row)
                    except psycopg2.ProgrammingError:
                        # Happens when no results (e.g., CREATE TABLE)
                        pass
                    conn.notices.clear()


                if filename:
                    with open(filename, 'r') as f:
                        sql_script = f.read()
                    #cur.execute(sql_script)
                    statements = [s.strip() for s in sql_script.split(';') if s.strip()]
                    for stmt in statements:
                        exec_and_print(stmt)
                    print(f"^^^Executed SQL file: {filename}")

                if query:
                    #cur.execute(query)
                    exec_and_print(query)
                    print(f"^^^Executed Query:\n{query}")
                    #for row in cur.fetchall():
                        #print(row)

                if cmd:
                    #cur.execute(cmd)
                    exec_and_print(cmd)
                    print(f"^^^Executed command: {cmd}")

                if return_conn:
                    return conn, cur  # let caller handle closing

                cur.close()
                conn.close()
                return True

            except Exception as e:
                print(f"Database connection failed: {e}")
                return None
            
    def update_config(self, key, value):   
        db = self.connectDB()
        with db.cursor() as cursor:
            cursor.execute(f"UPDATE config_table SET value = {value} WHERE key = {key};")
            db.commit()
        db.close()