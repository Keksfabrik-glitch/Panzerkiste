class Player():
    def __init__(self,position):
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
    def move_right(self):
        self.direction = direction_vector.normalize()
        self.position += self.direction * self.speed
    
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
        self.behaviour = 0 #Noch nicht
        

