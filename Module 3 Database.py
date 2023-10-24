# This file was imported from Figma by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
#hier zie je welke python tool er gebruikt is om het om te zetten vanaf de design tool naar python.

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)
#zorg ervoor dat ook op 4k beeldschermen het er mooi uit zien. door DPI aan te zetten. Hij checkt hiermee hoeveel pixels er per inch zitten.
import tkinter as tk
from PIL import Image, ImageTk
import random
import requests
import datetime
from datetime import datetime, timedelta
import psycopg2
import sys
try:
    from Database import establish_connection, close_connection

    conn = establish_connection()

    if conn is None:
        sys.exit(1)
except ModuleNotFoundError:
    print("Het databasebestand is niet gevonden. Zorg ervoor dat de 'Databases.py' bestaat.")
    sys.exit(1)


from locatie import firsttimeinstall

varstad = firsttimeinstall()
#pak de var van firsttimeinstall

if varstad is not None:
    station = varstad
    #station is firsttimeinstall return
else:
    station = firsttimeinstall()
    #omweg omdat het eerst none geeft op de eerste run. dus nu run je het gewoon een 2e keer als het de eerste is.


vandaagname = datetime.today().date()
morgenname = (datetime.today() + timedelta(days=1)).date()
overmorgenname = (datetime.today() + timedelta(days=2)).date()
oovermorgenname = (datetime.today() + timedelta(days=3)).date()
#maak variabelen aan voor de datum van vandaag en morgen en de dag daarop


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
#maak een window aan met de goede achtergrond en de goede grootte

window.title(f"Stationszuil NS {station}")
city = station
#Een random station kiezen waar de stationszuil zich bevindt en maak hier een titel van bij het window

#Alle weerincoontjes uit assets nu gelinkt met een weersdescription
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

#krijg de weersverwachting voor vandaag en de volgende dagen.
def weersverwachtingdagen(city, hoeveeldagen, lang):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"
    #een variabele voor de api key.

    lat, lon = krijgstadcordinaten(city)
    #hiermee krijg je de cordinaten van de city die je zoekt. Dit was vroeger wel gelijk een functie bij openweatherapi
    #maar dit is er nu niet meer. dus je moet nu met een iets omslachtigere manier de cordinaten krijgen.

    if lat is None or lon is None:
        print(f"Er is iets fout gegaan, Probeer het later opnieuw.")
        return None, None
    #er gaat iets fout in de code van het ophalen van de cordinaten van een stad.

    url = f"http://api.openweathermap.org/data/2.5/onecall?appid={API_KEY}&lat={lat}&lon={lon}&units=metric&lang={lang}"
    #api url met toegevoegde f string variabelen

    response = requests.get(url)
    #krijg een reactie terug van de url in json

    # als de statuscode 200 is ga door. (statuscode 200 betekent succes)
    if response.status_code == 200:
        weather_data = response.json()
        #krijg de weersdata van het json bestand
        welkedag = (datetime.now() + timedelta(days=hoeveeldagen)).strftime('%Y-%m-%d')
        #krijg hier de datum van de dag. met de variabele hoeveeldagen. Dit is dus de variabele die het aantal dagen vanaf nu neerzet
        for daily_data in weather_data['daily']:
            #zoek in daily_Data het woord daily
            if datetime.utcfromtimestamp(daily_data['dt']).strftime('%Y-%m-%d') == welkedag:
                #Deze code vergelijkt of de datum in daily_data['dt'] overeenkomt met de datum in de variabele welkedag
                temperature = daily_data['temp']['day']
                description = daily_data['weather'][0]['description']
                # pak het eerste variabele van de daily_data['weather'][0]) description
                #krijg de temperatuur en description terug van de json file
                return temperature, description
        else:
            return None, None
    else:
        print("Fout:", response.status_code)
        #als er iets fout gaat print je de statuscode van de https
        return None, None

def krijgstadcordinaten(city):
    API_KEY = "404f6ef44205711ecabaf88bcc8e7c83"
    #api key van weatherapi
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    #url met variabelen erin

    response = requests.get(url)
    #krijg de response terug in json

    if response.status_code == 200:
        #als de statuscode 200 is ga door (200 is succes)
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        #pak de volgende data uit de json
        return lat, lon
    else:
        print("Fout:", response.status_code)
        # als er iets fout gaat print je de statuscode van de https
        return None, None


