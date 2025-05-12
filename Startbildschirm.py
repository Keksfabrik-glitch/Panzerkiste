# Pygame Template
import pygame
stellen = ["Singelplayer" ,"Multiplayer" , "Einstellungen" , "Beenden"]
selected_index = 0
# Setup
pygame.init()
BREITE = 600
HOEHE = 600
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Startbildschirm")
# clock = pygame.time.Clock()
laeuft = True

# Gameloop / Spielschleife
while laeuft:
  for i in range (0,len(stellen)):
      if i == selected_index:
            color = (255, 0, 0)  # ROT für Auswahl
        else:
            color = (255, 255, 255)  # WEISS normal
        
      rendered = font.render(stellen[i], True, color)
      screen.blit(rendered, (100, 100 + i * 50))  # vertikal untereinander

    pygame.display.flip()
    # Ereignisse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laeuft = False
    tastatur = pygame.key.get_pressed()
    if tastatur[pygame.K_DOWN] :
      selected_index += 1
    if tastatur[pygame.K_UP] :
      selected_index += 1
        
            

    pygame.display.flip()

    # clock.tick(60)  # limits FPS to 60

# Ende
pygame.quit()
exit()
