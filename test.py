import os

# Functie om feedback te lezen uit het bestand
def lees_feedback(bestandsnaam):
    feedback = []
    if os.path.exists(bestandsnaam):
        with open(bestandsnaam, 'r') as bestand:
            feedbacktekst = bestand.readlines()
            for blok in feedbacktekst:
                feedback.append(blok.strip())
    return feedback

# Functie om feedback te schrijven naar geaccepteerd of afgewezen bestand
def schrijf_feedback(bestandsnaam, feedback, status):
    with open(bestandsnaam, 'a') as bestand:
        for bericht in feedback:
            bestand.write(bericht + "\n")
        bestand.write("Status: " + status + "\n" + "-------------------------------------------------------------\n")

# Functie om feedback te verwijderen uit het bronbestand
def verwijder_feedback(bestandsnaam, start, einde):
    if os.path.exists(bestandsnaam):
        with open(bestandsnaam, 'r') as bestand:
            lijnen = bestand.readlines()
        with open(bestandsnaam, 'w') as bestand:
            for i, lijn in enumerate(lijnen):
                if i < start or i > einde:
                    bestand.write(lijn)

def main():
    print("Welkom bij het feedback moderatiedashboard")

    naam = input("Voer uw naam in: ")
    email = input("Voer uw e-mailadres in: ")

    bestandsnaam = "input.csv"  # Veronderstel dat feedback in een tekstbestand zit

    # Lees feedback uit het bestand in blokken van 7 regels
    feedbacktekst = lees_feedback(bestandsnaam)
    index = 0

    while index < len(feedbacktekst):
        blok = feedbacktekst[index:index+7]
        print("\n".join(blok))
        antwoord = input("Wilt u deze feedback accepteren? (ja/nee): ").lower()

        if antwoord == "ja":
            # Voeg de geaccepteerde feedback toe aan het geaccepteerd bestand
            schrijf_feedback("geaccepteerd_feedback.csv", blok, "geaccepteerd")
        elif antwoord == "nee":
            # Voeg de afgewezen feedback toe aan het afgewezen bestand
            schrijf_feedback("afgewezen_feedback.csv", blok, "afgewezen")
        else:
            print("Ongeldige invoer. Voer 'ja' of 'nee' in.")
            break

        # Verwijder de feedback uit het bronbestand
        start = index
        einde = index + 6
        verwijder_feedback(bestandsnaam, start, einde)

        # Ga door naar het volgende blok van 7 regels
        index += 7

print("Alle feedback is verwerkt.")

if __name__ == "__main__":
    main()
