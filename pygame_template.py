# Pygame Template
import pygame

# Setup
pygame.init()
BREITE = 600
HOEHE = 600
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Weihnachtsspiel")
# clock = pygame.time.Clock()
laeuft = True

# Gameloop / Spielschleife
while laeuft:
    # Ereignisse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laeuft = False
            

    pygame.display.flip()

    # clock.tick(60)  # limits FPS to 60

# Ende
pygame.quit()
exit()