# This file was imported from Figma by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
#hier zie je welke python tool er gebruikt is om het om te zetten vanaf de design tool naar python.


from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)
import tkinter as tk
from PIL import Image, ImageTk
import random
import requests
import datetime
import os
import csv
from datetime import datetime, timedelta
import json
import psycopg2




db_params = {
    "dbname": "Stationszuil",
    "user": "postgres",
    "password": "797979",
    "host": "localhost",
    "port": "5432"
}


vandaagname = datetime.today().date()
morgenname = (datetime.today() + timedelta(days=1)).date()
overmorgenname = (datetime.today() + timedelta(days=2)).date()
oovermorgenname = (datetime.today() + timedelta(days=3)).date()


from pathlib import Path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")
#path naar de gecurvde vierkanten pngs


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
#define wat hoort bij het path


window = Tk()

window.geometry("937x1461")
window.configure(bg = "#FFFFFF")

list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
window.title(f"Stationszuil NS {station}")
city = station

#Een random station kiezen waar de stationszuil zich bevindt

#alle mogelijke descriptions aan een image gekoppeld....
weather_icons = {
    "overcast clouds": "assets/04d@2x.png",
    "clear sky": "assets/01d2x.png",
    "few clouds": "assets/02d@2x.png",
    "scattered clouds": "assets/03d@2x.png",
    "broken clouds": "assets/04d@2x.png",
    "rain": "assets/09d@2x.png",
    "thunderstorm": "assets/11d@2x.png",
    "mist": "assets/50d@2x.png",
    "thunderstorm with light rain": "assets/11d@2x.png",
    "thunderstorm with rain": "assets/11d@2x.png",
    "thunderstorm with heavy rain": "assets/11d@2x.png",
    "light thunderstorm": "assets/11d@2x.png",
    "heavy thunderstorm": "assets/11d@2x.png",
    "ragged thunderstorm": "assets/11d@2x.png",
    "thunderstorm with light drizzle": "assets/11d@2x.png",
    "thunderstorm with drizzle": "assets/11d@2x.png",
    "thunderstorm with heavy drizzle": "assets/11d@2x.png",
    "light intensity drizzle": "assets/09d@2x.png",
    "drizzle": "assets/09d@2x.png",
    "heavy intensity drizzle": "assets/09d@2x.png",
    "light intensity drizzle rain": "assets/09d@2x.png",
    "drizzle rain": "assets/09d@2x.png",
    "heavy intensity drizzle rain": "assets/09d@2x.png",
    "shower rain and drizzle": "assets/09d@2x.png",
    "heavy shower rain and drizzle": "assets/09d@2x.png",
    "shower drizzle": "assets/09d@2x.png",
    "light rain": "assets/10d@2x.png",
    "moderate rain": "assets/09d@2x.png",
    "heavy intensity rain": "assets/09d@2x.png",
    "very heavy rain": "assets/09d@2x.png",
    "extreme rain": "assets/09d@2x.png",
    "freezing rain": "assets/09d@2x.png",
    "light intensity shower rain": "assets/10d@2x.png",
    "shower rain": "assets/09d@2x.png",
    "heavy intensity shower rain": "assets/09d@2x.png",
    "ragged shower rain": "assets/09d@2x.png",
    "light snow": "assets/13d@2x.png",
    "snow": "assets/13d@2x.png",
    "heavy snow": "assets/13d@2x.png",
    "sleet": "assets/13d@2x.png",
    "light shower sleet": "assets/13d@2x.png",
    "shower sleet": "assets/13d@2x.png",
    "light rain and snow": "assets/13d@2x.png",
    "rain and snow": "assets/13d@2x.png",
    "light shower snow": "assets/13d@2x.png",
    "shower snow": "assets/13d@2x.png",
    "heavy shower snow": "assets/13d@2x.png"
}

