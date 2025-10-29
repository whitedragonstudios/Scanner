import classInstall
import psycopg2

user = "marcus"
password = "stoic"
db_name = "scanner"
port = 5000
host = "localhost"

if __name__ == "__main__":
    # Run classInstall and check the server connection works, if not updates path and installs psql.
    server = classInstall.Postgre_Install(user, password, db_name, port, host)
    server.check_install()
    # Check if db and config has been initialized.
    server.create_database()



# If not launch setup wizzard

#setup wizzard is a flask based app to save config settings to postgreSQL DB NOTE convert config.json to postgreSQL in future

# Load a config file which allows users to easily change settings


# Event handler for opening Database

# Create person object for output to flask

# Run DB search to match idnumber to name

# Update flask server with person output

# Send clock in time to timesheet DB 

