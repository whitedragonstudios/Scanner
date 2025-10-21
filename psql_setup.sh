#!/bin/bash

# change these variables as needed to create a custom user and database
user="marcus"
port=5000
dbname="scanner"


echo "Create password for your PostgreSQL databases"
while true; do
    read -sp "Enter password: " password #stoic
    echo
    read -sp "Confirm password: " password2
    echo
    # Check if the passwords match.
    if [[ "$password" != "$password2" ]]; then
        echo "Passwords do not match."
    else
        echo "Passwords match."
        break
    fi
done

choice=""
while true; do
    read -sp "Install PostgreSQL? (y/n): " choice
    echo
    if [[ "$choice" == "n" || "$choice" == "N" ]]; then
        echo "Skipping PostgreSQL installation."
        break
    elif [[ "$choice" == "y" || "$choice" == "Y" ]]; then
        echo "Intalling PostgreSQL."
        sudo apt-get update && sudo apt-get upgrade -y
        sudo apt-get install -y postgresql postgresql-contrib
        break
    else
        echo "Invalid choice. Please enter 'y' or 'n'."
    fi
done

sudo service postgresql start
echo "PostgreSQL service started."


sudo -u postgres psql -p "$port" -d postgres -c "
DO \$\$
BEGIN
   IF EXISTS (SELECT FROM pg_roles WHERE rolname = '${user}') THEN
      RAISE NOTICE 'User ${user} already exists. Resetting password.';
      EXECUTE format('ALTER ROLE %I WITH PASSWORD %L', '${user}', '${password}');
   ELSE
      RAISE NOTICE 'Creating new user ${user}.';
      EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', '${user}', '${password}');
   END IF;
END
\$\$;
"

echo "'$dbname' exists..."
sudo -u postgres psql -p "$port" -d postgres -c "
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '${dbname}') THEN
      EXECUTE format('CREATE DATABASE %I OWNER %I', '${dbname}', '${user}');
   END IF;
END
\$\$;
"

sudo -u postgres psql -p "$port" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${dbname} TO ${user};"

echo "Choose which tables you want to reset"
echo "  1) CLEAN re-install - DROP all tables (WARNING: will delete all data stored in people & timesheets)"
echo "  2) RESET configuration settings only (set to defaults)"
echo "  3) KEEP all tables (choose this to keep all existing data)"
read -p "Enter 1, 2 or 3: " choice
choice=${choice:-3}

case "$choice" in
    1)
        echo "Performing CLEAN re-install"
        sudo -u postgres psql -p "$port" -d scanner -c "
            DROP TABLE IF EXISTS timesheet_database CASCADE;
            DROP TABLE IF EXISTS people_database CASCADE;
            DROP TABLE IF EXISTS config_database CASCADE;"
        ;;
    2)
        echo "Resetting configuration settings to defaults"
        sudo -u postgres psql -p "$port" -d scanner -c "
            DROP TABLE IF EXISTS config_database CASCADE;"
        ;;
    3)
        echo "Keeping existing tables (no drops)."
        ;;
    *)
        echo "Invalid choice - keeping existing tables."
        ;;
esac


echo "Creating tables as needed..."
sudo -u postgres psql -p "$port" -d "$dbname" -f createDB.sql


echo "Setup complete."