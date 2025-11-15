import classInstall, classSettings, databaseConfig
import psycopg2

db = databaseConfig.databaseSettings()
user = db["user"]
password = db["password"]
db_name = db["db_name"]
port = db["port"]
host = db["host"]

if __name__ == "__main__":
    # Run classInstall and check the server connection works, if not updates path and installs psql.
    server = classInstall.Postgre_Install()
    server.drop_database(db_name) #uncomment if you need to reset database
    server.drop_user(user) #uncomment if you need to reset user
    # run controls the flow of classInstall
    server.run()
    server.insert_test_data()
 
    # Load a config file which allows users to easily change settings
    #cf = classSettings.Setting(user, password, db_name, port, host)
    #config_dict =cf.assign_settings()
    #print(cf.company)
    #print(config_dict)

# Check if people_database has entries. If it is empty immidiately open settings html to add employees.

# Create person object for output to flask

# Run DB search to match idnumber to name

# Update flask server with person output

# Send clock in time to timesheet DB 

