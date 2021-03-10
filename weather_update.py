# -*- coding: utf-8 -*-

from data import DARK_SKY_API_KEY
from get_json import get_json
import datetime

url = 'https://api.darksky.net/forecast/8bd8d54b4b0561468f1f52090d22bc45/51.68186,-1.40617/?units=uk2'

def get_forecast(url):
    
    forecast = get_json(url)

    return forecast

def get_current_conditions():
    
    forecast = get_forecast(url)
    summary = forecast['currently']['summary']
    temperature = int(round(forecast['currently']['temperature'],0))
    rain_chance = int(round(forecast['currently']['precipProbability'] * 100, 0))
    wind_speed = int(round(forecast['currently']['windSpeed'], 0))
    wind_bearing = forecast['daily']['data'][0]['windBearing']
    if wind_bearing <= 22.5 or wind_bearing >= 337.5:
        wind_direction = 'S'
    elif wind_bearing <= 67.5:
        wind_direction = 'SW'
    elif wind_bearing <= 112.5:
        wind_direction = 'W'
    elif wind_bearing <= 157.5:
        wind_direction = 'NW'
    elif wind_bearing <= 202.5:
        wind_direction = 'N'
    elif wind_bearing <= 247.5:
        wind_direction = 'NE'
    elif wind_bearing <= 292.5:
        wind_direction = 'E'
    elif wind_bearing <= 337.5:
        wind_direction = 'SE'
    
    hourly = forecast['hourly']['summary']

    return temperature, summary, rain_chance, wind_speed, wind_direction, hourly
    
if __name__ == '__main__':
    
    t, sum, r, w, d, h = get_current_conditions()
    print(t)
    print(sum)
    print(r)
    print(w)
    print(d)
    print(h)
