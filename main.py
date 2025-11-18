import classInstall, classSettings


if __name__ == "__main__":
    # Run classInstall and check the server connection works, if not updates path and installs psql.
    initalize = classInstall.Postgre_Install()
    initalize.drop_tables("people_database") #uncomment if you need to reset people_database table
    initalize.drop_tables("timesheet_database") #uncomment if you need to reset timesheet_database table
    initalize.drop_tables("config_database") #uncomment if you need to reset config_database table
    initalize.drop_tables("email_list") #uncomment if you need to reset email_list table
    initalize.drop_database('scanner') #uncomment if you need to reset database
    initalize.drop_user('marcus') #uncomment if you need to reset user
    # run controls the flow of classInstall
    initalize.run()
    #initalize.insert_test_data() # uncomment to add test data to people and email databases
 
    # Load a config file which allows users to easily change settings
    cf = classSettings.Setting()
    print(cf.data)

# Check config statue if false loop back to initialize phase 

# Run app factory ==> routes ==> services



# Create person object for output to flask

# Run DB search to match idnumber to name

# Update flask server with person output

# Send clock in time to timesheet DB 

