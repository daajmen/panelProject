import subprocess
from datetime import datetime
import threading


# Funktion för att köra adb-kommandon
def run_adb_commands(ip):
    try:
        # Anslut till enheten via ADB
        subprocess.run(f"adb connect {ip}", shell=True)
        # Väck enheten
        subprocess.run(f"adb shell input keyevent KEYCODE_WAKEUP", shell=True)
    except Exception as e:
        print(f"Error running ADB commands: {e}")

# Funktion för att schemalägga ADB-kommandon
def schedule_adb(ip, start_time, end_time):
    while True:
        now = datetime.now().time()
        if start_time <= now <= end_time:
            run_adb_commands(ip)
        # Vänta en minut innan nästa koll
        threading.Event().wait(60)

# Funktion för att starta schemaläggningen i en separat tråd
def start_adb_scheduler(ip, start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()
    
    threading.Thread(target=schedule_adb, args=(ip, start_time, end_time), daemon=True).start()
    print(f"ADB commands scheduled between {start_time_str} and {end_time_str} for IP: {ip}")
