PreisPS = 100
Stats = 3
StatsAktuell = 0
diff = (Stats- StatsAktuell)
preis = diff*PreisPS
if preis < 0:
    spreis = preis/2
else:
    preisalt = preis
    preis= preis*(1-diff/100)
print(preis,"Rabatt: ",(preis-preisalt)*-1)

