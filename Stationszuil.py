import random
#import randomgenerator toolbox
import csv
#import csv file generator
import requests

from datetime import datetime
now = datetime.now()
datum = now.strftime("%d/%m/%Y %H:%M:%S")
#datum in een variable

list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
#Een random station kiezen waar de stationszuil zich bevindt

def get_weather_forecast(city):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},nl&units=metric&lang=nl&appid={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return temperature, description
    else:
        print("Fout:", response.status_code)

city = station
temperature, description = get_weather_forecast(city)
rounded_temperature = round(temperature, 1)

print(f"Hallo, welkom bij het stationszuil NS {station}.")
print(f"Het is op dit moment {rounded_temperature:.1f}°C en het is {description}.")
print("U kunt op deze paal uw feedback invoeren.")

#define naaminput om later te gebruiken
def naaminput():
    while True:
        naam = str(input("Wat is uw naam?: "))
        if len(naam) == 0:
            naam = "Annoniem"
            return naam
        elif len(naam) > 20:
            print("Voer alstublieft een kortere naam in.")
        else:
            return naam

# Sla de userinput op
tekstinput = naaminput()

#define berichtinput om later te gebruiken
def berichtinput():
    while True:
        bericht = str(input("Wat is uw feedback?: "))
        if len(bericht) <= 140 and len(bericht) > 0:
            return bericht
        elif len(bericht) == 0:
            print("Er staat niks in je bericht.")
        elif len(bericht) > 140:
            print("Uw bericht is langer dan 140 karakters.")

# Sla de bericht input op
berichtinput = berichtinput()

csv_file_path = 'input.csv'
#maak een file aan

try:
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
#open de file die je net hebt gemaakt

except FileNotFoundError:
    pass
#als de file niet word gevonden gaat hij gewoon door met de code

# Schrijf variabelen weg in een csv file
with open(csv_file_path, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([tekstinput, berichtinput, station, datum])
    #variabelen zijn in de tekstfile gezet in comma,seperated,file

print("Bedankt voor uw feedback!")
#Final message sturen