def get_weather_icon(description):
    # krijg het weersicoontje
    def generate_variations(description):
        variations = []
        variations.append(description.lower().replace("-", ""))
        return variations
    #haal de spaties en underscores uit de descriptions. Tegen het niet vinden van icoontjes
    #hier zie je dat er eerst een - tussen de weersdescription stond waardoor hij niet gevonden werd

    # voer deze descriptions uit. en zoek daarna de icoontjes op
    variations = generate_variations(description)

    for var in variations:
        if var in weather_icons:
            return weather_icons[var]
        #return de variabele van de weersicoontjes

    print("Er is iets fout gegaan met het ophalen van de weericons.")
    return None
    #als er iets fout is gegaan krijg je een error. met daaronder er is iets fout gegaan om het probleem te kunnen verkleinen mocht een user hier last van hebben

# maak een define statement aan om de de faciliteiten te kunnen ophalen uit de database
def databaseconnectionselectstationszuil(station_city):
    try:
        # connect met de database
        conn = establish_connection()
        cursor = conn.cursor()
        #het opzetten van een cursor om een query te kunnen vragen later in de file

        #Maak een select op de database waarin je alles * wilt zien van de database.
        insert_query = """SELECT * FROM station_service WHERE station_city=%s;"""

        cursor.execute(insert_query, (station_city,))
        #voer de variabelen in en execute de query


        #eerste rij pakken. Als het goed is komt hier sowieso maar 1 rij uit.
        row = cursor.fetchone()

        if row:
            # vul de gevonden dingen in een variabele neerzetten voor de rij
            city, country, wc, pr, ovf, lift = row

            # maak een mapping aan voor de images. krijg betekent dat het er niet is
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
        close_connection(conn)
    # sluit de database connectie als je klaar bent.


#alles in variabelen opschrijven voor vandaag en de dagen erna

temperature, description = weersverwachtingdagen(city, 0, "eng")
temperature1, description1 = weersverwachtingdagen(city, 1, "eng")
temperature2, description2 = weersverwachtingdagen(city, 2, "eng")
temperature3, description3 = weersverwachtingdagen(city, 3, "eng")

none, descriptionNL = weersverwachtingdagen(city, 0, 'nl')
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
            # maak test text om te kijken hoe lang de text gaat worden. Maak hierna gebruik van de split functie
            # [2] <= max_width: haalt uit het bbox uitkomst, (x0, y0, x1, y1) de 3e value eruit, rechter onder hoek van de tekst en kijkt of dit niet langer is dan de max width
            current_line = test_line
            # de samenvoeging van tekst boxen bij elkaar zetten in current_line

        else:
            lines.append(current_line)
            current_line = word
        # split de lijn op in stukjes waar het laatste ding over de max width is gegaan

    lines.append(current_line)
    # zet de lijnen bij elkaar
    return lines

# voeg een plaatje toe aan het canvas Dit is nodig om plaatjes op het canvas te maken.
def add_image_to_canvas(canvas, image_path, x, y, width, height):
    # Load the image and resize it
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height))

    # Create a PhotoImage object from the resized image
    tk_image = ImageTk.PhotoImage(resized_image)

    # Create an image item at the specified coordinates
    canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
    return tk_image



#begin tkinter code

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
#fake een entry om afgeronde vierkantjes te krijgen
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




