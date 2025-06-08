import pygame

# === Zielsystem für FeindPanzer ===
def hat_sichtlinie(start_pos, ziel_pos, wände):
    schritte = int((ziel_pos - start_pos).length() // 5)
    richtung = (ziel_pos - start_pos).normalize()
    pos = pygame.Vector2(start_pos)

    for _ in range(schritte):
        pos += richtung * 5
        rect = pygame.Rect(pos.x - 1, pos.y - 1, 2, 2)
        if any(rect.colliderect(w.rect) for w in wände):
            return False
    return True

def finde_abprall_zielrichtung(start_pos, ziel_pos, wände, max_abpraller=2):
    richtung = (ziel_pos - start_pos).normalize()
    pos = pygame.Vector2(start_pos)
    abpraller = 0

    for _ in range(1000):
        pos += richtung * 5
        rect = pygame.Rect(pos.x - 2, pos.y - 2, 4, 4)

        if rect.collidepoint(ziel_pos):
            return (ziel_pos - start_pos).normalize()

        for wand in wände:
            if rect.colliderect(wand.rect):
                delta = pos - wand.rect.center
                normal = pygame.math.Vector2(0, 0)
                if abs(delta.x) > abs(delta.y):
                    if delta.x > 0:
                        normal.x = 1
                    else :
                        normal.x = -1
                else:
                    if delta.y > 0:
                        normal.y = 1
                    else:
                        normal.y = -1

                richtung = richtung.reflect(normal)
                abpraller += 1
                if abpraller > max_abpraller:
                    return None
                break
    return None

def berechne_turmwinkel(panzer_pos, spieler_pos, wände):
    if hat_sichtlinie(panzer_pos, spieler_pos, wände):
        richtung = spieler_pos - panzer_pos
        if richtung.length() > 0:
            return -richtung.angle_to(pygame.Vector2(1, 0))
    else:
        reflektiert = finde_abprall_zielrichtung(panzer_pos, spieler_pos, wände)
        if reflektiert:
            return -reflektiert.angle_to(pygame.Vector2(1, 0))
    return None
