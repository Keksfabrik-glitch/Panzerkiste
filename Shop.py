
import pygame
import colorsys
import math
import json
import Speicher as Daten
import panzer as P
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
# Setup
font = pygame.font.SysFont(None, 24)
SAND = (239, 228, 176)
SCHWARZ = (0,0,0)
GRAU = (200, 200, 200)
BLAU = (50, 100, 255)
FarbStartPreis = 20
PastelMaxAufpreis = 90
#Sounds
SH_Speicherort = "Accounts.json"
pygame.mixer.init()
sound_ca_cing = pygame.mixer.Sound("Sounds/Tanks_Ca-ching.mp3")
sounds = [sound_ca_cing]
def setze_lautstärke(wert):
    pygame.mixer.music.set_volume(wert)
    for sound in sounds:
        sound.set_volume(wert)
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
    if v > 80 and s > 20:
        steps = (FarbStartPreis+5)/20
        preis += int((v-80)*steps)
    preis = max(preis,1)
    return preis



class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, breite,höhe,value,min,max,steps = 1,interaktions_padding = 5):
        super().__init__()
        self.rect = pygame.Rect(x,y,breite,höhe)
        self.interaktions_padding = interaktions_padding
        self.InteractionRect = pygame.Rect(x- interaktions_padding, y - interaktions_padding, breite + 2 * interaktions_padding, höhe + 2 * interaktions_padding)
        self.pos = (x,y)
        self.größe = (breite,höhe)
        self.color = (0,0,0)
        self.min = min
        self.max = max-min
        self.steps = steps
        self.sliderPos = self.pos
        self.handle_rect = pygame.Rect(self.sliderPos[0], self.sliderPos[1]-2.5, 10, self.größe[1]+5)
        self.internValue = value
        self.value = self.internValue
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, SCHWARZ, self.rect, 2)
        pygame.draw.rect(screen, BLAU, self.handle_rect)
        pygame.draw.rect(screen, SCHWARZ, self.handle_rect, 1)

    def SliderButtonPos(self):
        relPos = self.internValue / self.max
        x = self.pos[0] + relPos * self.größe[0]
        y = self.pos[1]
        self.sliderPos = (x,y)
        self.handle_rect = pygame.Rect(self.sliderPos[0]-5, self.sliderPos[1]-2.5, 10, self.größe[1]+5)

    def valueVonPos(self,touch):
        diff = touch[0] - self.pos[0] 
        self.internValue = round((self.max*(1/self.steps)/self.größe[0])*diff) * self.steps
        self.value = self.internValue+self.min
        self.SliderButtonPos()
        
    def handle_event(self, pos):
        if self.InteractionRect.collidepoint(pos): 
            self.valueVonPos(pos)

class Button:
    def __init__(self, x, y, w, h, text, callback, font=font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (180, 180, 180)
        self.hover_color = (150, 150, 150)
        self.text = text
        self.callback = callback
        self.font = font
        self.text_surf = self.font.render(self.text, True, SCHWARZ)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        if is_hover:
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, SCHWARZ, self.rect, 2)

        text_rect = self.text_surf.get_rect(center=self.rect.center)
        screen.blit(self.text_surf, text_rect)

    def handle_event(self,mousePos):
        if self.rect.collidepoint(mousePos):
            self.callback()

#Ppwerlevel?

