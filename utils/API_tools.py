import datetime
import requests 
from secret import API_KEY


def fetchCalendar(): 
    # Hämta dagens datum
    today = datetime.datetime.utcnow()

    # Beräkna 30 dagar framåt
    end_date = today + datetime.timedelta(days=30)
    
    url = "http://192.168.50.11:8123/api/calendars/calendar.hanna_alex_bastisar"


    # Din Long-lived access token för autentisering
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }

    # Använd dagens datum och 30 dagar framåt
    params = {
        "start": today.strftime("%Y-%m-%dT%H:%M:%SZ"),  # Format till ISO 8601
        "end": end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    # Skicka GET-begäran
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        events = response.json()
        
        # Strukturera data
        structured_data = {}
        for event in events:
            # Extrahera datum (dagens datum)
            if 'dateTime' in event['start']:
                event_date = event['start']['dateTime'][:10]  # YYYY-MM-DD format
            else:
                event_date = event['start']['date']  # För heldagshändelser

            # Beräkna veckodagen
            event_date_obj = datetime.datetime.strptime(event_date, "%Y-%m-%d")
            day_of_week = event_date_obj.strftime("%A")  # Exempel: "Monday"
            
            # Lägg till händelsen under rätt dag och datum
            if event_date not in structured_data:
                structured_data[event_date] = {'tasks': [], 'day_of_week': day_of_week}
            
            structured_data[event_date]['tasks'].append(event['summary'])
        
        return structured_data
    else:
        print(f"Fel: {response.status_code}")
        return None
