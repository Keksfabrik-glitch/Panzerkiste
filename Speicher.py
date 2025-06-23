# Speicher.py
import json
import os

Speicherort = "Accounts.json"

def speichere_daten(dateiname, daten):
    with open(dateiname, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4, ensure_ascii=False)

def lade_daten(dateiname):
    if not os.path.exists(dateiname):
        return {}
    with open(dateiname, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def read(nutzername, value, ort="stats", speicherort=Speicherort):
    daten = lade_daten(speicherort)
    return daten.get(nutzername, {}).get(ort, {}).get(value, False)

def write(nutzername, value, set, ort="stats", speicherort=Speicherort):
    daten = lade_daten(speicherort)
    if nutzername in daten and ort in daten[nutzername]:
        daten[nutzername][ort][value] = set
        speichere_daten(speicherort, daten)
        return True
    return False
