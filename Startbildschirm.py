#Startbildschirm
# Pygame Template https://www.pygame.org/project-Pathfinding+Experiment-2932-4829.html
import pygame
from time import sleep
import Speicher as S
try:
    from win11toast import toast, notify, update_progress
    wintoast = True
except:
    wintoast = False
    print("Bitte installiere Win11toast, um alle Features freizuschalten")
pygame.init()
#Sounds
pygame.mixer.init
sound_startbildschirm = pygame.mixer.Sound("Sounds/Tanks_Startbildschirm.mp3")
SB_Speicherort = "Accounts.json"
sounds = [sound_startbildschirm]
def setze_lautstärke(wert):
    pygame.mixer.music.set_volume(wert)
    for sound in sounds:
        sound.set_volume(wert)
# Setup für Startbildschirm
def Main(Nutzername):
    SB_BREITE = 600  # screenbreite für Startbildschirm
    SB_HOEHE = 600   # screenhöhe für Startbildschirm
    #Sounds
    
    lautstärke = S.read(Nutzername,"Lautstärke",ort = "Einstellungen",speicherort=SB_Speicherort)
    setze_lautstärke(lautstärke)
    
    sound_startbildschirm.play(loops=-1)
    screen = pygame.display.set_mode((SB_BREITE, SB_HOEHE))  # screengröße für den Startbildschirm
    pygame.display.set_caption("Startbildschirm")  # screentitel

    # Hintergrund und Schriftart für das Menü
    hintergrund = pygame.image.load("Hintergrund_Panzerkiste.png")
    hintergrund = pygame.transform.scale(hintergrund, (SB_BREITE, SB_HOEHE))  # Skaliere Hintergrundbild auf die angegebene Größe

    font = pygame.font.SysFont("Arial", 36)  # Schriftart und -größe
    BLAU = (0, 0, 255)  # Blaue Farbe für Auswahl
    WEIß = (255, 255, 255)  # Weiße Farbe für nicht selektierte Optionen

    stellen = ["Singleplayer","Shop", "Einstellungen", "Beenden"]
    selected_index = 0
    laeuft = True

    while laeuft:
        screen.blit(hintergrund, (0, 0))

        for i, text in enumerate(stellen):
            color = BLAU if i == selected_index else WEIß
            rendered = font.render(text, True, color)
            screen.blit(rendered, (200, 250 + i * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_startbildschirm.stop()
                return "Beenden"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(stellen)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(stellen)
                elif event.key == pygame.K_RETURN:
                    auswahl = stellen[selected_index]
                    if auswahl == "Singleplayer":
                        sound_startbildschirm.stop()
                        if wintoast:
                            notify(progress={
                                'title': 'Wird gestartet',
                                'status': 'Singleplayer wird vorbereited...',
                                'value': '0',
                                'valueStringOverride': '0/100%'
                            })

                            for i in range(1, 102,1):
                                sleep(0.025)
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
                        else:
                            print("Installier jetzt endlich win11toast !!!")
                        return "Singleplayer"
                        
                    elif auswahl == "Multiplayer":
                        sound_startbildschirm.stop()
                        return "Multiplayer"
                    elif auswahl == "Einstellungen":
                        sound_startbildschirm.stop()
                        return "Einstellungen"
                    elif auswahl == "Beenden":
                        sound_startbildschirm.stop()
                        return "Beenden"
                    elif auswahl == "Shop":
                        sound_startbildschirm.stop()
                        return "Shop"

        pygame.display.flip()
