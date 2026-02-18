# Dokumentation der BCI-Logik (Single Metric Ratio)

Diese Dokumentation beschreibt die Änderungen am BCI-System und wie der neue Algorithmus funktioniert.

## Ziel der Änderung
Das vorherige System ("Dual-Channel Agreement") erforderte, dass **zwei separate Bedingungen gleichzeitig** erfüllt sind (Frontal Beta hoch UND Okzipital Alpha niedrig). Dies führte teilweise zu Problemen, wenn einer der beiden Werte schwankte.

Das neue System ("Single Metric Ratio") kombiniert diese beiden Werte zu **einer einzigen, robusten Kennzahl (Ratio)**.

---

## 1. Die Kern-Formel (Ratio)

Die "Ratio" (das Verhältnis) beschreibt, wie stark die Konzentration im Verhältnis zur Entspannung ist.

$$
\text{Ratio} = \frac{\text{Beta-Power (Kanal 1, Stirn)}}{\text{Alpha-Power (Kanal 8, Hinterkopf)}}
$$

*   **Beta-Wellen (Stirn):** Steigen bei Konzentration / kognitiver Last.
*   **Alpha-Wellen (Hinterkopf):** Sinken bei visueller Aufmerksamkeit / offenen Augen / Konzentration.
*   **Effekt:** Wenn du dich konzentrierst, wird der Zähler größer und der Nenner kleiner -> **Die Ratio steigt stark an.**

---

## 2. Berechnung des Schwellenwerts (Kalibrierung)

In der Datei `CalibrationModel.py` werden während der zwei Phasen Daten gesammelt:
1.  **Relaxed-Phase:** Du entspannst dich. -> Wir berechnen den Durchschnitt `Avg_Ratio_Relaxed`.
2.  **Concentrated-Phase:** Du rechnest Kopforgaben. -> Wir berechnen den Durchschnitt `Avg_Ratio_Concentrated`.

Der **Schwellenwert (Threshold)** wird nun gewichtet berechnet:

```python
# Sensitivity = 0.7 (70% Richtung Konzentration)
Threshold = Avg_Ratio_Relaxed + 0.7 * (Avg_Ratio_Concentrated - Avg_Ratio_Relaxed)
```

Dies bedeutet, dass du 70% des Weges von "Entspannt" zu "Konzentriert" zurücklegen musst, um als "Konzentriert" erkannt zu werden. Dies verhindert Fehlalarme, wenn du nur leicht unruhig bist.

Zusätzlich berechnen wir eine **Margin (Hysterese)**:
```python
Margin = |Avg_Ratio_Concentrated - Avg_Ratio_Relaxed| * 0.1  (10% Abstand)
```

---

## 3. Live-Überprüfung (RealTimeProcessor)

Im Spiel (`RealTimeProcessor.py`) wird kontinuierlich (alle 4ms) die aktuelle EEG-Messung analysiert.

1.  Es werden die letzten 250 Messwerte (1 Sekunde) genommen.
2.  Es wird die aktuelle `Live_Ratio` berechnet: `Beta_Live / Alpha_Live`.
3.  **Entscheidungslogik (Hysterese):**

Um ein "Flackern" (schnelles An/Aus) zu verhindern, gibt es zwei Grenzen:

*   **Start Laufen (Move):**
    Die Figur läuft erst los, wenn du den Schwellenwert **deutlich überschreitest**.
    `Live_Ratio > (Threshold + Margin)`

*   **Stop Laufen (Idle):**
    Die Figur bleibt stehen, wenn du den Schwellenwert **deutlich unterschreitest**.
    `Live_Ratio < (Threshold - Margin)`

**Beispiel:**
*   Threshold = 2.0
*   Margin = 0.2
*   -> Du musst über **2.2** kommen, um loszulaufen.
*   -> Du musst unter **1.8** fallen, um stehenzubleiben.
*   (Werte zwischen 1.8 und 2.2 behalten den aktuellen Zustand bei.)

---

## Zusammenfassung der Dateien

*   **`CalibrationModel.py`**: Sammelt Daten, berechnet `Avg_Relaxed` und `Avg_Concentrated`, und bestimmt daraus `Threshold` und `Margin`.
*   **`CalibrationApp.py` & `Main.py`**: Übergeben diese zwei Werte an das Spiel.
*   **`RealTimeProcessor.py`**: Berechnet live die Ratio und vergleicht sie mit `Threshold +/- Margin`, um `PRESS SPACE` oder `RELEASE SPACE` zu senden.

---

## 4. Signalverarbeitung (Verbesserung)

Zusätzlich wurde eine Verbesserung im `SignalProcessor.py` vorgenommen, um die Trennung der Frequenzen zu schärfen.

### Das Problem: Spectral Leakage
Da wir das EEG-Signal in sehr kurze Stücke schneiden (Fensterung), entstehen an den Rändern mathematisch harte Kanten. Diese Kanten erzeugen im Frequenzspektrum "Rauschen" (neue Frequenzen, die eigentlich gar nicht da sind).
Besonders problematisch: Starke **Alpha-Wellen (10-12 Hz)** können dadurch fälschlicherweise als **Beta-Wellen (13+ Hz)** erkannt werden. Das System denkt dann, du konzentrierst dich, obwohl du eigentlich tief entspannt bist.

### Die Lösung: Hanning-Fenster
Wir multiplizieren das Signal nun vor der Analyse mit einer **Hanning-Funktion**.
Diese Funktion blendet das Signal an den Rändern sanft auf Null aus.

*   **Effekt:** Die Kanten verschwinden.
*   **Ergebnis:** Alpha-Wellen bleiben sauber bei Alpha, Beta-Wellen bei Beta. Die Unterscheidung wird viel präziser.

---

---

## 5. Zeit-Filter ("Debounce")

Anstatt einer rechnerischen Glättung (Smoothing) nutzen wir nun eine **Zeit-Bedingung**.

*   **Regel:** Der Schwellenwert muss für **mindestens 0,5 Sekunden UNUNTERBROCHEN** überschritten sein, damit die Figur losläuft.
*   **Regel:** Der Schwellenwert muss für **mindestens 0,5 Sekunden UNUNTERBROCHEN** unterschritten sein, damit die Figur stehen bleibt.

**Vorteil:**
Kurze "Ausreißer" (Spikes) von z.B. 0,2 Sekunden werden komplett ignoriert. Das System reagiert erst, wenn du den Zustand stabil hältst. Dies führt zu einer sehr viel ruhigeren Steuerung ohne "Geister-Laufen" durch kurze Schwankungen.

---

## 6. Störungs-Erkennung (Artifact Rejection)

**Hinweis:** Diese Funktion ist im Code aktuell vorbereitet, aber **auskommentiert (inaktiv)**.

Muskelbewegungen (Zähneknirschen, Stirnrunzeln, Blinzeln) erzeugen elektrische Signale, die viel stärker sind als echtes EEG. Diese Signale können fälschlicherweise als "Konzentration" erkannt werden.

*   **Funktionsweise:** Das System prüft die Signalstärke (Amplitude).
*   **Grenze:** Wenn das Signal stärker als **100 µV** ist.
*   **Reaktion:** Der aktuelle Moment wird **ignoriert**. Das System blockiert jegliche Bewegung, bis das Signal wieder normal ist.

Falls du merkst, dass Grimassen schneiden die Figur bewegt, kannst du diesen Block im Code (`RealTimeProcessor.py`) wieder aktivieren ("einkommentieren").
