import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import pandas as pd

def get_connection(database):
    return psycopg2.connect(
        host="192.168.50.16",
        database=database,
        user="postgres",
        password= '',
        port=5432
    )

def create_database():
    # Anslut till PostgreSQL-databasen
    conn = get_connection('account_balance')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account_balance (
            id SERIAL PRIMARY KEY,
            datum DATE NOT NULL,
            matkonto NUMERIC(10, 2),
            buffert NUMERIC(10, 2)
        )
    ''')
    conn.commit()
    cursor.close()


def insert_accountbalance(date, food_account=None, buffer=None):
    # Skapar en anslutning till databasen med hjälp av get_connection()
    with get_connection('account_balance') as conn:
        # Skapar en cursor för att exekvera SQL-frågor
        with conn.cursor() as cursor:
            # SQL-fråga för att infoga data i account_balance-tabellen
            cursor.execute('''
                INSERT INTO account_balance (datum, matkonto, buffert)
                VALUES (%s, %s, %s)
            ''', (date, food_account, buffer))  # Parametriserade värden för att förhindra SQL-injektion
            
            # Bekräftar (commitar) ändringarna i databasen
            conn.commit()

def insert_household(date, label, person, description, amount):
    # Skapar en anslutning till databasen med hjälp av get_connection()
    with get_connection('household_2024') as conn:
        # Skapar en cursor för att exekvera SQL-frågor
        with conn.cursor() as cursor:
            # SQL-fråga för att infoga data i account_balance-tabellen
            cursor.execute('''
                INSERT INTO household_2024 (label, person, description, amount, date)
                VALUES (%s, %s, %s, %s, %s)
            ''', (label, person, description, amount, date))  # Parametriserade värden för att förhindra SQL-injektion
            
            # Bekräftar (commitar) ändringarna i databasen
            conn.commit()

def get_household_data() -> pd.DataFrame:
    with get_connection('household_2024') as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT label, person, description, amount, date FROM household_2024')
            rows = cursor.fetchall()
            
            # Skapa en DataFrame
            df = pd.DataFrame(rows, columns=['label', 'person', 'description', 'amount', 'date'])
            
            # Konvertera 'amount' och 'date' till rätt typ
            df['amount'] = df['amount'].astype(float)
            df['date'] = pd.to_datetime(df['date'])
            
            return df


def calculate_last_7_days(): 

    def days_until_25th():
        today = datetime.now().date()
        current_year = today.year
        current_month = today.month

        # Datum för den 25:e i den aktuella månaden
        target_date = datetime(current_year, current_month, 25).date()

        # Om dagens datum är efter den 25:e, räkna ut dagar till nästa månads 25:e
        if today > target_date:
            if current_month == 12:
                # Om det är december, gå till januari nästa år
                target_date = datetime(current_year + 1, 1, 25).date()
            else:
                # Annars gå till nästa månad
                target_date = datetime(current_year, current_month + 1, 25).date()

        days_left = (target_date - today).days
        return days_left


    conn = get_connection('account_balance')
    cursor = conn.cursor()

    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)

    # Hämta data från de senaste 7 dagarna
    cursor.execute('''
        SELECT matkonto, buffert
        FROM account_balance
        WHERE datum BETWEEN %s AND %s
    ''', (seven_days_ago, today))
    rows = cursor.fetchall()

    # Hämta det senaste värdet
    cursor.execute('''
        SELECT matkonto, buffert
        FROM account_balance
        ORDER BY datum DESC
        LIMIT 1
    ''')

    latest_row = cursor.fetchone()
    latest_matkonto = latest_row[0] if latest_row and latest_row[0] is not None else 0
    latest_buffert = latest_row[1] if latest_row and latest_row[1] is not None else 0
    days_left = days_until_25th()
    money_left = round(latest_matkonto / days_left, 2) if days_left > 0 else 0
    conn.close()

    return latest_matkonto, latest_buffert, days_left, money_left