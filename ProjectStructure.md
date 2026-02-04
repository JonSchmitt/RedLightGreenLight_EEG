# Projektstruktur & EEG-Logik

Dieses Dokument bietet einen detaillierten Überblick über die Architektur des Projekts, insbesondere über das Zusammenspiel der Brain-Computer Interface (BCI) Komponenten mit dem Spiel.

## 1. Programmablauf und Architektur

Das folgende Diagramm zeigt den vollständigen Ablauf des Programms, beginnend bei `Main.py`:

![Programmablauf von Main.py](docs/architecture_flow.png)

### Erklärung des Programmablaufs:

1. **Programmstart (`Main.py`)**:
   - Das Programm startet in der `Main`-Klasse
   - Die `main()`-Methode orchestriert den gesamten Ablauf

2. **Phase 1: Kalibrierung**:
   - `CalibrationApp` wird gestartet
   - Der Nutzer durchläuft zwei 30-sekündige Phasen (Relaxed und Concentrated)
   - Die Kalibrierung liefert 6 Werte zurück: `th1, dir1, m1, th8, dir8, m8`
     - `th1/th8`: Schwellenwerte für Kanal 1 und 8
     - `dir1/dir8`: Richtung (+1 oder -1) für jeden Kanal
     - `m1/m8`: Sicherheitsmargen (15% des Schwellenwerts)

3. **Phase 2: BCI-Prozess starten**:
   - `RealTimeProcessor` wird mit den Kalibrierungswerten initialisiert
   - Der Prozess startet als separater Hintergrundprozess
   - Er analysiert kontinuierlich EEG-Daten und sendet Befehle über eine `Queue`

4. **Phase 3: Spiel starten**:
   - `GameApp` wird gestartet und erhält die `command_queue`
   - Die Spielschleife läuft mit 60 FPS
   - In jedem Frame:
     - Werden EEG-Befehle aus der Queue gelesen (falls vorhanden)
     - Tastendrücke simuliert (LEERTASTE drücken/loslassen)
     - Der aktuelle Spielzustand aktualisiert
     - Zwischen Zuständen gewechselt (Menu, Game, Settings, Quit)

5. **Programmende**:
   - Bei `QuitState` wird die Schleife beendet
   - Der BCI-Prozess wird gestoppt
   - Pygame wird beendet

---

## 2. Kalibrierungs-Logik im Detail

Der Kalibrierungsprozess ist entscheidend für die Bestimmung der individuellen Beta/Alpha-Verhältnis-Schwellenwerte. Das folgende Diagramm zeigt alle Berechnungsschritte:

![Detaillierter Kalibrierungs-Ablauf](docs/calibration_flow.png)

### Detaillierte Erklärung der Berechnungsschritte:

**Phase 1 & 2: Datensammlung**
- Jede Phase dauert 30 Sekunden
- Bei 250 Hz Abtastrate werden 7500 Samples pro Kanal gesammelt
- Kanal 1 (Frontal) und Kanal 8 (Okzipital) werden verwendet

**Schritt 1: Filterung**
- Butterworth-Bandpass-Filter 3. Ordnung
- **Kausale Filterung** mit `lfilter` (wichtig für Konsistenz mit Echtzeit)
- Alpha-Band: 8-12 Hz
- Beta-Band: 13-30 Hz

**Schritt 2: FFT-Berechnung**
- Fast Fourier Transform wird auf die gefilterten Signale angewendet
- Transformation vom Zeitbereich in den Frequenzbereich

**Schritt 3: Spektralleistung**
- Die Magnituden der FFT-Werte werden summiert
- Ergibt die Gesamtleistung im jeweiligen Frequenzband

**Schritt 4: Verhältnis-Berechnung**
- `Ratio = Beta_Power / Alpha_Power`
- Wird für beide Kanäle und beide Phasen berechnet
- Ergibt: `Ch1_rel`, `Ch1_con`, `Ch8_rel`, `Ch8_con`

**Schritt 5: Schwellenwert-Berechnung**
- Mittelwert der beiden Phasen:
  - `th1 = (Ch1_rel + Ch1_con) / 2`
  - `th8 = (Ch8_rel + Ch8_con) / 2`

**Schritt 6: Richtungsbestimmung**
- Bestimmt, ob höhere oder niedrigere Werte Konzentration bedeuten:
  - `dir = +1` wenn `Concentrated > Relaxed` (höhere Werte = Konzentration)
  - `dir = -1` sonst (niedrigere Werte = Konzentration)

**Schritt 7: Sicherheitsmarge**
- 15% des Schwellenwerts als Hysterese-Margin:
  - `m1 = th1 × 0.15`
  - `m8 = th8 × 0.15`
- Verhindert zu häufiges Umschalten bei Rauschen

---

## 3. Echtzeit-Steuerungslogik (BCI)

Während das Spiel läuft, analysiert der `RealTimeProcessor` kontinuierlich EEG-Daten:

### Diagramm der Steuerungs-Pipeline

![Steuerungs-Pipeline](docs/realtime_pipeline.png)

### Verarbeitungsschritte:
1.  **Datenerfassung**: `EEGManager` ruft Samples mit 250Hz ab
2.  **Sliding Window**: 1-Sekunden-Puffer (250 Samples) wird kontinuierlich aktualisiert
3.  **Signalverarbeitung**: Identisch zur Kalibrierung (Filter, FFT, Ratio-Berechnung)
4.  **Hystereselogik** (Dual-Channel Agreement):
    - **BEWEGUNG auslösen**: Beide Kanäle müssen `threshold + margin` überschreiten
    - **STILLSTAND auslösen**: Mindestens ein Kanal muss unter `threshold - margin` fallen
5.  **Befehlsausführung**: Befehle werden über `multiprocessing.Queue` an `GameApp` gesendet

---

## 4. Überblick der Ordnerstruktur

- **`Main.py`**: Einstiegspunkt, orchestriert Kalibrierung → BCI → Spiel
- **`EEG/`**: Kernlogik für Signalverarbeitung und Echtzeit-Multiprocessing
- **`Calibration/`**: MVC-Implementierung für die EEG-Kalibrierungs-Sub-Anwendung
- **`RedLightGreenLight/`**: Hauptanwendung des Spiels, State Machine und Assets
- **`UIUtils/`**: Wiederverwendbare Pygame GUI-Komponenten
- **`TestData/`**: Mock-Daten für Entwicklung ohne EEG-Hardware
- **`Tests/`**: Automatisierte Skripte zur Verifizierung der Signalverarbeitung
