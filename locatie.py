# maak een functie aan die elke keer word opgeroepen om de locatie te vinden. als er nog niks in het bestand staat word het first time install script uitgevoerd
# hierbij komt er een schermpje waar een ns medewerker de locatie van de zuil kan instellen. dit is alleen bij de eerste keer dat je het uitvoerd
def firsttimeinstall():
    import csv
    import tkinter as tk
    import ctypes
    import os

    csv_file_path = 'station.csv'
    # maak een file aan

    if os.path.getsize(csv_file_path) == 0:

        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        #zorg ervoor dat ook op 4k beeldschermen het er mooi uit zien. door DPI aan te zetten. Hij checkt hiermee hoeveel pixels er per inch zitten.

        # Create the main window
        window = tk.Tk()
        window.title("Instalatieprogramma voor medewerkers")

        # Create the canvas
        canvas = tk.Canvas(window, width=800, height=1200)
        canvas.place(x=0, y=0)


        window.geometry("790x602")
        window.configure(bg = "#FFFFFF")

        canvas.create_rectangle(
            0.0,
            0.0,
            788.0,
            600.0,
            fill="#003082",
            outline=""
        )

        canvas.create_text(
            82.0,
            55.0,
            anchor="nw",
            text="Welkom bij het instalatieprogramma",
            fill="#FFFFFF",
            font=("Rubik Medium", 36 * -1)
        )

        canvas.create_text(
            82.0,
            103.0,
            anchor="nw",
            text="Dit is een instalatieprogramma voor NS-medewerkers.",
            fill="#FFFFFF",
            font=("Rubik Medium", 20 * -1)
        )

        canvas.create_text(
            262.0,
            165.0,
            anchor="nw",
            text="Waar staat de stationspaal?",
            fill="#FFFFFF",
            font=("Rubik Light", 20 * -1)
        )

        # lijst met stations waaruit je kan kiezen
        options = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]

        # maak een variabele aan die de optie die geselecteerd word hierin opslaat
        selected_option = tk.StringVar()
        selected_option.set(options[0])
        #altijd ingesteld op de eerste

        # maak het dropdown menu
        dropdown_menu = tk.OptionMenu(window, selected_option, *options)

        # Maak een dropdownmenu in window, en vul het met de options in
        # de keuze die word gemaakt die word opgeslagen in selected_option
        # Het * voor options pakt de dingen uit die er in options staat en gebruikt hierbij de tkinter action option menu

        dropdown_menu.place(x=345, y=200)
        #plaats het dropdown menu op deze locatie in het midden


        # maak een functie voor de option die gemaakt is
        def on_option_selected(*args):
            selected = selected_option.get()
            #krijg de geselecteerde optie met selected_option.get()
            print(f"De machine word nu ingesteld op de locatie: {selected}")


            # Schrijf variabelen weg in een csv file
            with open(csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                #schrijf iets weg in de file
                writer.writerow([selected])
                # variabelen zijn in de tekstfile gezet in comma,seperated,file

            print("Succesvol het instalatieprogramma afgerond \nEven geduld aub...")
            window.destroy()
            return selected
        #dit returnd Null, maar hier is in de main code een oplossing voor bedacht door het 2 keer te loopen als er null uit komt!

        # trace de option en kijk wat er gebeurd tot er op option word geklikt
        selected_option.trace("w", on_option_selected)

        # tkinter window
        window.mainloop()
    else:
        #als er iets in de file staat lees het dan uit en maak dat de stad waar hij is ingesteld
        with open(csv_file_path, 'r') as csv_file:
            stad = csv_file.readline().strip()
            #stad is readline() en haal met strip alle gekke spaties enters en strings eruit
            return stad