def get_next_day_forecast(city, hoeveeldagen, lang):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"  # Replace with your OpenWeatherMap API key

    # Get latitude and longitude for the city
    lat, lon = get_city_coordinates(city)
    #de cords van een stad krijgen

    if lat is None or lon is None:
        print(f"Er is iets fout gegaan, Probeer het later opnieuw.")
        return None, None

    url = f"http://api.openweathermap.org/data/2.5/onecall?appid={API_KEY}&lat={lat}&lon={lon}&units=metric&lang={lang}"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        # Get the forecast for the next day
        tomorrow = (datetime.now() + timedelta(days=hoeveeldagen)).strftime('%Y-%m-%d')
        for daily_data in weather_data['daily']:
            if datetime.utcfromtimestamp(daily_data['dt']).strftime('%Y-%m-%d') == tomorrow:
                temperature = daily_data['temp']['day']
                description = daily_data['weather'][0]['description']
                return temperature, description
        else:
            return None, None
    else:
        print("Fout:", response.status_code)
        return None, None

def get_city_coordinates(city):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None, None
def construct_api_argument():
    # Constructing the main argument for the API with "main" instead of "description"
    api_argument = {
        "main": weather_icons
    }
    return json.dumps(api_argument)
def get_weather_icon(description):
    # Function to generate variations of the description
    def generate_variations(description):
        variations = []
        variations.append(description.lower().replace(" ", "_").replace("-", "_"))
        variations.append(description.lower().replace(" ", ""))
        variations.append(description.lower().replace("-", ""))
        return variations
    #haal de spaties en underscores uit de descriptions. Tegen het niet vinden van icoontjes

    # Generate variations of the description
    variations = generate_variations(description)

    for var in variations:
        if var in weather_icons:
            return weather_icons[var]

    return "Icon not found"
def retrieve_data_from_database():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        # connect met de database ** betekent dat hij de db_params hoe ze staan in json vorm per ding moet pakken en dat als login informatie moet gebruiken
        cursor = conn.cursor()
        #het opzetten van een cursor om een query te kunnen vragen later in de file

        #Maak een select op de database waarin je alles * wilt zien van de database.
        cursor.execute(f"SELECT * FROM station_service WHERE station_city='{station}';")

        #eerste rij pakken. Als het goed is komt hier sowieso maar 1 rij uit.
        row = cursor.fetchone()

        if row:
            # vul de gevonden dingen in een variabele neerzetten voor de rij
            city, country, wc, pr, ovf, lift = row

            WC = "assets/img_toilet.png"
            PR = "assets/img_pr.png"
            OVF = "assets/img_ovfiets.png"
            LIFT = "assets/img_lift.png"
            WCn = "assets/img_toiletnot.png"
            PRn = "assets/img_prnot.png"
            OVFn = "assets/img_ovfietsnot.png"
            LIFTn = "assets/img_liftnot.png"

            # Er staat hier eigenlijk de variabelen WC als WC=true ANDERS WCn.
            wc_var1 = WC if wc else WCn
            pr_var1 = PR if pr else PRn
            ovf_var1 = OVF if ovf else OVFn
            lift_var1 = LIFT if lift else LIFTn
            return wc_var1, pr_var1, ovf_var1, lift_var1
            #return de variabelen

            #Print als er niks uit de query is gekomen. Moet eigenlijk nooit voorkomen omdat alle stations in de randomlist ook in de database staan.
        else:
            print("Er is iets fout gegaan.")

    # als postgreSQL een fout geeft wordt deze hier opgeslagen en kan je hem dus snel en mooi terug geven ipv een hele grote rode error.
    except psycopg2.Error as e:
        print("Er is iets fout gegaan. Dit is de errorcode: ", e)

    finally:
        cursor.close()
        conn.close()
    # sluit de database connectie als je klaar bent.




temperature, description = get_next_day_forecast(city, 0, "eng")
temperature1, description1 = get_next_day_forecast(city, 1, "eng")
temperature2, description2 = get_next_day_forecast(city, 2, "eng")
temperature3, description3 = get_next_day_forecast(city, 3, "eng")
#alles in variabelen opschrijven voor vandaag en de dagen erna

none, descriptionNL = get_next_day_forecast(city, 0, 'nl')
# 1x in het nederlands de api uithoren om de Weersverwachting in het nederlands neer te zetten.

rounded_temperature = round(temperature, 0)
rounded_temperature1 = round(temperature1, 0)
rounded_temperature2 = round(temperature2, 0)
rounded_temperature3 = round(temperature3, 0)
#Vars maken voor elke temperatuur en dag

