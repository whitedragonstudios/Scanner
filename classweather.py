import requests, json
from classSettings import Setting
from classHandler import Handler


import databaseConfig
db = databaseConfig. databaseSettings()
user = db["user"]
password = db["password"]
db_name = db["db_name"]
port = db["port"]
host = db["host"]

# weather report uses an api to send weather to the flask interface
class weather_report():
    def __init__(self, city_name, weather_key):
        # city name and weather key come from config database.
        self.city_name = city_name
        self.weather_key = weather_key
        # API needs gps coordinates so city has to be passed to get_gps
        gps = self.get_gps(self.city_name)
        self.longitude = gps[0]
        self.latitude = gps[1]
        self.city = gps[2]
        self.state = gps[3]
        self.country = gps[4]
        # Once gps is retrieved a second call to get_weather is performed
        data = self.get_weather()
        # response is formatted for direct output.
        self.description = data['weather'][0]['description'].title()
        self.icon = data['weather'][0]['icon'] + ".png"
        self.feel = int((data['main']['feels_like']) * 1.8 - 459.67)
        min = int((data['main']['temp_min']) * 1.8 - 459.67)
        max = int((data['main']['temp_max']) * 1.8 - 459.67)
        self.temp = f"{min} - {max}"
        self.humid = data['main']['humidity']
        self.clouds = data['clouds']['all']
        dir = self.wind_direction(data['wind']['deg'])
        self.wind = f"{dir} {int(data['wind']['speed'])}mp/h "
        # config database is updated with changes to match new city
        self.update_config()


    # Get gps passes city to return long and lat
    def get_gps(self,city):
        try:
            # requests api response
            GPS_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={self.weather_key}").json()
            #print(GPS_response)
            if not GPS_response:
                print(f"WARNING: No results found for city '{city}'. Using default (New York City).")
                # Returns usable list with default data sets
                return [-74.0060152, 40.7127281, "New York", "NY", "US"]
            # Extract list and dictionary to get usable data.
            country = GPS_response[0].get('country', 'US')
            state = GPS_response[0].get('state', '')
            name = GPS_response[0].get('name', city)
            lon = GPS_response[0].get('lon', -74.0060152)
            lat = GPS_response[0].get('lat', 40.7127281)
            # return a list
            return [lon, lat, name, state, country]
        
        except requests.exceptions.RequestException as e:
            print("ERROR: weather.get_gps >>> api request >>>", e)
            # Returns usable list with default data sets
            return [-74.0060152, 40.7127281, "New York", "NY", "US"]
    

    #Get weather makes second call to the api for detailed weather 
    def get_weather(self):
        # api call uses gps coordinates from get gps
        try: 
            WEATHER_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.weather_key}").json()
        except requests.exceptions.RequestException as e:
            print("ERROR: weather.get_weather >>> api request >>>", e)
            WEATHER_response = "Error Weather Data" # should add default data response
        #print(WEATHER_response)
        # Returns full dict
        return WEATHER_response
    

    # update config sends gps city and country data to the config database
    def update_config(self):
        conn = Handler(user, password, db_name, port, host)
        conn.update_config('city', self.city)
        conn.update_config('lon', self.longitude)
        conn.update_config('lat', self.latitude)
        conn.update_config('country', self.country)
    
    # Weather direction translates degrees returned from api to cardinal directions.
    def wind_direction(self, wind_dir):
        try:
            wind_float = float(wind_dir)
            if wind_float in range(23, 66): cardinal = 'NE'
            elif wind_float in range(67, 112): cardinal = 'E'
            elif wind_float in range(113, 156): cardinal = 'SE'
            elif wind_float in range(157, 202): cardinal = 'S'
            elif wind_float in range(203, 246): cardinal = 'SW'
            elif wind_float in range(247, 292): cardinal = 'W'
            elif wind_float in range(293, 336): cardinal = 'NW'
            else: cardinal = 'N' # 0-22 and 337-360
        except: 
            # returns a blank string
            cardinal = " "
            print("ERROR: (wind_direction) assigning >>> wind_dir")
        # print("CF --- wind_direction RUN")
        return cardinal
