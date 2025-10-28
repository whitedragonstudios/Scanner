import os, platform, subprocess, sys, shutil
import psycopg2


class Postgre_Install:
    def __init__(self, user, port, dbname, host):
        self.user = user
        self.port = port
        self.host = host
        self.dbname = dbname
        self.system = platform.system().lower()
        self.port_list = [self.port, 5432, 5000]
        print(self.system.title(), " detected")


    # Function for running shell commands. 
    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {cmd}")
            print(e.stderr.strip())
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
    

    # Function to check if psql is installed. 
    def check_path(self):
        psql_path = shutil.which("psql")
        if psql_path:
            print(f"Found psql at: {psql_path}")
            return True
        print("psql not found in PATH. Attempting to locate...")
        for path in self.path_list():
            if os.name == "nt" or os.name == "windows":
                bin_name = "psql.exe"
            else:
                bin_name = "psql"
            psql_location = os.path.join(path, bin_name)
            if os.path.exists(psql_location):
                print(f"Found PostgreSQL at: {psql_location}")
                os.environ["PATH"] += os.pathsep + path
                print(f"Added '{path}' to PATH for this session.")
                return True
        print("Could not locate psql automatically.")
        # Install psql
        if shutil.which("psql") is None:
            ans = input("Failed to locate PostgreSQL on your computer. /nDo you with to install it automatically? y/n").lower().strip()
            if ans == "y":
                print("Installing PostgreSQL make sure to note your PASSWORD use: /n>>Username: marcus/n >>Port: 5000")
                self.install_psql()
                return True
            else: 
                print("PostgreSQL is required to ensure this program works. Please install it manually.")
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

    # Tests connection to psql sever.
    def connection_test(self):
        if not self.check_path():
            sys.exit(1)
        psql_version = self.run_command("psql --version")
        if psql_version:
            print(f"PostgreSQL version: {psql_version} Installed")
        else:
            sys.exit("psql not working after Path update. Restatrt program or manually install PostgreSQL.")
        print("\nTesting connection to PostgreSQL > > > > ")
        connect = self.run_command(f'psql -U postgres -p {self.port} -c "\\conninfo"')
        if connect:
            print(f"PostgreSQL connection test successful on port: {self.port}. < < < <")
        else:
            print("Could not connect as 'postgres'. Ensure the service is running and credentials are correct.")
            print("   You can start it manually, for example:")
            if self.system == "windows":
                print("   net start postgresql-x64-16")
            else:
                print("   sudo service postgresql start")
    def database_install(self):
        print("Checking if databases have been created")
        db_exists = self.run_command(f'psql -U postgres -p {self.port} -W -tAc "SELECT * FROM config_database;"')
        if db_exists == "1":
            print("Databases already created")
        else: 
            print("Not Databases found: creating them")
            with open("createDB.sql", 'r') as file:
                script = file.read()
            try: 
                connection = psycopg2.connect(dbname=self.dbname, user=self.user, host=self.host, port=self.port)
                connection.autocommit = True 
                cursor = connection.cursor()
                cursor.execute(script)
                cursor.close()
                connection.close()
            except Exception as e:
                print("Filed to create sql databases error: ",e)