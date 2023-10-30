import psycopg2
import threading


def print_message():
    print("Het duurt langer dan normaal om de database te bereiken...")
    print("Wacht alstublieft nog even...")

# Start a thread to print a message after 3.5 seconds
timer_thread = threading.Timer(3.5, print_message)
timer_thread.start()
def establish_connection():
    connection_string = "host='172.166.152.26' dbname='Stationzuil' user='postgres' password='Sander0345'"

    try:
        connection = psycopg2.connect(connection_string)
        timer_thread.cancel()
        return connection
    except psycopg2.Error as e:
        print(f"Kan niet verbinden met de database. Staat de server uit? \nERROR: {e}")
        timer_thread.cancel()
        return None


def close_connection(connection):
    if connection:
        connection.close()