#split de text als hij te lang word voor de feedbackbox
def split_text(text, max_width):
    words = text.split()
    #de tekst word gesplit op woorden
    lines = []
    # maak een lege lijst aan om de lijnen in op te slaan
    current_line = words[0]
    #hij begint bij het eerste woord

    for word in words[1:]:
        test_line = current_line + " " + word
        if canvas.bbox(canvas.create_text(0, 0, anchor="nw", fill="#E4E4E4", text=test_line, font=font))[2] <= max_width:
            #maak test text om te kijken hoe lang de text gaat worden. Maak hierna gebruik van de split functie
            # [2] <= max_width: haalt uit het bbox uitkomst, (x0, y0, x1, y1) de 3e value eruit, rechter onder hoek van de tekst en kijkt of dit niet langer is dan de max width
            current_line = test_line
            #de samenvoeging van tekst boxen bij elkaar zetten in current_line

        else:
            lines.append(current_line)
            current_line = word
        #split de lijn op in stukjes waar het laatste ding over de max width is gegaan

    lines.append(current_line)
    #zet de lijnen bij elkaar
    return lines

#voeg een plaatje toe aan het canvas Dit is nodig om plaatjes op het canvas te maken.
def add_image_to_canvas(canvas, image_path, x, y, width, height):
    # Load the image and resize it
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height))

    # Create a PhotoImage object from the resized image
    tk_image = ImageTk.PhotoImage(resized_image)

    # Create an image item at the specified coordinates
    canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
    return tk_image




#maak een window aan.
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1461,
    width = 937,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    937.0,
    1461.0,
    fill="#E4E4E4",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    462.0,
    431.5,
    image=entry_image_1
)

canvas.create_text(
    58.0,
    38.0,
    anchor="nw",
    text=f"Welkom op station NS {station}",
    fill="#0063D3",
    font=("Rubik Medium", 50 * -1)
)
canvas.create_text(
    61.0,
    96.0,
    anchor="nw",
    text="Hier vind je de weersverwachting en feedback",
    fill="#4D4D4D",
    font=("Rubik Medium", 29 * -1)
)

canvas.create_text(
    178.0,
    271.0,
    anchor="nw",
    text=f"{rounded_temperature:.0f}°C",
    fill="#FFFFFF",
    font=("Rubik SemiBold", 36 * -1)
)

canvas.create_text(
    178.0,
    220.0,
    anchor="nw",
    text=f"{station}, Nederlands",
    fill="#DFDFDF",
    font=("Rubik Regular", 20 * -1)
)


