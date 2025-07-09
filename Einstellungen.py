# Einstellungen
import pygame
import Speicher as S

# Setup
pygame.init()
E_BREITE = 500
E_HOEHE = 250

pygame.display.set_caption("Einstellungen")
E_Speicherort = "Accounts.json"

# Farben
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)
WEISS = (255, 255, 255)
SAND = (239, 228, 176)
SCHWARZ = (0,0,0)
BLAU = (0, 169, 252)
#Schrift
pygame.font.init()
FONT = pygame.font.SysFont("arial", 20,bold =  True)
#Sprite Groups
slider = pygame.sprite.Group()
pygame.mixer.init()
BlingSound = pygame.mixer.Sound("Sounds/Lautstaerke.wav")
sounds = [BlingSound]
def setze_lautstärke(wert):
    pygame.mixer.music.set_volume(wert)
    for sound in sounds:
        sound.set_volume(wert)


def main(nutzer, screen=None):
    class SwitchButton:
        def __init__(self, x, y, parameter, label= None, width=60, height=30):
            self.rect = pygame.Rect(x, y, width, height)
           
            self.nutzer = nutzer
            self.parameter = parameter
            self.label = label
            if self.label is None:
                self.label = self.parameter
            self.zustand = S.read(self.nutzer, self.parameter, ort="Einstellungen", speicherort=E_Speicherort)
            if self.parameter == "Sound":
                Lautstärke = S.read(nutzer,"Sound","Einstellungen")*100
                if Lautstärke >= 1: 
                    self.zustand = 1
                elif Lautstärke < 1:
                    self.zustand = 0
            self.anim_fortschritt = 1.0 if self.zustand else 0.0
            self.anim_geschwindigkeit = 0.1
            self.anim_zielwert = self.anim_fortschritt

        def draw(self, surface):
            # Text zeichnen links vom Button
            text_surface = FONT.render(self.label, True, WEISS)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (self.rect.right + 10, self.rect.centery)  # 10px Abstand links vom Button 
            surface.blit(text_surface, text_rect)


            r = ROT[0] + (GRÜN[0] - ROT[0]) * self.anim_fortschritt
            g = ROT[1] + (GRÜN[1] - ROT[1]) * self.anim_fortschritt
            b = ROT[2] + (GRÜN[2] - ROT[2]) * self.anim_fortschritt
            color = (int(r), int(g), int(b))

            pygame.draw.rect(surface, color, self.rect, border_radius=15)
            kreis_radius = self.rect.height // 2 - 3

            start = self.rect.x + kreis_radius + 3
            ende = self.rect.right - kreis_radius - 3
            kreis_x = start + (ende - start) * self.anim_fortschritt

            kreis_center = (kreis_x, self.rect.centery)
            pygame.draw.circle(surface, WEISS, kreis_center, kreis_radius)
            if abs(self.anim_fortschritt - self.anim_zielwert) > 0.01:
                richtung = 1 if self.anim_fortschritt < self.anim_zielwert else -1
                self.anim_fortschritt += self.anim_geschwindigkeit * richtung
                self.anim_fortschritt = max(0.0, min(1.0, self.anim_fortschritt))
            else:
                self.anim_fortschritt = self.anim_zielwert
        def klick(self,zustand):
            self.zustand = zustand
            self.anim_zielwert = 1.0 if self.zustand else 0.0  
            if self.parameter != "Lautstärke":
                S.write(self.nutzer, self.parameter, self.zustand, ort="Einstellungen", speicherort=E_Speicherort)
        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.zustand = not self.zustand
                    self.anim_zielwert = 1.0 if self.zustand else 0.0  
                    if self.parameter == "Lautstärke":
                        if self.zustand == 1:
                            S.write(nutzer,"Lautstärke", 0.5, ort="Einstellungen", speicherort=E_Speicherort)
                        else:
                            S.write(nutzer,"Lautstärke", 0,  ort="Einstellungen", speicherort=E_Speicherort)
                    else:
                       S.write(self.nutzer, self.parameter, True if self.zustand == 1 else False, ort="Einstellungen", speicherort=E_Speicherort)


    class Slider(pygame.sprite.Sprite):
        def __init__(self,parameter,x, y, breite,höhe,min,max,steps = 1,interaktions_padding = 10,Toggle = None):
            super().__init__()
            self.rect = pygame.Rect(x,y,breite,höhe)
            self.SaveValue = parameter
            self.interaktions_padding = interaktions_padding
            self.InteractionRect = pygame.Rect(x- interaktions_padding, y - interaktions_padding, breite + 2 * interaktions_padding, höhe + 2 * interaktions_padding)
            self.pos = (x,y)
            self.größe = (breite,höhe)
            self.color = WEISS
            self.min = min
            self.max = max-min
            self.steps = steps
            self.sliderPos = self.pos
            self.Toggle = Toggle
            self.handle_rect = pygame.Rect(self.sliderPos[0], self.sliderPos[1]-2.5, 10, self.größe[1]+5)
            self.letzterSound = pygame.time.get_ticks()
            self.internValue = S.read(nutzer,self.SaveValue,"Einstellungen")
            if self.SaveValue == "Lautstärke":
                self.internValue= self.internValue*100
            self.value = self.internValue
            self.SliderButtonPos()
        def draw(self, screen):
            if self.SaveValue == "Lautstärke":
                self.SliderButtonPos()
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WEISS, self.rect, 2)
            pygame.draw.rect(screen, BLAU, self.handle_rect)
            pygame.draw.rect(screen, WEISS, self.handle_rect, 1)

        def SliderButtonPos(self):
            if self.SaveValue == "Lautstärke":
                self.internValue = S.read(nutzer,self.SaveValue,"Einstellungen")*100
           
            relPos = self.internValue / self.max
            x = self.pos[0] + relPos * self.größe[0]
            y = self.pos[1]
            self.sliderPos = (x,y)
            self.handle_rect = pygame.Rect(self.sliderPos[0], self.sliderPos[1]-2.5, 10, self.größe[1]+5)


        def valueVonPos(self,touch):
            relative_x = touch[0] - self.pos[0]
            relative_x = max(0, min(self.größe[0], relative_x)) 
            rel_pos = relative_x / self.größe[0]
            roher_wert = self.min + rel_pos * self.max
            self.internValue = round(roher_wert / self.steps) * self.steps
            self.value = self.internValue
            save = self.value
            if self.SaveValue == "Lautstärke":
                save = self.value/100
                if self.value >= 1: 
                    self.Toggle.klick(1)
                elif self.value < 1:
                    self.Toggle.klick(0)
            S.write(nutzer, self.SaveValue, save, ort="Einstellungen", speicherort=E_Speicherort)
            self.SliderButtonPos()
            if pygame.time.get_ticks() >= self.letzterSound + 20:
                self.letzterSound = pygame.time.get_ticks()
                lautstärke = S.read(nutzer, "Lautstärke", ort="Einstellungen")
                setze_lautstärke(lautstärke)

            BlingSound.play()
        def handle_event(self, pos):
            if self.InteractionRect.collidepoint(pos): 
                self.valueVonPos(pos)
        def set_value(self, wert):
            self.internValue = wert
            self.value = self.internValue
            self.SliderButtonPos()

    if screen is None:
        screen = pygame.display.set_mode((E_BREITE, E_HOEHE))
    SoundToogle =  SwitchButton(130, 125,"Lautstärke","Sound")
    StartLabelToggel = SwitchButton(130, 85, "SL_beendbar","Start Label überspringbar")
    switches = [SoundToogle,StartLabelToggel]

    LautstärkeSlider = Slider("Lautstärke",130,190,150,5,0,100,4,10,SoundToogle)
    Sliders = [LautstärkeSlider]
    E_laeuft = True
    clock = pygame.time.Clock()
    mouseUP = True
    #Hintergrund
    hintergrund = pygame.image.load("Hintergrund_Einstellungen.png")
    hintergrund = pygame.transform.scale(hintergrund,(E_BREITE, E_HOEHE))# Skaliere Hintergrundbild auf die angegebene Größe

    while E_laeuft:
        screen.blit(hintergrund, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                E_laeuft = False
            for switch in switches:
                switch.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseUP = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouseUP = True
        if mouseUP == False:
            for s in Sliders:
                s.handle_event(pygame.mouse.get_pos())
        for switch in switches:
            switch.draw(screen)
        #Slider
        for s in Sliders:
            s.draw(screen)
        #Text
        screen.blit(FONT.render("Lautstärke:", True, WEISS), (130, 160))
        pygame.display.flip()
        clock.tick(60)