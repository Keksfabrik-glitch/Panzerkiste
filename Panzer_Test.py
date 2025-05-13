# Pygame Template
import pygame

# Setup
pygame.init()
BREITE = 600
HOEHE = 600
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Testareal")
# clock = pygame.time.Clock()
laeuft = True
# Farben
SAND = (239,228,176)
BLAU = (0,0,255)
SCHWARZ = (0,0,0)
# Panzer
panzer_größe = 30
unten = pygame.Surface((panzer_größe,panzer_größe-(panzer_größe/6)) , pygame.SRCALPHA)
unten.fill(BLAU)
pygame.draw.rect(unten, SCHWARZ, (0, 0, panzer_größe,panzer_größe-(panzer_größe/6)), 2)
position = pygame.Vector2(400, 300)
oben = pygame.Surface((panzer_größe,panzer_größe/6) , pygame.SRCALPHA)
oben.fill(BLAU)
pygame.draw.rect(oben, SCHWARZ, (0, 0, panzer_größe,panzer_größe-(panzer_größe/6)), 2)
speed_level = 1 #Hier Attribut abfragen
speed = speed_level/6
# Gameloop / Spielschleife
while laeuft:
    fenster.fill(SAND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laeuft = False

    # Richtung zur Maus
    maus_pos = pygame.mouse.get_pos()
    richtung = pygame.Vector2(maus_pos) - position
    if richtung.length() != 0:
        richtung = richtung.normalize()  # auf Länge 1 bringen
    winkel = -richtung.angle_to(pygame.Vector2(1, 0))
    
    #Zur Maus drehen
    rotiert = pygame.transform.rotate(unten, -winkel)
    neu_rect = rotiert.get_rect(center=position)

    # Bewegungen
    tastatur = pygame.key.get_pressed()
    quer = pygame.Vector2(-richtung.y, richtung.x)  # 90° gedreht
    if tastatur[pygame.K_w]:
        position += richtung * speed
    if tastatur[pygame.K_s]:
        position -= richtung * speed
    if tastatur[pygame.K_a]:
        position -= quer * speed
    if tastatur[pygame.K_d]:
        position += quer * speed

    fenster.blit(rotiert, neu_rect)
    pygame.display.flip()

    # clock.tick(60)  # limits FPS to 60

# Ende
pygame.quit()
exit()