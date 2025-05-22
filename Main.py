# Main
try:
    from win11toast import toast, notify, update_progress
    wintoast = True
except:
    wintoast = False
    print("Bitte installiere Win11toast, um alle Features freizuschalten")
import pygame
import Startbildschirm as SB
import panzer as P

# Setup
pygame.init()
pygame.display.set_caption("Panzerkiste")

# Hauptschleife
running = True
while running:
    auswahl = SB.Main()  # Fenster übergeben
    if auswahl == "Singleplayer":
        P.Main()          # Fenster übergeben
    elif auswahl == "Beenden":
        running = False
    elif auswahl == "Multiplayer":
        if wintoast:
            notify('Fehler', 'Multiplayer ist noch nicht verfügbar.', audio='ms-winsoundevent:Notification.IM')
        else:
            print:("Fehler, Einstellungen sind noch nicht verfügbar.")
    elif auswahl == "Einstellungen":
        if wintoast:
            notify('Fehler', 'Einstellungen sind noch nicht verfügbar.', audio='ms-winsoundevent:Notification.IM')
        else:
            print:("Fehler, Einstellungen sind noch nicht verfügbar.")

# Ende
pygame.quit()
exit()
