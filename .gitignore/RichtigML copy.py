import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LeakyReLU
import matplotlib.transforms as mtransforms
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import os
import tkinter as tk
import pandas as pd

# 🧾 PARAMETER
symbol = "RHM.DE"#"SPOT"  #"RBLX"#"AAPL"#"RHM.DE""^GDAXI"#"Dax"
steps_ahead = 12  # 1 Stunde (12×5min)
features = ["Open", "High", "Low", "Close", "Volume"]
    
# 📥 DATEN LADEN
df = yf.download(tickers=symbol, period="5d", interval="1m", auto_adjust=True)
df.index = pd.to_datetime(df.index)
df.index = df.index.tz_localize(None)  # Erst entziehen, falls schon tz-aware
df.index = df.index.tz_localize("UTC").tz_convert("Europe/Berlin")

df = df.between_time("09:00", "17:30")
df = df[df.index.dayofweek < 5]
df.dropna(inplace=True)

# 🎯 ZIEL ERZEUGEN: Kurs in 1h > 1% höher?
future_close = df["Close"].shift(-steps_ahead)
change = (future_close - df["Close"]) / df["Close"]
y_raw = (change > 0.01).astype(int)

# 🧮 EINGABEN & ZIEL ABGLEICHEN
X = df[features].iloc[:-steps_ahead].copy()
y = y_raw.iloc[:-steps_ahead]

# ⚖️ BALANCING (via Upsampling der Minderheit)
data = X.copy()
data["label"] = y
majority = data[data["label"] == 0]
minority = data[data["label"] == 1]

if len(minority) > 0:
    minority_upsampled = resample(minority, replace=True, n_samples=len(majority), random_state=42)
    balanced = pd.concat([majority, minority_upsampled])
else:
    balanced = majority  # Falls keine Anstiege > 1% vorhanden

X = balanced[features].to_numpy()
y = balanced["label"].to_numpy()

# 🔢 SCALING
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 🔀 SPLIT
split_index = int(len(X_scaled) * 0.8)
X_train, X_test = X_scaled[:split_index], X_scaled[split_index:]
y_train, y_test = y[:split_index], y[split_index:]


# 🧠 MODELL
#model = Sequential([
   # Input(shape=(X.shape[1],)),
  #  Dense(128, activation='relu'),
    #Dropout(0.3),
   # Dense(64, activation='relu'),
  #  Dropout(0.2),
    #Dense(32, activation='relu'),
  #  Dropout(0.1),
 #   Dense(16, activation='relu'),
 #   Dense(1, activation='sigmoid')
#])
model = Sequential([
    Input(shape=(X.shape[1],)),
    Dense(100),
    LeakyReLU(alpha=0.1),  # LeakyReLU mit alpha=0.1 (Standardwert)
    Dropout(0.5),

    Dense(120),
    LeakyReLU(alpha=0.1),
    Dropout(0.2),

    Dense(50),
    LeakyReLU(alpha=0.1),
    Dropout(0.1),

    Dense(10),
    LeakyReLU(alpha=0.1),
    Dense(5),
    LeakyReLU(alpha=0.1),
    Dense(1, activation='sigmoid')
])
#adamax: 64
# Adam: 63
#nadam: 65
model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=['accuracy'])

# ⏱ EARLY STOPPING
early_stop = EarlyStopping(monitor='val_accuracy', mode='max', patience=10, restore_best_weights=True, verbose=1)

# 🚀 TRAINING
print("🚀 Training startet...")

# ⚖️ Klassengewichtung statt Upsampling
class_weight = {
    0: 1.0,
    1: len(y[y == 0]) / max(len(y[y == 1]), 1)
}

# 🚀 Training mit Gewichtung
history = model.fit(
    X_train, y_train,
    epochs=60,
    validation_data=(X_test, y_test),
    callbacks=[early_stop],
    verbose=1,
    class_weight=class_weight
)


# 💾 SPEICHERN
model.save("modell_rheinmetall.keras")

# 📈 TRAININGSGENAUIGKEIT
plt.plot(history.history['accuracy'], label='Training')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title("Modellgenauigkeit")
plt.xlabel("Epoche")
plt.ylabel("Accuracy")
plt.legend()
plt.grid()
plt.show()

# ✅ TESTGENAUIGKEIT
loss, acc = model.evaluate(X_test, y_test)
print(f"🎯 Testgenauigkeit: {acc*100:.2f}%")

# 🔮 LETZTE VORHERSAGE
last_input = X_scaled[-1].reshape(1, -1)
print(last_input)
prob = model.predict(last_input)[0][0]
entscheidung = "📈 Long (steigt)" if prob > 0.5 else "📉 Short (fällt)"
print(f"🔍 Wahrscheinlichkeit {prob:.2f} das es steigt.")