def Main(Nutzername):
    #Sounds
    lautstärke = Daten.read(Nutzername, "Lautstärke", ort="Einstellungen", speicherort=SH_Speicherort)
    Sounds = Daten.read(Nutzername,"Sound", ort="Einstellungen", speicherort=SH_Speicherort)
    setze_lautstärke(lautstärke)
    P.sound_jingle.stop()
    laeuft = True
    if Sounds:
        sound_ca_cing.play()
    class SettingsGroup():
        def kaufen(self):
            Geld = Daten.read(Nutzername,"punkte")
            Preis = self.preis
            if Geld >= Preis:
                self.saveValue = self.value
                if self.SaveName == "abprallChance":
                    self.saveValue = self.value/100
                Daten.write(Nutzername,"punkte",(Daten.read(Nutzername,"punkte")-Preis))
                Daten.write(Nutzername, self.SaveName, self.saveValue)
                self.maxOwnedValue = Daten.read(Nutzername,self.SaveName)
                if self.SaveName == "abprallChance":
                    self.maxOwnedValue = self.maxOwnedValue*100
                self.slider.internValue = self.value -self.min
                self.slider.SliderButtonPos()
                if Sounds:
                    sound_ca_cing.play()
                #if wintoast == True:
                    
            else:
                if wintoast:
                    toast("Fehler","Du hast zu wenig Geld. Upgrade um weniger Stats, oder verdiehne mehr Geld.",audio='ms-winsoundevent:Notification.IM')
            pygame.display.set_caption("Shop | Guthaben: {}$".format(Daten.read(Nutzername,"punkte")))
        def __init__(self,x,y,min,max,steps =1,name = "Titel",saveName = "farbe",Beschreibung = "Beschreibung",Preis = 10):
            self.pos = (x,y)
            
            self.Titel = name
            self.Beschreibung = Beschreibung
            self.PreisPS = Preis
            self.preis = 0
            self.min = min
            self.max = max
            self.SaveName = saveName
            self.maxOwnedValue = Daten.read(Nutzername,self.SaveName)
            if self.SaveName == "abprallChance":
                self.maxOwnedValue = self.maxOwnedValue*100


            
            self.value = self.maxOwnedValue
            self.Button = Button(x,y+55, 100, 40, "Kaufen", self.kaufen)
            self.slider = Slider(x, y+20, 200, 5, self.maxOwnedValue,min,max, steps)
            self.slider.internValue = self.value -self.min
            self.slider.SliderButtonPos()
        def sliderEvent(self,mousePos):
            self.slider.handle_event(mousePos)
            self.value = self.slider.value
            self.preis = (int(self.value) - self.maxOwnedValue)*self.PreisPS
        
            if self.max < self.min:
                self.preis = self.preis *-1
            if self.preis < 0:
                self.preis = self.preis/2
            else:
                self.preis = self.preis*(1-(int(self.value) - self.maxOwnedValue)/200)
            self.preis = int(self.preis)
        def buttonEvent(self,event):
            self.Button.handle_event(event)
        def draw(self,screen):
            self.slider.draw(screen)
            self.displayValue = self.value
            if self.SaveName == "abprallChance":
                #self.displayValue = self.value
                screen.blit(font.render("{}: {}% für {}$".format(self.Titel,self.displayValue,self.preis),True, SCHWARZ), (self.pos))
            else:
                screen.blit(font.render("{}: {} für {}$".format(self.Titel,self.displayValue,self.preis),True, SCHWARZ), (self.pos))
            screen.blit(font.render(str(self.Beschreibung), True, SCHWARZ), (self.pos[0],self.pos[1]+35))
            self.Button.draw(screen)

    SH_BREITE = 1325
    SH_HOEHE = 665

    screen = pygame.display.set_mode((SH_BREITE, SH_HOEHE), pygame.RESIZABLE)  
    Geld = Daten.read(Nutzername,"punkte")
    pygame.display.set_caption("Shop | Guthaben: {}$".format(Geld))  

    BLAU = (0, 0, 255)  
    WEIß = (255, 255, 255)  
    SCHWARZ = (0,0,0)
    clock = pygame.time.Clock()


    mouseUP = True
    FARBBEREICH_POS = (10,10)
    farbe =  pygame.Color(*tuple(json.loads(Daten.read(Nutzername,"farbe"))))
    FarbTon= (255,0,0)
    FarbWahlHSVBereichGröße = (300,250)
    FarbTonSliderGröße = (25,250)
    FarbTonSlider_pos = (310+FARBBEREICH_POS[0], FARBBEREICH_POS[1]) 


    STATS_POS = (FARBBEREICH_POS[0]+470,10)

    AbstandY = 135
    #3. Reihe
    
    GeschwindigkeitGroup = SettingsGroup(STATS_POS[0]+460,STATS_POS[1]+AbstandY*0,25,61,2,"Geschwindigkeit","geschwindigkeit","Die Geschwindigkeit deines Panzers",50/2)
    DrehGeschwindigkeitsGroup = SettingsGroup(STATS_POS[0]+460,STATS_POS[1]+AbstandY*1,5,10,1,"Dreheschwindigkeit","drehgeschwindigkeit","Die Drehgeschwindigkeit deines Panzers",25)
    AbprallerGroup = SettingsGroup(STATS_POS[0]+460,STATS_POS[1]+AbstandY*2,2,7,1,"Abpraller","abpraller","Maximale Abpraller deiner Kugeln",125) 
    AbprallChanceGroup = SettingsGroup(STATS_POS[0]+460,STATS_POS[1]+AbstandY*3,75,100,5,"Abprallchance","abprallChance","Die Chance das deine Kugel Abprallt",100/5) 
   
    #2. Reihe
    lebenGroup = SettingsGroup(STATS_POS[0],STATS_POS[1]+AbstandY*0,3,10,1,"Leben","leben","Die Anzahl der Leben deines Panzers",100)
    MaxKugelnGroup = SettingsGroup(STATS_POS[0],STATS_POS[1]+AbstandY*1,5,10,1,"Kugeln","maxKugeln","Kugeln pro Magazin",75)
    KugelSpeedGroup = SettingsGroup(STATS_POS[0],STATS_POS[1]+AbstandY*2,5,35,10,"Kugel Geschwindigkeit","kugelSpeed","Die Geschwindigkeit einer Kugel",150/10)
    SchussCooldownGroup = SettingsGroup(STATS_POS[0],STATS_POS[1]+AbstandY*3,240,40,20,"Schuss Cooldown","schussCooldown","Abstand zwischen zwei Schüssen",150/20)   
    NachladezeitGroup = SettingsGroup(STATS_POS[0],STATS_POS[1]+AbstandY*4,1,5,1,"Nachladezeit","nachladezeit","Nachladezeit deines Panzers in ms",150)

   
    #1. Reihe
    mieneZeitGroup = SettingsGroup(STATS_POS[0]-460,STATS_POS[1]+AbstandY*2,15,35,5,"Zünddauer Miene","mieneZeit","Zeit bis eine Miene Explodiert.",75/5) 
    mienenCooldownGroup = SettingsGroup(STATS_POS[0]-460,STATS_POS[1]+AbstandY*3,5,1,1,"Mienen Cooldown","mieneCooldown","Zeitspanne bis du eine neue Miene legen kannst.",150)
    explosionsRadiusGroup = SettingsGroup(STATS_POS[0]-460,STATS_POS[1]+AbstandY*4,40,80,10,"Explosionsradius","explosionsRadius","Der Betroffene Bereich bei einer Explosion.",100/10)
    #mienenAnzahlGroup = SettingsGroup(STATS_POS[0],STATS_POS[1]+AbstandY*6,5,10,1,"Kugeln","maxKugeln","Kugeln pro Magazin",75) UNENDLICH PRO SPIEL ZURZEIT. LEVELABHÄNGIG
    SettingGroupsss = [lebenGroup,GeschwindigkeitGroup,DrehGeschwindigkeitsGroup,MaxKugelnGroup,KugelSpeedGroup,SchussCooldownGroup,NachladezeitGroup,AbprallerGroup,AbprallChanceGroup,mieneZeitGroup,mienenCooldownGroup,explosionsRadiusGroup]    



    def FarbeKaufen():
        Farbpreis = FarbPreisBerechnen(farbe)
        Geld = Daten.read(Nutzername,"punkte")
        if Geld >= Farbpreis:
            Daten.write(Nutzername,"punkte",(Daten.read(Nutzername,"punkte")-Farbpreis))
            Daten.write(Nutzername, "farbe", json.dumps(list(farbe)))
            if Sounds:
                sound_ca_cing.play()
            #if wintoast == True:
                
        else:
            if wintoast:
                toast("Fehler","Du hast zu wenig Geld. Suche eine andere Farbe aus, oder verdiene mehr Geld.",audio='ms-winsoundevent:Notification.IM')
        pygame.display.set_caption("Shop | Guthaben: {}$".format(Daten.read(Nutzername,"punkte")))
    basis = pygame.Surface((360, 1))
    for x in range(360):
        h = x / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        basis.set_at((x, 0), (int(r*255), int(g*255), int(b*255)))
    basis = pygame.transform.rotate(basis, 90)
    FarbTonSurface = pygame.transform.smoothscale(basis, FarbTonSliderGröße)
    FarbWahlSurface = pygame.Surface(FarbWahlHSVBereichGröße)
    Farbpreis = 10

    FarbeKaufenButton = Button(FARBBEREICH_POS[0]+345,FARBBEREICH_POS[1]+50, 100, 40, "Kaufen", FarbeKaufen)

    hintergrund = pygame.image.load("Hintergrund_Shop.png")
    hintergrund = pygame.transform.scale(hintergrund,(SH_BREITE, SH_HOEHE))  # Skaliere Hintergrundbild auf die angegebene Größe
    while laeuft:
        screen.blit(hintergrund, (0, 0))
        
        for event in pygame.event.get ():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseUP = False
                for group in SettingGroupsss:
                    group.buttonEvent(pygame.mouse.get_pos())
                FarbeKaufenButton.handle_event(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                mouseUP = True
            if event.type == pygame.QUIT:
                laeuft = False

        if mouseUP == False: # Maustaste gedrückt
            MausX, MausY = pygame.mouse.get_pos()
            for group in SettingGroupsss:
                group.sliderEvent(pygame.mouse.get_pos())


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
                    farbe = farbe
            Farbpreis = FarbPreisBerechnen(farbe) # Punkte
            
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

        screen.blit(font.render("Farbpreis", True, SCHWARZ), (FARBBEREICH_POS[0]+345,FARBBEREICH_POS[1]))
        screen.blit(font.render(str(Farbpreis), True, SCHWARZ), (FARBBEREICH_POS[0]+345,FARBBEREICH_POS[1]+20))
        FarbeKaufenButton.draw(screen)

    
        for group in SettingGroupsss:
            group.draw(screen)
        pygame.display.flip()   
        clock.tick(60)

#Main("_Hannes_")