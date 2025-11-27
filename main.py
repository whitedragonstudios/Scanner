import classInstall, classSettings
from server import app, frontend

reset = False

if __name__ == "__main__":
    cf = None
    if reset == True:
        initalize = classInstall.Postgre_Install()
        initalize.drop_tables("people_database") #uncomment if you need to reset people_database table
        initalize.drop_tables("timesheet_database") #uncomment if you need to reset timesheet_database table
        initalize.drop_tables("config_database") #uncomment if you need to reset config_database table
        initalize.drop_tables("email_list") #uncomment if you need to reset email_list table
        initalize.drop_database('scanner') #uncomment if you need to reset database
        initalize.drop_user('marcus') #uncomment if you need to reset user
    try:
        # Load config file
        cf = classSettings.Setting()
        print("Settings loaded successfully.")
        #print(cf.data)
    except Exception as e:
        print(f"Failed to load settings: {e}")
        print("Initializing installation process...")
        # Run classInstall and check the server connection works, if not updates path and installs psql.
        initalize = classInstall.Postgre_Install()
        # run controls the flow of classInstall
        initalize.run()
        # initalize.insert_test_data() # uncomment to add test data to people and email databases
        cf = classSettings.Setting()
        print("Settings loaded successfully.")
    try:
        if cf.config_status == "True":
            # Launcher server
            app.register_blueprint(frontend)
            app.run(host="0.0.0.0", port=2000, debug=True)
            #serve(app, host="0.0.0.0", port=2000))
            pass
            
        else:
            print("Configuration status is False. Please complete the installation process.")
    except Exception as e:
        print(f"Error during startup: {e}")
        print("Please complete the installation process.")


