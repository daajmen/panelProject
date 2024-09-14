from flask import Flask, render_template, request
from utils.API_tools import fetchCalendar
from adb_scheduler import start_adb_scheduler  # Importera din ADB-logik

app = Flask(__name__)

@app.route('/')
def home():
    # Hämta kalenderdata dynamiskt
    week_data = fetchCalendar()
    
    # Skicka kalenderdatan till din HTML-mall
    return render_template('index.html', week_data=week_data)


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
    app.run(host='0.0.0.0', port=5001)
