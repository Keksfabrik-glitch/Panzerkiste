# Pygame Template
from win11toast import toast, notify, update_progress
import pygame
import Startbildschirm as SB

# Setup
pygame.init()
BREITE = 600
HOEHE = 600
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Panzerkiste")
# clock = pygame.time.Clock()
laeuft = True

# Gameloop / Spielschleife
while laeuft:

    SB.Main()



# Ende
pygame.quit()
exit()
