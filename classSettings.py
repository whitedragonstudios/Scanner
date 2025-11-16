from classHandler import Handler


class Setting:
    def __init__(self, autorun=True):
        if autorun:
            self.data = self.assign_settings()
    
    
    # Setting can be accessed in two ways through a dictionary returned or through individual class attributes. Must test which is more efficient
    def assign_settings(self):
        # Uses handler to retrieve config settings from database.
        self.user_handle=Handler(profile='user')
        # data is also the raw dictionary which is returned from this method.
        data = self.user_handle.send_query("SELECT key, value FROM config_database;")
        print(data)
        data = dict(data)
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
    
    
    def start_settings(self):
        return{
                "config_status": "False",
                "config_date": "2025-01-01",
                "webpage_title": "Populus Numerus",
                "company": "Scanner",
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
                "weather_key": "baeb0ce1961c460b651e6a3a91bfeac6",
                "country": "us",
                "news_key": "04fbd2b9df7b49f6b6a626b4a4ae36be"
                }