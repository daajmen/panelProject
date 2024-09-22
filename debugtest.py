import datetime
import requests 
from secret import API_KEY


def fetchHourlyWeather():
    # URL för att hämta väderdata från Home Assistant API
    url = "http://192.168.50.11:8123/api/services/weather/get_forecasts?return_response=true"

    # Din Long-lived access token för autentisering
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }
    data = {
        "type" : "hourly",
        "entity_id" : "weather.hem",
    }

    # Skicka GET-begäran
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        weather_data = response.json()

        print(weather_data)

        # Hämta relevanta attribut från 'attributes'
        attributes = weather_data['attributes']
        structured_weather_data = {
            'temperature': attributes.get('temperature'),
            'condition': weather_data.get('state'),  # 'state' håller väderbeskrivningen (t.ex. partlycloudy)
            'humidity': attributes.get('humidity'),
            'wind_speed': attributes.get('wind_speed'),
            'wind_gust_speed': attributes.get('wind_gust_speed'),
            'cloud_coverage': attributes.get('cloud_coverage'),
            'pressure': attributes.get('pressure'),
            'last_updated': weather_data.get('last_updated')
        }

        return structured_weather_data
    else:
        print(f"Fel: {response.status_code}")
        print(data)
        print (response.json())
        return None
    
fetchHourlyWeather()