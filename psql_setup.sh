#!/bin/bash

# change these variables as needed to create a custom user and database
user = 'marcus'
employee_database = 'people'
timesheet_database = 'timesheet'
roles_database = 'roles'
id_length = 8
port = 5000

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

choice= ""
while true; do
    read -sp "Install PostgreSQL? (y/n): " choice
    echo
    if [[ "$choice" == "n" || "$choice" == "N" ]]; then
        echo "Skipping PostgreSQL installation."
        break
    elif [[ "$choice" == "y" || "$choice" == "Y" ]]; then
        echo "Intalling PostgreSQL."
        sudo apt-get update && ugrade -y
        sudo apt-get install -y postgresql postgresql-contrib
        break
    else
        echo "Invalid choice. Please enter 'y' or 'n'."
    fi
done


sudo -u postgre psql -p $port << EOF
    CREATE USER $user WITH PASSWORD '$password';
    CREATE TABLE $employee_database (
        id SERIAL PRIMARY KEY, 
        employee_id INTEGER ($id_length) UNIQUE,
        name VARCHAR(50) UNIQUE,
        email VARCHAR(50) UNIQUE, 
        phone VARCHAR(15) UNIQUE
        ) WITH OWNER = $user;
    GRANT ALL PRIVILEGES ON DATABASE $employee_database TO $user;

    CREATE TABLE $roles_database (
        id SERIAL PRIMARY KEY,
        employee_id INTEGER($id_length) NOT NULL REFERENCES $employee_database(employee_id) ON DELETE CASCADE,
        name VARCHAR(100) NOT NULL REFERENCES $employee_database(name) ON DELETE CASCADE,
        role VARCHAR(50) UNIQUE
        position VARCHAR(50),
        department VARCHAR(50)
        ) WITH OWNER = $user;
    GRANT ALL PRIVILEGES ON DATABASE $roles_database TO $user;

    CREATE TABLE $timesheet_database (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL REFERENCES $employee_database(name) ON DELETE CASCADE,
        role VARCHAR(50) NOT NULL REFERENCES $roles_database(role) ON DELETE CASCADE,
        clock_in TIMESTAMPTZ,
        clock_out TIMESTAMPTZ
        ) WITH OWNER = $user;
    GRANT ALL PRIVILEGES ON DATABASE $timesheet_database TO $user;
EOF

echo "Setup complete."

psql -h localhost -p $port -U $user -d $d
database