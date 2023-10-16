import psycopg2
# import csv file generator

from datetime import datetime
now = datetime.now()
datummod = now.strftime("%d/%m/%Y %H:%M:%S")
# datum in een variable

import sys
try:
    from Database import establish_connection, close_connection
    import sys

    conn = establish_connection()

    if conn is None:
        sys.exit(1)
except ModuleNotFoundError:
    print("Het databasebestand is niet gevonden. Zorg ervoor dat de 'Databases.py' bestaat.")
    sys.exit(1)

print("Hallo, welkom op het moderatiedashboard")

# maak een define aan om later te gebruiken. Hiermee kan je makkelijk dingen wegschrijven naar de database.
def toevoegen_database(naam, feedback, datum, Modnaamvar, Modemailvar, MODdatum, statusacceptatie):
    try:
        #verbind met de database.
        conn = establish_connection()
        cursor = conn.cursor()
        # maak een variabele aan voor de sql query
        insert_querymod = """INSERT INTO moderator (MODnaam, MODemail) VALUES (%s, %s) RETURNING moderatorid;"""
        cursor.execute(insert_querymod, (Modnaamvar, Modemailvar))
        conn.commit()

        #door moderatorid te returnen kan je hier vinden welk id de moderator had. Hierna zet je dit dus in beoordeelde feedback.
        moderatorid1 = cursor.fetchone()[0]

        # maak een variabele aan voor de sql query
        insert_query = """INSERT INTO beoordeelde_feedback (naam, feedback, datum, status, statusdatum, moderatorid) VALUES (%s, %s, %s, %s, %s, %s);"""

        # Execute de insert into op de database met de goede variabelen.
        cursor.execute(insert_query, (naam, feedback, datum, statusacceptatie, MODdatum, moderatorid1))
        # commit het
        conn.commit()

    except psycopg2.Error as error:
        print("Er is iets fout gegaan. \nERROR: ", error)
        #als sql een error geeft word deze hier weer gegeven zodat je die snel kan oplossen.

    finally:
        cursor.close()
        close_connection(conn)
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

continuefeedback = True

while continuefeedback:
    try:
        #verbind met de database.
        conn = establish_connection()
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
                toevoegen_database(row[1], row[2], row[3], naaminput123, emailinput123, datummod, "Geaccepteerd")

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
                toevoegen_database(row[1], row[2], row[3], naaminput123, emailinput123, datummod, "Afgewezen")

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
                continuefeedback = True
                # als er iets anders wordt getypt in plaats van ja/nee
        if not rowsfeedback:
            print("U heeft alle feedback verwerkt.")
            continuefeedback = False

    except psycopg2.Error as e:
        print("Er is iets fout gegaan. ERROR: ", e)

    finally:
        cursor.close()
        close_connection(conn)
