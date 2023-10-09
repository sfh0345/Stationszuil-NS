import psycopg2

#Database connection parameters
db_params = {
    "dbname": "Stationszuil",
    "user": "postgres",
    "password": "797979",
    "host": "localhost",
    "port": "5432"
}

#Verbinding maken met de database
connection = psycopg2.connect(**db_params)

#Cursor maken
cursor = connection.cursor()

#SQL-invoegquery uitvoeren
insert_query = "SELECT * FROM station_service;"
data_to_insert = ("utrecht",)  # Note the comma to create a single-element tuple
cursor.execute(insert_query, data_to_insert)

connection.commit()
connection.close()

print("Query uitgevoerd")
