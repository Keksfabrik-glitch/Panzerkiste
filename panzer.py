#Panzer
#+ tuple(min(c + amount, 255) for c in color)
import pygame
import math
import random
import string
import Maps as M
import zielsystem as Z
import Speicher as Daten
import json
pygame.init()
clock = pygame.time.Clock()
panzer_größe = 40

P_WIDTH, P_HEIGHT = 800, 400
#Farben
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
SCHWARZ = (0, 0, 0)
SAND = (239, 228, 176)
BLAU = (0, 0, 255)
GRÜN = (0,255,0)
GOLD = (212, 175, 55)
TRANSPARENT = (0,0,0,0)
#Sprite Groups
wände = pygame.sprite.Group()
explosions_gruppe = pygame.sprite.Group()
kugel_gruppe = pygame.sprite.Group()
spieler_gruppe = pygame.sprite.Group()
löcher = pygame.sprite.Group()
GelegteMienen = pygame.sprite.Group()
feindPanzerGR = pygame.sprite.Group()
label_gruppe = pygame.sprite.Group()

screen = pygame.display.set_mode((P_WIDTH,P_HEIGHT))  # screengröße für den Startbildschirm
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

    def __init__(self, position,Name):
        super().__init__()
        self.Punkte = Daten.read(Name,"punkte")
        self.farbe = pygame.Color(*tuple(json.loads(Daten.read(Name,"farbe"))))
        self.ID = Name
        self.position = pygame.Vector2(position)
        self.richtung = 90
        self.turmWinkel = 0
        self.leben = Daten.read(Name,"leben")
        self.geschwindigkeit = Daten.read(Name,"geschwindigkeit")
        self.drehgeschwindigkeit = Daten.read(Name,"drehgeschwindigkeit")
        self.schuss_cooldown = Daten.read(Name,"schussCooldown")
        self.kugeln = Daten.read(Name,"maxKugeln")
        self.maxKugeln = self.kugeln
        self.kugelSpeed = Daten.read(Name,"kugelSpeed")
        self.nachladezeit = Daten.read(Name,"nachladezeit")
        self.letzterSchuss = 0
        self.letzterEinzelschuss = 0
        self.mieneZeit = Daten.read(Name,"mieneZeit")
        self.mienenAnzahl = Daten.read(Name,"mienenAnzahl")
        self.letzte_mine_zeit = -2000
        self.mine_cooldown = Daten.read(Name,"mieneCooldown")
        self.explosionsRadius = Daten.read(Name,"explosionsRadius")
        self.abpraller = Daten.read(Name,"abpraller")
        self.abprallChance = Daten.read(Name,"abprallChance")
        self.mienenPos = []
        self.rewriteGuthaben = pygame.time.get_ticks()+5*1000
        pygame.display.set_caption("Panzerkiste | Punkte: {}$".format(Daten.read(self.ID,"punkte"))) 
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
        if pygame.time.get_ticks() >= self.rewriteGuthaben:
            self.rewriteGuthaben = pygame.time.get_ticks()+60*60*1000
            pygame.display.set_caption("Panzerkiste | Punkte: {}$".format(Daten.read(self.ID,"punkte"))) 
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
                                   shooter_id=self.ID,shooter = self)
                kugel_gruppe.add(neue_kugel)
                self.kugeln -= 1
                self.letzterEinzelschuss = jetzt
                if self.kugeln == 0:
                    self.letzterSchuss = jetzt
    def Schaden(self,amount=1):
        self.leben -= amount
        self.PunkteGeben(-amount)
        if self.leben <= 0:
            print("Ende")
            #running = False       
    def PunkteGeben(self,amount=1):             
        anzeige = amount
        if amount > 0:
            anzeige = "+" + str(amount)
        Daten.write(self.ID,"punkte",(Daten.read(self.ID,"punkte")+amount))
        pygame.display.set_caption("Panzerkiste | Punkte: {}$ | {}$!".format(Daten.read(self.ID,"punkte"),str(anzeige)))   

        self.rewriteGuthaben = pygame.time.get_ticks()+3*1000       
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

        #Zielsystem
        winkel = Z.berechne_turmwinkel(self.position, player.position, wände)
        if winkel is not None:
            self.turmWinkel = winkel
            if Z.hat_sichtlinie(self.position, player.position, wände) == True:
                self.Schuss(winkel*-1)

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
                    
    def Schuss(self, winkel):
        jetzt = pygame.time.get_ticks()
        if self.kugeln > 0 and jetzt - self.letzterEinzelschuss >= self.schuss_cooldown:
            if winkel is not None:
                rad = math.radians(winkel)
                richtung = pygame.Vector2(math.cos(rad), -math.sin(rad))
            else:
                return  # Weder Winkel noch Mausposition

            panzer_radius = panzer_größe * 0.5
            kugel_radius = 5
            abstand = panzer_radius + kugel_radius + 2

            start_pos = self.position + richtung * abstand

            neue_kugel = Kugel(start_pos, richtung, self.kugelSpeed,
                            abpraller=self.abpraller, abprallChance=self.abprallChance,
                            shooter_id=self.ID,shooter = self)
            kugel_gruppe.add(neue_kugel)
            self.kugeln -= 1
            self.letzterEinzelschuss = jetzt
            if self.kugeln == 0:
                self.letzterSchuss = jetzt
    def Schaden(self,amount=1):
        self.leben -= amount
        #if self.leben <= 0:
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
            kugelSpeed = int(min(8, 3 + (level - 1) *0.5)) #steigt: [a,a,][b,b][c,c][d,d,d..] max 12, min 8
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
    def __init__(self, start_pos, richtung, geschwindigkeit=8, abpraller=2, abprallChance=1, shooter_id=None,shooter = None):
        super().__init__()
        self.original_image = pygame.Surface((14, 7), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, ROT, self.original_image.get_rect())
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=start_pos)

        self.position = pygame.math.Vector2(start_pos)
        self.richtung = pygame.math.Vector2(richtung).normalize()
        self.geschwindigkeit = geschwindigkeit
        self.abpraller = abpraller
        self.abprallChance = abprallChance
        self.shooter_id = shooter_id
        self.freund_ignorieren_bis = pygame.time.get_ticks() + 150
        self.shooter = shooter
        self.update_rotation()
    def remove_self(self):
        self.kill()
    def update_rotation(self):
        winkel = self.richtung.angle_to(pygame.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.original_image, winkel)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        jetzt = pygame.time.get_ticks()

        # Bewegung in kleinen Schritten für genaue Kollision
        steps = int(self.geschwindigkeit)
        if steps < 1:
            steps = 1
        step_vector = self.richtung * (self.geschwindigkeit / steps)

        for _ in range(steps):
            self.position += step_vector
            self.rect.center = self.position
            self.update_rotation()

            # --- Wandkollision ---
            for wand in wände:
                if self.rect.colliderect(wand.rect):
                    offset = (wand.rect.left - self.rect.left, wand.rect.top - self.rect.top)
                    overlap = self.mask.overlap(wand.mask, offset)

                    if overlap:  # tatsächliche Pixelkollision
                        self.position -= step_vector  # Schritt zurück
                        self.rect.center = self.position
                        self.update_rotation()

                        if wand.zerstörbarkeit:
                            explosions_gruppe.add(Explosion(*self.rect.center))
                            wand.schaden(1)
                            self.kill()
                            return
                        
                        # Abprallverhalten
                        if self.abpraller > 0 and self.abprallChance  > random.random():
                            normal = self.get_normal_vector(wand)
                            self.richtung = self.richtung.reflect(normal)
                            self.abpraller -= 1
                            self.geschwindigkeit *= 0.85
                            self.update_rotation()
                            return
                        else:
                            explosions_gruppe.add(Explosion(*self.rect.center))
                            self.kill()
                            return

            # --- Gegnerkollision ---
            for ziel in spieler_gruppe.sprites() + feindPanzerGR.sprites():
                if ziel.ID == self.shooter_id and jetzt < self.freund_ignorieren_bis:
                    continue

                if self.rect.colliderect(ziel.rect):
                    offset = (ziel.rect.left - self.rect.left, ziel.rect.top - self.rect.top)
                    if self.mask.overlap(ziel.mask, offset):
                        ziel.Schaden()
                        explosions_gruppe.add(Explosion(*self.rect.center))
                        if self.shooter_id != ziel.ID:
                            if self.shooter_id == player.ID:
                                self.shooter.PunkteGeben(1*ziel.level)
                        self.kill()
                        return

            # --- Spielfeld verlassen ---
            if not screen.get_rect().inflate(40, 40).collidepoint(self.rect.center):
                self.kill()
                return

    def get_normal_vector(self, hindernis):
        # Berechne den exakten Kollisionspunkt via Maske
        offset = (hindernis.rect.left - self.rect.left, hindernis.rect.top - self.rect.top)
        overlap_point = self.mask.overlap(hindernis.mask, offset)
        if not overlap_point:
            return pygame.math.Vector2(0, -1)  # fallback nach oben

        # Erzeuge eine Gradientmaske der Hindernis-Maske für "Normale"
        # Suche Nachbarn um den Kollisionspunkt herum
        x, y = overlap_point
        grad = pygame.math.Vector2(0, 0)

        # Nachbarpixel in der Hindernis-Maske abfragen
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            try:
                if hindernis.mask.get_at((x + dx, y + dy)) == 0:
                    grad += pygame.math.Vector2(dx, dy)
            except IndexError:
                pass

        if grad.length_squared() == 0:
            # Kein Rand gefunden, also fallback
            grad = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(hindernis.rect.center)

        return grad.normalize()

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

