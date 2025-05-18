import pygame
import time
import math
import threading
import random
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
panzer_größe = 40

#Farben
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
SCHWARZ = (0, 0, 0)
SAND = (239, 228, 176)
BLAU = (0, 0, 255)
GRÜN = (0,255,0)
TRANSPARENT = (0,0,0,0)
#Sprite Groups
wände = pygame.sprite.Group()
explosions_gruppe = pygame.sprite.Group()
kugel_gruppe = pygame.sprite.Group()

class Player:
    def __init__(self, position):
        self.level = 1
        self.position = pygame.Vector2(position)
        self.geschwindigkeit = 10
        self.kugeln = 5
        self.kugel_art = 1  # 2 = Feuer
        self.nachladezeit = 3
        self.letzterSchuss = 0
        self.schuss_cooldown = 250  # in Millisekunden
        self.letzterEinzelschuss = 0
        self.mieneZeit = 7 #Bis zur explosion
        self.mienenAnzahl = -1  # -1 = unendlich viele
        self.letzte_mine_zeit = -2*1000 #5 Cooldown. 3 Sekunden nach Spawn erste Miene
        self.mine_cooldown = 5    # zwischen neuen Mienen
        self.explosionsRadius = 40
        self.drehgeschwindigkeit = 5
        self.turmDrehgeschw = 8
        self.abpraller = 2
        self.abprallChance = 0.75
        self.richtung = 90  # 
        self.turmWinkel = 0
        self.leben = 1
        self.mienenPos = []
        self.winkel = 0
        self.turmWinkel = 0
        self.leben = 3
    def Drehen(self,Um):

        self.richtung += Um
        self.richtung %= 360

    def goW(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.geschwindigkeit / 10
        neue_pos = self.position + bewegung
        spieler_rect = pygame.Rect(neue_pos.x - 20, neue_pos.y - 20, 40, 40)
        if not any(spieler_rect.colliderect(w.rect) for w in wände):
            self.position = neue_pos

    def goD(self):
        self.Drehen(self.drehgeschwindigkeit)

    def goA(self):
        self.Drehen(-self.drehgeschwindigkeit)

    def goS(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.geschwindigkeit / 10
        neue_pos = self.position - bewegung
        spieler_rect = pygame.Rect(neue_pos.x - 20, neue_pos.y - 20, 40, 40)
        if not any(spieler_rect.colliderect(w.rect) for w in wände):
            self.position = neue_pos
        
    def Miene(self):
        jetzt = pygame.time.get_ticks()
        if jetzt - self.letzte_mine_zeit >= self.mine_cooldown*1000:
            if self.mienenAnzahl >= 1 or self.mienenAnzahl == -1:
                if self.mienenAnzahl != -1:
                    self.mienenAnzahl -= 1
                if len(self.mienenPos) <= 5:
                    pos = self.position.copy()
                    self.mienenPos.append({'pos': pos, 'gelegt': jetzt})
                    self.letzte_mine_zeit = jetzt
    def Schuss(self):
         if self.kugeln > 0 and jetzt - self.letzterEinzelschuss >= self.schuss_cooldown:
            richtung = pygame.Vector2(maus_pos) - self.position
            if richtung.length() != 0:
                neue_kugel = Kugel(self.position, richtung,abpraller=player.abpraller,abprallChance=player.abprallChance)
                kugel_gruppe.add(neue_kugel)
                self.kugeln -= 1
                self.letzterEinzelschuss = jetzt
                # Wenn letzte Kugel verschossen wurde, starte Nachladezeit
                if self.kugeln == 0:
                    self.letzterSchuss = jetzt


                                       
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
        
class Kugel(pygame.sprite.Sprite):
    def __init__(self, start_pos, richtung, geschwindigkeit=8, abpraller=2, abprallChance=0.75):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(ROT)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=start_pos)
        self.richtung = pygame.Vector2(richtung).normalize()
        self.geschwindigkeit = geschwindigkeit
        self.abpraller = abpraller
        self.abprallChance = abprallChance
        self.winkel = -richtung.angle_to(pygame.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.original_image, self.winkel)

    def update(self):
        bewegung = self.richtung * self.geschwindigkeit
        neue_rect = self.rect.move(bewegung)

        getroffeneWand = pygame.sprite.spritecollideany(self, wände)
        if getroffeneWand:
            if getroffeneWand.zersörbarkeit:
                getroffeneWand.schaden()
                self.kill()
            else:
                if self.abpraller > 0 and random.random() <= self.abprallChance:
                    if getroffeneWand.rect.width > getroffeneWand.rect.height:
                        self.richtung.y *= -1
                    else:
                        self.richtung.x *= -1

                    self.abpraller -= 1
                    self.winkel = -self.richtung.angle_to(pygame.Vector2(1, 0))
                    self.image = pygame.transform.rotate(self.original_image, self.winkel)   
                    self.rect = self.rect.move(self.richtung * self.geschwindigkeit)
                else:
                    self.kill()
                    explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
        else:
            self.rect = neue_rect

        
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, breite, höhe, zersörbarkeit=False, leben=1):
        super().__init__()
        self.image = pygame.Surface((breite, höhe))
        self.image.fill((120, 120, 120) if zersörbarkeit else SCHWARZ)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.zersörbarkeit = zersörbarkeit
        self.leben = leben
        self.mask = pygame.mask.from_surface(self.image)

    def schaden(self):
        if self.zersörbarkeit:
            self.leben -= 1
            if self.leben <= 0:
                explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                self.kill()
        
