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

#Schrift
pygame.font.init()
FONT = pygame.font.SysFont("arial", 20)

class SwitchButton:
    def __init__(self, x, y, nutzer, parameter, label= None, width=60, height=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.nutzer = nutzer
        self.parameter = parameter
        self.label = label
        if self.label is None:
            self.label = self.parameter
        self.zustand = S.read(self.nutzer, self.parameter, ort="Einstellungen", speicherort=E_Speicherort)

    def draw(self, surface):
        # Text zeichnen links vom Button
        text_surface = FONT.render(self.label, True, WEISS)
        text_rect = text_surface.get_rect()
        text_rect.midright = (self.rect.x - 10, self.rect.centery)  # 10px Abstand links vom Button
        surface.blit(text_surface, text_rect)

        # Button Hintergrund und Kreis
        color = GRÜN if self.zustand else ROT
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        kreis_radius = self.rect.height // 2 - 3
        kreis_x = self.rect.x + kreis_radius + 3 if not self.zustand else self.rect.right - kreis_radius - 3
        kreis_center = (kreis_x, self.rect.centery)
        pygame.draw.circle(surface, WEISS, kreis_center, kreis_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.zustand = not self.zustand
                S.write(self.nutzer, self.parameter, self.zustand, ort="Einstellungen", speicherort=E_Speicherort)

def main(nutzer, screen=None):
    if screen is None:
        screen = pygame.display.set_mode((E_BREITE, E_HOEHE))

    # Switches als Liste
    switches = [
        SwitchButton(300, 85, nutzer, "Sound","Sound"),
        SwitchButton(300, 125, nutzer, "SL_beendbar","Start Label überspringbar")
    ]

    E_laeuft = True
    clock = pygame.time.Clock()

    while E_laeuft:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                E_laeuft = False
            for switch in switches:
                switch.handle_event(event)

        screen.fill((30, 30, 30))  # Hintergrundfarbe
        for switch in switches:
            switch.draw(screen)

        pygame.display.flip()
        clock.tick(60)

#Ende
pygame.quit()