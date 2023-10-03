import csv
import os

# Define file paths
csv_file_path = 'geaccepteerd.csv'

lines_to_read = 6  # Number of lines to read

if os.path.getsize(csv_file_path) == 0:
    print("Er zijn geen reviews om weer te geven.")
else:
    try:
        inputlijst = []
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for i, row in enumerate(csv_reader):
                if i >= lines_to_read:
                    break
                if len(row) == 8:
                    inputlijst.append({
                        'Naam': row[0],
                        'Feedback': row[1],
                        'Locatie': row[2],
                        'Datum': row[3]
                    })

        # Print the data vertically
        for row in inputlijst:


    except FileNotFoundError:
        print(f"Het bestand is niet gevonden.")
