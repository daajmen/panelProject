import sqlite3
from datetime import datetime, timedelta

def get_month_range(year, month):
    """Hämtar start och slutdatum för en månad."""
    first_day = datetime(year, month, 1)
    next_month = (first_day + timedelta(days=32)).replace(day=1)
    last_day = next_month - timedelta(days=1)
    return first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')

def fetch_yearly_summaries(cursor, year):
    """Hämtar summor för varje månad under det givna året."""
    monthly_summaries = []

    # Iterera över varje månad (1 till 12) för det givna året
    for month in range(1, 13):
        month_start, month_end = get_month_range(year, month)

        # SQL-fråga för att hämta den totala summan för varje månad
        query = '''
            SELECT SUM(summa) as total_sum
            FROM receipts
            WHERE datum BETWEEN ? AND ?
        '''

        cursor.execute(query, (month_start, month_end))
        result = cursor.fetchone()[0]  # Hämtar summan, om ingen post finns blir det None
        total_sum = round(result,2) if result else 0  # Om resultatet är None, sätt till 0

        # Spara månadens summa och månadens namn
        monthly_summaries.append((month, total_sum))

    return monthly_summaries

def present_data():
    # Koppla upp till databasen
    conn = sqlite3.connect('../receipts_db/receipt_database.db')
    cursor = conn.cursor()

    # Hämta aktuellt år
    current_year = datetime.today().year

    # Hämta summor för varje månad under det aktuella året
    monthly_summaries = fetch_yearly_summaries(cursor, current_year)

    # Stäng uppkopplingen
    conn.close()

    return monthly_summaries
