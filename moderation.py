import csv
import os
#inport csv file generator

from datetime import datetime
now = datetime.now()
datummod = now.strftime("%d/%m/%Y %H:%M:%S")
#datum in een variable

print("Hallo, welkom op het moderatiedashboard")

def naaminput():
    while True:
        naam = str(input("Naam?: "))
        if len(naam) <= 0 or naam == " ":
            print("U heeft geen naam opgegeven.")
            break
        else:
            return naam

# Sla de userinput op
naaminput = naaminput()

def emailinput():
    while True:
        email = str(input("Email: "))
        if len(email) <= 0:
            print("Er staat niks in je bericht.")
        else:
            return email

# Sla de bericht input op
emailinput = emailinput()

csv_file_path = 'input.csv'
csv_file_geaccepteerd = 'geaccepteerd.csv'
csv_file_afgewezen = 'afgewezen.csv'
#maak een file aan

continue_review = True

while continue_review:
    if os.path.getsize(csv_file_path) == 0:
        print("U heeft alle feedback verwerkt.")
        nothinginfile = "true"
    else:
        nothinginfile = "false"
        try:

            inputlijst = []  # List to store the data

            try:
                with open(csv_file_path, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        # Assuming there are four fields in each row
                        if len(row) == 4:
                            inputlijst.append({
                                'field1': row[0],
                                'field2': row[1],
                                'field3': row[2],
                                'field4': row[3]
                            })

            except FileNotFoundError:
                print(f"Het bestand is niet gevonden.")

            # Print the data vertically
            for row in inputlijst:
                print("------------------------------")
                print("Naam:", row['field1'])
                print("Feedback:", row['field2'])
                print("Locatie:", row['field3'])
                print("Datum:", row['field4'])
                print("------------------------------")
                print()# Add an empty line between records

                geaccepteerd = str(input("Wil je deze feedback accepteren? (ja/nee) ")).lower()
                if geaccepteerd == "ja":
                    status = "Geaccepteerd"
                    # Schrijf variabelen weg in een csv file
                    with open(csv_file_geaccepteerd, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([row['field1'],row['field2'],row['field3'],row['field4'],naaminput,emailinput,datummod,status])


                    # verwijder
                    with open(csv_file_path, 'r') as file:
                        lines = file.readlines()
                    # verwijder 1 line
                    updated_lines = lines[1:]
                    # schrijf de lines terug die geupdate waren
                    with open(csv_file_path, 'w') as file:
                        file.writelines(updated_lines)
                    print("Je hebt deze feedback geaccepteerd")

                elif geaccepteerd == "nee":
                    status = "Afgewezen"
                    # Schrijf variabelen weg in een csv file
                    with open(csv_file_afgewezen, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([row['field1'],row['field2'],row['field3'],row['field4'],naaminput,emailinput,datummod,status])


                    # verwijder
                    with open(csv_file_path, 'r') as file:
                        lines = file.readlines()
                    # verwijder 1 line
                    updated_lines = lines[1:]
                    # schrijf de lines terug die geupdate waren
                    with open(csv_file_path, 'w') as file:
                        file.writelines(updated_lines)


                    print("Je hebt deze feedback afgewezen")
                else:
                    print("Ongeldig antwoord (ja/nee)")


        except FileNotFoundError:
            pass
    if nothinginfile == "false":
        another_feedback = "true"
    else:
        break