import os, platform, subprocess, sys, shutil
import psycopg2


class Postgre_Install:
    def __init__(self, user, password, dbname, port, host):
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.host = host
        self.system = platform.system().lower()
        self.port_list = [self.port, 5432, 5000]
        print(self.system.title(), " detected")

    
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
                conn.autocommit = True  # <-- set autocommit here
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


    # List of all psql paths
    def path_list(self):
        return [
            r"C:\Program Files\PostgreSQL\18\bin",
            r"C:\Program Files\PostgreSQL\17\bin",
            r"C:\Program Files\PostgreSQL\16\bin",
            r"C:\Program Files\PostgreSQL\15\bin",
            r"C:\Program Files\PostgreSQL\14\bin",
            r"C:\Program Files\PostgreSQL\13\bin",
            r"C:\Program Files\PostgreSQL\12\bin",
            r"C:\Program Files\PostgreSQL\11\bin",
            r"C:\Program Files\PostgreSQL\10\bin",
            r"C:\Program Files\PostgreSQL\9.6\bin",
            r"C:\Program Files (x86)\PostgreSQL\13\bin",
            r"C:\Program Files (x86)\PostgreSQL\12\bin",
            r"/usr/local/bin",
            r"/usr/local/pgsql/bin",
            r"/Library/PostgreSQL/18/bin",
            r"/Library/PostgreSQL/17/bin",
            r"/Library/PostgreSQL/16/bin",
            r"/Library/PostgreSQL/15/bin",
            r"/Library/PostgreSQL/14/bin",
            r"/opt/homebrew/bin",
            r"/opt/homebrew/opt/postgresql@16/bin",
            r"/opt/homebrew/opt/postgresql@15/bin",
            r"/opt/homebrew/opt/postgresql@14/bin",
            r"/opt/homebrew/opt/postgresql@13/bin",
            r"/usr/bin",
            r"/usr/local/bin",
            r"/usr/pgsql-18/bin",
            r"/usr/pgsql-17/bin",
            r"/usr/pgsql-16/bin",
            r"/usr/pgsql-15/bin",
            r"/usr/pgsql-14/bin",
            r"/usr/lib/postgresql/18/bin",
            r"/usr/lib/postgresql/17/bin",
            r"/usr/lib/postgresql/16/bin",
            r"/usr/lib/postgresql/15/bin",
            r"/usr/lib/postgresql/14/bin",
            r"/opt/postgres/18/bin",
            r"/opt/postgres/17/bin",
            r"/opt/postgres/16/bin",
            r"/opt/postgres/15/bin",
            r"/usr/lib/aarch64-linux-gnu/postgresql/16/bin",
            r"/usr/lib/arm-linux-gnueabihf/postgresql/15/bin",
            r"/usr/local/pgsql/bin",
            r"/opt/pgsql/bin",
            r"/usr/local/pgsql/bin",
            r"/var/lib/postgresql/bin",
            r"/mnt/c/Program Files/PostgreSQL/16/bin",
        ]
    
    # Automatically looks for PostgreSQL install
    def check_install(self):
        print("Checking PATH for PostgreSQL installation")
        try:
            self.connectDB(dbname="postgres", user="postgres")
            print("Connection to default psql server confirmed.")
            return True
        except Exception as e:
            print(f"Failed to connect to psql server: {e}")
            print("Locating installation manually")
        for path in self.path_list():
            bin_name = "psql.exe" if os.name == "nt" else "psql"
            psql_location = os.path.join(path, bin_name)
            if os.path.exists(psql_location):
                print(f"Found PostgreSQL at: {psql_location}")
                os.environ["PATH"] += os.pathsep + path
                print(f"Added '{path}' to PATH for this session.")
                return True
        print("PostgreSQL not found")
        if shutil.which("psql") is None:
            ans = input("Install PostgreSQL? (y/n): ").lower().strip()
            if ans == "y":
                print("Installing PostgreSQL.\nMake sure to remember your password.")
                self.install_psql()
                return True
            else:
                print("PostgreSQL is required for this program to run. Please install manually.")
                return False
        return False


    # Automaticaly install psql.
    def install_psql(self):
        print("Installing PostgreSQL")
        if self.system == "windows" or self.system == "nt":
            print("Installing PostgreSQL with Chocolatey")
            cmd = "choco install postgresql --yes"
        elif self.system == "darwin":  # macOS
            print("Installing PostgreSQL with Homebrew")
            cmd = "brew install postgresql"
        elif self.system == "linux":
            # Find package managner
            distro = platform.freedesktop_os_release().get("ID", "").lower() if hasattr(platform, "freedesktop_os_release") else ""
            if shutil.which("apt"):
                cmd = "sudo apt update && sudo apt install -y postgresql-client"
            elif shutil.which("dnf"):
                cmd = "sudo dnf install -y postgresql"
            elif shutil.which("yum"):
                cmd = "sudo yum install -y postgresql"
            elif shutil.which("pacman"):
                cmd = "sudo pacman -Sy postgresql --noconfirm"
            else:
                print("Unsupported Linux distribution.")
                return
        else:
            print("Unsupported system for automatic installation.")
            return
        result = self.run_command(cmd)
        if result:
            print(">>> PostgreSQL installed <<<")
        else:
            print("!!! Automatic installation failed !!!")

    # Setup the database that you will need for the program to run
    def create_database(self):
        print("Checking if databases have been created")
        conn = False#self.connectDB(user="postgres")
        if conn == True:
            print("Databases already created")
        else: 
            print("No Databases found: creating them")
            try:
                self.connectDB(cmd=f"CREATE DATABASE {self.dbname};", dbname="postgres", user="postgres", info=True)
                self.connectDB(cmd=f"CREATE USER {self.user} WITH PASSWORD '{self.password}';", dbname="postgres", user="postgres")
                self.connectDB(cmd=f"GRANT USAGE, CREATE ON SCHEMA public TO {self.user}; ALTER SCHEMA public OWNER TO {self.user};", user="postgres")
                self.connectDB(filename="createDB.sql", info=True)
                print(f"Database creation complete")
                self.connectDB(query="SELECT * FROM config_database;")
            except Exception as e:
                print(f"Failed to open createDB {e}") 