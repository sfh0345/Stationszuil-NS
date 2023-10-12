# This file was imported from Figma by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
#hier zie je welke python tool er gebruikt is om het om te zetten vanaf de design tool naar python.


from pathlib import Path
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label
import random
import psycopg2

from datetime import datetime
now = datetime.now()
datum = now.strftime("%d/%m/%Y %H:%M:%S")
#datum in een variable

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1349x877")
window.configure(bg = "#003082")


list_stations = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]
station = random.choice(list_stations)
window.title(f"Stationszuil NS {station}")
#database connectie om later te gebruiken.

connection_string = "host='172.166.152.26' dbname='Stationzuil' user='postgres' password='Sander0345'"


#database connectie om later te kunnen gebruiken.
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
        print("Er is iets fout gegaan. ERROR: ", e)

    finally:
        cursor.close()
        conn.close()

canvas = Canvas(
    window,
    bg = "#003082",
    height = 877,
    width = 1349,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

csv_file_path = 'input.csv'
def naaminput():
    global time123
    naam = entry_2.get("1.0", "end-1c").strip()  # Remove trailing newline
    if len(naam) == 0:
        naam = "Anoniem"
    elif len(naam) > 25 or "\n" in naam:
        time123 = canvas.create_text(
            320.0,
            812.0,
            anchor="nw",
            text="Vul alstubieft een kortere naam in.",
            fill="#FFFFFF",
            font=("Rubik SemiBold", 40 * -1)
        )
        window.after(3000, lambda: canvas.delete(time123))
        return None  # Return None if the name is too long
    return naam


def berichtinput():
    global time123
    bericht = text_widget.get("1.0", "end-1c").strip()  # Remove trailing newline

    if len(bericht) <= 140 and len(bericht) > 0:
        return bericht
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
        return None  # Return None if the message is empty
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
        return None  # Return None if the message is too long


def inleverenbutton():
    naam = naaminput()
    bericht = berichtinput()

    if naam is not None and bericht is not None:
        databaseconnectioninsert(naaminput(), berichtinput(), datum)

        text_widget.delete("1.0", "end")
        entry_2.delete("1.0", "end")
        time123 = canvas.create_text(
            416.0,
            812.0,
            anchor="nw",
            text="Bedankt voor uw feedback",
            fill="#FFFFFF",
            font=("Rubik SemiBold", 40 * -1)
        )
        window.after(3000, lambda: canvas.delete(time123))

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

text_widget = Text(
    bd=0,
    bg="#003062",
    fg="#FFFFFF",
    highlightthickness=0,
    wrap="word",  # Word wrapping
    padx=10,  # Horizontal padding
    pady=10,  # Vertical padding
    font=("Rubik Regular", 12),  # Adjust the font as needed

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
entry_2 = Text(
    bd=0,
    bg="#003070",
    fg="#FFFFFF",
    highlightthickness=0,
    font=("Rubik Regular", 12),  # Adjust the font as needed
    wrap="word",  # Word wrapping
    padx=10,  # Horizontal padding
    pady=10,  # Vertical padding
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
button_1.place(
    x=490.0,
    y=740.0,
    width=392.0,
    height=62.0
)
window.resizable(False, False)
window.mainloop()
