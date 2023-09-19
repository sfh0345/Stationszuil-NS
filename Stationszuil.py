import random
#inport randomgenerator toolbox
import csv
#inport csv file generator

from datetime import date
datum = date.today()
#datum in een variable


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
#Een random station kiezen waar de stationszuil zich bevindt

print("Hallo, welkom bij het stationszuil NS " + station + ".")






def naaminput():
    while True:
        naam = str(input("Wat is uw naam?: "))
        if len(naam) <= 140:
            return naam
        if len(naam) <= 0:
            naam = "Annoniem"
        else:
            print("Uw naam is langer dan 140 karakters.")

# Get user input
tekstinput = naaminput()

csv_file_path = 'input.csv'
run_number = 1

try:
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                run_number += 1
except FileNotFoundError:
    pass

# Write the input to the CSV file
with open(csv_file_path, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([" "])
    writer.writerow(["Gebruiker heeft feedback achtergelaten -----------", datum])
    writer.writerow(["Naam: " + tekstinput])


print("done")





