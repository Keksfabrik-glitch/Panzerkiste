#Startbildschirm
# Pygame Template https://www.pygame.org/project-Pathfinding+Experiment-2932-4829.html
import pygame
from time import sleep
try:
    from win11toast import toast, notify, update_progress
    wintoast = True
except:
    wintoast = False
    print("Bitte installiere Win11toast, um alle Features freizuschalten")
pygame.init()
# Setup für Startbildschirm
font = pygame.font.SysFont(None, 24)
SAND = (239, 228, 176)
def Main(screen=None):
    BREITE = 100*16  # screenbreite für Startbildschirm
    HOEHE = 100*9   # screenhöhe für Startbildschirm

    if screen is None:
        screen = pygame.display.set_mode((BREITE, HOEHE))  # screengröße für den Startbildschirm
    pygame.display.set_caption("Startbildschirm")  # screentitel

    # Hintergrund und Schriftart für das Menü
    #hintergrund = pygame.image.load("Hintergrund_Panzerkiste.png")
    #hintergrund = pygame.transform.scale(hintergrund, (BREITE, HOEHE))  # Skaliere Hintergrundbild auf die angegebene Größe
    BLAU = (0, 0, 255)  # Blaue Farbe für Auswahl
    WEIß = (255, 255, 255)  # Weiße Farbe für nicht selektierte Optionen

    laeuft = True

    while laeuft:
        #screen.blit(hintergrund, (0, 0))
        screen.fill(SAND)
        pygame.display.flip()
        #clock.tick(60)

#Main()