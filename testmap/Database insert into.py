import random
import psycopg2

from datetime import datetime
now = datetime.now()
datum = now.strftime("%d/%m/%Y %H:%M:%S")

connection_string = "host='localhost' dbname='Stationszuil' user='postgres' password='797979'"


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)



def databaseconnectioninsert(naam, feedback, datum):
    try:
        #verbind met de database.
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        # Create the SQL query with a parameterized query using %s
        insert_query = "INSERT INTO feedback (naam, feedback, datum) VALUES (%s, %s, %s);"

        # Execute the SELECT query with the provided format
        cursor.execute(insert_query, (naam, feedback, datum))

        # Fetch the first row (assuming you're fetching a single row)
        conn.commit()

    except psycopg2.Error as e:
        print("An error occurred:", e)

    finally:
        cursor.close()
        conn.close()
databaseconnectioninsert(naam, feedback, datum)
