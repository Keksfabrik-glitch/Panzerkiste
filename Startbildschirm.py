# Pygame Template https://www.pygame.org/project-Pathfinding+Experiment-2932-4829.html
from win11toast import toast
import pygame
#Variablen
stellen = ["Singelplayer" ,"Multiplayer" , "Einstellungen" , "Beenden"]
selected_index = 0
# Setup
pygame.init()
BREITE = 600
HOEHE = 600
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Startbildschirm")
laeuft = True
# clock = pygame.time.Clock()
#Hintergrund
hintergrund = pygame.image.load("Hintergrund_Panzerkiste.png")
hintergrund = pygame.transform.scale(hintergrund ,(BREITE, HOEHE))
#Schriftart
font = pygame.font.SysFont("Arial", 36)  # Schriftart & Größe
#Farben
ROT = (255, 0, 0)
SCHWARZ = (0, 0, 0)
GRÜN = (0, 255, 0)
WEIß = (255,255,255)
BLAU = (0,0,255)
# Gameloop / Spielschleife
while laeuft:
    #Hintergrund
    fenster.blit(hintergrund , (0,0))
    for i in range (0,len(stellen)):
        if i == selected_index:
            color = BLAU  #  für Auswahl
        else:
            color = WEIß  #  normal
        
        rendered = font.render(stellen[i], True, color)
        fenster.blit(rendered, (200, 250 + i * 50))  # vertikal untereinander

    
    # Ereignisse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laeuft = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(stellen)
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(stellen)
            elif event.key == pygame.K_RETURN:
                print("Ausgewählt:", stellen[selected_index])
                toast('Ausgewählt: ', stellen[selected_index])
                if stellen[selected_index] == "Beenden":
                    laeuft = False
            

    pygame.display.flip()

    # clock.tick(60)  # limits FPS to 60

# Ende
pygame.quit()
exit()

