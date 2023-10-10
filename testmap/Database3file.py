import psycopg2
import random

# Database connection parameters
db_params = {
    "dbname": "Stationszuil",
    "user": "postgres",
    "password": "797979",
    "host": "localhost",
    "port": "5432"
}

list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
#Een random station kiezen waar de stationszuil zich bevindt

def retrieve_data_from_database():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        # connect met de database ** betekent dat hij de db_params hoe ze staan in json vorm per ding moet pakken en dat als login informatie moet gebruiken
        cursor = conn.cursor()

        # Execute the SELECT query
        cursor.execute(f"SELECT * FROM station_service WHERE station_city='{station}';")

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

            # Print the values
            print("City:", city)
            print("Country:", country)
            print("WC variable:", wc_var)
            print("PR variable:", pr_var)
            print("OVF variable:", ovf_var)
            print("LIFT variable:", lift_var)
        else:
            print("No data found.")

    except psycopg2.Error as e:
        print("An error occurred:", e)

    finally:
        cursor.close()
        conn.close()

# Retrieve and store data from the database
retrieve_data_from_database()
