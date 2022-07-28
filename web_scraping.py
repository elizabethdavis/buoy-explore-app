from bs4 import BeautifulSoup
import requests, lxml
import pandas as pd

url = "https://www.ndbc.noaa.gov/activestations.xml"
xml = requests.get(url)

soup = BeautifulSoup(xml.content, 'lxml')

station_list = soup.find_all('station')

for x in station_list:
    id = x.get('id')
    name = x.get('name')
    met = x.get('met')

    print("ID: " + id)
    print("Name: " + name)
    print("Met Data: " + met)

stations = pd.DataFrame({
    "id": id,
    "name": name,
    "met": met
})

print(stations)