canvas.create_text(
    750.0,
    303.0,
    anchor="e",
    text=f"{descriptionNL}",
    fill="#DFDFDF",
    font=("Rubik Regular", 32 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    464.5,
    345.5,
    image=entry_image_2
)
#fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles

canvas.create_rectangle(
    57.0,
    728.0,
    871.0,
    738.0,
    fill="#003082",
    outline="")

canvas.create_text(
    178.0,
    390.0,
    anchor="nw",
    text="Today",
    fill="#FFFFFF",
    font=("Rubik Regular", 20 * -1)
)

canvas.create_text(
    178.0,
    458.0,
    anchor="nw",
    text="Tomorrow",
    fill="#FFFFFF",
    font=("Rubik Regular", 20 * -1)
)

canvas.create_text(
    178.0,
    527.0,
    anchor="nw",
    text=(overmorgenname.strftime('%A')),
    fill="#FFFFFF",
    font=("Rubik Regular", 20 * -1)
)

canvas.create_text(
    178.0,
    608.0,
    anchor="nw",
    text=(oovermorgenname.strftime('%A')),
    fill="#FFFFFF",
    font=("Rubik Regular", 20 * -1)
)

canvas.create_text(
    669.0,
    382.0,
    anchor="nw",
    text=f"{rounded_temperature:.0f}°C",
    fill="#FFFFFF",
    font=("Rubik Semibold", 24 * -1)
)

canvas.create_text(
    179.0,
    374.0,
    anchor="nw",
    text=(vandaagname.strftime('%d %B')),
    fill="#C3C3C3",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    179.0,
    442.0,
    anchor="nw",
    text=(morgenname.strftime('%d %B')),
    fill="#C3C3C3",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    179.0,
    511.0,
    anchor="nw",
    text=(overmorgenname.strftime('%d %B')),
    fill="#C3C3C3",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    179.0,
    592.0,
    anchor="nw",
    text=(oovermorgenname.strftime('%d %B')),
    fill="#C3C3C3",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    670.0,
    457.0,
    anchor="nw",
    text=f"{rounded_temperature1:.0f}°C",
    fill="#FFFFFF",
    font=("Rubik Semibold", 24 * -1)
)

canvas.create_text(
    670.0,
    530.0,
    anchor="nw",
    text=f"{rounded_temperature2:.0f}°C",
    fill="#FFFFFF",
    font=("Rubik Semibold", 24 * -1)
)

canvas.create_text(
    670.0,
    611.0,
    anchor="nw",
    text=f"{rounded_temperature3:.0f}°C",
    fill="#FFFFFF",
    font=("Rubik Semibold", 24 * -1)
)

canvas.create_text(
    121.0,
    750.0,
    anchor="nw",
    text="Hier vind je de feedback van andere reizigers",
    fill="#0063D3",
    font=("Rubik Medium", 32 * -1)
)


csv_file_path = 'geaccepteerd.csv'


if os.path.getsize(csv_file_path) == 0:
    print("Er zijn geen reviews om weer te geven.")
else:
    lines_to_read = 6
    #6 lijnen vanaf de onderkant lezen

    input_list = []

    # lees de csv file en draai de output om.
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        lines = list(csv_reader)
        #lees alle lijnen en zet het in een lijst

    reversed_lines = reversed(lines[-lines_to_read:])
    #draai de lijst om

    # Process the reversed lines
    for i, row in enumerate(reversed_lines):
        if len(row) == 8:
            input_list.append({
                'Naam': row[0],
                'Feedback': row[1],
                'Datum': row[3]
            })
            #sla de dingen op die je uit de csv file nodig hebt.
    for i, row in enumerate(input_list):
            if i == 0:
                #ga door deze lijst heen totdat je de goede box hebt gevonden voor de aantalste keer dat je hebt gerunned.


                entry_image_3 = PhotoImage(
                    file=relative_to_assets("entry_3.png"))
                entry_bg_3 = canvas.create_image(
                    252.0,
                    891.5,
                    image=entry_image_3
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles

                canvas.create_text(
                    88.0,
                    833.0,
                    anchor="nw",
                    text=f"Naam: {row['Naam']}",
                    fill="#FFFFFF",
                    font=("Rubik Medium", 14 * -1)
                )

                entry_image_4 = PhotoImage(
                    file=relative_to_assets("entry_4.png"))
                entry_bg_4 = canvas.create_image(
                    251.5,
                    855.5,
                    image=entry_image_4
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles

                # Feedback opsplitsen als het te lang word
                x = 88.0
                y = 865.0
                max_width = 327  # Maximum width for wrapping
                font = ("Rubik Medium", 11 * -1)

                # Split the text into lines and display
                lines = split_text(row['Feedback'], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # Adjust spacing between lines

                canvas.create_text(
                    301.0,
                    951.0,
                    anchor="nw",
                    text=f"{row['Datum']}",
                    fill="#C7C7C7",
                    font=("Rubik Medium", 11 * -1)
                )


            elif i == 1:
                entry_image_5 = PhotoImage(
                    file=relative_to_assets("entry_5.png"))
                entry_bg_5 = canvas.create_image(
                    674.5,
                    891.5,
                    image=entry_image_5
                )

                canvas.create_text(
                    511.0,
                    833.0,
                    anchor="nw",
                    text=f"Naam: {row['Naam']}",
                    fill="#FFFFFF",
                    font=("Rubik Medium", 14 * -1)
                )

                entry_image_6 = PhotoImage(
                    file=relative_to_assets("entry_6.png"))
                entry_bg_6 = canvas.create_image(
                    674.0,
                    857.0,
                    image=entry_image_6
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles
                x = 511.0
                y = 865.0
                max_width = 327  # Maximum width for wrapping
                font = ("Rubik Medium", 11 * -1)

                # Split the text into lines and display
                lines = split_text(row['Feedback'], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # Adjust spacing between lines

                canvas.create_text(
                    725.0,
                    951.0,
                    anchor="nw",
                    text=f"{row['Datum']}",
                    fill="#C7C7C7",
                    font=("Rubik Medium", 11 * -1)
                )
            elif i == 2:
                entry_image_7 = PhotoImage(
                    file=relative_to_assets("entry_7.png"))
                entry_bg_7 = canvas.create_image(
                    252.0,
                    1091.5,
                    image=entry_image_7
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles

                canvas.create_text(
                    88.0,
                    1035.0,
                    anchor="nw",
                    text=f"Naam: {row['Naam']}",
                    fill="#FFFFFF",
                    font=("Rubik Medium", 14 * -1)
                )

                entry_image_8 = PhotoImage(
                    file=relative_to_assets("entry_8.png"))
                entry_bg_8 = canvas.create_image(
                    251.5,
                    1057.5,
                    image=entry_image_8
                )

                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles
                x = 88.0
                y = 1065.0
                max_width = 327  # Maximum width for wrapping
                font = ("Rubik Medium", 11 * -1)

                # Split the text into lines and display
                lines = split_text(row['Feedback'], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # Adjust spacing between lines

                canvas.create_text(
                    301.0,
                    1152.0,
                    anchor="nw",
                    text=f"{row['Datum']}",
                    fill="#C7C7C7",
                    font=("Rubik Medium", 11 * -1)
                )

            elif i == 3:
                entry_image_9 = PhotoImage(
                    file=relative_to_assets("entry_9.png"))
                entry_bg_9 = canvas.create_image(
                    674.5,
                    1091.5,
                    image=entry_image_9
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles

                canvas.create_text(
                    511.0,
                    1035.0,
                    anchor="nw",
                    text=f"Naam: {row['Naam']}",
                    fill="#FFFFFF",
                    font=("Rubik Medium", 14 * -1)
                )

                entry_image_10 = PhotoImage(
                    file=relative_to_assets("entry_10.png"))
                entry_bg_10 = canvas.create_image(
                    674.0,
                    1057.0,
                    image=entry_image_10
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles
                x = 511.0
                y = 1065.0
                max_width = 327  # Maximum width for wrapping
                font = ("Rubik Medium", 11 * -1)

                # Split the text into lines and display
                lines = split_text(row['Feedback'], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # Adjust spacing between lines

                canvas.create_text(
                    725.0,
                    1152.0,
                    anchor="nw",
                    text=f"{row['Datum']}",
                    fill="#C7C7C7",
                    font=("Rubik Medium", 11 * -1)
                )

            elif i == 4:
                entry_image_11 = PhotoImage(
                    file=relative_to_assets("entry_11.png"))
                entry_bg_11 = canvas.create_image(
                    252.0,
                    1291.0,
                    image=entry_image_11
                )

                canvas.create_text(
                    88.0,
                    1232.0,
                    anchor="nw",
                    text=f"Naam: {row['Naam']}",
                    fill="#FFFFFF",
                    font=("Rubik Medium", 14 * -1)
                )

                entry_image_12 = PhotoImage(
                    file=relative_to_assets("entry_12.png"))
                entry_bg_12 = canvas.create_image(
                    251.5,
                    1255.5,
                    image=entry_image_12
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles
                    # Feedback opsplitsen als het te lang word
                x = 88.0
                y = 1264.0
                max_width = 327  # Maximum width for wrapping
                font = ("Rubik Medium", 11 * -1)

                # Split the text into lines and display
                lines = split_text(row['Feedback'], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # Adjust spacing between lines

                canvas.create_text(
                    301.0,
                    1350.0,
                    anchor="nw",
                    text=f"{row['Datum']}",
                    fill="#C7C7C7",
                    font=("Rubik Medium", 11 * -1)
                )
            elif i == 5:
                entry_image_13 = PhotoImage(
                    file=relative_to_assets("entry_13.png"))
                entry_bg_13 = canvas.create_image(
                    674.5,
                    1291.0,
                    image=entry_image_13
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles

                canvas.create_text(
                    511.0,
                    1232.0,
                    anchor="nw",
                    text=f"Naam: {row['Naam']}",
                    fill="#FFFFFF",
                    font=("Rubik Medium", 14 * -1)
                )

                entry_image_14 = PhotoImage(
                    file=relative_to_assets("entry_14.png"))
                entry_bg_14 = canvas.create_image(
                    674.0,
                    1257.0,
                    image=entry_image_14
                )
                # fake een entry om mooie ronden boxen te krijgen ipv perfect reqtangles

                x = 511.0
                y = 1264.0
                max_width = 327  # Maximum width for wrapping
                font = ("Rubik Medium", 11 * -1)

                # Split the text into lines and display
                lines = split_text(row['Feedback'], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # Adjust spacing between lines

                canvas.create_text(
                    725.0,
                    1350.0,
                    anchor="nw",
                    text=f"{row['Datum']}",
                    fill="#C7C7C7",
                    font=("Rubik Medium", 11 * -1)
                )
            else:
                print("Er is iets misgegaan, probeer het later opnieuw.")


forecast_data = [
    (temperature, description),
    (temperature1, description1),
    (temperature2, description2),
    (temperature3, description3)
]
#sla alle weersinformatie op in een lijst. hiermee kan je over de lijst itereren en de goede keer pakken

#start een counter om op 1 te beginnen. vandaag, en te eindigen bij 4
day_counter = 1

for temp, desc in forecast_data:
    if temp is not None and desc is not None:
        #kijken of de weersinfo wel gevonden is.

        rounded_temperature = round(temp, 0)
        #rond de temperatuur af.

        #zorg ervoor dat het goede weersicoontje bij het goede weersinformatie komt te staan. desc is een afkorting van description
        icon = get_weather_icon(desc)

        #Update de weersinformatie van elke dag met bijbehoorende cordinaten van de image.
        if day_counter == 1:
            Vandaagbig = add_image_to_canvas(canvas, icon, x=673, y=210, width=100, height=100)
            Vandaag = add_image_to_canvas(canvas, icon, x=590, y=360, width=75, height=75)
        elif day_counter == 2:
            morgen = add_image_to_canvas(canvas, icon, x=590, y=435, width=75, height=75)
        elif day_counter == 3:
            overmorgen = add_image_to_canvas(canvas, icon, x=590, y=505, width=75, height=75)
        elif day_counter == 4:
            overovermorgen = add_image_to_canvas(canvas, icon, x=590, y=586, width=75, height=75)

        #Counter plus 1 om door te gaan naar de volgende dag
        day_counter += 1

    else:
        print(f"Er is iets mis gegaan met het ophalen van de weersinformatie. Probeer het later opnieuw.")
        #als de weersinformatie niet goed is opgehaald send een errormessage


WCvar1, PRvar1, OVFvar1, LIFTvar1 = retrieve_data_from_database()
#krijg ded variabelen van de define statment en gebruik ze hier.

#if true wc if false wcn
# WCvar = WCvar1
# PRvar = PRvar1
# OVFvar = OVFvar1
# LIFTvar = LIFTvar1



wcimg = add_image_to_canvas(canvas, WCvar1, x=869, y=138, width=47, height=47)
primg = add_image_to_canvas(canvas, PRvar1, x=867, y=204, width=47, height=47)
ovfimg = add_image_to_canvas(canvas, OVFvar1, x=864, y=260, width=47, height=47)
liftimg = add_image_to_canvas(canvas, LIFTvar1, x=866, y=325, width=47, height=47)





image_path = "assets/Nederlandse_Spoorwegen_logo.svg.png"
image = add_image_to_canvas(canvas, image_path, x=870, y=17, width=50, height=20)
image_path1 = "assets/hogeschool-utrecht-logo-png-transparent.png"
image1 = add_image_to_canvas(canvas, image_path1, x=360, y=1390, width=210, height=49)
#voeg plaatjes toe aan het window.

window.resizable(False, False)
#je mag het niet resizen.
window.mainloop()