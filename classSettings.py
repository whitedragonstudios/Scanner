import psycopg2
from classHandler import Handler


class Setting:
    def __init__(self, user, password, dbname, port, host):
        # Settings must get server creds to send to handler. This may be abstracted to a seperate dictionary which will be accessed seperately
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.host = host
        self.data = self.assign_settings()
        # These variables are unused may be intergrate as settings methods are added.
        #DBpeople = "people_database"
        #DBtime = "timesheet_database"
        #DBrole = "role"
        #DBconfig = "config_database"
    
    
    # Setting can be accessed in two ways through a dictionary returned or through individual class attributes. Must test which is more efficient
    def assign_settings(self):
        # Uses handler to retrieve config settings from database.
        user_handle=Handler(dbname=self.dbname, user=self.user, password=self.password)
        # data is also the raw dictionary which is returned from this method.
        data = user_handle.request_config()
        self.config_status = data["config_status"]
        self.config_date = data["config_date"]
        self.CSV_path = data["CSV_path"]
        self.XLSX_path = data["XLSX_path"]
        self.JSON_path = data["JSON_path"]
        self.webpage_title = data["webpage_title"]
        self.company = data["company"]
        # CSS Variables
        self.main_background_color = data["main_background_color"]
        self.main_text_color = data["main_text_color"]
        self.content_color = data["content_color"]
        self.content_text_color = data["content_text_color"]
        self.sidebar_color = data["sidebar_color"]
        self.sidebar_text_color = data["sidebar_text_color"]
        self.button_color = data["button_color"]
        self.button_text_color = data["button_text_color"]
        self.button_hover_color = data["button_hover_color"]  
        self.border_color = data["border_color"]
        # API Variables
        self.city = data["city"]
        self.lon = data["lon"]
        self.lat = data["lat"]
        self.weather_key=data["weather_key"]
        self.country = data["country"]
        self.news_key = data["news_key"]
        #self.emails = data["emails"]
        return data
        
