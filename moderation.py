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
            with open(csv_file_path, 'r') as infile:
                # Read the first 7 lines of the file
                lines = infile.readlines()[:1]  # Slice the list to get the first 7 lines

                # Iterate over the lines and print them
                for line in lines:
                    print(line.strip())  # Strip to remove newline characters
                geaccepteerd = str(input("Wil je deze feedback accepteren? (ja/nee) ")).lower()
                if geaccepteerd == "ja":
                    # Schrijf variabelen weg in een csv file
                    with open(csv_file_geaccepteerd, 'a', newline='') as file:
                        writer = csv.writer(file)
                        for line in lines:
                            writer.writerow([line.strip()])

                        writer.writerow(["Administrator moderation dashboard logs"])
                        writer.writerow(["Naam: " + naaminput])
                        writer.writerow(["Email: " + emailinput])
                        writer.writerow(["Datum: " + datummod])
                        writer.writerow(["-------------------------------------------------------------"])
                        writer.writerow(["Status: Geaccepteerd"])
                        writer.writerow(["-------------------------------------------------------------"])
                        #variabelen zijn in de tekstfile gezet

                    # verwijder
                    with open(csv_file_path, 'r') as file:
                        lines = file.readlines()
                    # verwijder 7 lines
                    updated_lines = lines[7:]
                    # schrijf de lines terug die geupdate waren
                    with open(csv_file_path, 'w') as file:
                        file.writelines(updated_lines)


                    print("Je hebt deze feedback geaccepteerd")


                elif geaccepteerd == "nee":
                    # Schrijf variabelen weg in een csv file
                    with open(csv_file_afgewezen, 'a', newline='') as file:
                        writer = csv.writer(file)
                        for line in lines:
                            writer.writerow([line.strip()])

                        writer.writerow(["Administrator moderation dashboard logs"])
                        writer.writerow(["Naam: " + naaminput])
                        writer.writerow(["Email: " + emailinput])
                        writer.writerow(["Datum: " + datummod])
                        writer.writerow(["-------------------------------------------------------------"])
                        writer.writerow(["Status: Afgewezen"])
                        writer.writerow(["-------------------------------------------------------------"])
                        # variabelen zijn in de tekstfile gezet

                    # verwijder
                    with open(csv_file_path, 'r') as file:
                        lines = file.readlines()
                    # verwijder 7 lines
                    updated_lines = lines[7:]
                    # schrijf de lines terug die geupdate waren
                    with open(csv_file_path, 'w') as file:
                        file.writelines(updated_lines)

                    print("Je hebt deze feedback geaccepteerd")
                else:
                    print("Ongeldig antwoord (ja/nee)")


        except FileNotFoundError:
            pass
    if nothinginfile == "false":
        another_feedback = str(input("Wilt u nog een bericht reviewen? (ja/nee) ")).lower()
        if another_feedback == "nee":
            print("U verlaat nu het moderatiedashboard...")
            continue_review = False
    else:
        break