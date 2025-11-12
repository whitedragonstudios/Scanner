# PowerShell script to setup PostgreSQL for Scanner
# Save as setup_postgres.ps1

# Change these variables as needed
$user = "marcus"
$port = 5000
$dbname = "scanner"

# Prompt user to create a password for PostgreSQL
do {
    $password = Read-Host "Enter password for PostgreSQL user $user" -AsSecureString
    $password2 = Read-Host "Confirm password" -AsSecureString

    if ((ConvertFrom-SecureString $password) -ne (ConvertFrom-SecureString $password2)) {
        Write-Host "Passwords do not match. Try again." -ForegroundColor Red
    } else {
        Write-Host "Passwords match." -ForegroundColor Green
        break
    }
} while ($true)

# Convert secure string to plain text for psql commands
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$passwordPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Prompt user to install PostgreSQL if not already installed
$choice = Read-Host "Install PostgreSQL? (y/n)"
switch ($choice.ToLower()) {
    "y" {
        Write-Host "Installing PostgreSQL..."
        # On Windows, suggest to use PostgreSQL installer manually or winget
        Write-Host "Please install PostgreSQL from https://www.postgresql.org/download/windows/ or run:" -ForegroundColor Yellow
        Write-Host "winget install PostgreSQL.PostgreSQL.16" -ForegroundColor Yellow
    }
    "n" { Write-Host "Skipping PostgreSQL installation." }
    default { Write-Host "Invalid choice. Skipping installation." }
}

# Create PostgreSQL user and database
Write-Host "Creating/updating PostgreSQL user and database..."

# Define SQL command to create user if not exists, else reset password
$sqlUserCmd = @"
DO \$\$
BEGIN
   IF EXISTS (SELECT FROM pg_roles WHERE rolname = '$user') THEN
      RAISE NOTICE 'User $user already exists. Resetting password.';
      EXECUTE format('ALTER ROLE %I WITH PASSWORD %L', '$user', '$passwordPlain');
   ELSE
      RAISE NOTICE 'Creating new user $user.';
      EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', '$user', '$passwordPlain');
   END IF;
END
\$\$;
"@

# Run SQL command for user creation
& psql -U postgres -p $port -d postgres -c $sqlUserCmd

# Create database if it doesn't exist
$sqlDbCmd = @"
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$dbname') THEN
      EXECUTE format('CREATE DATABASE %I OWNER %I', '$dbname', '$user');
   END IF;
END
\$\$;
"@

& psql -U postgres -p $port -d postgres -c $sqlDbCmd

# Grant privileges
& psql -U postgres -p $port -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $dbname TO $user;"

# Prompt for table reset
Write-Host "Choose which tables you want to reset:"
Write-Host "  1) CLEAN re-install (delete all data)"
Write-Host "  2) RESET configuration only (keep people & timesheets)"
Write-Host "  3) KEEP all tables (default)"
$choice = Read-Host "Enter 1, 2 or 3"
if ([string]::IsNullOrEmpty($choice)) { $choice = "3" }

switch ($choice) {
    "1" {
        Write-Host "Performing CLEAN re-install..."
        & psql -U $user -p $port -d $dbname -c "DROP TABLE IF EXISTS timesheet_database CASCADE; DROP TABLE IF EXISTS people_database CASCADE; DROP TABLE IF EXISTS config_database CASCADE;"
    }
    "2" {
        Write-Host "Resetting configuration tables only..."
        & psql -U $user -p $port -d $dbname -c "DROP TABLE IF EXISTS config_database CASCADE;"
    }
    "3" { Write-Host "Keeping all existing tables." }
    default { Write-Host "Invalid choice, keeping tables." }
}

# Run createDB.sql to setup tables
Write-Host "Creating tables as needed..."
& psql -U $user -p $port -d $dbname -f "createDB.sql"

Write-Host "Setup complete."
Write-Host "Database $dbname is configured and ready to be used by $user on port $port."
