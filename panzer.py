import pygame
import time
import math
import threading
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WEISS = (255, 255, 255)
ROT = (255, 0, 0)
SCHWARZ = (0, 0, 0)
SAND = (239, 228, 176)
BLAU = (0, 0, 255)
GRÜN = (0,255,0)
panzer_größe = 40

class Player:
    def __init__(self, position):
        self.level = 1
        self.position = pygame.Vector2(position)
        self.geschwindigkeit = 10
        self.kugeln = 5
        self.kugel_art = 1  # 2 = Feuer
        self.nachladezeit = 3
        self.letzterSchuss = 0
        self.mieneZeit = 7
        self.mienenAnzahl = -1  # -1 = unendlich viele
        self.letzte_mine_zeit = 0  
        self.mine_cooldown = 500   
        self.drehgeschwindigkeit = 5
        self.turmDrehgeschw = 8
        self.abpraller = 2
        self.abprallChance = 0.75
        self.richtung = 90  # 
        self.turmWinkel = 0
        self.leben = 3
        self.mienenPos = []
        self.winkel = 0
        self.turmWinkel = 0
        self.leben = 3
        self.mienenPos = []
    def Drehen(self,Um):

        self.richtung += Um
        self.richtung %= 360

    def goW(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2( math.sin(rad), -math.cos(rad) ) * self.geschwindigkeit/10
        self.position += bewegung

    def goD(self):
        self.Drehen(self.drehgeschwindigkeit)

    def goA(self):
        self.Drehen(-self.drehgeschwindigkeit)

    def goS(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2( math.sin(rad), -math.cos(rad) ) * self.geschwindigkeit/10
        self.position -= bewegung
    def Miene(self):
        aktuelle_zeit = pygame.time.get_ticks()
        if aktuelle_zeit - self.letzte_mine_zeit >= self.mine_cooldown:
            if self.mienenAnzahl >= 1 or self.mienenAnzahl == -1:
                if self.mienenAnzahl != -1:
                    self.mienenAnzahl -= 1
                if len(self.mienenPos) <= 5:
                    self.mienenPos.append(self.position.copy())
                    self.letzte_mine_zeit = aktuelle_zeit  
                    
        
#IGNORIEREN NUR DAMIT MAN ES VISUELL SIEHT 

player = Player((400, 300))
# Definiere Kanone
kanone = pygame.Surface((panzer_größe / 4, panzer_größe / 4), pygame.SRCALPHA)
kanone.fill(BLAU)
pygame.draw.rect(kanone, SCHWARZ, (0, 0, panzer_größe / 4, panzer_größe / 4), 2)
# Definiere den Turm
turm = pygame.Surface((panzer_größe / 4, panzer_größe / 4), pygame.SRCALPHA)
turm.fill(BLAU)
pygame.draw.rect(turm, SCHWARZ, (0, 0, panzer_größe / 4, panzer_größe / 4), 2)
# Zeichne den Unteren (rotierend)
panzer_surface = pygame.Surface((panzer_größe-(panzer_größe/4), panzer_größe), pygame.SRCALPHA)
panzer_surface.fill(GRÜN)
pygame.draw.rect(panzer_surface, SCHWARZ, (0, 0,panzer_größe-(panzer_größe/4), panzer_größe), 2)

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

    # Drehe den Turm
    rotiert = pygame.transform.rotate(turm, -winkel)
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
    if keys[pygame.K_SPACE]:
        MieneVerarbeitung = threading.Thread(target=player.Miene(), args=())
    
    for pos in player.mienenPos:
        miene = pygame.draw.circle(screen, ROT, (pos.x,pos.y), 8)
    #Drehe das untere
    gedreht = pygame.transform.rotate(panzer_surface, -player.richtung)
    gedreht_rect = gedreht.get_rect(center=player.position)
    #Drehe die Kanone
    drehen = pygame.transform.rotate(kanone, -winkel)
    neu_rect = rotiert.get_rect(center=player.position)
    # Zeichne den Unterteil
    screen.blit(gedreht, gedreht_rect.topleft)

    # Das blaue Quadrat im Zentrum des Panzers
    screen.blit(rotiert, neu_rect.topleft)
    
    #Zeichne die Kanone
    screen.blit(drehen, neu_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()