player = Player((400, 300))
# Definiere den Turm
turm = pygame.Surface((panzer_größe // 2.15, panzer_größe // 2.15), pygame.SRCALPHA)
turm.fill(BLAU)
pygame.draw.rect(turm, SCHWARZ, (0, 0, panzer_größe // 2.15, panzer_größe // 2.15), 2)
# Definiere Kanone
kanone = pygame.Surface((panzer_größe, panzer_größe // 8), pygame.SRCALPHA)
kanone.fill(TRANSPARENT)  
pygame.draw.rect(kanone, ROT, (panzer_größe // 2, 0, panzer_größe // 1.5, panzer_größe // 8))  # Hauptteil
pygame.draw.rect(kanone, SCHWARZ, (panzer_größe // 2, 0, panzer_größe // 1.5, panzer_größe // 8), 2)
# Definiere den Unteren 
panzer_surface = pygame.Surface((panzer_größe * 0.75, panzer_größe), pygame.SRCALPHA)
panzer_surface.fill(GRÜN)
pygame.draw.rect(panzer_surface, SCHWARZ, (0, 0,panzer_größe * 0.75, panzer_größe), 2)
#Wände
wände.add(Wall(0, 0, WIDTH, 2))               # Oben
wände.add(Wall(0, HEIGHT - 2, WIDTH, 2))      # Unten
wände.add(Wall(0, 0, 2, HEIGHT))              # Links
wände.add(Wall(WIDTH - 2, 0, 2, HEIGHT))      # Rechts
wände.add(Wall(200, 200, 50, 50, zersörbarkeit=True, leben=1))  # zerstörbar


# Haupt-Game Loop
running = True
while running:
    screen.fill(SAND)
    #Zeit
    jetzt = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    maus_pos = pygame.mouse.get_pos()
    richtung = pygame.Vector2(maus_pos) - player.position
    if richtung.length() != 0:
        richtung = richtung.normalize()  # auf Länge 1 bringen
    winkel = -richtung.angle_to(pygame.Vector2(1, 0))
    player.turmWinkel = winkel

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
    
    ##PLAYER: KUGELN
    # Wenn linke Maustaste gedrückt ist und Spieler Kugeln hat
    if pygame.mouse.get_pressed()[0]:
       player.Schuss()
    # Nachladen nach Pause
    if player.kugeln == 0 and jetzt - player.letzterSchuss >= player.nachladezeit * 1000:
        player.kugeln = 5
  
    ## PLAYER: MIENEN   
    for m in player.mienenPos[:]:
        t = (jetzt - m['gelegt']) / 1000
        rest = player.mieneZeit - t
        if rest <= 0:
            explosions_gruppe.add(Explosion(m['pos'].x, m['pos'].y))
            player.mienenPos.remove(m)
            # Sprite 
            explosions_sprite = pygame.sprite.Sprite()
            radius = player.explosionsRadius
            explosions_sprite.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(explosions_sprite.image, (255, 0, 0, 128), (radius, radius), radius)
            explosions_sprite.rect = explosions_sprite.image.get_rect(center=(m['pos'].x, m['pos'].y))
            explosions_sprite.mask = pygame.mask.from_surface(explosions_sprite.image)
            # Kollisionnen 
            getroffeneWand = pygame.sprite.spritecollideany(explosions_sprite, wände, collided=pygame.sprite.collide_mask)
            if getroffeneWand:
                if getroffeneWand.zersörbarkeit:
                    getroffeneWand.schaden()
            
            #getroffenenPlayer = pygame.sprite.spritecollideany(explosions_sprite, panzer_mask, collided=pygame.sprite.collide_mask)
            #if getroffenenPlayer:
            #    if getroffenenPlayer.leben:
            #        if getroffenenPlayer.leben >= 1:
            #            getroffenenPlayer.leben -= 1
            #        if getroffenenPlayer.leben <= 0:
            #            print("Ende")
        else:
            if rest <= 2:   # letzte 2 Sekunden
                # schneller Blinken
                blink = 500 - ((2 - rest) / 2) *100
                blinkend = (jetzt // blink) % 2 == 0
                farbe = (255, 255, 0) if blinkend else (255, 0, 0)
            else:
                farbe = (255, 0, 0)  # normal rot, kein Blinken
                
            pygame.draw.circle(screen, farbe, (int(m['pos'].x), int(m['pos'].y)), 8)
    ## PLAYER: ZEICHNEN
    #Drehe das untere [Panzerkörper]
    gedreht = pygame.transform.rotate(panzer_surface, -player.richtung)
    gedreht_rect = gedreht.get_rect(center=player.position)
    panzer_mask = pygame.mask.from_surface(gedreht)
    #Drehe den Turm
    rotiert = pygame.transform.rotate(turm, -winkel)
    neu_rect = rotiert.get_rect(center=player.position)
    # Drehe die Kanone
    gedrehte_kanone = pygame.transform.rotate(kanone, -winkel)
    kanone_rect = gedrehte_kanone.get_rect(center=player.position)
    # Zeichne den Unterteil
    screen.blit(gedreht, gedreht_rect.topleft)
    #KUGELN : ZEICHEN
    kugel_gruppe.update()
    kugel_gruppe.draw(screen)
    #PLAYER: ZEICHNEN
    #Zeichne die Kanone
    screen.blit(gedrehte_kanone, kanone_rect.topleft)
    #Zeichne den Turm
    screen.blit(rotiert, neu_rect.topleft)

    ## WÄNDE: ZEICHENN
    wände.draw(screen)
    #Explosionen: Zeichnen
    explosions_gruppe.update()
    explosions_gruppe.draw(screen)
    #TEXT: ZEICHNEN
    font = pygame.font.SysFont(None, 24)
    text = font.render("Kugeln: {}".format(player.kugeln), True, SCHWARZ)
    screen.blit(text, (30, 30))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()