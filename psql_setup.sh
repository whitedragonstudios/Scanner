#!/bin/bash

# change these variables as needed to create a custom user and database
user="marcus"
port=5000


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


psql -U postgres -d postgres -p 5000 -f createDB.sql


echo "Setup complete."