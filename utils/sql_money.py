import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

def get_connection():
    return psycopg2.connect(
        host="192.168.50.16",
        database="account_balance",
        user="postgres",
        password= '',
        port=5432
    )

def create_database():
    # Anslut till PostgreSQL-databasen
    conn = get_connection()
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
    with get_connection() as conn:
        # Skapar en cursor för att exekvera SQL-frågor
        with conn.cursor() as cursor:
            # SQL-fråga för att infoga data i account_balance-tabellen
            cursor.execute('''
                INSERT INTO account_balance (datum, matkonto, buffert)
                VALUES (%s, %s, %s)
            ''', (date, food_account, buffer))  # Parametriserade värden för att förhindra SQL-injektion
            
            # Bekräftar (commitar) ändringarna i databasen
            conn.commit()

def calculate_last_7_days(): 
    conn = get_connection()
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