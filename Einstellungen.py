# Einstellungen
import pygame
import Speicher as S

# Setup
pygame.init()
E_BREITE = 500
E_HOEHE = 250
screen = pygame.display.set_mode((E_BREITE, E_HOEHE))
pygame.display.set_caption("Einstellungen")
E_Speicherort = "Accounts.json"

# Farben
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)
WEISS = (255, 255, 255)
SAND = (239, 228, 176)
SCHWARZ = (0,0,0)
BLAU = (0,0,255)
#Schrift
pygame.font.init()
FONT = pygame.font.SysFont("arial", 20)
#Sprite Groups
slider = pygame.sprite.Group()

class SwitchButton:
    def __init__(self, x, y, nutzer, parameter, label= None, width=60, height=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.nutzer = nutzer
        self.parameter = parameter
        self.label = label
        if self.label is None:
            self.label = self.parameter
        self.zustand = S.read(self.nutzer, self.parameter, ort="Einstellungen", speicherort=E_Speicherort)
        self.anim_fortschritt = 1.0 if self.zustand else 0.0
        self.anim_geschwindigkeit = 0.1
        self.anim_zielwert = self.anim_fortschritt

    def draw(self, surface):
        # Text zeichnen links vom Button
        text_surface = FONT.render(self.label, True, SCHWARZ)
        text_rect = text_surface.get_rect()
        text_rect.midright = (self.rect.x - 10, self.rect.centery)  # 10px Abstand links vom Button
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.zustand = not self.zustand
                self.anim_zielwert = 1.0 if self.zustand else 0.0  
                S.write(self.nutzer, self.parameter, self.zustand, ort="Einstellungen", speicherort=E_Speicherort)

class Tonslider(pygame.sprite.Sprite):
    def __init__(self, x, y, nutzer, parameter="Lautstärke"):
        super().__init__()
        self.x = x
        self.y = y
        self.w = 300
        self.h = 10
        self.knob_radius = 6
        self.padding = self.knob_radius  # space on both left and right

        self.total_width = self.w + 2 * self.padding
        self.total_height = self.h + 2 * self.knob_radius

        self.nutzer = nutzer
        self.parameter = parameter
        self.wert = S.read(self.nutzer, self.parameter, ort="Einstellungen")

        self.image = pygame.Surface((self.total_width, self.total_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x - self.padding, self.y))  # Shift so track stays aligned

        self.dragging = False
        self.update_image()

    def update_image(self):
        self.image.fill((0, 0, 0, 0))

        # Linie im Hintergrund
        pygame.draw.rect(self.image,SCHWARZ,(self.padding, self.total_height // 2 - self.h // 2, self.w, self.h)
        )

        # Knopf
        knob_x = int(self.padding + self.w * self.wert)
        pygame.draw.circle(self.image, BLAU, (knob_x, self.total_height // 2), self.knob_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x = event.pos[0] - self.rect.x - self.padding
            self.wert = max(0.0, min(1.0, relative_x / self.w))
            S.write(self.nutzer, self.parameter, self.wert, ort="Einstellungen")
            self.update_image()

def main(nutzer, screen=None):
    if screen is None:
        screen = pygame.display.set_mode((E_BREITE, E_HOEHE))

    switches = [
        SwitchButton(300, 85, nutzer, "Sound","Sound"),
        SwitchButton(300, 125, nutzer, "SL_beendbar","Start Label überspringbar")
    ]
    slider.add(Tonslider(60,230,nutzer))
    E_laeuft = True
    clock = pygame.time.Clock()

    while E_laeuft:
        screen.fill(SAND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                E_laeuft = False
            for switch in switches:
                switch.handle_event(event)

            for s in slider:
                s.handle_event(event)

        for switch in switches:
            switch.draw(screen)
        #Slider
        slider.update()
        slider.draw(screen)
        #Text
        screen.blit(FONT.render("Lautstärke:", True, SCHWARZ), (60, 200))
        pygame.display.flip()
        clock.tick(60)