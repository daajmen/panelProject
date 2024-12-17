import threading
from flask import Flask, render_template, request
from utils.API_tools import fetchCalendar, fetchHourlyWeather, activate_script,fetch_value
from adb_scheduler import start_adb_scheduler  # Importera din ADB-logik
from utils.handlerSQL import fetch_database, fetch_healthresults  # Importera SQL-logiken från handlerSQL.py
from utils.sql_receipt_handler import present_data
from utils.api_skolmaten import fetch_skolmat
from utils.sql_money import insert_accountbalance, create_database, get_connection

app = Flask(__name__)

# CLI-loop för att hantera terminalkommandon
def command_line_interface():
    while True:
        command = input("Skriv ett kommando (fetch, avsluta): ")
        
        if command == "create_db":
            create_database()
        else:
            print("Ogiltigt kommando.")


@app.route('/')
def home():

    daily_weather = fetchHourlyWeather()
    week_data = fetchCalendar()
    health_data = fetch_healthresults()
    lunch_week = fetch_skolmat()
    electric_price = fetch_value('sensor.furulundsvagen_5a_elpris')
    hanna_carBattery = fetch_value('sensor.battery_level')
    
    return render_template('index.html',week_data=week_data, 
        weather_data= {'current_temp': daily_weather.current_temp,
                        'max_temp': daily_weather.max_temp,
                        'min_temp': daily_weather.min_temp,
                        'condition': daily_weather.hourly_forecasts[0].condition},

        health_data= {'work_status': health_data.work_status,
                      'sleep_status': health_data.sleep_status, 
                      'private_status': health_data.private_status},
        lunch = {
            'måndag' : lunch_week['rätt_1'],
            'tisdag' : lunch_week['rätt_2'],
            'onsdag' : lunch_week['rätt_3'],
            'torsdag' : lunch_week['rätt_4'],
            'fredag' : lunch_week['rätt_5']},
        elpris = {'actual_price' : electric_price},
        hanna_bil = {'battery' : hanna_carBattery})

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

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        date = request.form.get('date')
        food_account = request.form.get('food_account') or None
        buffer = request.form.get('buffer') or None

        insert_accountbalance(date, food_account, buffer)

    # Hämta all data för grafen
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT datum, matkonto, buffert FROM account_balance ORDER BY datum")
            data = cursor.fetchall()

    # Skicka datan som en lista till frontend
    return render_template('account.html', balances=data)


@app.route('/api/clean', methods=['POST'])
def clean():
    data = request.json  # Få JSON-data från klienten
    action = data.get('action')  # Läs vilken åtgärd som begärts
    
    # Hantera olika knapptryck
    if action == 'cleanLivingroom':
        activate_script('script.stada_vardagsrum')

    elif action == 'cleanKitchen':
        activate_script('script.stada_kok')

    elif action == 'cleanDiningroom':
        activate_script('script.stada_matsal')

    elif action == 'cleanAbort':
        activate_script('script.skicka_hem_dammsugare')
    else:
        return {'status': 'error', 'message': 'Okänd åtgärd'}, 400
    
    # Returnera svar till frontend
    return {'status': 'success', 'message': f"Åtgärden '{action}' har utförts."}


if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5001))
    flask_thread.start()
    
    # Starta CLI för att hantera kommandon i terminalen
    command_line_interface()