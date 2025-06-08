import pygame
import hashlib
import Speicher as Sp
from panzer import WEISS

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
        daten[nutzername] = {
            "passwort": hash_passwort(passwort),
            "stats": {
                "leben": 3,
                "abpraller": 2,
                "geschwindigkeit": 10,
                "drehgeschwindigkeit": 5,
                "schuss_cooldown": 250,
                "kugeln": 5,
                "maxKugeln": 5,
                "kugelSpeed": 10,
                "nachladezeit": 3,
                "abprallChance": 0.75,
                "mieneZeit": 15,
                "mienenAnzahl": -1,
                "mine_cooldown": 5,
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
            return True,daten[nutzername]["stats"] # Account Daten werden zurückgegeben
    else:
        return False,"Nutzername nicht vergeben."
passt , statment = anmelden ("test","1234567")
print(statment)
def Main (screen = None):
    AC_BREITE = 600
    AC_HOEHE = 800

    if screen is None:
        screen = pygame.display.set_mode((AC_BREITE, AC_HOEHE))

    screen.set_caption("Anmelden")

    #Farben
    WEISS = (255,255,255)
    laueft = True

    while laueft:
        screen.fill(WEISS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laueft = False