import threading
from flask import Flask, render_template, request
from utils.API_tools import fetchCalendar, fetchHourlyWeather
from adb_scheduler import start_adb_scheduler  # Importera din ADB-logik
from utils.handlerSQL import fetch_database, fetch_healthresults  # Importera SQL-logiken från handlerSQL.py
from utils.sql_receipt_handler import present_data

app = Flask(__name__)

# CLI-loop för att hantera terminalkommandon
def command_line_interface():
    while True:
        command = input("Skriv ett kommando (fetch, avsluta): ")
        
        if command == "fetchsql":
            present_data(); 
            print('Har kört kommando')
        elif command == "avsluta":
            print("Stänger ner CLI...") 
            break
        else:
            print("Ogiltigt kommando.")


@app.route('/')
def home():

    daily_weather = fetchHourlyWeather()
    week_data = fetchCalendar()
    health_data = fetch_healthresults()
    monthly_summaries = present_data()
    
    return render_template('index.html',week_data=week_data, 
        weather_data= {'current_temp': daily_weather.current_temp,
                        'max_temp': daily_weather.max_temp,
                        'min_temp': daily_weather.min_temp,
                        'condition': daily_weather.hourly_forecasts[0].condition},

        health_data= {'work_status': health_data.work_status,
                      'sleep_status': health_data.sleep_status, 
                      'private_status': health_data.private_status},
        monthly_expenses = {
            'januari': monthly_summaries[0][1],
            'februari': monthly_summaries[1][1],
            'mars': monthly_summaries[2][1],
            'april': monthly_summaries[3][1],
            'maj': monthly_summaries[4][1],
            'juni': monthly_summaries[5][1],
            'juli': monthly_summaries[6][1],
            'augusti': monthly_summaries[7][1],
            'september': monthly_summaries[8][1],
            'oktober': monthly_summaries[9][1],
            'november': monthly_summaries[10][1],
            'december': monthly_summaries[11][1]})

@app.route('/debug', methods=['GET', 'POST'])
def debug():
    if request.method == 'POST':
        ip = request.form['ip']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        # Anropa funktionen för att starta ADB-schemaläggningen
        start_adb_scheduler(ip, start_time, end_time)

        return f"ADB commands will run between {start_time} and {end_time} on IP: {ip}"

    return render_template('debug.html')


if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5001))
    flask_thread.start()
    
    # Starta CLI för att hantera kommandon i terminalen
    command_line_interface()