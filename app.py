from flask import Flask, render_template
from utils.API_tools import fetchCalendar

app = Flask(__name__)

@app.route('/')
def home():
    # Hämta kalenderdata dynamiskt
    week_data = fetchCalendar()
    
    # Skicka kalenderdatan till din HTML-mall
    return render_template('index.html', week_data=week_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