try:
    #verbind met de database.
    conn = establish_connection()
    cursor = conn.cursor()

    # maak een sql query van feedback_accepteren en maak het op feedback id, descending met een limiet van 6 rijen
    insert_query = """SELECT * FROM beoordeelde_feedback where status = 'Geaccepteerd' order by feedbackid DESC LIMIT 6"""

    # execute de query
    cursor.execute(insert_query)
    rowsfeedback = cursor.fetchall()
    #krijg alle feedbackrijene terug
    if not rowsfeedback:
        print("Er zijn geen reviews om weer te geven.")
        #als er niks in die rijen staat geef je terug dat er geen feedback is om neer te zetten.
    else:
        for i, row in enumerate(rowsfeedback):
            # ga door deze lijst heen totdat je de goede box hebt gevonden voor de aantalste keer dat je hebt gerunned.
            if i == 0:

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
                    text=f"Naam: {row[1]}",
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
                max_width = 327  # maximum groote van de tekst voordat hij gaat splitten.
                font = ("Rubik Medium", 11 * -1)

                # split de text in lijnen en laat het zien.
                lines = split_text(row[2], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # 20 pixels tussen de lijnen

                canvas.create_text(
                    301.0,
                    951.0,
                    anchor="nw",
                    text=f"{row[3]}",
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
                    text=f"Naam: {row[1]}",
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
                max_width = 327  # maximum groote van de tekst
                font = ("Rubik Medium", 11 * -1)

                # split de lijnen met de split_Text functie
                lines = split_text(row[2], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # hoeveel pixels er tussen de lijnen komen.

                canvas.create_text(
                    725.0,
                    951.0,
                    anchor="nw",
                    text=f"{row[3]}",
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
                    text=f"Naam: {row[1]}",
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
                max_width = 327  # Maximum groote van de text
                font = ("Rubik Medium", 11 * -1)

                # split het in lijnen en laat het daarna zien
                lines = split_text(row[2], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # Adjust spacing between lines

                canvas.create_text(
                    301.0,
                    1152.0,
                    anchor="nw",
                    text=f"{row[3]}",
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
                    text=f"Naam: {row[1]}",
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
                max_width = 327  # Maximum groote van de tekst
                font = ("Rubik Medium", 11 * -1)

                # split de lijnen en laat ze daarna zien
                lines = split_text(row[2], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # groote in pixels tussen lijnen

                canvas.create_text(
                    725.0,
                    1152.0,
                    anchor="nw",
                    text=f"{row[3]}",
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
                    text=f"Naam: {row[1]}",
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
                max_width = 327  # maximum groote van de tekst
                font = ("Rubik Medium", 11 * -1)

                # split de text in lijnen en laat ze daarna zien
                lines = split_text(row[2], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # groote in pixels tussen lijnen

                canvas.create_text(
                    301.0,
                    1350.0,
                    anchor="nw",
                    text=f"{row[3]}",
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
                    text=f"Naam: {row[1]}",
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
                max_width = 327  # maximum groote van de tekst
                font = ("Rubik Medium", 11 * -1)

                # split de tekst en laat het daarna zien
                lines = split_text(row[2], max_width)

                for line in lines:
                    canvas.create_text(x, y, anchor="nw", text=line, fill="#FFFFFF", font=font)
                    y += 20  # groote in pixeles tussen de lijnen

                canvas.create_text(
                    725.0,
                    1350.0,
                    anchor="nw",
                    text=f"{row[3]}",
                    fill="#C7C7C7",
                    font=("Rubik Medium", 11 * -1)
                )



            else:
                print("er is iets fout gegaan ERROR: teveelrijen")
                #hoort normaal niet te kunnen. maar als er iets fout is in de code waar er te veel lijnen getoont worden kan je dit hier goed zien.

except psycopg2.Error as error:
    print("Er is iets fout gegaan. ERROR: ", error)
    # als er iets is fout gegaan in het sql query wordt dat hier getoont

finally:
    cursor.close()
    close_connection(conn)
    #sluit de database connectie

forecast_data = [
    (temperature, description),
    (temperature1, description1),
    (temperature2, description2),
    (temperature3, description3)
]
#sla alle weersinformatie op in een lijst. hiermee kan je over de lijst itereren en de goede keer pakken
#hiermee per keer dat je over de lijst heen gaat pakt hij een nieuwe variabele. Dit moet omdat dit geen normale for loop is met dezelfde variabelen.


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


WCvar1, PRvar1, OVFvar1, LIFTvar1 = databaseconnectionselectstationszuil(station)
#krijg ded variabelen van de define statment en gebruik ze hier.


wcimg = add_image_to_canvas(canvas, WCvar1, x=869, y=138, width=47, height=47)
primg = add_image_to_canvas(canvas, PRvar1, x=867, y=204, width=47, height=47)
ovfimg = add_image_to_canvas(canvas, OVFvar1, x=864, y=260, width=47, height=47)
liftimg = add_image_to_canvas(canvas, LIFTvar1, x=866, y=325, width=47, height=47)
#gebruik de faciliteiten en zet ze als plaatje in het window. WCvar1 bijvoorbeeld geeft de waarde assets/wc.png dit word geregeld in de define databaseconnectionselectstationszuil


image_path = "assets/Nederlandse_Spoorwegen_logo.svg.png"
image = add_image_to_canvas(canvas, image_path, x=870, y=17, width=50, height=20)
image_path1 = "assets/hogeschool-utrecht-logo-png-transparent.png"
image1 = add_image_to_canvas(canvas, image_path1, x=360, y=1390, width=210, height=49)
#voeg plaatjes toe aan het window.

window.resizable(False, False)
#je mag het niet resizen.
window.mainloop()