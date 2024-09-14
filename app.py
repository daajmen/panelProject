from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Skapa en lista med veckodagar och tillhörande uppgifter
    week_data = [
        {'day': 'Måndag', 'tasks': ['Uppgift 1', 'Uppgift 2']},
        {'day': 'Tisdag', 'tasks': ['Uppgift 1', 'Uppgift 2']},
        {'day': 'Onsdag', 'tasks': ['Uppgift 1', 'Uppgift 2']},
        {'day': 'Torsdag', 'tasks': ['Uppgift 1', 'Uppgift 2']},
        {'day': 'Fredag', 'tasks': ['Uppgift 1', 'Uppgift 2']},
        {'day': 'Lördag', 'tasks': ['Uppgift 1', 'Uppgift 2']},
        {'day': 'Söndag', 'tasks': ['Uppgift 1', 'Uppgift 2']}
    ]
    return render_template('index.html', week_data=week_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
