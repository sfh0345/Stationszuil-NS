import random
#import randomgenerator toolbox
import csv
#import csv file generator

from datetime import datetime
now = datetime.now()
datum = now.strftime("%d/%m/%Y %H:%M:%S")
#datum in een variable


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
#Een random station kiezen waar de stationszuil zich bevindt

print("Hallo, welkom bij het stationszuil NS " + station + ".")
print("U kunt op deze paal uw feedback invoeren.")

#define naaminput om later te gebruiken
def naaminput():
    while True:
        naam = str(input("Wat is uw naam?: "))
        if len(naam) <= 0:
            naam = "Annoniem"
            return naam
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
        elif len(bericht) <= 0:
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

