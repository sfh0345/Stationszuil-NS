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

        # Create a label
        label = tk.Label(window, text="Welkom bij het instalatieprogramma")
        label1 = tk.Label(window, text="Dit is een instalatieprogramma voor NS-medewerkers.")
        label.pack()

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

        # Define the options for the dropdown menu
        options = ["Arnhem", "Almere", "Amersfoort", "Almelo", "Alkmaar", "Apeldoorn", "Assen", "Amsterdam", "Boxtel", "Breda", "Dordrecht", "Delft", "Deventer", "Enschede", "Gouda", "Groningen", "Den Haag", "Hengelo", "Haarlem", "Helmond", "Hoorn", "Heerlen", "Den Bosch", "Hilversum", "Leiden", "Lelystad", "Leeuwarden", "Maastricht", "Nijmegen", "Oss", "Roermond", "Roosendaal", "Sittard", "Tilburg", "Utrecht", "Venlo", "Vlissingen", "Zaandam", "Zwolle", "Zutphen"]

        # Create a variable to hold the selected option
        selected_option = tk.StringVar()
        selected_option.set(options[0])  # Set the default selected option

        # Create the dropdown menu and set its coordinates
        dropdown_menu = tk.OptionMenu(window, selected_option, *options)
        dropdown_menu.place(x=320, y=200)  # Adjust the coordinates as needed






        # Function to handle option selection
        def on_option_selected(*args):
            selected = selected_option.get()
            print(f"Optie geselecteerd: {selected}")


            # Schrijf variabelen weg in een csv file
            with open(csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([selected])
                # variabelen zijn in de tekstfile gezet in comma,seperated,file

            print("Succesvol het instalatieprogramma afgerond")
            return selected

            window.destroy()

        # Attach a callback function to the variable to monitor changes
        selected_option.trace("w", on_option_selected)

        # Run the Tkinter main loop
        window.mainloop()
    else:
        with open(csv_file_path, 'r') as csv_file:
            stad = csv_file.readline().strip()
            print(f"The first word in the CSV file is: {stad}")
            return stad