def plot_heutiger_tagesverlauf_mit_ai():
    jetzt = pd.Timestamp.now(tz="Europe/Berlin")
    heute = jetzt.normalize()
    morgen = heute + pd.Timedelta(days=1)

    df = yf.download(symbol, start=heute.strftime("%Y-%m-%d"),
                     end=morgen.strftime("%Y-%m-%d"),
                     interval="5m", auto_adjust=True)

    if df.empty:
        print("❌ Keine heutigen Kursdaten verfügbar.")
        return

    df = df.tz_convert("Europe/Berlin")
    df = df.between_time("09:00", jetzt.strftime("%H:%M"))

    if df.empty:
        print("❌ Keine Daten im heutigen Börsenzeitfenster.")
        return

    # Aktueller Kurs
    aktueller_kurs = df["Close"].iloc[-1]
    letzter_zeitpunkt = df.index[-1]

    # AI-Vorhersage
    slope = (prob - 0.5) * 2
    y_scale = aktueller_kurs * 0.005

    # Prognose-Zeitraum: 20 Minuten in die Zukunft
    x_vals = [letzter_zeitpunkt, letzter_zeitpunkt + pd.Timedelta(minutes=20)]
    y_vals = [aktueller_kurs, aktueller_kurs + slope * y_scale]
   
    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["Close"], label="Kursverlauf heute", color='blue')
    plt.axvline(letzter_zeitpunkt, color='red', linestyle='--', label='Jetzt')
    plt.plot(x_vals, y_vals, color="orange", linewidth=3,
             label=f"AI-Prognose ({prob:.2f})")
    plt.title(f"{symbol} – Heutiger Börsentag")
    plt.xlabel("Zeit")
    plt.ylabel("Preis (€)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
plot_heutiger_tagesverlauf_mit_ai()
#END END END
# Variante 1: Unskalierte & Skalierte Eingaben VOR Balancing plotten (originale Zeitachse nutzen)

original_len = df[features].iloc[:-steps_ahead].shape[0]
index_for_plot = df.index[-original_len:]

# Unskalierte Eingaben
plt.figure(figsize=(12, 6))
for col in features:
    plt.plot(index_for_plot, df[col].iloc[-original_len:], label=col)
plt.title("Unskalierte Eingabewerte (Input-Features)")
plt.xlabel("Zeit")
plt.ylabel("Wert")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Skalierte Eingaben (vor Balancing!)
scaler_for_plot = MinMaxScaler()
X_before_balancing = df[features].iloc[:-steps_ahead].to_numpy()
X_scaled_before_balancing = scaler_for_plot.fit_transform(X_before_balancing)

plt.figure(figsize=(12, 6))
for i, col in enumerate(features):
    plt.plot(index_for_plot, X_scaled_before_balancing[:, i], label=col)
plt.title("Skalierte Eingabedaten (ohne Balancing)")
plt.xlabel("Zeit")
plt.ylabel("Skalierter Wert (0–1)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
def plot_historischer_trainingstag_mit_ai(tag_index=100):
    # Wähle einen beliebigen Index aus dem (unbalancierten) Original-Dataset
    df_tag = df.iloc[:-steps_ahead]  # damit es zu y_raw passt
    if tag_index >= len(df_tag):
        print("❌ Index außerhalb des Datenbereichs.")
        return

    zeitpunkt = df_tag.index[tag_index]
    kurs_bis_dahin = df.loc[df.index.date == zeitpunkt.date()]

    if kurs_bis_dahin.empty:
        print("❌ Keine Kursdaten für den gewählten Tag.")
        return

    # Aktueller Punkt und Zielpunkt für Vorhersage
    vorher = df["Close"].iloc[tag_index]
    nachher = df["Close"].iloc[tag_index + steps_ahead]
    steigung = (nachher - vorher) / vorher
    ziel_erreicht = steigung > 0.01

    # Vorhersage simulieren
    x_input = df[features].iloc[tag_index].values.reshape(1, -1)
    x_input_scaled = scaler.transform(x_input)
    prob = model.predict(x_input_scaled)[0][0]
    entscheidung = prob > 0.5

    # Prognose-Pfeil (wie bei heutiger AI)
    slope = (prob - 0.5) * 2
    y_scale = vorher * 0.005
    zeit_von = zeitpunkt
    zeit_bis = zeitpunkt + timedelta(minutes=steps_ahead * 5)
    x_vals = [zeit_von, zeit_bis]
    y_vals = [vorher, vorher + slope * y_scale]

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(kurs_bis_dahin.index, kurs_bis_dahin["Close"], label="Kursverlauf", color='blue')
    plt.axvline(zeitpunkt, color='red', linestyle='--', label='AI-Vorhersage-Zeitpunkt')
    plt.plot(x_vals, y_vals, color="orange", linewidth=3, label=f"AI-Prognose ({prob:.2f})")

    # Tatsächlicher Endpunkt nach steps_ahead
    plt.scatter(zeit_bis, nachher, color="green" if ziel_erreicht else "black", 
                label=f"Tatsächlicher Kurs (+1h): {'↑' if ziel_erreicht else '↓'}")

    plt.title(f"{symbol} – Historischer Tag mit AI-Prognose")
    plt.xlabel("Zeit")
    plt.ylabel("Preis (€)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()





# 🔍 Einzelner Input – Balkendiagramm
plt.figure(figsize=(6, 4))
plt.bar(features, last_input[0])
plt.title("Letzter Eingabewert (Modellinput vor Vorhersage)")
plt.ylabel("Skalierter Wert (0–1)")
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# Beispielaufruf
plot_historischer_trainingstag_mit_ai(tag_index=70)