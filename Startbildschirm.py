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
def Main(fenster):
    stellen = ["Singleplayer", "Multiplayer", "Einstellungen", "Beenden"]
    selected_index = 0
    laeuft = True

    # Assets laden etc. (wie gehabt)

    while laeuft:
        fenster.blit(hintergrund, (0, 0))

        for i, text in enumerate(stellen):
            color = BLAU if i == selected_index else WEIß
            rendered = font.render(text, True, color)
            fenster.blit(rendered, (200, 250 + i * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Beenden"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(stellen)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(stellen)
                elif event.key == pygame.K_RETURN:
                    auswahl = stellen[selected_index]
                    if auswahl == "Singleplayer":
                        notify(progress={
                            'title': 'Wird gestartet',
                            'status': 'Singleplayer wird vorbereited...',
                            'value': '0',
                            'valueStringOverride': '0/100%'
                        })

                        for i in range(1, 102):
                            sleep(0.01)
                            update_progress({'value': i/100, 'valueStringOverride': f'{i}/100%'})
                            if i == 25:
                                update_progress({'status': 'Panzer werden geladen!'})
                            elif i == 75:
                                update_progress({'status': 'Projektile werden geladen!'})
                        update_progress({'status': 'Fertig!'})

                        return "Singleplayer"
                    elif auswahl == "Multiplayer":
                        return "Multiplayer"
                    elif auswahl == "Einstellungen":
                        return "Einstellungen"
                    elif auswahl == "Beenden":
                        return "Beenden"

        pygame.display.flip()
