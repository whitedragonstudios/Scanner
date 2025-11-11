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
            # Create the End User username
            self.admin.send_command(f"CREATE USER {self.user} WITH PASSWORD '{self.password}';")

            # Create database owned by the new user
            self.admin.send_command(f"CREATE DATABASE {self.dbname} OWNER {self.user};")

            # Connect as the end user to initialize database and run all table commands
            user_handle = Handler(dbname=self.dbname, user=self.user, password=self.password)

            # Drop tables if they exist
            self.drop_tables("people_database")
            self.drop_tables("timesheet_database")
            self.drop_tables("config_database")
            self.drop_tables("email_list")

            # Create config_database table
            user_handle.send_command("""
                CREATE TABLE config_database (
                    key VARCHAR(50) PRIMARY KEY,
                    value VARCHAR(128)
                );
            """)

            user_handle.send_command("""
                CREATE TABLE email_list(
                    key SERIAL PRIMARY KEY,
                    email VARCHAR(255),
                    freqency VARCHAR(8)
                );
            """)

            user_handle.send_command("""INSERT INTO email_list (email) VALUES 
                    ('rowens.wds@gmail.com'), 
                    ('test@scanner.com')
                ;""")

            # Insert default config data
            user_handle.send_command("""
                INSERT INTO config_database (key, value) VALUES
                    ('config_status', 'False'),
                    ('config_date', '2025-01-01'),
                    ('CSV_path', NULL),
                    ('XLSX_path', NULL),
                    ('JSON_path', NULL),
                    ('webpage_title', 'Populus Numerus'),
                    ('company','Scanner'),         
                    ('main_background_color','#0a0a1f'),
                    ('main_text_color','#f0f0f0'),
                    ('content_color', '#1c1c33'),
                    ('content_text_color', '#ffffff'),
                    ('sidebar_color','#193763'),
                    ('sidebar_text_color','#ffffff'),   
                    ('button_color','#1a73ff'),
                    ('button_text_color','#ffffff'),
                    ('button_hover_color','#0050b3'),
                    ('border_color','#3399ff'),
                    ('city', 'New York City'),
                    ('lon', '-74.0060152'),
                    ('lat', '40.7127281'),
                    ('weather_key', 'baeb0ce1961c460b651e6a3a91bfeac6'),
                    ('country', 'us'),
                    ('news_key', '04fbd2b9df7b49f6b6a626b4a4ae36be');
            """)

            # Create people_database table
            user_handle.send_command("""
                CREATE TABLE people_database (
                    id SERIAL PRIMARY KEY, 
                    employee_id INTEGER UNIQUE,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(50), 
                    phone VARCHAR(15),
                    pic_path VARCHAR(128) UNIQUE,
                    employee_role VARCHAR(50),
                    position VARCHAR(50),
                    department VARCHAR(50)
                );
            """)

            self.insert_test_data()

            # Create timesheet_database table
            user_handle.send_command("""
                CREATE TABLE timesheet_database (
                    id SERIAL PRIMARY KEY,
                    employee_id INTEGER NOT NULL REFERENCES people_database(employee_id) ON DELETE CASCADE,
                    clock_in TIMESTAMPTZ DEFAULT NOW(),
                    clock_out TIMESTAMPTZ,
                    work_date DATE DEFAULT CURRENT_DATE
                );
            """)

            # Grant privileges to user
            user_handle.send_command(f"GRANT ALL PRIVILEGES ON DATABASE {self.dbname} TO {self.user};")
            user_handle.send_command(f"GRANT ALL PRIVILEGES ON SCHEMA public TO {self.user};")
            user_handle.send_command(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {self.user};")
            user_handle.send_command(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {self.user};")

            # Update config_database to mark initialization complete
            user_handle.send_command("UPDATE config_database SET value = CURRENT_DATE WHERE key = 'config_date';")
            user_handle.send_command("UPDATE config_database SET value = 'True' WHERE key = 'config_status';")

            print("@@@ Database creation complete @@@")
            # Verify table creation
            user_handle.send_query("SELECT * FROM config_database;")
            user_handle.send_query("SELECT * FROM email_list;")
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


    def insert_test_data(self):

        user_handle = Handler(dbname=self.dbname, user=self.user, password=self.password)
        user_handle.send_command("""INSERT INTO people_database (
    employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department
) VALUES
    (11111111, 'Han', 'Solo', 'hsolo@scanner.com', '100-555-1976', '1111.jpg', 'Scoundrel', 'Pilot', 'Only in it for the money'),
    (22222222, 'Luke', 'Skywalker', 'lskywalker@scanner.com', '100-555-1978', '1112.jpg', 'Jedi Master', 'Like his father', 'Peace and Justice')
ON CONFLICT (employee_id)
DO UPDATE SET
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    pic_path = EXCLUDED.pic_path,
    employee_role = EXCLUDED.employee_role,
    position = EXCLUDED.position,
    department = EXCLUDED.department;""")


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
    

    def drop_tables(self, table_name):
        try:
            self.admin.send_command(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        except Exception as e:
            print(f"Failed to drop {table_name}")