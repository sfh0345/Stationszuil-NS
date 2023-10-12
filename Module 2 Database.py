import psycopg2
# import csv file generator

from datetime import datetime
now = datetime.now()
datummod = now.strftime("%d/%m/%Y %H:%M:%S")
# datum in een variable

connection_string = "host='172.166.152.26' dbname='Stationzuil' user='postgres' password='Sander0345'"


print("Hallo, welkom op het moderatiedashboard")

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




def select_database():
    # global naam
    # global email
    try:
        #verbind met de database.
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        # Create the SQL query with a parameterized query
        insert_query = """SELECT * FROM feedback;"""

        # Execute the SELECT query with the provided format
        cursor.execute(insert_query, ())

        rowsfeedback = cursor.fetchall()

        # Check if there is no feedback
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
                # Schrijf variabelen weg in een csv file
                toevoegen_database("feedback_accepteren", row[1], row[2], row[3], naaminput123, emailinput123, datummod)

                feedback_id = row[0]

                # Construct the DELETE query
                delete_query = """DELETE FROM feedback WHERE feedbackid = %s"""

                # Execute the DELETE query
                cursor.execute(delete_query, (feedback_id,))

                # Commit the changes to the database
                conn.commit()
                print("Je hebt deze feedback geaccepteerd")

            elif geaccepteerd == "nee":
                # Schrijf variabelen weg in een csv file
                toevoegen_database("feedback_afgewezen", row[1], row[2], row[3], naaminput123, emailinput123, datummod)

                feedback_id = row[0]

                # Construct the DELETE query
                delete_query = """DELETE FROM feedback WHERE feedbackid = %s"""

                # Execute the DELETE query
                cursor.execute(delete_query, (feedback_id,))

                # Commit the changes to the database
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



def toevoegen_database(status, naam, feedback, datum, Modnaamvar, Modemailvar, MODdatum):
    try:
        #verbind met de database.
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()


        if status == "feedback_accepteren":
            insert_query = """INSERT INTO feedback_accepteren (naam, feedback, datum, MODnaam, MODemail, MODdatum) VALUES (%s, %s, %s, %s, %s, %s);"""

            # Execute the SELECT query with the provided format
            cursor.execute(insert_query, (naam, feedback, datum, Modnaamvar, emailinput123, MODdatum))
            conn.commit()

        elif status == "feedback_afgewezen":
            insert_query = """INSERT INTO feedback_afgewezen (naam, feedback, datum, MODnaam, MODemail, MODdatum) VALUES (%s, %s, %s, %s, %s, %s);"""

            # Execute the SELECT query with the provided format
            cursor.execute(insert_query, (naam, feedback, datum, Modnaamvar, emailinput123, MODdatum))
            conn.commit()

        else:
            print("Er is iets fout gegaan.")

    except psycopg2.Error as e:
        print("Er is iets fout gegaan. ERROR: ", e)

    finally:
        cursor.close()
        conn.close()


select_database()
