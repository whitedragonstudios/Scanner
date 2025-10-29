import os, platform, subprocess, sys, shutil
import psycopg2
from time import sleep



class Postgre_Install:
    def __init__(self, user, password, dbname, port, host):
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.host = host
        self.system = platform.system().lower()


    # universal function for connecting to the database
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
        print("Checking for PostgreSQL installation...")
        try:
            # Try to connect to the default psql database
            self.connectDB(dbname="postgres", user="postgres")
            print("Connection to default psql server confirmed.")
            # Skip the rest of this function
            return True
        except Exception as e:
            print(f"Failed to connect to psql server: {e}")
            print("Locating installation manually")
        # Search through every likely Path for pqsl
        for path in self.path_list():
            # Check which version of psql to look for.
            if os.name == "nt":
                bin_name = "psql.exe"
            else:
                bin_name = "psql"
            psql_location = os.path.join(path, bin_name)
            # Check Path against psql location
            if os.path.exists(psql_location):
                print(f"Found PostgreSQL at: {psql_location}")
                # Append env:PATH to include psql's path for the future
                os.environ["PATH"] += os.pathsep + path
                print(f"Added '{path}' to PATH for this session.")
                return True
        # If Path cannot be loacted function returns false
        if shutil.which("psql") is None:
            print("Failure: PATH detection \n!!! Could not locate PostgreSQL installation !!!\nYou must install PostgreSQL")
            return False
        

    # Detect os and automaticaly install psql.
    def install_psql(self):
        print(self.system.title(), " detected")
        # Check for windows OS
        if self.system == "windows" or self.system == "nt":
            print("Installing PostgreSQL with Chocolatey")
            # Install postgresql with chocolatey
            cmd = "choco install postgresql --yes"
        # Check for Mac OS
        elif self.system == "darwin": 
            print("Installing PostgreSQL with Homebrew")
            # Install postgresql with homebrew
            cmd = "brew install postgresql"
        # Check for Linux OS
        elif self.system == "linux":
            # Find package managner
            distro = platform.freedesktop_os_release().get("ID", "").lower() if hasattr(platform, "freedesktop_os_release") else ""
            if shutil.which("apt"):
                # Install postgresql with apt
                cmd = "sudo apt update && sudo apt install -y postgresql-client"
            elif shutil.which("dnf"):
                # Install postgresql with dnf
                cmd = "sudo dnf install -y postgresql"
            elif shutil.which("yum"):
                # Install postgresql with yum
                cmd = "sudo yum install -y postgresql"
            elif shutil.which("pacman"):
                # Install postgresql with pacman
                cmd = "sudo pacman -Sy postgresql --noconfirm"
            else:
                # Could not determine linux distro
                print("Failure: Linux Distro detection \n!!! Automatic installation failed !!!\nPlease install PostgreSQL manually then try running this program again")
                return False
        else:
            # Could not determine OS
            print("Failure: OS detection \n!!! Automatic installation failed !!!\nPlease install PostgreSQL manually then try running this program again")
            return False
        installed = True
        try:
            # Send the correct OS command to shell
            result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {cmd}")
            print(e.stderr.strip())
            installed = False
        # Check that the command worked
        if installed == True:
            print(">>> PostgreSQL sucessfully installed <<<")
            return True
        else:
            print("Failure: installing psql\n!!! Automatic installation failed !!!\nPlease install PostgreSQL manually then try running this program again")
            return False


    # Setup the database that you will need for the program to run
    def create_database(self):
        print("No Databases found: creating them")
        try:
            # Connect using default credentials to create the database
            self.connectDB(cmd=f"CREATE DATABASE {self.dbname};", dbname="postgres", user="postgres", info=True)
            # Connect using default credentials to create the user
            self.connectDB(cmd=f"CREATE USER {self.user} WITH PASSWORD '{self.password}';", dbname="postgres", user="postgres")
            # Connect to scanner using postgre credenitals to grant user full permissions
            self.connectDB(cmd=f"GRANT USAGE, CREATE ON SCHEMA public TO {self.user}; ALTER SCHEMA public OWNER TO {self.user};", user="postgres")
            # Run createDB sql script to create all tables and populate config_databse
            self.connectDB(filename="createDB.sql", info=True)
            print(f"Database creation complete")
            # Query config_database the ensure it was created.
            self.connectDB(query="SELECT * FROM config_database;")
        except Exception as e:
            print(f"Failed to open createDB {e}")

    
    # This method controls the flow of the entire class.
    # Call this method in order to begin initalization fo the program.
    def run(self):
        # Run check_install to see if psql is installed.
        if self.check_install() == False:
            # ask if the user wants to automatically install psql
            ans = input("Install PostgreSQL? (y/n): ").lower().strip()
            if ans != "y":
                print("PostgreSQL is required for this program to run.\nPlease install manually.\n!!! Aborting program launch !!!")
                # Abort setup the user must install psql for the program to work
                sleep(5)
                return False
            else:
                # Install psql, works on most OS and Distros
                print("Installing PostgreSQL.\n   !!! Make sure to remember your password. !!!")
                if self.install_psql() == False:
                    print("Failure: install_ psql\nPostgreSQL is required for this program to run.\nPlease install manually.\n!!! Aborting program launch !!!")
                    sleep(5)
                    return False
        # Set up the database which the program will use.
        print("Checking if databases have been created")
        # Connect to scanner with the postgre default user
        if self.connectDB(user="postgres"):
            print("Databases already created")
        else:
            self.create_database
            print("Success databases created")

    # Quick function to delete the scanner database to be used in debugging
    def drop_database(self):
        try:
            # Connect with default credentials and drop database
            self.connectDB(cmd=f"DROP DATABASE IF EXISTS scanner CASCADE;", dbname="postgres", user="postgres", info=True)
        except Exception as e:
            print(f"Failed to drop database:{e}")
        