class StartLabel(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, level, fpanzer, time, letzte=False, color=(150,0,0)):
        super().__init__()
        jetzt = pygame.time.get_ticks()

        self.level = level
        self.fpanzer = fpanzer
        self.time = time
        self.ende = jetzt + self.time

        if letzte:
            self.mission = "Letzte Mission"
        else:
            self.mission = "Mission: " + str(self.level)
        self.fpanzer_text = "Feindpanzer: " + str(self.fpanzer)

        # Rechteck-Fläche
        self.image = pygame.Surface((w, h))
        self.image.fill(color)

        # Goldränder oben und unten
        pygame.draw.rect(self.image, GOLD, (0, 0, w, 5))           # obere Leiste
        pygame.draw.rect(self.image, GOLD, (0, h - 5, w, 5))       # untere Leiste

        # Schrift vorbereiten
        font = pygame.font.SysFont("Arial", 20, bold=True)

        # Missionstext zentrieren
        mission_surf = font.render(self.mission, True, (255, 255, 255))
        mission_rect = mission_surf.get_rect(centerx=self.image.get_width() // 2)
        mission_rect.top = self.image.get_height() // 2 - mission_surf.get_height() - 5

        # Feindpanzer-Text zentrieren
        panzer_surf = font.render(self.fpanzer_text, True, (255, 255, 255))
        panzer_rect = panzer_surf.get_rect(centerx=self.image.get_width() // 2)
        panzer_rect.top = mission_rect.bottom + 10

        # Texte auf die Fläche zeichnen
        self.image.blit(mission_surf, mission_rect)
        self.image.blit(panzer_surf, panzer_rect)

        # Position
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        jetzt = pygame.time.get_ticks()
        if jetzt >= self.ende:
            self.kill()

def lade_map(map_data,Nutzername):
    wände.empty()
    löcher.empty()

    # Map-spezifische Wände laden
    for wand in map_data.get("walls", []):
        wände.add(Wall(wand["x"], wand["y"], wand["w"], wand["h"], wand.get("destroyable", False)))

    # Immer die vier Randwände laden
    wände.add(Wall(0, -2, P_WIDTH, 4))                  # Oben
    wände.add(Wall(-2, P_HEIGHT - 2, P_WIDTH, 4))         # Unten
    wände.add(Wall(-2, 0, 4, P_HEIGHT))                 # Links
    wände.add(Wall(P_WIDTH - 2, 0, 4, P_HEIGHT))         # Rechts

    # Löcher laden
    for loch in map_data.get("holes", []):
        löcher.add(Loch(loch["x"], loch["y"], loch["radius"]))

    # Spieler neu platzieren
    global player
    player = Player(map_data["player_start"], Nutzername)
    spieler_gruppe.empty()
    spieler_gruppe.add(player)

def Main(Nutzername):
    #feindPanzer.add(Player(10,10))
    global player, running
    P_WIDTH, P_HEIGHT = 800, 400
    screen = pygame.display.set_mode((P_WIDTH, P_HEIGHT))  # Fenstergröße für das Spiel
    pygame.display.set_caption("Panzerkiste")  # Fenstertitel

    lade_map(M.map_test,Nutzername)
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    #Startlabel Test
    start_running = True
    label_gruppe.add(StartLabel(0,0,P_WIDTH,P_HEIGHT,0,1,2000))
    while start_running:
        clock.tick(60)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
                running = False
        if pygame.mouse.get_pressed()[0]:
            start_running = False
        label_gruppe.update()
        label_gruppe.draw(screen)
        if len(label_gruppe) == 0:
            start_running = False
        pygame.display.flip()
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
        for panzer in feindPanzerGR:
            if panzer.kugeln == 0 and jetzt - panzer.letzterSchuss >= panzer.nachladezeit * 1000:
                panzer.kugeln = panzer.maxKugeln
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

#Main()
