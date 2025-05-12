import pygame


# Pygame initialisieren
pygame.init()

# Fenstergröße festlegen
fenster_breite = 800
fenster_hoehe = 600
fenster = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Player Testumgebung")

# Farben definieren
WEISS = (255, 255, 255)
ROT = (255, 0, 0)

# Player-Klasse
class Player():
    def __init__(self, position):
        self.level = 1
        self.position = pygame.Vector2(position)
        self.speed = 1
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

    def move_right(self):
        self.position.x += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, ROT, (int(self.position.x), int(self.position.y)), 10)

# Spieler-Objekt erstellen
spieler = Player((400, 300))

# Hauptschleife
laufend = True
clock = pygame.time.Clock()
while laufend:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laufend = False

    # Hintergrund füllen
    fenster.fill(WEISS)

    spieler.move_right()

    spieler.draw(fenster)

    pygame.display.flip()

    # Frame-Rate begrenzen
    clock.tick(60)

# Pygame beenden
pygame.quit()
sys.exit()

