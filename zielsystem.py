#Zielsystem
import pygame
import math

def hat_sichtlinie(start_pos, ziel_pos, wände):

    schritte = int((ziel_pos - start_pos).length() // 5)
    richtung = (ziel_pos - start_pos).normalize()
    pos = pygame.Vector2(start_pos)

    for _ in range(schritte):
        pos += richtung * 5
        rect = pygame.Rect(pos.x - 1, pos.y - 1, 2, 2)
        for w in wände:
            if rect.colliderect(w.rect) and not w.zerstörbarkeit:
                return False
    return True
def distanzPzuP(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def berechneReflexionswinkel(winkel_rad, normale):
    vx, vy = math.cos(winkel_rad), math.sin(winkel_rad)
    dot = vx * normale[0] + vy * normale[1]
    rx = vx - 2 * dot * normale[0]
    ry = vy - 2 * dot * normale[1]
    return math.atan2(ry, rx)

def prüfeWandkollision(start, ende, wände):
    linie_rect = pygame.Rect(min(start[0], ende[0]), min(start[1], ende[1]),
                             abs(ende[0] - start[0]) + 1, abs(ende[1] - start[1]) + 1)
    for wand in wände:
        if wand.zerstörbarkeit == False:
            if wand.rect.colliderect(linie_rect):
                dx = ende[0] - start[0]
                dy = ende[1] - start[1]
                #dir = richtung
                if abs(dx) > abs(dy):
                    normale = pygame.math.Vector2(0, -1 if dy > 0 else 1)

                else:
                    normale =  pygame.math.Vector2(-1 if dx > 0 else 1, 0)
                #if abs(dx) > abs(dy):
                #    normale = (-1 if dx > 0 else 1, 0)  # vertikale Wand getroffen
                #else:
                #    normale = (0, -1 if dy > 0 else 1)  # horizontale Wand getroffen
                return start, normale
    return None

def Raycast(start_pos, winkel, ziel_pos, wände, max_schritte=2000, max_abpraller=3):
    eigener_rect = pygame.Rect(start_pos[0]-10, start_pos[1]-10, 20, 20)
    ziel_rect = pygame.Rect(ziel_pos[0]-10, ziel_pos[1]-10, 20, 20)  # Spielergröße
    aktuelle_pos = list(start_pos)
    aktueller_winkel = winkel
    abpraller_count = 0
    min_abstand = 100000000000
    schrittweite = 1.0

    for _ in range(max_schritte):
        # nächste Position berechnen
        next_x = aktuelle_pos[0] + math.cos(aktueller_winkel) * schrittweite
        next_y = aktuelle_pos[1] + math.sin(aktueller_winkel) * schrittweite
        naechste_pos = [next_x, next_y]

        # Kollision prüfen
        kollision = prüfeWandkollision(aktuelle_pos, naechste_pos, wände)

        if kollision:
            kollisionspunkt, wand_normale = kollision
            if abpraller_count >= max_abpraller:
                return min_abstand
            aktueller_winkel = berechneReflexionswinkel(aktueller_winkel, wand_normale)
            aktuelle_pos = kollisionspunkt
            abpraller_count += 1
            if eigener_rect.collidepoint(aktuelle_pos):
                return 1000000

            if ziel_rect.collidepoint(aktuelle_pos):
                return 0
            continue
        else:
            aktuelle_pos = naechste_pos

        abstand = 100000
        if hat_sichtlinie(aktuelle_pos,ziel_pos,wände):
            abstand = distanzPzuP(aktuelle_pos, ziel_pos)

        min_abstand = min(min_abstand, abstand)


    
    return min_abstand 


def anim(panzer_pos,spieler_pos,wände):
    if hat_sichtlinie(panzer_pos, spieler_pos, wände):
        richtung = spieler_pos - panzer_pos
        if richtung.length() > 0:
            return -richtung.angle_to(pygame.Vector2(1, 0))
    else:
        return None
#WEITER 

def berechneTurmwinkel(panzer_pos, spieler_pos, wände, nummer,alterBesterWinkel = None, maxAbpraller = 3,Rays=50,sicht=189):

    if hat_sichtlinie(panzer_pos, spieler_pos, wände):
        richtung = spieler_pos - panzer_pos
        if richtung.length() > 0:
            return -richtung.angle_to(pygame.Vector2(1, 0)),0
    else:
        Rays = Rays
        FaecherBreite = sicht
        if nummer == 1:
            FaecherBreite -= 40
            print(FaecherBreite)
            Rays -=5
        elif nummer == 2:
            FaecherBreite -= 30
            print(FaecherBreite)
            Rays -= 10
        elif nummer == 3:
            FaecherBreite -= 20
            Rays -= 15
        elif nummer == 4:
            FaecherBreite -= 10
            Rays -= 10

        MaxSchritte = 4000
        besteDistanz = 1000000000 
        besterWinkel = 0.0
        mittelWinkel = 0
        if alterBesterWinkel == None:
            dx = spieler_pos[0] - panzer_pos[0]
            dy = spieler_pos[1] - panzer_pos[1]
            mittelWinkel = math.degrees(math.atan2(dy, dx))
        else:
            mittelWinkel = alterBesterWinkel

        startWinkel = mittelWinkel - FaecherBreite / 2
        for i in range(Rays):
            if Rays == 1:
                rayWinkel = mittelWinkel
            else:
                fortschritt = i / (Rays - 1)
                rayWinkel = startWinkel + fortschritt * FaecherBreite
            
            rayWinkelRad = math.radians(rayWinkel)
            
            minAbstand = Raycast(panzer_pos, rayWinkelRad, spieler_pos, wände,MaxSchritte, maxAbpraller)
            #print(minAbstand)
            if minAbstand == None:
                minAbstand = 100000000

            if minAbstand < besteDistanz:
                besteDistanz = minAbstand
                besterWinkel = rayWinkel
        return besterWinkel,besteDistanz

def WinkelBerechnen(panzer_pos,spieler_pos,wände,nummer,alterBesterWinkel,maxAbpraller,Rays,sicht):
    bester_winkel,genauigkeit = berechneTurmwinkel(panzer_pos,spieler_pos,wände,nummer,alterBesterWinkel,maxAbpraller,Rays,sicht)
    return bester_winkel,genauigkeit
