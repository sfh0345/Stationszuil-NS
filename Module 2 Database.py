import psycopg2
# import csv file generator

from datetime import datetime
now = datetime.now()
datummod = now.strftime("%d/%m/%Y %H:%M:%S")
# datum in een variable

connection_string = "host='172.166.152.26' dbname='Stationzuil' user='postgres' password='Sander0345'"
#connection naar de database.

print("Hallo, welkom op het moderatiedashboard")

# maak een define aan om later te gebruiken. Hiermee kan je makkelijk dingen wegschrijven naar de database.
def toevoegen_database(status, naam, feedback, datum, Modnaamvar, Modemailvar, MODdatum):
    try:
        #verbind met de database.
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        #check welke status er is gegeven
        if status == "feedback_accepteren":
            #maak een variabele aan voor de sql query
            insert_query = """INSERT INTO feedback_accepteren (naam, feedback, datum, MODnaam, MODemail, MODdatum) VALUES (%s, %s, %s, %s, %s, %s);"""

            # Execute de insert into op de database met de goede variabelen.
            cursor.execute(insert_query, (naam, feedback, datum, Modnaamvar, emailinput123, MODdatum))
            #commit het
            conn.commit()

        elif status == "feedback_afgewezen":
            # maak een variabele aan voor de sql query
            insert_query = """INSERT INTO feedback_afgewezen (naam, feedback, datum, MODnaam, MODemail, MODdatum) VALUES (%s, %s, %s, %s, %s, %s);"""

            #  Execute de insert into op de database met de goede variabelen.
            cursor.execute(insert_query, (naam, feedback, datum, Modnaamvar, emailinput123, MODdatum))
            # commit het
            conn.commit()

        else:
            print("Er is iets fout gegaan.")
            #dit komt eigenlijk niet voor. maar als er iets fout gaat met de code. Dan crashed niet het hele programma

    except psycopg2.Error as error:
        print("Er is iets fout gegaan. \nERROR: ", error)
        #als sql een error geeft word deze hier weer gegeven zodat je die snel kan oplossen.

    finally:
        cursor.close()
        conn.close()
        #close de connection met de database


# define naaminput om later te gebruiken
def naaminput():
    global naam123
    while True:
        naam123 = str(input("Naam?: "))
        if len(naam123) <= 0 or naam123 == " ":
            print("U heeft geen naam opgegeven.")
            break
        else:
            return naam123

# Sla de userinput op
naaminput123 = naaminput()


#define naaminput om later te gebruiken
def emailinput():
    global email123
    while True:
        email123 = str(input("Email: "))
        if len(email123) <= 0:
            print("U heeft uw email niet ingevoerd")
        else:
            return email123

# Sla de bericht input op
emailinput123 = emailinput()


try:
    #verbind met de database.
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # maak de variabele aan om te selecten op de database
    insert_query = """SELECT * FROM feedback;"""

    # Execute de database select query
    cursor.execute(insert_query, ())

    rowsfeedback = cursor.fetchall()
    #hier krijg je een lijst van de de rijen en de dingen erin.

    # print de variabelen die zijn gevonden in de rij
    for row in rowsfeedback:
        print("------------------------------")
        print("Naam:", row[1])
        print("Feedback:", row[2])
        print("Datum:", row[3])
        print("------------------------------")
        print()

        geaccepteerd = str(input("Wil je deze feedback accepteren? (ja/nee) ")).lower()
        # input voor feedback accpeteren of afwijzen
        if geaccepteerd == "ja":
            # Schrijf variabelen weg naar feedback accepteren in de database
            toevoegen_database("feedback_accepteren", row[1], row[2], row[3], naaminput123, emailinput123, datummod)

            # variabele maken voor feedback_id om in de query te zetten
            feedback_id = row[0]

            # maak een variabele om hierna de feedback te verwijderen uit de database.
            delete_query = """DELETE FROM feedback WHERE feedbackid = %s"""

            # excecute de query op de database
            cursor.execute(delete_query, (feedback_id,))

            # commit de aanpassingen aan de database
            conn.commit()
            print("Je hebt deze feedback geaccepteerd")

        elif geaccepteerd == "nee":
            # Schrijf variabelen weg naar database afgewezen
            toevoegen_database("feedback_afgewezen", row[1], row[2], row[3], naaminput123, emailinput123, datummod)

            # variabele maken voor feedback_id om in de query te zetten
            feedback_id = row[0]

            # maak een variabele om hierna de feedback te verwijderen uit de database.
            delete_query = """DELETE FROM feedback WHERE feedbackid = %s"""

            # excecute de query op de database
            cursor.execute(delete_query, (feedback_id,))

            # commit de aanpassingen aan de database
            conn.commit()
            print("Je hebt deze feedback afgewezen")


        else:
            print("Ongeldig antwoord (ja/nee)")
            # als er iets anders wordt getypt in plaats van ja/nee
    if not rowsfeedback:
        print("U heeft alle feedback verwerkt.")

except psycopg2.Error as e:
    print("Er is iets fout gegaan. ERROR: ", e)

finally:
    cursor.close()
    conn.close()
