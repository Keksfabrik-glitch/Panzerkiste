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
        self.mieneZeit = 7 #Bis zur explosion
        self.mienenAnzahl = -1  # -1 = unendlich viele
        self.letzte_mine_zeit = 0
        self.mine_cooldown = 5    # zwischen neuen Mienen
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
        if aktuelle_zeit - self.letzte_mine_zeit >= self.mine_cooldown*1000:
            if self.mienenAnzahl >= 1 or self.mienenAnzahl == -1:
                if self.mienenAnzahl != -1:
                    self.mienenAnzahl -= 1
                if len(self.mienenPos) <= 5:
                    pos = self.position.copy()
                    self.mienenPos.append({'pos': pos, 'gelegt': aktuelle_zeit})
                    self.letzte_mine_zeit = aktuelle_zeit

                    
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.bilder = []
        for i in range(1, 6):
            bild = pygame.image.load(f"BilderExplosion/exp{i}.png")
            bild = pygame.transform.scale(bild, (100, 100))
            self.bilder.append(bild)
        self.index = 0
        self.image = self.bilder[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0

    def update(self):
        geschwindigkeit = 4
        self.timer += 1
        if self.timer >= geschwindigkeit:
            self.timer = 0
            self.index += 1
            if self.index < len(self.bilder):
                self.image = self.bilder[self.index]
            else:
                self.kill()        
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

explosions_gruppe = pygame.sprite.Group()
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
       threading.Thread(target=player.Miene).start()

    
    jetzt = pygame.time.get_ticks()
    for m in player.mienenPos[:]:
        t = (jetzt - m['gelegt']) / 1000
        rest = player.mieneZeit - t
        if rest <= 0:
            explosions_gruppe.add(Explosion(m['pos'].x, m['pos'].y))
            player.mienenPos.remove(m)
        else:
            if rest <= 2:   # letzte 2 Sekunden
                # schneller Blinken
                blink = 500 - ((2 - rest) / 2) *100
                blinkend = (jetzt // blink) % 2 == 0
                farbe = (255, 255, 0) if blinkend else (255, 0, 0)
            else:
                farbe = (255, 0, 0)  # normal rot, kein Blinken
                
            pygame.draw.circle(screen, farbe, (int(m['pos'].x), int(m['pos'].y)), 8)

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
    explosions_gruppe.update()
    explosions_gruppe.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()
