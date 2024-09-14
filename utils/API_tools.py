from secret import API_KEY
import requests
import datetime

# Hämta dagens datum
today = datetime.datetime.utcnow()

# Beräkna 30 dagar framåt
end_date = today + datetime.timedelta(days=30)

# Din Long-lived access token för autentisering
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "content-type": "application/json",
}

def fetchCalendar(): 
    url = "http://192.168.50.11:8123/api/calendars/calendar.hanna_alex_bastisar"

    # Använd dagens datum och 30 dagar framåt
    params = {
        "start": today.strftime("%Y-%m-%dT%H:%M:%SZ"),  # Format till ISO 8601
        "end": end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    # Skicka GET-begäran
    response = requests.get(url, headers=headers, params=params) 

    if response.status_code == 200:
        events = response.json()
        return events
    else:
        print(f"Fel: {response.status_code}")
        return None
