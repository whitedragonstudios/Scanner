#!/bin/bash

# change these variables as needed to create a custom user and database
user = 'marcus'
employee_database = 'people'
timesheet_database = 'timesheet'
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
    CREATE DATABASE $atabase WITH OWNER = $user;
    GRANT ALL PRIVILEGES ON DATABASE $atabase TO $user;
EOF

echo "Setup complete."

psql -h localhost -p $port -U $user -d $atabase