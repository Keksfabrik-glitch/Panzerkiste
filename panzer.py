#+ tuple(min(c + amount, 255) for c in color)
import pygame
import math
import random
import string
import Maps as M

pygame.init()
clock = pygame.time.Clock()
panzer_größe = 40

WIDTH, HEIGHT = 800, 400
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
feindPanzerGR = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH,HEIGHT))  # screengröße für den Startbildschirm
## CLASSES
def FarbeVerändern(farbe, amount):
    ret = []
    for ft in farbe:
        ret.append(max(min(255, ft + amount),0))
    return tuple(ret)
def randomNameID(länge=5,idOrName=True):
    
    if idOrName == True:
        Zeichen = string.ascii_letters + string.digits
        return "".join(random.choices(Zeichen, k = länge))
class Player(pygame.sprite.Sprite):

    def __init__(self, position,Name,farbe):
        super().__init__()
        self.Punkte = 0
        self.farbe = farbe
        self.ID = Name
        self.position = pygame.Vector2(position)
        self.richtung = 90
        self.turmWinkel = 0
        self.leben = 1
        self.geschwindigkeit = 10
        self.drehgeschwindigkeit = 5
        self.schuss_cooldown = 250
        self.kugeln = 5
        self.maxKugeln = 5
        self.kugelSpeed = 10 #bei manchen
        self.nachladezeit = 3
        self.letzterSchuss = 0
        self.letzterEinzelschuss = 0
        self.mieneZeit = 15
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
        self.body_surface.fill(FarbeVerändern(self.farbe,-25))
        pygame.draw.rect(self.body_surface, SCHWARZ, (0, 0, panzer_größe * 0.75, panzer_größe), 2)
        # Turm
        self.turm = pygame.Surface((panzer_größe // 2.15, panzer_größe // 2.15), pygame.SRCALPHA)
        self.turm.fill(self.farbe)
        pygame.draw.rect(self.turm, SCHWARZ, (0, 0, panzer_größe // 2.15, panzer_größe // 2.15), 2)
        #Kanone
        self.kanone = pygame.Surface((panzer_größe, panzer_größe // 8), pygame.SRCALPHA)
        pygame.draw.rect(self.kanone, FarbeVerändern(self.farbe,25), (panzer_größe // 2+1, 0, panzer_größe // 1.5, panzer_größe // 8))
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
            if abstand-20 <= loch.radius:
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
            #if abstand -(loch.radius /2) < loch.radius:
            if abstand-20 <= loch.radius: # panzer mitte
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

                neue_kugel = Kugel(start_pos, richtung, self.kugelSpeed,
                                   abpraller=self.abpraller, abprallChance=self.abprallChance,
                                   shooter_id=self.ID)
                kugel_gruppe.add(neue_kugel)
                self.kugeln -= 1
                self.letzterEinzelschuss = jetzt
                if self.kugeln == 0:
                    self.letzterSchuss = jetzt
    def Schaden(self,amount=1):
        self.leben -= amount
        if self.leben <= 0:
            print("Ende")
            #running = False                                  
class FeindPanzer(pygame.sprite.Sprite):

    def __init__(self, position,Name,level,leben,kannFahren,geschwindigkeit,drehgeschwindigkeit,schuss_cooldown,kugeln,kugelSpeed,nachladezeit,farbe):
        super().__init__()
        self.kannFahren = kannFahren
        self.Punkte = 0
        self.ID = Name
        self.level = level
        self.position = pygame.Vector2(position)
        self.richtung = 90
        self.turmWinkel = 0
        self.leben = leben
        self.geschwindigkeit = geschwindigkeit
        self.drehgeschwindigkeit = drehgeschwindigkeit
        self.schuss_cooldown = schuss_cooldown
        self.kugeln = kugeln
        self.maxKugeln = self.kugeln
        self.kugelSpeed = kugelSpeed
        self.nachladezeit = nachladezeit
        self.letzterSchuss = 0
        self.letzterEinzelschuss = 0
        self.farbe = farbe
        
        self.mieneZeit = 15
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
        self.body_surface.fill(FarbeVerändern(farbe,-25))
        pygame.draw.rect(self.body_surface, SCHWARZ, (0, 0, panzer_größe * 0.75, panzer_größe), 2)
        # Turm
        self.turm = pygame.Surface((panzer_größe // 2.15, panzer_größe // 2.15), pygame.SRCALPHA)
        self.turm.fill(farbe)
        pygame.draw.rect(self.turm, SCHWARZ, (0, 0, panzer_größe // 2.15, panzer_größe // 2.15), 2)
        #Kanone
        self.kanone = pygame.Surface((panzer_größe, panzer_größe // 8), pygame.SRCALPHA)
        pygame.draw.rect(self.kanone, FarbeVerändern(farbe,25), (panzer_größe // 2+1, 0, panzer_größe // 1.5, panzer_größe // 8))
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
        panzer_rect = pygame.Rect(neue_pos.x - 20, neue_pos.y - 20, 40, 40)

        loch_kollision = False
        for loch in löcher:
            abstand = neue_pos.distance_to(loch.rect.center)
            if abstand - 20 <= loch.radius:
                loch_kollision = True
                break

        wand_kollision = any(panzer_rect.colliderect(w.rect) for w in wände)

        if not wand_kollision and not loch_kollision:
            self.position = neue_pos

    def goS(self):
        rad = math.radians(self.richtung)
        bewegung = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.geschwindigkeit / 10
        neue_pos = self.position + bewegung
        panzer_rect = pygame.Rect(neue_pos.x - 20, neue_pos.y - 20, 40, 40)

        loch_kollision = False
        for loch in löcher:
            abstand = neue_pos.distance_to(loch.rect.center)
            if abstand - 20 <= loch.radius:
                loch_kollision = True
                break

        wand_kollision = any(panzer_rect.colliderect(w.rect) for w in wände)

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
                    
    def Schuss(self, maus_pos=None, jetzt=None, winkel=None):
        if self.kugeln > 0 and jetzt - self.letzterEinzelschuss >= self.schuss_cooldown:
            if winkel is not None:
                rad = math.radians(winkel)
                richtung = pygame.Vector2(math.cos(rad), -math.sin(rad))
            elif maus_pos is not None:
                richtung = pygame.Vector2(maus_pos) - self.position
                if richtung.length() == 0:
                    return
                richtung = richtung.normalize()
            else:
                return  # Weder Winkel noch Mausposition

        panzer_radius = panzer_größe * 0.5
        kugel_radius = 5
        abstand = panzer_radius + kugel_radius + 2

        start_pos = self.position + richtung * abstand

        neue_kugel = Kugel(start_pos, richtung, self.kugelSpeed,
                           abpraller=self.abpraller, abprallChance=self.abprallChance,
                           shooter_id=self.ID)
        kugel_gruppe.add(neue_kugel)
        self.kugeln -= 1
        self.letzterEinzelschuss = jetzt
        if self.kugeln == 0:
            self.letzterSchuss = jetzt
    def Schaden(self,amount=1):
        self.leben -= amount
        if self.leben <= 0:
            print("Ende")
            #running = False 

class FeindPanzerManage():
    def __init__(self):
        self.panzer =  []
    def NeuerPanzer(self,level,typ,position):
        id = randomNameID().join(str(level))
        if typ == "stehend": # viel Lebel   # int(min(MAX, MIN + (level - 1) *STEIGUNG))
            leben = int(min(10, 1 + (level - 1) *0.6)) #steigt: [a,a][b,b][c][d,d]... max 10
            kannFahren = False
            geschwindigkeit = 0
            drehgeschwindigkeit = int(min(12, 2 + (level - 1) *0.4)) #steigt: [a,a,][b,b][c,c,c][d,d]... max 12
            schuss_cooldown = int(max(50, 500 + (level - 1) *-20)) # sinkt um -20
            kugeln = int(min(20, 1 + (level - 1) *0.8)) #steigt: [a,a,][b][c][d,d]... max 20 [19]
            #maxKugeln = kugeln
            kugelSpeed = int(min(12, 8 + (level - 1) *0.5)) #steigt: [a,a,][b,b][c,c][d,d,d..] max 12, min 8
            nachladezeit = int(max(1, 50 + (level - 1) *-1.5))/10 #sink: -[a],-[b],-[a]... max 5, min 0.1  #/10 damit es im Nachstellenbereich ist
            farbe = (222, 166, 44)
            neuerPanzer = FeindPanzer(position,id,level,leben,kannFahren,geschwindigkeit,drehgeschwindigkeit,schuss_cooldown,kugeln,kugelSpeed,nachladezeit,farbe)
            self.panzer.append(neuerPanzer)
            feindPanzerGR.add(neuerPanzer)
            # Mienen Stats und appraller danach noch...
#Testing
FM = FeindPanzerManage()
#for i in range(1,25):
FM.NeuerPanzer(1,"stehend",(300,300))
  
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
    def __init__(self, start_pos, richtung, geschwindigkeit=8, abpraller=2, abprallChance=0.75, winkel=None, shooter_id=None):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(ROT)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=start_pos)
        self.richtung = pygame.Vector2(richtung).normalize()
        self.geschwindigkeit = geschwindigkeit
        self.abpraller = abpraller
        self.abprallChance = abprallChance

        self.shooter_id = shooter_id
        self.freund_ignorieren_bis = pygame.time.get_ticks() + 150  # Nur kurz ignorieren

        if winkel is not None:
            self.winkel = winkel
        else:
            self.winkel = -richtung.angle_to(pygame.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.original_image, self.winkel)

    def remove(self):
        self.kill()

    def update(self):
        anzahl_schritte = max(1, int(self.geschwindigkeit))
        teil_bewegung = self.richtung * (self.geschwindigkeit / anzahl_schritte)
        jetzt = pygame.time.get_ticks()

        for _ in range(anzahl_schritte):
            neues_rect = self.rect.move(teil_bewegung)
            self.rect = neues_rect
            # Wandkollision
            wand = pygame.sprite.spritecollideany(self, wände, collided=pygame.sprite.collide_mask)
            if wand:
                if wand.zerstörbarkeit:
                    explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                    wand.schaden(1)
                    self.kill()
                    return
                elif self.abpraller > 0 and random.random() <= self.abprallChance:
                    if wand.rect.width > wand.rect.height:
                        self.richtung.y *= -1
                    else:
                        self.richtung.x *= -1

                    self.abpraller -= 1
                    self.geschwindigkeit *= 0.85
                    self.winkel = -self.richtung.angle_to(pygame.Vector2(1, 0))
                    self.image = pygame.transform.rotate(self.original_image, self.winkel)
                    self.rect = self.rect.move(self.richtung * self.geschwindigkeit / anzahl_schritte)
                else:
                    explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                    self.kill()
                    return

            if jetzt >= self.freund_ignorieren_bis:
                # Nach Ablauf der Schutzzeit: jeder darf getroffen werden
                for panzer in list(spieler_gruppe) + list(feindPanzerGR):
                    if pygame.sprite.collide_mask(self, panzer):
                        panzer.Schaden()
                        explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                        self.kill()
                        return
            else:
                # Während Schutzzeit: Shooter ignorieren
                for panzer in list(spieler_gruppe) + list(feindPanzerGR):
                    if panzer.ID == self.shooter_id:
                        continue  # eigenen Schützen ignorieren
                    if pygame.sprite.collide_mask(self, panzer):
                        panzer.Schaden()
                        explosions_gruppe.add(Explosion(self.rect.centerx, self.rect.centery))
                        self.kill()
                        return

        # Rand verlassen
        puffer = 20
        erweiterter_bereich = pygame.Rect(-puffer, -puffer, WIDTH + 2 * puffer, HEIGHT + 2 * puffer)
        if not erweiterter_bereich.collidepoint(self.rect.center):
            self.kill()
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
        self.ZeitBisEx = mieneZeit
        self.explosionsRadius = explosionsRadius
        self.ErstellerID = ID
        self.ErstellerLastIn = self.ZeitBisEx - jetzt/1000
        self.toleranz = 0.25
        self.early = False
        self.radius = 8
        self.rest = self.ZeitBisEx
        #self.rect = pygame.Rect(pos.x -9, pos.y - 8, 16, 16)
        #self.mienenPos.append({'pos': pos, 'gelegt': jetzt,"von":self.ID, "early":False})
    def update(self):
        jetzt = pygame.time.get_ticks()
        t = (jetzt - self.gelegt) / 1000
        self.rest = self.ZeitBisEx - t
        if self.rest <= 0:
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
            for miene in GelegteMienen:
                diff = miene.pos - self.pos
                abstand = diff.length()
                if abstand <= self.explosionsRadius:
                    miene.early = True
                    miene.gelegt += (2 - miene.rest)*1000  # Gelegte Zeit manipulieren, dass es so war das jetzt nur noch 2 Sekunden verbleibend sind

            if explosions_sprite.mask.overlap(player.mask, offset):
                player.Schaden(2)
            self.kill() 

            ##!!! Bei den getroffenem Panzer, nicht immer Player
        else:
            if self.rest <= 2:   # letzte 2 Sekunden
                # schnelles Blinken
                blink = 500 - ((2 - self.rest) / 2) *100
                blinkend = (jetzt // blink) % 2 == 0
                farbe = (255, 255, 0) if blinkend else (255, 0, 0)
            else:
                farbe = (255, 0, 0)  # normal rot, kein Blinken
                if self.early == False:
                    explosions_sprite = pygame.sprite.Sprite()
                    radius = self.radius # Kugeln sollen nur, wenn sie bei AUF die Miene fliegen, diese Aktivieren. Spieler sollen sie auch im Umkreis aktivieren. Daher unterschiedlicher Radius
                    explosions_sprite.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(explosions_sprite.image, (255, 0, 0, 128), (radius, radius), radius)
                    explosions_sprite.rect = explosions_sprite.image.get_rect(center=(self.pos.x, self.pos.y))
                    explosions_sprite.mask = pygame.mask.from_surface(explosions_sprite.image)
                    # Kollisionen 
                    getroffeneKugel = pygame.sprite.spritecollideany(explosions_sprite, kugel_gruppe, collided=pygame.sprite.collide_mask)
                    if getroffeneKugel:
                        getroffeneKugel.remove()
                        self.early = True
                        self.gelegt += (2 - self.rest)*1000  # Gelegte Zeit manipulieren, dass es so war das jetzt nur noch 2 Sekunden verbleibend sind
                    explosions_sprite = pygame.sprite.Sprite()
                    radius = self.explosionsRadius
                    explosions_sprite.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(explosions_sprite.image, (255, 0, 0, 128), (radius, radius), radius)
                    explosions_sprite.rect = explosions_sprite.image.get_rect(center=(self.pos.x, self.pos.y))
                    explosions_sprite.mask = pygame.mask.from_surface(explosions_sprite.image)
                    offset = (player.rect.left - explosions_sprite.rect.left,player.rect.top - explosions_sprite.rect.top) # NUR SPIELER. ANDERE PANZER MÜSSEN AUCH 
                    if explosions_sprite.mask.overlap(player.mask, offset):
                        if player.ID == self.ErstellerID:
                            if self.ErstellerLastIn - self.rest >= self.toleranz:
                                self.early = True
                                self.gelegt += (2 - self.rest)*1000  # Gelegte Zeit manipulieren, dass es so war das jetzt nur noch 2 Sekunden verbleibend sind
                                
                            self.ErstellerLastIn = self.rest
                            if self.rest <= self.ZeitBisEx - 4: #4 Sekunden zum rausgehen 
                                self.early = True
                                self.gelegt += (2 - self.rest)*1000  # Gelegte Zeit manipulieren, dass es so war das jetzt nur noch 2 Sekunden verbleibend sind
                        else: # Nicht der Leger, also auch keine Vorteile 
                            self.early = True
                            self.gelegt += (2 - self.rest)*1000  # Gelegte Zeit manipulieren, dass es so war das jetzt nur noch 2 Sekunden verbleibend sind
           # pygame.draw.circle(screen, farbe, (int(self.pos.x), int(self.pos.y)), self.radius)
            pygame.draw.circle(screen, farbe, (int(self.pos.x), int(self.pos.y)), self.radius)

def lade_map(map_data):
    wände.empty()
    löcher.empty()

    # Map-spezifische Wände laden
    for wand in map_data.get("walls", []):
        wände.add(Wall(wand["x"], wand["y"], wand["w"], wand["h"], wand.get("destroyable", False)))

    # Immer die vier Randwände laden
    wände.add(Wall(0, 0, WIDTH, 2))                  # Oben
    wände.add(Wall(0, HEIGHT - 2, WIDTH, 2))         # Unten
    wände.add(Wall(0, 0, 2, HEIGHT))                 # Links
    wände.add(Wall(WIDTH - 2, 0, 2, HEIGHT))         # Rechts

    # Löcher laden
    for loch in map_data.get("holes", []):
        löcher.add(Loch(loch["x"], loch["y"], loch["radius"]))

    # Spieler neu platzieren
    global player
    player = Player(map_data["player_start"], "Spieler1",(23, 133, 227))
    spieler_gruppe.empty()
    spieler_gruppe.add(player)

def Main(screen = None):
    #feindPanzer.add(Player(10,10))
    global player, running
    WIDTH, HEIGHT = 800, 400
    if screen is None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Fenstergröße für das Spiel
    pygame.display.set_caption("Panzerkiste")  # Fenstertitel

    lade_map(M.map_test)
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    while running:
        screen.fill(SAND)
        löcher.draw(screen)
        jetzt = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        maus_pos = pygame.mouse.get_pos()
        richtung = pygame.Vector2(maus_pos) - player.position
        if richtung.length() != 0:
            richtung = richtung.normalize()
        winkel = -richtung.angle_to(pygame.Vector2(1, 0))
        player.turmWinkel = winkel
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
            player.Miene()

        if pygame.mouse.get_pressed()[0]:
            player.Schuss(maus_pos, jetzt)

        if player.kugeln == 0 and jetzt - player.letzterSchuss >= player.nachladezeit * 1000:
            player.kugeln = player.maxKugeln 
        GelegteMienen.update()
        spieler_gruppe.update()
        feindPanzerGR.update()
        kugel_gruppe.update()
        kugel_gruppe.draw(screen)
        spieler_gruppe.draw(screen)
        feindPanzerGR.draw(screen)
        wände.draw(screen)
        explosions_gruppe.update()
        explosions_gruppe.draw(screen)

        
        screen.blit(font.render("Kugeln: {}".format(player.kugeln), True, SCHWARZ), (30, 30))
        screen.blit(font.render("Leben: {}".format(player.leben), True, SCHWARZ), (30, 55))

        pygame.display.flip()
        clock.tick(60)

Main()
