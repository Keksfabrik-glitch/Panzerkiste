#Speicher
import json
Speicherort = "Accounts.json"
def speichere_daten(dateiname, daten):
    with open(dateiname, "w") as f:
        json.dump(daten, f, indent=4)

def lade_daten(dateiname):
    with open(dateiname, "r") as f:
        return json.load(f)
    
def read(nutzername,value):
    try :
        daten = lade_daten(Speicherort)
    except :
        return False
    if nutzername in daten: 
        return daten[nutzername]["stats"][value]
    return False 
   

def write(nutzername, value, set):
    try :
        daten = lade_daten(Speicherort)
    except :
        return False
    if nutzername in daten: 
        daten[nutzername]["stats"][value] = set
        speichere_daten(Speicherort, daten)
        return True
    return False 

#
#print(write("Andreas","leben",0))
#print(read("Andreas","leben"))
   