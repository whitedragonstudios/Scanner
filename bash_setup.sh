#!/bin/bash

# change these variables as needed to create a custom user, port, and database names advanced users only
user="marcus"
port=5000
dbname="scanner"

# Prompt user to create a password for the PostgreSQL user
# In current itteration password is reset each time script is run. For security this will need to be changed in future versions.
echo "Create password for your PostgreSQL databases"
while true; do
    read -sp "Enter password: " password #stoic is the deault password for the development environment
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

# Prompt user to install PostgreSQL if not already installed. 
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

# Start PostgreSQL service if not already running
sudo service postgresql start
echo "PostgreSQL service started."

# Create PostgreSQL user and database if they do not already exist
# Here the passwrod is reset. Higher security implementations will be added in future versions.
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


# Create database if it does not already exist
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
# Grant all privileges on database to user. After setup user marcus will be used to access the database.
sudo -u postgres psql -p "$port" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${dbname} TO ${user};"

# Prompt user to choose how to handle existing tables. If there is a catastrophic error users may want to restore only config settings or keep all existing data.
# Or if data for employees completely changes a clean re-install may be desired. 
# Finally option 3 is the default to keep all existing data. If the tables do not exist they will be created fresh in createDB.sql
echo "Choose which tables you want to reset"
echo "  1) CLEAN re-install - Delete all tables (WARNING: will delete all data stored in people & timesheets)"
echo "  2) RESET configuration settings only (people and timesheet data will be kept)"
echo "  3) KEEP all tables (choose this to keep all existing data)"
read -p "Enter 1, 2 or 3: " choice
choice=${choice:-3}

# Conditional logic to drop tables based on user choice
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
        echo "Keeping existing tables."
        ;;
    *)
        echo "Invalid choice - keeping existing tables."
        ;;
esac

# Run createDB.sql to complete the table setup. 
echo "Creating tables as needed..."
sudo -u postgres psql -p "$port" -d "$dbname" -f createDB.sql
# Table creation is seperated in this module so that shell scripts for other platfroms can be created.


# After completing createDB.sql this script finishes
echo "Setup complete."
echo "Your PostGreSQL datebase: $dbname is configured and ready to be used by: $user on port: $port"