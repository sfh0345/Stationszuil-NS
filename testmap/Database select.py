import random
import psycopg2

connection_string = "host='localhost' dbname='Stationszuil' user='postgres' password='797979'"


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)



def databaseconnectionselectstationszuil(station_city):
    try:
        #verbind met de database.
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        # Create the SQL query with a parameterized query using %s
        insert_query = "SELECT * FROM station_service WHERE station_city=%s;"

        # Execute the SELECT query with the provided format
        cursor.execute(insert_query, (station_city,))

        # Fetch the first row (assuming you're fetching a single row)
        row = cursor.fetchone()

        if row:
            # Store the values in variables
            city, country, wc, pr, ovf, lift = row

            # Check boolean values and set appropriate variables
            wc_var = "WC" if wc else "WCn"
            pr_var = "PR" if pr else "PRn"
            ovf_var = "OVF" if ovf else "OVFn"
            lift_var = "LIFT" if lift else "LIFTn"
        else:
            print("No data found.")

    except psycopg2.Error as e:
        print("An error occurred:", e)

    finally:
        cursor.close()
        conn.close()
retrieve_data_from_database(station)
