# Main
try:
    from win11toast import toast, notify, update_progress
    wintoast = True
except:
    wintoast = False
    print("Bitte installiere Win11toast, um alle Features freizuschalten")
#try:
    #from moviepy import VideoFileClip
    #werbung = True
#except:
    #werbung = False
    #if wintoast:
        #notify('unvollständig', 'Bitte installiere moviepy um alle features freizuschalten', audio='ms-winsoundevent:Notification.IM')
    #else:
        #print("Bitte installiere moviepy um alle features freizuschalten")
import random
import pygame
import panzer as P
import Shop as S
import Startbildschirm as SB
import Account as Acc
import Einstellungen as E
# Setup
pygame.init()
pygame.display.set_caption("Panzerkiste")
pygame.font.init()
#Werbung
#werbespots = ["RickRoll.mp4","Schumacher.mp4"]
# Hauptschleife
Nutzername = Acc.Main()
if Nutzername == None:
    running = False
else:
    running = True
    #print(Nutzername)
while running:
    auswahl = SB.Main(Nutzername)  # Fenster übergeben
    if auswahl == "Singleplayer":
        P.Main(Nutzername)          # Fenster übergeben
    elif auswahl == "Beenden":
        running = False
    elif auswahl == "Einstellungen":
        #if werbung:
            #VideoFileClip(random.choice(werbespots)).preview()
        E.main(Nutzername)
    elif auswahl == "Shop":
        S.Main(Nutzername)
# Ende
pygame.quit()
exit()
