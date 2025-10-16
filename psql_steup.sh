# server password stoic
# port 5000


read -sp "Enter password: " DB_PASSWORD
echo
read -sp "Confirm password: " DB_PASSWORD_CONFIRM
echo

# Check if the passwords match.
if [[ "$DB_PASSWORD" != "$DB_PASSWORD_CONFIRM" ]]; then
    echo "Passwords do not match. Exiting."
    exit 1
fi

sudo -u postgre psql -p 5000 << EOF
    CREATE USER 'marcus' WITH PASSWORD 'stoic';
    CREATE DATABASE people WITH OWNER = marcus;
    GRANT ALL PRIVILEGES ON DATABASE people TO marcus;
EOF

echo "Setup complete."

psql -h localhost -p 5000 -U marcus -d people