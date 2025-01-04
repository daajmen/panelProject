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

    # Beräkna medelvärde
    matkonto_values = [row[0] for row in rows if row[0] is not None]
    buffert_values = [row[1] for row in rows if row[1] is not None]

    matkonto_avg = sum(matkonto_values) / len(matkonto_values) if matkonto_values else 0
    buffert_avg = sum(buffert_values) / len(buffert_values) if buffert_values else 0    


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

    cursor.close()
    conn.close()

    return round(matkonto_avg,2), round(buffert_avg,2), latest_matkonto, latest_buffert