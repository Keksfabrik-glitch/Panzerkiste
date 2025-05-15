import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
SCHWARZ = (0, 0, 0)
SAND = (239, 228, 176)
BLAU = (0, 0, 255)
panzer_größe = 40

def angle_diff(a, b):
    """Kleinste Differenz zwischen zwei Winkeln"""
    diff = (b - a + 180) % 360 - 180
    return diff

class Player:
    def __init__(self, position):
        self.level = 1
        self.position = pygame.Vector2(position)
        self.geschwindigkeit = 10
        self.kugeln = 5
        self.kugelgeschwindigkeit = 20
        self.kugel_art = 1  # 2 = Feuer
        self.nachladezeit = 3
        self.letzterSchuss = 0
        self.mineZeit = 7
        self.minenAnzahl = -1  # -1 = unendlich viele
        self.drehgeschwindigkeit = 5
        self.turmDrehgeschw = 8
        self.abpraller = 2
        self.abprallChance = 0.75
        self.richtung = 90  # 
        self.winkel = 0
        self.turmWinkel = 0
        self.leben = 3
        self.ActiveKugeln = []

    def Drehen(self, Um):
        self.richtung += Um
        self.richtung %= 360

    def goW(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.geschwindigkeit / 10
        self.position += bewegung

    def goD(self):
        self.Drehen(self.drehgeschwindigkeit)

    def goA(self):
        self.Drehen(-self.drehgeschwindigkeit)

    def goS(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.geschwindigkeit / 10
        self.position -= bewegung

# IGNORIEREN NUR DAMIT MAN ES VISUELL SIEHT
player = Player((400, 300))

# Definiere das blaue Quadrat (unten)
unten = pygame.Surface((panzer_größe / 4, panzer_größe / 4), pygame.SRCALPHA)
unten.fill(BLAU)
pygame.draw.rect(unten, SCHWARZ, (0, 0, panzer_größe / 4, panzer_größe / 4), 2)

# Haupt-Game Loop
running = True
while running:
    screen.fill(SAND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    maus_pos = pygame.mouse.get_pos()
    richtung = pygame.Vector2(maus_pos) - player.position
    if richtung.length() != 0:
        richtung = richtung.normalize()  # auf Länge 1 bringen
    winkel = -richtung.angle_to(pygame.Vector2(1, 0))

    # Zur Maus drehen
    rotiert = pygame.transform.rotate(unten, -winkel)
    neu_rect = rotiert.get_rect(center=player.position)

    # Steuerung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.goW()
    if keys[pygame.K_s]:
        player.goS()
    if keys[pygame.K_a]:
        player.goA()
    if keys[pygame.K_d]:
        player.goD()

    # Zeichne den Turm (rotierend)
    panzer_surface = pygame.Surface((panzer_größe-(panzer_größe/4), panzer_größe), pygame.SRCALPHA)
    panzer_surface.fill((0, 255, 0))
    pygame.draw.rect(panzer_surface, SCHWARZ, (0, 0,panzer_größe-(panzer_größe/4), panzer_größe), 2)
    
    gedreht = pygame.transform.rotate(panzer_surface, -player.richtung)
    gedreht_rect = gedreht.get_rect(center=player.position)

    # Zeichne den Unterteil
    screen.blit(gedreht, gedreht_rect.topleft)

    # Das blaue Quadrat im Zentrum des Panzers
    screen.blit(rotiert, neu_rect.topleft)  # Das rotiert in der Mitte des grünen Panzers bleibt

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()
