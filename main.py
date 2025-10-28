import classInstall
import psycopg2

user = "marcus"
port = 5000
db_name = "scanner"
host = "localhost"

if __name__ == "__main__":
    # Run classInstall and check the server connection works, if not updates path and installs psql.
    server_test = classInstall.Postgre_Install(user, port,db_name,host)
    server_test.connection_test()
    # Check if db and config has been initialized.
    server_test.database_install()



# If not launch setup wizzard

#setup wizzard is a flask based app to save config settings to postgreSQL DB NOTE convert config.json to postgreSQL in future

# Load a config file which allows users to easily change settings


# Event handler for opening Database

# Create person object for output to flask

# Run DB search to match idnumber to name

# Update flask server with person output

# Send clock in time to timesheet DB 

