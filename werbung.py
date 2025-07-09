import pygame
import cv2
import numpy as np

def werbung(video_path, audio_path):
    # Video laden
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Fehler: Video {video_path} konnte nicht geöffnet werden.")
        return

    # Pygame initialisieren
    pygame.init()
    pygame.mixer.init()

    # Audio laden und abspielen
    try:
        pygame.mixer.music.load(audio_path)
    except pygame.error as e: #Error Message abfangen
        print(f"Fehler beim Laden der Audiodatei: {e}") #Diese hinzufügen
        cap.release()
        pygame.quit()
        return
    pygame.mixer.music.play()#Abspielen der Audiodatei

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2)# breite des videos laden und halbieren
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)# breite des videos laden und halbieren
    fps = cap.get(cv2.CAP_PROP_FPS)# FPS des Videos laden
    if fps == 0:
        fps = 30  # Fallback FPS

    # Fenster erstellen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Kurze Werbepause")

    clock = pygame.time.Clock()

    running = True
    while running and cap.isOpened():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()

        ret, frame = cap.read()
        if not ret: #letztes frame erreicht
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # cv2 und pygame haben andere Farbangaben BGR vs. RGB
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
        # cv2 und pygame haben andere rotierung
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        #Entspiegelt
        frame_surface = pygame.transform.scale(frame_surface, (width, height))
        #kleinere größe

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        clock.tick(fps)

    cap.release()