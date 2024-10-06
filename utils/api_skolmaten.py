import requests
from bs4 import BeautifulSoup
from collections import namedtuple

def fetch_skolmat():
    url = "https://skolmaten.se/furulund/"
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        items = soup.find_all("div", class_='items')
        matsedel = {}

        for index, item in enumerate(items): 
            matsedel[f"rätt_{index + 1}"] = item.text.strip()
        print(matsedel)
        return matsedel
    
    else:
        print(f"Fel: {response.status_code}")
        return None
       

fetch_skolmat()