# server password stoic
# port 5000

user = 'marcus'
db_name = 'people'
port = 5000


read -sp "Enter password: " password
echo
read -sp "Confirm password: " password2
echo

# Check if the passwords match.
if [[ "$password" != "$password2" ]]; then
    echo "Passwords do not match."
    exit 1
fi

sudo -u postgre psql -p 5000 << EOF
    CREATE USER $user WITH PASSWORD '$password';
    CREATE DATABASE $db_name WITH OWNER = $user;
    GRANT ALL PRIVILEGES ON DATABASE $db_name TO $user;
EOF

echo "Setup complete."

psql -h localhost -p 5000 -U marcus -d people