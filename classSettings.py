import psycopg2
from classHandler import Handler


class Setting:
    def __init__(self, user, password, dbname, port, host):
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.host = host
        DBpeople = "people_database"
        DBtime = "timesheet_database"
        DBrole = "role"
        DBconfig = "config_database"
    
    
    def assign_settings(self):
        db=Handler(dbname=self.dbname, user=self.user, password=self.password, autorun=False)
        data = db.request_config()
        self.config_dict = data
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

        
