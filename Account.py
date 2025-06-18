import pygame
import hashlib
import Speicher as Sp

try:
    from win11toast import toast, notify, update_progress
    wintoast = True
except:
    wintoast = False
    print("Bitte installiere Win11toast, um alle Features freizuschalten")
pygame.init()
Speicherort = "Accounts.json"

def hash_passwort(passwort):
    return hashlib.sha256(passwort.encode()).hexdigest()

def registrieren (nutzername,passwort):
    try :
        daten = Sp.lade_daten(Speicherort)
    except :
        daten = {} #Fals Accounts leer


    if nutzername in daten: #Ist Nutzername Vergeben ?
        return False,"Nutzername bereits vergeben."
    else: #Wenn nein wird neuer Account angelegt
        daten[nutzername] = {  #Name
            "passwort": hash_passwort(passwort),
            "stats": {
                "punkte": 0, #Geld
                "farbe": "[98, 255, 255, 255]",
                "leben": 3,
                "schussCooldown": 250,
                "drehgeschwindigkeit": 5,
                "geschwindigkeit": 10,
                "maxKugeln": 5,
                "kugelSpeed": 5,
                "nachladezeit": 5,
                "abpraller":2,
                "abprallChance": 0.75,
                "mieneZeit": 15,
                "mienenAnzahl": -1, # unendlich -1
                "mieneCooldown": 5,
                "explosionsRadius": 40
            }
        }
        Sp.speichere_daten(Speicherort,daten)
        return True,"Erfolgreich Registriert"


def anmelden (nutzername,passwort):
    try :
        daten = Sp.lade_daten(Speicherort)
    except :
        return False,"Noch keine Nutzer definiert."
    if nutzername in daten:  # Ist Nutzername Vergeben ?
        if daten[nutzername]["passwort"] == hash_passwort(passwort): #Es wird überprüft ob Passwort zu Nutzername passt
            return True,"Erfolg" # Account Daten werden zurückgegeben
        else:
            return False,"Falsches Passwort"
    else:
        return False,"Nutzername nicht vergeben."

# Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
HELLBLAU = pygame.Color('lightskyblue3')
WEISS_AKTIV = pygame.Color('white')

# Schrift
FONT = pygame.font.Font(None, 32)


class InputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, *, password=False, placeholder='', text_color=SCHWARZ):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.color_active = WEISS_AKTIV
        self.color_passive = HELLBLAU
        self.color = self.color_passive
        self.text_color = text_color
        self.active = False
        self.text = ''
        self.placeholder = placeholder or ''
        self.font = FONT
        self.password = password
        self.image = pygame.Surface((w, h))
        self.update_image()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.update_image()

    def update(self):
        self.color = self.color_active if self.active else self.color_passive
        self.update_image()

    def update_image(self):
        if self.password:
            if self.text:
                display_text = '*' * len(self.text)
                display_color = self.text_color  # normale Farbe
            else:
                display_text = self.placeholder  # Platzhaltertext
                display_color = (150, 150, 150)  # grau für Platzhalter
        else:
            if self.text:
                display_text = self.text
                display_color = self.text_color
            else:
                display_text = self.placeholder
                display_color = (150, 150, 150)

        text_surface = self.font.render(display_text, True, display_color)

        # Box aktualisieren
        box_width = max(200, text_surface.get_width() + 20)
        self.image = pygame.Surface((box_width, self.rect.height))
        self.image.fill(self.color)

        # Text zentriert
        text_x = (self.image.get_width() - text_surface.get_width()) // 2
        text_y = (self.image.get_height() - text_surface.get_height()) // 2
        self.image.blit(text_surface, (text_x, text_y))

        # Schwarzen Rahmen zeichnen
        pygame.draw.rect(self.image, SCHWARZ, self.image.get_rect(), 2)

        # Rechteck aktualisieren
        self.rect.w = self.image.get_width()

class Button:
    def __init__(self, x, y, w, h, text, callback, font=FONT):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (180, 180, 180)
        self.hover_color = (150, 150, 150)
        self.text = text
        self.callback = callback
        self.font = font
        self.text_surf = self.font.render(self.text, True, SCHWARZ)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        if is_hover:
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, SCHWARZ, self.rect, 2)

        text_rect = self.text_surf.get_rect(center=self.rect.center)
        screen.blit(self.text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()


def Main(screen=None):
    AC_BREITE = 600
    AC_HOEHE = 500

    if screen is None:
        screen = pygame.display.set_mode((AC_BREITE, AC_HOEHE))

    pygame.display.set_caption("Anmelden")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    # Eingabefelder
    input_nutzer = InputBox(200, 150, 200, 32, placeholder="Benutzername")
    input_pass = InputBox(200, 200, 200, 32, password=True, placeholder="Passwort")
    input_group = pygame.sprite.Group(input_nutzer, input_pass)

    meldung = ""
    meldung_surface = None
    laeuft = True
    # Callback-Funktionen
    def versuche_anmeldung():
        nonlocal meldung, meldung_surface, laeuft
        erfolg, result = anmelden(input_nutzer.text, input_pass.text)
        meldung = "Erfolgreich Angemeldet" if erfolg else result
        if erfolg:
            laeuft = False
        if wintoast == False:
            meldung_surface = font.render(meldung, True, SCHWARZ)
        else:
            if erfolg == False:
                toast("Anmeldung fehlgeschlagen",meldung,audio='ms-winsoundevent:Notification.IM')
                input_pass.text = ""

    def versuche_registrierung():
        nonlocal meldung, meldung_surface,laeuft
        passwort = input_pass.text
        erfolg,result = False,False
        if len(passwort) < 5:
            erfolg = False
            result = "Passwort muss mindestens 5 Zeichen lang sein"
        else:
            erfolg, result = registrieren(input_nutzer.text, input_pass.text)
        meldung = "Registrierung erfolgreich!" if erfolg else result
        if erfolg:
            laeuft = False
        if wintoast == False:
            meldung_surface = font.render(meldung, True, SCHWARZ)
        else:
            if erfolg == False:
                toast("Registrierung fehlgeschlagen",meldung,audio='ms-winsoundevent:Notification.IM')

    # Buttons
    button_anmelden = Button(150, 300, 130, 40, "Anmelden", versuche_anmeldung)
    button_registrieren = Button(320, 300, 130, 40, "Registrieren", versuche_registrierung)


    while laeuft:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laeuft = False

            for box in input_group:
                box.handle_event(event)

            button_anmelden.handle_event(event)
            button_registrieren.handle_event(event)

        screen.fill(WEISS)

        input_group.update()
        input_group.draw(screen)

        # Schwarze Rahmen um Eingabefelder
        for box in input_group:
            pygame.draw.rect(screen, SCHWARZ, box.rect, 2)

        button_anmelden.draw(screen)
        button_registrieren.draw(screen)

        if meldung_surface:
            screen.blit(meldung_surface, (200, 260))

        pygame.display.flip()
        clock.tick(60)
    return str(input_nutzer.text)