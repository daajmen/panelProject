import psycopg2
from psycopg2 import sql

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
