# Pygame Template
from win11toast import toast, notify, update_progress
import pygame
import Startbildschirm as SB
import panzer as P

# Setup
pygame.init()
BREITE = 600
HOEHE = 600
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Panzerkiste")

# Hauptschleife
running = True
while running:
    auswahl = SB.Main(fenster)  # Fenster übergeben
    if auswahl == "Singleplayer":
        P.Main(fenster)          # Fenster übergeben
    elif auswahl == "Beenden":
        running = False
    elif auswahl == "Multiplayer":
        notify('Fehler', 'Multiplayer ist noch nicht verfügbar.', audio='ms-winsoundevent:Notification.IM')
    elif auswahl == "Einstellungen":
        notify('Fehler', 'Einstellungen sind noch nicht verfügbar.', audio='ms-winsoundevent:Notification.IM')

# Ende
pygame.quit()
exit()
