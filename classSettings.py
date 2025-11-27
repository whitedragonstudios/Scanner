from classHandler import Handler
from datetime import datetime as dt


class Setting:
    def __init__(self, autorun=True):
        # Uses handler to retrieve config settings from database.
        self.user_handle=Handler(profile='user')
        if autorun:
            data = self.user_handle.send_query("SELECT key, value FROM config_database;")
            data = dict(data)
            self.data = self.assign_settings(data)

    
    # Setting can be accessed in two ways through a dictionary returned or through individual class attributes. Must test which is more efficient
    def assign_settings(self, data):
        #print(data)
        self.config_status = data["config_status"]
        self.config_date = data["config_date"]
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
        self.sender_email = data["sender_email"]
        self.sender_password = data["sender_password"]
        self.last_email = data["last_email_date"]
        return data
    
    # This method stotres default color settings.
    def default_colors(self):
        return { 
            "main_background_color" : "#0a0a1f",
            "main_text_color" : "#ffffff",
            "content_color" : "#020203",
            "content_text_color" : "#ffffff",
            "sidebar_color" : "#193763",
            "sidebar_text_color" : "#ffffff",
            "button_color" : "#1a73ff",
            "button_text_color" : "#ffffff",
            "button_hover_color" : "#0050b3",  
            "border_color" : "#3399ff"
            }
    

    def default_config(self):
        return{
                "config_status": "True",
                "config_date": dt.now().strftime("%m-%d-%y"),
                "webpage_title": "TimeWise Gateway",
                "company": "TimeWise",
                "city": "New York City",
                "lon": "-74.0060152",
                "lat": "40.7127281",
                "country": "us",
                }
    
    
    def start_settings(self):
        return{
                "config_status": "True",
                "config_date": dt.now().strftime("%m-%d-%y"),
                "webpage_title": "TimeWise Gateway",
                "company": "TimeWise",
                "main_background_color": "#0a0a1f",
                "main_text_color": "#f0f0f0",
                "content_color": "#1c1c33",
                "content_text_color": "#ffffff",
                "sidebar_color": "#193763",
                "sidebar_text_color": "#ffffff",
                "button_color": "#1a73ff",
                "button_text_color": "#ffffff",
                "button_hover_color": "#0050b3",
                "border_color": "#3399ff",
                "city": "New York City",
                "lon": "-74.0060152",
                "lat": "40.7127281",
                "country": "us",
                # is setup in intial config does not get reset
                "weather_key": "baeb0ce1961c460b651e6a3a91bfeac6",
                "news_key": "04fbd2b9df7b49f6b6a626b4a4ae36be",
                "sender_email": "timewisemailer@gmail.com",
                "sender_password": "qtwd mvdt kcgt acmz",
                "last_email_date": dt.now().strftime("%m-%d-%y")
                }