
import pygame
import colorsys
import math
from time import sleep
try:
    from win11toast import toast, notify, update_progress
    wintoast = True
except:
    wintoast = False
    print("Bitte installiere Win11toast, um alle Features freizuschalten")
try:
    import sys
    sysVerfügbar = True
except:
    sysVerfügbar = False
    print("Bitte installiere sys, um alle Features freizuschalten")
pygame.init()
# Setup für Startbildschirm
font = pygame.font.SysFont(None, 24)
SAND = (239, 228, 176)

FarbStartPreis = 10
PastelMaxAufpreis = 90
def FarbPreisBerechnen(Farbe):
    preis = 10
    r, g, b, a = Farbe
    r, g, b = r/255, g/255, b/255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s,v = s*100,v*100
    PastelEck = [(32, 95),(32, 58),(95, 74),(70, 95)]
    Mitte = (57.25, 80.5)    
    FarbPunkt = (s,v)
    max_entfernung = 0 # 
    for pastell in PastelEck:
        if math.dist(Mitte, pastell) > max_entfernung:
            max_entfernung = math.dist(Mitte, pastell)
    entfernung = math.dist(Mitte, FarbPunkt)
    entfernung = min(entfernung, max_entfernung)
    f = entfernung / max_entfernung
    preis = PastelMaxAufpreis - f #* (PastelMaxAufpreis - BASIS_PREIS)
    print(s,v)
    print(preis,int(preis))
    print("---")

class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, länge,value,max,min,steps):
        super().__init__()
        self.pos = (x,y)
        self.länge = länge
        self.value = value
        self.max = max
        self.min = min
        self.steps = steps


def Main(screen=None):
    BREITE = 100*16  # screenbreite für Startbildschirm
    HOEHE = 100*9   # screenhöhe für Startbildschirm

    if screen is None:
        screen = pygame.display.set_mode((BREITE, HOEHE), pygame.RESIZABLE)  # screengröße für den Startbildschirm
    pygame.display.set_caption("Startbildschirm")  # screentitel

    # Hintergrund und Schriftart für das Menü
    #hintergrund = pygame.image.load("Hintergrund_Panzerkiste.png")
    #hintergrund = pygame.transform.scale(hintergrund, (BREITE, HOEHE))  # Skaliere Hintergrundbild auf die angegebene Größe
    BLAU = (0, 0, 255)  # Blaue Farbe für Auswahl
    WEIß = (255, 255, 255)  # Weiße Farbe für nicht selektierte Optionen

    laeuft = True
    #screensurface = pygame.display.get_surface ()
    clock = pygame.time.Clock()
    #image = pygame.image.load ("./ColourPicture.bmp")
    #image_rect = image.get_rect()

    mouseUP = True
    farbe = (0,0,0,0)
    FarbTon= (255,0,0)
    FarbWahlHSVBereichGröße = (300,250)
    while laeuft:
        #screen.blit(hintergrund, (0, 0))
        screen.fill(SAND)
        #screen.blit (image, image_rect)
        #pygame.display.flip()
        for event in pygame.event.get ():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseUP = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouseUP = True
        if mouseUP == False: # Maustaste gedrückt
            mouse = pygame.mouse.get_pos()
            #if image_rect.collidepoint(mouse):  # Maus über der Auswahlfläche
            #    farbe = screensurface.get_at(mouse)
             #   FarbPreisBerechnen(farbe)
        surf = pygame.Surface((1, 2))
        surf.fill((255,255,255))
        surf.set_at((0, 1), (0, 0,0))
        surf = pygame.transform.smoothscale(surf, FarbWahlHSVBereichGröße)

        surf2 = pygame.Surface((2,1))
        surf2.fill((255,255,255))
        surf2.set_at((1, 0), (FarbTon))
        surf2 = pygame.transform.smoothscale(surf2, (FarbWahlHSVBereichGröße))
        surf.blit(surf2, (0, 0), special_flags=pygame.BLEND_MULT)
        screen.blit(surf, (0, 0))
        
        farbPreview = pygame.Rect(325, 200, 50, 50)
        pygame.draw.rect(screen, farbe, farbPreview, border_radius=10)
        pygame.draw.rect(screen, (0,0,0), farbPreview, width=3, border_radius=10)
        pygame.display.flip()   
        clock.tick(60)

Main()