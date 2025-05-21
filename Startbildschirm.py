# Pygame Template https://www.pygame.org/project-Pathfinding+Experiment-2932-4829.html
from time import sleep
from win11toast import notify, update_progress,toast

import pygame
#Variablen

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
def Main():
    stellen = ["Singelplayer" ,"Multiplayer" , "Einstellungen" , "Beenden"]
    selected_index = 0
    laeuft = True
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
                    if stellen[selected_index] == "Beenden":
                        laeuft = False
                        pygame.quit()
                    if stellen[selected_index] == "Singelplayer":
                        notify(progress={
                            'title': 'Wird gestarted',
                            'status': 'Singelplayer wird vorbereited...',
                            'value': '0',
                            'valueStringOverride': '0/15 videos'
                        })

                        for i in range(1, 102,1):
                            sleep(0.05)
                            update_progress({'value': i/100, 'valueStringOverride': f'{i}/100%'})
                            if i == 1: 
                                update_progress({'status': 'Map wird geladen!'})
                            if i == 25: 
                                update_progress({'status': 'Panzer werden geladen!'})
                            elif i == 50:
                                update_progress({'status': 'Gegner werden trainiert!'})
                            elif i == 75:
                                update_progress({'status': 'Projektiele werden geladen!'})
                            elif i == 101:
                                update_progress({'value': "100/100", 'valueStringOverride': "100/100%"})
                                i = 100
                        update_progress({'status': 'Fertig!'})
                    if stellen[selected_index] == "Multiplayer":
                        notify('Fehler', 'Es gibt noch keinen Multiplayer', audio='ms-winsoundevent:Notification.IM')
        pygame.display.flip()

        # clock.tick(60)  # limits FPS to 60

    # Ende
    pygame.quit()
    exit()

Main()
