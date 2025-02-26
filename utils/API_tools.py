import datetime
import requests 
from secret import API_KEY


def fetchCalendar(): 
    url = "http://192.168.50.11:8123/api/calendars/calendar.hanna_alex_bastisar"

    # Hämta dagens datum
    today = datetime.datetime.utcnow()

    # Beräkna 30 dagar framåt
    end_date = today + datetime.timedelta(days=14)

    # Din Long-lived access token för autentisering
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }

    # Använd dagens datum och 30 dagar framåt
    params = {
        "start": today.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end": end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    # Skicka GET-begäran
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        events = response.json()
        
        # Strukturera data
        structured_data = {}
        for event in events:
            # Extrahera datum och tid
            if 'dateTime' in event['start']:
                event_date = event['start']['dateTime'][:10]  # YYYY-MM-DD format
                event_time = event['start']['dateTime'][11:16]  # HH:MM format
            else:
                event_date = event['start']['date']  # För heldagshändelser
                event_time = "Heldag"

            # Beräkna veckodagen
            event_date_obj = datetime.datetime.strptime(event_date, "%Y-%m-%d")
            day_of_week = event_date_obj.strftime("%A")

            # Lägg till händelsen under rätt dag och datum
            if event_date not in structured_data:
                structured_data[event_date] = {'tasks': [], 'day_of_week': day_of_week}

            # Lägg till både tid och beskrivning
            structured_data[event_date]['tasks'].append(f"{event_time} - {event['summary']}")
        

        return structured_data
    else:
        print(f"Fel: {response.status_code}")
        return None


class HourlyWeather:
    def __init__(self, condition, temperature, wind_speed, time):
        self.condition = condition
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.time = time

class DailyWeather:
    def __init__(self):
        self.hourly_forecasts = []
        self.max_temp = None
        self.min_temp = None
        self.current_temp = None

    def add_hourly_forecast(self, forecast):
        self.hourly_forecasts.append(forecast)
        # Uppdatera max och min temperatur
        if self.max_temp is None or forecast.temperature > self.max_temp:
            self.max_temp = forecast.temperature
        if self.min_temp is None or forecast.temperature < self.min_temp:
            self.min_temp = forecast.temperature

    def set_current_temp(self, temp):
        self.current_temp = temp


def fetchHourlyWeather():
    url = "http://192.168.50.11:8123/api/services/weather/get_forecasts?return_response=true"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }
    data = {
        "type": "hourly",
        "entity_id": "weather.hem",
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        weather_data = response.json()

        daily_weather = DailyWeather()

        # Bearbeta varje timme i forecast
        for forecast in weather_data['service_response']['weather.hem']['forecast']:
            hourly_weather = HourlyWeather(
                condition=forecast['condition'],
                temperature=forecast['temperature'],
                wind_speed=forecast['wind_speed'],
                time=forecast['datetime']
            )
            daily_weather.add_hourly_forecast(hourly_weather)
        
        # Sätt aktuell temperatur (första timmen i forecast kan representera nuvarande)
        daily_weather.set_current_temp(weather_data['service_response']['weather.hem']['forecast'][0]['temperature'])

        return daily_weather
    else:
        print("Error fetching weather data")


def activate_script(script_to_run):

    url = "http://192.168.50.11:8123/api/services/script/turn_on"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }
    data = {
        "entity_id": script_to_run,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print('yep, script run')
    else: 
        print('failed.')

def fetch_value(entity):

    url = f"http://192.168.50.11:8123/api/states/{entity}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['state']
    else: 
        print('failed.')

def notify_with_tibber(message): 

    url = "http://192.168.50.11:8123/api/services/notify/tibber"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }
    data = {
        "message": message,
    }

    response = requests.post(url, headers=headers, json=data)


