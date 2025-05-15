import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

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
         

#IGNORIEREN NUR DAMIT MAN ES VISUELL SIEHT 

player = Player((400, 300))  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        player.fahr()
    screen.fill((0, 0, 0))
    panzer_breite = 20  
    panzer_länge = 40   
    panzer_surface = pygame.Surface((panzer_breite, panzer_länge), pygame.SRCALPHA)
    panzer_surface.fill((0, 255, 0))
    gedreht = pygame.transform.rotate(panzer_surface, -player.richtung)
    gedreht_rect = gedreht.get_rect(center=player.position)
    screen.blit(gedreht, gedreht_rect.topleft)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


class FeindPanzer(Level):
    def __init__(self):
        self.level = 1
        self.position = pygame.Vector2(position)
        self.speed = 10
        self.bullets = 5
        self.bullet_speed = 20
        self.bullet_type = 1  # 2 = Feuer
        self.reload_time = 3
        self.last_shot_time = 0
        self.mine_countdown = 7
        self.mines = -1  # -1 = unendlich
        self.rotation_speed = 5
        self.turret_rotation_speed = 8
        self.apprallen = 2
        self.apprall_probability = 0.75
        self.direction = pygame.Vector2(0, 0)
        self.angle = 0
        self.turret_angle = 0
        self.lives = 3
        self.active_bullets = []
        self.state = 0 # 
        
        

