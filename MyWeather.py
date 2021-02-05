class WeatherClass:

    class ForecastClass:
        maxtemp = ''
        mintemp = ''
        condition = ''
        def __init__(self, jsonData):
            self.mintemp = jsonData['forecastday'][0]['day']['mintemp_c']
            self.maxtemp = jsonData['forecastday'][0]['day']['maxtemp_c']
            self.condition = jsonData['forecastday'][0]['day']['condition']['text']

            
    city = ''
    region = ''
    country = ''
    localtime = ''

    currenttemp = ''
    condition = ''
    humidity = ''
    cloud = ''
    
    forecast = None
    
    def __init__(self, jsonData):
        self.city = jsonData['location']['name']
        self.region = jsonData['location']['region']
        self.country = jsonData['location']['country']
        self.localtime = jsonData['location']['localtime']
        
        self.currenttemp = jsonData['current']['temp_c']
        self.condition = jsonData['current']['condition']['text']
        self.humidity = jsonData['current']['humidity']
        self.cloud = jsonData['current']['cloud']

        jsonForecastData = jsonData['forecast']
        self.forecast = self.ForecastClass(jsonForecastData)





import requests
import json
import os
import time


key = os.getenv("WEATHER_KEY")


def getWeather(local):
    time.sleep(2)
    request = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={key}={local}&days=1')
    weatherJson = request.json()
    return WeatherClass(weatherJson)

def getIconUrl(condition):
    condition = condition.lower()
    id = '01d'

    if(condition.find('cloud') != -1):
        id = '02d'
    elif(condition.find('rain') != -1):
        if(condition.find('heavy') != -1):
            id = '09d'
        else:
            id= '10d' 
    elif(condition.find('clear') != -1):
        id= '01d'
    elif(condition.find('snow') != -1):
        id= '13d'
    elif(condition.find('thunderstorm') != -1):
        id= '11d'
    elif(condition.find('') != -1):
        id= '11d'
    
    
    return f"http://openweathermap.org/img/wn/{id}@4x.png"
