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
postgressql_role_db= "role"
postgressql_config = "scanner"
postgressql_user = "marcus"
postgressql_password = "stoic"

# Load a config file which allows users to easily change settings NOTE this may be changed to postgre DB in the future. 
#def load_config():
#    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')
#    try:
#        with open(config_path,"r") as config_file:
#            config = json.load(config_file)
#            print("Config file loaded.")
#    except FileNotFoundError:
#        config = {"placeholder_key": "placeholder_value"}
#        print("Config file not found. Using default settings.") 
#    return config

# config = load_config()


class Setting:
    def __init__(self):
        self.assign_setting()
    def connect_db(self):
        connect = psycopg2.connect(
            host = postgressql_host,
            dbname = postgressql_config,
            user = postgressql_user,
            password = postgressql_password,
            port = 5000
            )
        return connect
    def request_config(self):
        db=self.connect_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM config_database;")
            config_data = cursor.fetchall()
            config = {row[0]: row[1] for row in config_data}
        db.close()
        return config
    def update_config(self, key, value):   
        db = self.connect_db()
        with db.cursor() as cursor:
            cursor.execute("UPDATE config_table SET value = %s WHERE key = %s;", (value, key))
            db.commit()
        db.close()
    def assign_settings(self):
        data = self.request_config()
        self.config_status = data["config_status"]
        self.config_date = data["config_date"]
        self.CSV_path = data["CSV_path"]
        self.XLSX_path = data["XLSX_path"]
        self.JSON_path = data["JSON_path"]
        self.webpage_title = data["webpage_title"]
        self.company = data["company"]
        self.mainbackground_color = data["main_background_color"]
        self.main_text_color = data["main_text_color"]
        self.button_color = data["button_color"]
        self.button_text_color = data["button_text_color"]
        self.button_border_color = data["button_border_color"]
        self.button_border_hover_color = data["button_border_hover_color"]
        self.sidebar_color = data["sidebar_color"]
        self.sidebar_text_color = data["sidebar_text_color"]

        
setting = Setting()

paths = setting.CSV_path, setting.XLSX_path, setting.JSON_path
print(paths)
for item in paths:
    if item is not None:
        filetype_path = item
        print("Database source is: ", filetype_path)
        break
