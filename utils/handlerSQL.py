import sqlite3


class HealthObject: 
    def __init__(self,): 
        self.work_status = None
        self.sleep_status = None 
        self.private_status = []

def fetch_database():
    try:
        # Försök att ansluta till databasen
        conn = sqlite3.connect('../wellBeing/db/events.db')
        cursor = conn.cursor()

        # SQL-fråga för att hämta både action och tidsstämpel
        cursor.execute("SELECT action, time_fired FROM events")

        # Hämta alla värden
        data = cursor.fetchall()

    except sqlite3.Error as e:
        # Hantera fel om databasen inte kan nås eller SQL-frågan misslyckas
        print(f"Ett fel uppstod vid anslutning till databasen: {e}")
        data = []  # Returnera en tom lista om något gick fel

    finally:
        # Stäng anslutningen om den existerar
        if 'conn' in locals():
            conn.close()

    return data

def fetch_healthresults():
    data = fetch_database()
    health = []

    def calculate_Procent(data, positiveValue, negativeValue): 
        total_yes = 0
        total_no = 0
        total = 0 

        for action, _ in data: 
            if action == positiveValue:
                total_yes += 1
            elif action == negativeValue: 
                total_no += 1 

        total = total_yes + total_no
        procent = 100 if total_no == 0 else round((total_yes / total) * 100, 1)
        return procent
    
    def calculate_private(data, positive_value, okay_value, negative_value):
        # Initiera räknare
        total_good = 0
        total_okay = 0
        total_bad = 0

        # Loop för att räkna händelser
        for action, _ in data: 
            if action == positive_value:
                total_good += 1
            elif action == okay_value:
                total_okay += 1
            elif action == negative_value: 
                total_bad += 1 

        # Beräkna totalen
        total = total_good + total_okay + total_bad 

        # Initiera procentvärden
        good_percent = 0
        okay_percent = 0
        bad_percent = 0

        # Beräkna procent om det finns en total
        if total > 0: 
            good_percent = round((total_good / total) * 100, 1)
            okay_percent = round((total_okay / total) * 100, 1)
            bad_percent = round((total_bad / total) * 100, 1)

        # Returnera resultat som en tuple
        return good_percent, okay_percent, bad_percent

    health = HealthObject()
 
    health.sleep_status = calculate_Procent(data, 'sleepWell_yes', 'sleepWell_no')
    health.work_status = calculate_Procent(data, 'work_good', 'work_bad')
    health.private_status = calculate_private(data, 'private_good', 'private_okay','private_bad')

    return health 
