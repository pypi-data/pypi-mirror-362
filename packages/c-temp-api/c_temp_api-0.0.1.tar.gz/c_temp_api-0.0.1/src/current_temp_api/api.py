from .base import WeatherAPIBase
import requests

class OpenMeteo(WeatherAPIBase):

    def __init__(self, latitude, longitude, **kwargs):
        self.lat = latitude
        self.long = longitude


    def get_current_temperature(self):
        params = {"latitude":self.lat, "longitude":self.long, "current_weather":True}

        result = requests.get("https://api.open-meteo.com/v1/forecast", params=params)

        result_json = result.json()

        return result_json["current_weather"]["temperature"]


class OpenWeather(WeatherAPIBase):

    def __init__(self, latitude, longitude, **kwargs):
        self.lat = latitude
        self.long = longitude
        self.api_token = kwargs.get("api_token")


    def get_current_temperature(self):
        params = {"lat":self.lat, "lon":self.long, "appid":self.api_token}

        result = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)

        result_json = result.json()

        return format(result_json["main"]["temp"] - 273.15,".1f")
