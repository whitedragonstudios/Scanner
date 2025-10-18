# Scanner/initialization.py

import psycopg2
import json
import csv
import os
import openpyxl
import pandas as pd

postgressql_host = "localhost"
postgressql_employee_db = "people"
postgressql_timesheet_db = "timesheet"
postgressql_user = "marcus"
postgressql_password = "stoic"


# Load a config file which allows users to easily change settings NOTE this may be changed to postgre DB in the future. 
def load_config():
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')
    try:
        with open(config_path,"r") as config_file:
            config = json.load(config_file)
            print("Config file loaded.")
    except FileNotFoundError:
        config = {"placeholder_key": "placeholder_value"}
        print("Config file not found. Using default settings.") 
    return config

config = load_config()

paths = [config.get("CSV_path"), config.get("XLSX_path"), config.get("JSON_path")]
print(paths)
for item in paths:
    if item is not None:
        filetype_path = item
        print("Database source is: ", filetype_path)
        break
