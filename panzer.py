import pygame
import time
import math
import threading
import random
pygame.init()
WIDTH, HEIGHT = 800,400
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
spieler_gruppe = pygame.sprite.Group()
löcher = pygame.sprite.Group()
GelegteMienen = pygame.sprite.Group()
class Player(pygame.sprite.Sprite):
    def __init__(self, position,Name):
        super().__init__()
        self.ID = Name
        self.position = pygame.Vector2(position)
        self.richtung = 90
        self.turmWinkel = 0
        self.leben = 1
        self.geschwindigkeit = 10
        self.drehgeschwindigkeit = 5
        self.schuss_cooldown = 250
        self.kugeln = 5
        self.kugelSpeed = 10
        self.nachladezeit = 3
        self.letzterSchuss = 0
        self.letzterEinzelschuss = 0
        self.mieneZeit = 7
        self.mienenAnzahl = -1
        self.letzte_mine_zeit = -2000
        self.mine_cooldown = 5
        self.explosionsRadius = 40
        self.abpraller = 2
        self.abprallChance = 0.75
        self.mienenPos = []

        #  Grafik:
        #  Unten
        self.body_surface = pygame.Surface((panzer_größe * 0.75, panzer_größe), pygame.SRCALPHA)
        self.body_surface.fill(GRÜN)
        pygame.draw.rect(self.body_surface, SCHWARZ, (0, 0, panzer_größe * 0.75, panzer_größe), 2)
        # Turm
        self.turm = pygame.Surface((panzer_größe // 2.15, panzer_größe // 2.15), pygame.SRCALPHA)
        self.turm.fill(BLAU)
        pygame.draw.rect(self.turm, SCHWARZ, (0, 0, panzer_größe // 2.15, panzer_größe // 2.15), 2)
        #Kanone
        self.kanone = pygame.Surface((panzer_größe, panzer_größe // 8), pygame.SRCALPHA)
        pygame.draw.rect(self.kanone, ROT, (panzer_größe // 2+1, 0, panzer_größe // 1.5, panzer_größe // 8))
        pygame.draw.rect(self.kanone, SCHWARZ, (panzer_größe // 2+1, 0, panzer_größe // 1.5, panzer_größe // 8), 2)

        # Platzhalter (wird bei update() gesetzt)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # --- Körper drehen ---
        gedreht_body = pygame.transform.rotate(self.body_surface, -self.richtung)
        body_rect = gedreht_body.get_rect(center=(self.position.x, self.position.y))

        # --- Turm drehen ---
        gedreht_turm = pygame.transform.rotate(self.turm, -self.turmWinkel)
        turm_rect = gedreht_turm.get_rect(center=self.position)

        # --- Kanone drehen ---
        gedrehte_kanone = pygame.transform.rotate(self.kanone, -self.turmWinkel)
        kanone_rect = gedrehte_kanone.get_rect(center=self.position)

        # --- Neues Image mit allem zusammen ---
        # Fläche groß genug für alles
        w = max(body_rect.width, turm_rect.width, kanone_rect.width)
        h = max(body_rect.height, turm_rect.height, kanone_rect.height)
        full_image = pygame.Surface((w, h), pygame.SRCALPHA)

        # Zentriert zeichnen
        offset_body = (w//2 - body_rect.width//2, h//2 - body_rect.height//2)
        offset_turm = (w//2 - turm_rect.width//2, h//2 - turm_rect.height//2)
        offset_kanone = (w//2 - kanone_rect.width//2, h//2 - kanone_rect.height//2)

        full_image.blit(gedreht_body, offset_body)
        full_image.blit(gedrehte_kanone, offset_kanone)
        full_image.blit(gedreht_turm, offset_turm)

        self.image = full_image
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    # --- Bewegungsmethoden ---
    def Drehen(self, Um):
        self.richtung += Um
        self.richtung %= 360

    def goW(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.geschwindigkeit / 10
        neue_pos = self.position + bewegung
        spieler_rect = pygame.Rect(neue_pos.x - 20, neue_pos.y - 20, 40, 40)

        loch_kollision = False
        for loch in löcher:
            abstand = neue_pos.distance_to(loch.rect.center)
            if abstand -(loch.radius /2) < loch.radius:
                loch_kollision = True
                break

        wand_kollision = any(spieler_rect.colliderect(w.rect) for w in wände)

        if not wand_kollision and not loch_kollision:
            self.position = neue_pos

    def goS(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.geschwindigkeit / 10
        neue_pos = self.position - bewegung
        spieler_rect = pygame.Rect(neue_pos.x - 20, neue_pos.y - 20, 40, 40)

        loch_kollision = False
        for loch in löcher:
            abstand = neue_pos.distance_to(loch.rect.center)
            if abstand -(loch.radius /2) < loch.radius:
                loch_kollision = True
                break

        wand_kollision = any(spieler_rect.colliderect(w.rect) for w in wände)

        if not wand_kollision and not loch_kollision:
            self.position = neue_pos

    def goA(self):
        self.Drehen(-self.drehgeschwindigkeit)

    def goD(self):
        self.Drehen(self.drehgeschwindigkeit)

    def Miene(self):
        jetzt = pygame.time.get_ticks()
        if jetzt - self.letzte_mine_zeit >= self.mine_cooldown * 1000:
            if self.mienenAnzahl >= 1 or self.mienenAnzahl == -1:
                if self.mienenAnzahl != -1:
                    self.mienenAnzahl -= 1
                if len(self.mienenPos) <= 5:
                    pos = self.position.copy()
                    GelegteMienen.add(Miene(pos,jetzt,self.ID,self.mieneZeit,self.explosionsRadius))
                    self.letzte_mine_zeit = jetzt
                    
    def Schuss(self, maus_pos, jetzt):
        if self.kugeln > 0 and jetzt - self.letzterEinzelschuss >= self.schuss_cooldown:
            richtung = pygame.Vector2(maus_pos) - self.position
            if richtung.length() != 0:
                richtung = richtung.normalize()
                # Abstand von Panzerzentrum plus Kugelgröße (halbe Breite), damit Kugel komplett außerhalb startet
                panzer_radius = panzer_größe * 0.5  # ca. halbe Panzergröße (Radius)
                kugel_radius = 10 / 2  # Kugelgröße ist 10x4, also halbe Breite=5
                abstand = panzer_radius + kugel_radius + 2  # 2 Pixel extra als Puffer

                start_pos = self.position + richtung * abstand

                neue_kugel = Kugel(start_pos, richtung,self.kugelSpeed,
                                   abpraller=self.abpraller, abprallChance=self.abprallChance)
                kugel_gruppe.add(neue_kugel)
                self.kugeln -= 1
                self.letzterEinzelschuss = jetzt
                if self.kugeln == 0:
                    self.letzterSchuss = jetzt
    def Schaden(self):
        self.leben -= 1
        if player.leben <= 0:
            print("Ende")
            #running = False                                  
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
        self.letztes = 0
        self.original_image = self.image
        self.rect = self.image.get_rect(center=start_pos)
        self.richtung = pygame.Vector2(richtung).normalize()
        self.geschwindigkeit = geschwindigkeit
        self.abpraller = abpraller
        self.abprallChance = abprallChance
        self.winkel = -richtung.angle_to(pygame.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.original_image, self.winkel)
        
        # Zeit, bis die Kugel freundliche Kollisionen ignoriert (in ms)
        self.freund_ignorieren_bis = pygame.time.get_ticks() + 150  # 150 ms ignorieren
    def update(self):
        bewegung = self.richtung * self.geschwindigkeit
        neue_rect = self.rect.move(bewegung)

        # Kollision mit Wänden prüfen
        getroffeneWand = pygame.sprite.spritecollideany(self, wände)
        if getroffeneWand:
            jetzt = pygame.time.get_ticks()
            if (jetzt - self.letztes)/1000 >= 0.5:
                self.letztes = jetzt	
                if getroffeneWand.zerstörbarkeit:
                    explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                    getroffeneWand.schaden(1)
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
            return  # Wurde Wand getroffen, nicht weiter bewegen

        # Kollision mit Spieler prüfen — aber nur wenn Zeit abgelaufen ist
        jetzt = pygame.time.get_ticks()
        if jetzt >= self.freund_ignorieren_bis:
            if pygame.sprite.collide_mask(self, player):
                player.Schaden()
                self.kill()
                explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                return

        # Bewegung ausführen
        self.rect = neue_rect


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, breite, höhe, zerstörbarkeit=False, leben=8):
        super().__init__()
        self.image = pygame.Surface((breite, höhe))
        self.zerstörbarkeit = zerstörbarkeit
        if self.zerstörbarkeit:
            self.image.fill((160,85,58))
        else:
            self.image.fill(SCHWARZ)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.leben = leben
        self.mask = pygame.mask.from_surface(self.image)

    def schaden(self,amount=1):
        if self.zerstörbarkeit:
            self.leben -= amount
            if self.leben <= 0:
                explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                self.kill()


class Loch(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=20):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((radius*2 , radius*2 ), pygame.SRCALPHA)

        # Transparenter Kreis (Loch)
        self.image.fill((0, 0, 0, 0))  # komplett transparent
        pygame.draw.circle(self.image, (0, 0, 0, 100), (radius, radius), radius)

        # Kollisionsmaske (für Spieler)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Miene(pygame.sprite.Sprite):
    #Zwischenversion, die funktioniert
    def __init__(self,pos,jetzt,ID,mieneZeit,explosionsRadius):
        super().__init__()
        self.pos = pos
        self.gelegt = jetzt
        self.ErstellerID = ID
        self.ZeitBisEx = mieneZeit
        self.explosionsRadius = explosionsRadius
        self.early = False
        #self.mienenPos.append({'pos': pos, 'gelegt': jetzt,"von":self.ID, "early":False})
    def update(self):
        jetzt = pygame.time.get_ticks()
        t = (jetzt - self.gelegt) / 1000
        rest = self.ZeitBisEx - t
        if rest <= 0:
            explosions_gruppe.add(Explosion(self.pos.x, self.pos.y))
            explosions_sprite = pygame.sprite.Sprite()
            radius = self.explosionsRadius
            explosions_sprite.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(explosions_sprite.image, (255, 0, 0, 128), (radius, radius), radius)
            explosions_sprite.rect = explosions_sprite.image.get_rect(center=(self.pos.x, self.pos.y))
            explosions_sprite.mask = pygame.mask.from_surface(explosions_sprite.image)
            # Kollisionen 
            getroffeneWand = pygame.sprite.spritecollideany(explosions_sprite, wände, collided=pygame.sprite.collide_mask)
            if getroffeneWand:
                if getroffeneWand.zerstörbarkeit:
                    getroffeneWand.schaden(10)
            offset = (player.rect.left - explosions_sprite.rect.left,player.rect.top - explosions_sprite.rect.top)
            if explosions_sprite.mask.overlap(player.mask, offset):
                player.Schaden()
            self.kill() 

            ##!!! Bei den getroffenem Panzer, nicht immer Player
        else:
            if rest <= 2:   # letzte 2 Sekunden
                # schnelles Blinken
                blink = 500 - ((2 - rest) / 2) *100
                blinkend = (jetzt // blink) % 2 == 0
                farbe = (255, 255, 0) if blinkend else (255, 0, 0)
            else:
                farbe = (255, 0, 0)  # normal rot, kein Blinken
                explosions_sprite = pygame.sprite.Sprite()
                radius = self.explosionsRadius
                explosions_sprite.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(explosions_sprite.image, (255, 0, 0, 128), (radius, radius), radius)
                explosions_sprite.rect = explosions_sprite.image.get_rect(center=(self.pos.x, self.pos.y))
                explosions_sprite.mask = pygame.mask.from_surface(explosions_sprite.image)
                # Kollisionen 
                getroffeneKugel = pygame.sprite.spritecollideany(explosions_sprite, kugel_gruppe, collided=pygame.sprite.collide_mask)
                if getroffeneKugel:
                    if self.early == False:
                            #getroffeneKugel.kill()
                        self.early = True
                        self.gelegt += (2 - rest)*1000  # Gelegte Zeit manipulieren, dass es so war das jetzt nur noch 2 Sekunden verbleibend sind
                offset = (player.rect.left - explosions_sprite.rect.left,player.rect.top - explosions_sprite.rect.top)
                if explosions_sprite.mask.overlap(player.mask, offset):
                    if rest <= 5: #Ersetzten mit: Wenn ersteller Spieler nahe nach ein paar sekunden hoch, sonst immer direkt nach den zwei sekunden
                        if self.early == False:
                            self.early = True
                            self.gelegt += (2 - rest)*1000  # Gelegte Zeit manipulieren, dass es so war das jetzt nur noch 2 Sekunden verbleibend sind

            pygame.draw.circle(screen, farbe, (int(self.pos.x), int(self.pos.y)), 8)
        
player = Player((400, 300),"Spieler1")
spieler_gruppe.add(player)
#Wände
wände.add(Wall(0, 0, WIDTH,2))               # Oben
wände.add(Wall(0, HEIGHT - 2, WIDTH,2))      # Unten
wände.add(Wall(0, 0, 2, HEIGHT))              # Links
wände.add(Wall(WIDTH - 2, 0, 2, HEIGHT))      # Rechts
wände.add(Wall(200, 200, 50, 50, zerstörbarkeit=True,))  # zerstörbar

löcher.add(Loch(300, 300, radius=10))


# Haupt-Game Loop
running = True
while running:
    screen.fill(SAND)
    löcher.draw(screen)
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
    
    #PLAYER: KUGELN
    # wenn linke Maustaste gedrückt ist und Spieler Kugeln hat
    if pygame.mouse.get_pressed()[0]:
        player.Schuss(maus_pos, jetzt)
    # Nachladen nach Pause
    if player.kugeln == 0 and jetzt - player.letzterSchuss >= player.nachladezeit * 1000:
        player.kugeln = 5
        
    ## MIENEN MALEN
    GelegteMienen.update()
    ## PLAYER: ZEICHNEN
    spieler_gruppe.update()
    #KUGELN : ZEICHEN
    kugel_gruppe.update()
    kugel_gruppe.draw(screen)
    #PLAYER: ZEICHNEN
    spieler_gruppe.draw(screen)
    ## WÄNDE: ZEICHEN
    wände.draw(screen)
    #Explosionen: Zeichnen
    explosions_gruppe.update()
    explosions_gruppe.draw(screen)

    #TEXT: ZEICHNEN
    font = pygame.font.SysFont(None, 24)
    text1 = font.render("Kugeln: {}".format(player.kugeln), True, SCHWARZ)
    screen.blit(text1, (30, 30))
    text2 = font.render("Leben: {}".format(player.leben), True, SCHWARZ)
    screen.blit(text2, (30, 55))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()
