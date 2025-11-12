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

class weather_report():
    def __init__(self, city_name, weather_key):
        self.city_name = city_name
        self.weather_key = weather_key
        gps = self.get_gps(self.city_name)
        self.longitude = gps[0]
        self.latitude = gps[1]
        self.city = gps[2]
        self.state = gps[3]
        self.country = gps[4]
        data = self.get_weather()
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
        self.update_config()


    def get_gps(self,city):
        try: 
            GPS_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={self.weather_key}").json()
            #print(GPS_response)
            if not GPS_response:
                print(f"WARNING: No results found for city '{city}'. Using default (New York City).")
                return [-74.0060152, 40.7127281, "New York", "NY", "US"]

            country = GPS_response[0].get('country', 'US')
            state = GPS_response[0].get('state', '')
            name = GPS_response[0].get('name', city)
            lon = GPS_response[0].get('lon', -74.0060152)
            lat = GPS_response[0].get('lat', 40.7127281)
            return [lon, lat, name, state, country]
        
        except requests.exceptions.RequestException as e:
            print("ERROR: weather.get_gps >>> api request >>>", e)
            GPS_response = [-74.0060152, 40.7127281, "New York", "NY", "US"]
            return GPS_response
    

    def get_weather(self):
        try: 
            WEATHER_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.weather_key}").json()
        except requests.exceptions.RequestException as e:
            print("ERROR: weather.get_weather >>> api request >>>", e)
            WEATHER_response = "Error Weather Data"
        #print(WEATHER_response)
        return WEATHER_response
    

    def update_config(self):
        conn = Handler(user, password, db_name, port, host)
        conn.update_config('city', self.city)
        conn.update_config('lon', self.longitude)
        conn.update_config('lat', self.latitude)
        conn.update_config('country', self.country)
    

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
            cardinal = ""
            print("ERROR: (wind_direction) assigning >>> wind_dir")
        # print("CF --- wind_direction RUN")
        return cardinal
