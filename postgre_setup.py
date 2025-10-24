import os
import platform
import subprocess
import sys
import shutil

user = "marcus"
port = 5000
dbname = "scanner"

system = platform.system().lower()
print(system, " detected")

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(e.stderr.strip())
        return None

def check_psql():
    psql_path = shutil.which("psql")
    if psql_path:
        print(f"Found psql at: {psql_path}")
        return True
    print("psql not found in PATH. Attempting to locate...")

    possible_paths = [
        r"C:\Program Files\PostgreSQL\18\bin",
        r"C:\Program Files\PostgreSQL\17\bin",
        r"C:\Program Files\PostgreSQL\16\bin",
        r"C:\Program Files\PostgreSQL\15\bin",
        r"C:\Program Files\PostgreSQL\14\bin",
        r"/usr/bin",
        r"/usr/local/bin",
        r"/opt/homebrew/bin",  # macOS ARM
    ]

    for path in possible_paths:
        psql_candidate = os.path.join(path, "psql.exe" if system == "windows" else "psql")
        if os.path.exists(psql_candidate):
            print(f"Found PostgreSQL at: {psql_candidate}")
            os.environ["PATH"] += os.pathsep + path
            print(f"Added '{path}' to PATH for this session.")
            return True

    print("Could not locate psql automatically. Please ensure PostgreSQL is installed.")
    print("   Visit https://www.postgresql.org/download/ to install it.")
    return False


if not check_psql():
    sys.exit(1)


psql_version = run_command("psql --version")
if psql_version:
    print(f"PostgreSQL client available: {psql_version}")
else:
    sys.exit("psql command still not working after PATH update.")


print("\nTesting connection to PostgreSQL...")
connect_test = run_command(f'psql -U postgres -p {port} -c "\\conninfo"')
if connect_test:
    print("PostgreSQL connection test successful.")
else:
    print("Could not connect as 'postgres'. Ensure the service is running and credentials are correct.")
    print("   You can start it manually, for example:")
    if system == "windows":
        print("   net start postgresql-x64-16")
    else:
        print("   sudo service postgresql start")
