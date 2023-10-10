import psycopg2
import random


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
#Een random station kiezen waar de stationszuil zich bevindt


# Database connection parameters
db_params = {
    "dbname": "Stationszuil",
    "user": "postgres",
    "password": "797979",
    "host": "localhost",
    "port": "5432"
}

def execute_select_query(query):
    try:
        # Connect to the PostgreSQL database
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                # Execute the SELECT query
                cursor.execute(query)
                # Fetch all the results
                rows = cursor.fetchall()
                # Print the results
                for row in rows:
                    print(row)
    except psycopg2.Error as e:
        print("An error occurred:", e)

# Run the SELECT query
select_query = f"SELECT * FROM station_service WHERE station_city='{station}';"
execute_select_query(select_query)
