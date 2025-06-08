#Speicher
import json

def speichere_daten(dateiname, daten):
    with open(dateiname, "w") as f:
        json.dump(daten, f, indent=4)

def lade_daten(dateiname):
    with open(dateiname, "r") as f:
        return json.load(f)