from utils.API_tools import notify_with_tibber, fetch_value
from datetime import datetime 

import time

def remind_user_to_charge(): 

    def check_battery_level(): 

        battery = float(fetch_value('sensor.battery_level'))
        charge_state = fetch_value('binary_sensor.anslutning')

        if charge_state == 'off' and battery < 40: 
            notify_with_tibber(f'Bilen är inte inpluggad! 🛺🪫: {battery} %')

    def check_time(): 
        while True: 
            now = datetime.now() 

            if now.hour == 21 and now.minute == 0:
                check_battery_level()
                break
            elif now.hour == 20 and now.minute == 00: 
                check_battery_level()
                break            
            # Vänta 1 minut innan vi kollar igen
            time.sleep(30)
    
    check_time()



