
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

FarbStartPreis = 20
PastelMaxAufpreis = 90
def FarbPreisBerechnen(Farbe):
    preis = 10
    r, g, b, a = Farbe
    r, g, b = r/255, g/255, b/255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s,v = s*100,v*100
    #PastelEck = [(32, 95),(32, 58),(95, 74),(70, 95)]
    Mitte = (57.25, 80.5)    
    FarbPunkt = (s,v)
    preis = FarbStartPreis
    if s < 95 and s > 32:
        if v < 95 and v > 58:
            distS = abs(Mitte[0]-s)
            distV = abs(Mitte[1]-v)
            preis += int(PastelMaxAufpreis - (distS + distV))
    if v < 55:
        steps = (FarbStartPreis-5)/55
        preis -= int((55-v)*steps)
    if s < 20:
        steps = (FarbStartPreis-5)/20
        preis -= int((20-s)*steps)
    if v > 80:
        steps = (FarbStartPreis+5)/20
        preis += int((v-80)*steps)
    preis = max(preis,1)
    return preis

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
    SH_BREITE = 30*16  
    SH_HOEHE = 30*9   

    if screen is None:
        screen = pygame.display.set_mode((SH_BREITE, SH_HOEHE), pygame.RESIZABLE)  
    pygame.display.set_caption("Shop")  

    BLAU = (0, 0, 255)  
    WEIß = (255, 255, 255)  

    laeuft = True
    clock = pygame.time.Clock()

    mouseUP = True
    FARBBEREICH_POS = (10,10)
    farbe = (255,0,0,0)
    FarbTon= (255,0,0)
    FarbWahlHSVBereichGröße = (300,250)
    FarbTonSliderGröße = (25,250)
    FarbTonSlider_pos = (310+FARBBEREICH_POS[0], FARBBEREICH_POS[1]) 

    basis = pygame.Surface((360, 1))
    for x in range(360):
        h = x / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        basis.set_at((x, 0), (int(r*255), int(g*255), int(b*255)))
    basis = pygame.transform.rotate(basis, 90)
    FarbTonSurface = pygame.transform.smoothscale(basis, FarbTonSliderGröße)
    FarbWahlSurface = pygame.Surface(FarbWahlHSVBereichGröße)
    while laeuft:
        screen.fill(SAND)
        for event in pygame.event.get ():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseUP = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouseUP = True
        if mouseUP == False: # Maustaste gedrückt
            MausX, MausY = pygame.mouse.get_pos()
            RelX = MausX - FarbTonSlider_pos[0]
            RelY = MausY - FarbTonSlider_pos[1]
            if 0 <= RelX < FarbTonSliderGröße[0] and 0 <= RelY < FarbTonSliderGröße[1]:
                FarbTon = FarbTonSurface.get_at((int(RelX), int(RelY)))
                farbe = FarbTon #Absicht
            else:
                RelX = MausX - FARBBEREICH_POS[0]
                RelY = MausY - FARBBEREICH_POS[1]
                if 0 <= RelX < FarbWahlHSVBereichGröße[0] and 0 <= RelY < FarbWahlHSVBereichGröße[1]:
                    farbe = FarbWahlSurface.get_at((int(RelX), int(RelY)))
                else:
                    print("ELSE")
                    farbe = (255, 0,0, 0)
            FarbPreisBerechnen(farbe)
        screen.blit(FarbTonSurface, FarbTonSlider_pos)
        pygame.draw.rect(screen, (0, 0, 0), ((FarbTonSlider_pos[0],FarbTonSlider_pos[1]), (FarbTonSliderGröße[0],FarbTonSliderGröße[1])), 2, )
        
        surf = pygame.Surface((1, 2))
        surf.fill((255,255,255))
        surf.set_at((0, 1), (0, 0,0))
        surf = pygame.transform.smoothscale(surf, FarbWahlHSVBereichGröße)

        surf2 = pygame.Surface((2,1))
        surf2.fill((255,255,255))
        surf2.set_at((1, 0), (FarbTon))
        surf2 = pygame.transform.smoothscale(surf2, (FarbWahlHSVBereichGröße))
        surf.blit(surf2, (0, 0), special_flags=pygame.BLEND_MULT)
        screen.blit(surf, FARBBEREICH_POS)
        FarbWahlSurface.blit(surf, (0, 0))
        FarbWahlSurface.blit(surf2, (0, 0), special_flags=pygame.BLEND_MULT)
        farbPreview = pygame.Rect(345+FARBBEREICH_POS[0], 200+FARBBEREICH_POS[1], 50, 50)
        pygame.draw.rect(screen, (0, 0, 0), (FARBBEREICH_POS, FarbWahlHSVBereichGröße), 2)
        pygame.draw.rect(screen, farbe, farbPreview, border_radius=10)
        pygame.draw.rect(screen, (0,0,0), farbPreview, width=3, border_radius=10)
        pygame.display.flip()   
        clock.tick(60)

Main()