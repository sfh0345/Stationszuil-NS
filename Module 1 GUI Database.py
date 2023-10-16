# This file was imported from Figma by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
#hier zie je welke python tool er gebruikt is om het om te zetten vanaf de design tool naar python.


from pathlib import Path
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)
#zorg ervoor dat ook op 4k beeldschermen het er mooi uit zien. door DPI aan te zetten. Hij checkt hiermee hoeveel pixels er per inch zitten.
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label
import random
import psycopg2
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

#database connectie om later te gebruiken.

from datetime import datetime
now = datetime.now()
datum = now.strftime("%d/%m/%Y %H:%M:%S")
#datum in een variable

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")
#het pad naar de assets die worden gebruikt. Plaatjes etc

#code om deze paths ook te kunnen gebruiken verderop in de code
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("1349x877")
window.configure(bg = "#003082")
#maak een window aan met afmetingen en de goede achtergrondkleur.


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
window.title(f"Stationszuil NS {station}")
# hier word een random station gekozen en word de titel bovenaan het scherm ook gevuld

#database connectie om later te kunnen gebruiken.
def databaseconnectioninsert(naam, feedback, datum):
    try:
        #maak een cursor aan
        conn = establish_connection()
        cursor = conn.cursor()

        # maak een variabele aan om de insert into te storen voor als je hem later execute
        insert_query = "INSERT INTO feedback (naam, feedback, datum) VALUES (%s, %s, %s);"

        # execute de variabele met %s vervangen door variabelen
        cursor.execute(insert_query, (naam, feedback, datum))
        #commit het
        conn.commit()

    except psycopg2.Error as e:
        print("Er is iets fout gegaan. \nERROR: ", e)
        #als sql een error geeft word deze hier mooi neer geschreven

    finally:
        cursor.close()
        close_connection(conn)
        #close de connectie met de database

canvas = Canvas(
    window,
    bg = "#003082",
    height = 877,
    width = 1349,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
#maak een window aan

#define naaminput om later te kunnen gebruiken
def naaminput():
    naam = entry_2.get("1.0", "end-1c").strip()
    #krijg de naam zonder spaties of enters erachter
    if len(naam) == 0:
        naam = "Anoniem"
    elif len(naam) > 25 or "\n" in naam:
        #geen newline in naam. anders gaat de naambox kapot.
        time123 = canvas.create_text(
            320.0,
            812.0,
            anchor="nw",
            text="Vul alstubieft een kortere naam in.",
            fill="#FFFFFF",
            font=("Rubik SemiBold", 40 * -1)
        )
        window.after(3000, lambda: canvas.delete(time123))
        #verwijder het bericht na 3 seconden
        return None  # return niks als het bericht te lang is of niet goed is
    return naam

# define berichtinput om later te gebruiken.
def berichtinput():
    bericht = text_widget.get("1.0", "end-1c").strip()
    # verwijder met .strip spaties en enters achter het opgehaalde bericht

    if len(bericht) <= 140 and len(bericht) > 0:
        return bericht
    #als de lengte van het bericht goed is return
    elif len(bericht) == 0:
        time = canvas.create_text(
            416.0,
            812.0,
            anchor="nw",
            text="Er staat niks in uw bericht.",
            fill="#FFFFFF",
            font=("Rubik SemiBold", 40 * -1)
        )
        window.after(3000, lambda: canvas.delete(time))
        #verwijder na 3 seconden het bericht
        return None  # return niks als er niks in het bericht staat.
    else:
        time = canvas.create_text(
            310.0,
            812.0,
            anchor="nw",
            text="Uw bericht is langer dan 140 karakters.",
            fill="#FFFFFF",
            font=("Rubik SemiBold", 40 * -1)
        )
        window.after(3000, lambda: canvas.delete(time))
        #verwijder na 3 seconden het bericht
        return None  # return niks als er niks in het bericht staat

#define inleverenbutton omdat je geen meerdere regeles code in lambda mag zetten
def inleverenbutton():
    naam = naaminput()
    bericht = berichtinput()
    #pak de defines en stop ze in een variabele

    if naam is not None and bericht is not None:
        databaseconnectioninsert(naaminput(), berichtinput(), datum)
        #roep de database op met de goede variabelen

        text_widget.delete("1.0", "end")
        entry_2.delete("1.0", "end")
        #verwijder tekst uit de tekstboxen nadat er op inleveren is gedrukt. Er was namelijke een probleem dat als je op inleveren drukte je text bleef staan voor de volgende gebruiker om te zien.
        time123 = canvas.create_text(
            416.0,
            812.0,
            anchor="nw",
            text="Bedankt voor uw feedback",
            fill="#FFFFFF",
            font=("Rubik SemiBold", 40 * -1)
        )
        window.after(3000, lambda: canvas.delete(time123))
        #verwijder na 3 seconden

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1349.0,
    877.0,
    fill="#E4E4E4",
    outline="")

canvas.create_rectangle(
    0.0,
    168.0,
    1349.0,
    877.0,
    fill="#003082",
    outline="")

canvas.create_text(
    49.0,
    25.0,
    anchor="nw",
    text=f"Welkom op station NS {station}",
    fill="#0063D3",
    font=("Rubik Medium", 64 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    675.0,
    529.0,
    image=entry_image_1
)
#inputbox
text_widget = Text(
    bd=0,
    bg="#003062",
    fg="#FFFFFF",
    highlightthickness=0,
    wrap="word",  #zorg ervoor dat de woorden binnen de box blijven
    padx=10,  # padding op de box zodat de text niet buiten de box komt
    pady=10,  # padding op de box zodat de text niet butien de box komt
    font=("Rubik Regular", 12),  # pas het font aan naar rubik

)
text_widget.place(
    x=77.0,
    y=338.0,
    width=1196.0,
    height=380.0
)
canvas.create_rectangle(
    77.0,
    264.0,
    1273.0,
    274.0,
    fill="#FFC917",
    outline="")

canvas.create_text(
    49.0,
    95.0,
    anchor="nw",
    text="U kunt op deze paal uw feedback invoeren",
    fill="#4D4D4D",
    font=("Rubik Medium", 32 * -1)
)

canvas.create_text(
    77.0,
    200.0,
    anchor="nw",
    text="Naam:",
    fill="#FFFFFF",
    font=("Rubik SemiBold", 40 * -1)
)

canvas.create_text(
    77.0,
    294.0,
    anchor="nw",
    text="Typ hier uw feedback:",
    fill="#FFFFFF",
    font=("Rubik SemiBold", 29 * -1)
)
canvas.create_text(
    400.0,
    300.0,
    anchor="nw",
    text="(Max 140 karakters)",
    fill="#FFFFFF",
    font=("Rubik SemiBold", 20 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    743.5,
    225.0,
    image=entry_image_2
)
#maak een textbox
entry_2 = Text(
    bd=0,
    bg="#003070",
    fg="#FFFFFF",
    highlightthickness=0,
    font=("Rubik Regular", 12),  # verander het font naar rubik
    wrap="word",  # word wrapping zodat de tekst niet buiten de box kan komen.
    padx=10,  # padding zodat de woorden niet buiten de box komen
    pady=10,  # padding zodat de woorden niet buiten de box komen
)
entry_2.place(
    x=214.0,
    y=201.0,
    width=1059.0,
    height=46.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: inleverenbutton(),
    relief="flat"
)
#maak een button met als command lambda inleverenbutton()
button_1.place(
    x=490.0,
    y=740.0,
    width=392.0,
    height=62.0
)
#plaats de button.
window.resizable(False, False)
window.mainloop()
