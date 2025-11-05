import requests, json
from classSettings import Setting
import databaseConfig


class weather_report():
    def __init__(self, city_name, weather_key):
        self.city_name = city_name
        self.weather_key = weather_key
        gps = self.get_gps()
        self.longitude = gps[0]
        self.latitude = gps[1]
        self.city = gps[2]
        self.state = gps[3]
        self.country = gps[4]
        data = self.get_weather()
        self.description = data['weather'][0]['description'].title()
        self.icon = data['weather'][0]['icon'] + ".png"
        self.feel = int((data['main']['feels_like']) * 1.8 - 459.67)
        self.min = int((data['main']['temp_min']) * 1.8 - 459.67)
        self.max = int((data['main']['temp_max']) * 1.8 - 459.67)
        self.humid = data['main']['humidity']
        self.clouds = data['clouds']['all']
        print(self.icon)


    def get_gps(self):
        try: 
            GPS_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={self.city_name}&appid={self.weather_key}").json()
        except requests.exceptions.RequestException as e:
            print("ERROR: weather.get_gps >>> api request >>>", e)
            GPS_response = 40.7127281,-74.0060152 # Defaults to New York City
        return [GPS_response[0]["lon"], GPS_response[0]["lat"], GPS_response[0]['name'], GPS_response[0]['state'], GPS_response[0]['country']]
    

    def get_weather(self):
        try: 
            WEATHER_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.weather_key}").json()
        except requests.exceptions.RequestException as e:
            print("ERROR: weather.get_weather >>> api request >>>", e)
            WEATHER_response = "Error Weather Data"
        return WEATHER_response

