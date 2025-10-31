import os, platform, subprocess, sys, shutil
import psycopg2
from time import sleep
from classHandler import Handler


class Postgre_Install:
    def __init__(self, user, password, dbname, port, host):
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.host = host
        self.system = platform.system().lower()
        # Create instance of Handler with admin privilages
        self.admin = Handler(password=self.password)

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
            self.admin.connect()
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
                if os.name == "nt":
                    # Set path for windows
                    subprocess.run(f'setx PATH "%PATH%;{path}"', shell=True)
                else:
                    # Set path for linux/mac
                    with open(os.path.expanduser("~/.bashrc"), "a") as f:
                        f.write(f'\nexport PATH="$PATH:{path}"\n')
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
        if self.system == "windows":
            print("Installing PostgreSQL with Chocolatey")
            # Install postgresql with chocolatey
            cmd = "choco install postgresql --yes"
        # Check for Mac OS
        elif self.system == "darwin":
            # Install postgresql with homebrew
            print("Installing PostgreSQL with Homebrew")
            cmd = "brew install postgresql"
        # Check for Linux OS
        elif self.system == "linux":
            distro = platform.freedesktop_os_release().get("ID", "").lower() if hasattr(platform, "freedesktop_os_release") else ""
            print(f"Distro detected: {distro}")
            # Find package managner
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
            # Create the Ended User username
            self.admin.send_command(f"CREATE USER {self.user} WITH PASSWORD '{self.password}';")
            # Create database scanner using admin creds
            self.admin.send_command(f"CREATE DATABASE {self.dbname} OWNER {self.user};")
            # Run createDB sql script to create all tables and populate config_databse
            user_handle = Handler(dbname=self.dbname, user=self.user, password=self.password, info=True)
            user_handle.open_file("createDB.sql")
            print("@@@ Database creation complete @@@")
            # Query config_database the ensure it was created.
            user_handle.send_query("SELECT * FROM config_database;")
            return True
        except Exception as e:
            print(f"Failure in create_database: {e}")
            return False


    def check_database(self):
        print(f"Checking if database '{self.dbname}' is fully initialized.")
        # Create a handler using the end user credentials
        user_handle = Handler(dbname=self.dbname, user=self.user, password=self.password, port=self.port, host=self.host)
        try:
            # Check DB/User connection first
            user_handle.connect()
            # Check for required tables
            tables = ['config_database', 'timesheet_database', 'people_database']
            # A single query that fails if any table is missing
            for table in tables:
                query = f"SELECT 1 FROM {table} LIMIT 0;"
                user_handle.send_query(query) 
            print(f"Database '{self.dbname}' is fully initialized with the required tables.")
            return True
        except psycopg2.OperationalError as e:
            # Code '3D000' (DB missing), '28P01' (Password failed), '42P01' (Table missing)
            if e.pgcode in ('3D000', '28P01'): 
                print(f"!!! Failure: credentials not created !!!\nDatabase: {self.dbname}\nor\nUser: {self.user}")
                return False
            if e.pgcode == '42P01':
                print("Database exists, but one or more essential tables are missing.")
                return False
            print(f"Database check failed\n{e}")
            return False
        except Exception as e:
            print(f"Unexpected error during database check: {e}")
            return False
        

    # This method controls the flow of the entire class.
    # Call this method in order to begin initalization fo the program.
    def run(self):
        failure_detected = False
        # Check/Install PostgreSQL
        if not self.check_install():
            ans = input("PostgreSQL not found. Install automatically? (y/n): ").lower().strip()
            if ans == "y":
                if not self.install_psql():
                    print("!!! FATAL: Automatic PostgreSQL installation failed. Cannot proceed. !!!")
                    failure_detected = True
            else:
                print("!!! FATAL: PostgreSQL is required and was not installed. Cannot proceed. !!!")
                failure_detected = True
        # Exit if installation failed or was refused
        if failure_detected:
            sleep(5)
            return False

        # Check/Create Databases
        print("\n--- Database Setup ---")
        if not self.check_database():
            print("Attempting to create Database and User...")
            if not self.create_database():
                print("!!! FATAL: Database creation/verification failed. Cannot proceed. !!!")
                failure_detected = True
        else:
            print("Database already exists. Setup skipped.")

        # --- Final Status Check ---
        if failure_detected:
            print("\n!!! Program Initialization Failed !!!")
            sleep(5)
            return False
        else:
            print("\n>>> Program Initialization Successful <<<")
            return True

    # Quick function to delete database to be used in debugging
    def drop_database(self, dropDB):
        try:
            # Connect with default credentials and drop database
            self.admin.send_command(f"DROP DATABASE IF EXISTS {dropDB};")
            print(f"Database {dropDB} deleted")
        except Exception as e:
            print(f"Failed to drop database:{e}")

    # quick function to delete users to be used in bebugging
    def drop_user(self, dropUser):
        try:
            # Connect with deault credentials and drop user.
            self.admin.send_command(f"DROP OWNED BY {dropUser};")
            self.admin.send_command(f"DROP USER IF EXISTS {dropUser};")
            print(f"User {dropUser} deleted")
        except Exception as e:
            print(f"Failed to drop user '{dropUser}': {e}")