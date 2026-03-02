import base64

def encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')

d1 = """graph TD
    classDef eeg fill:#f96,stroke:#333,stroke-width:2px;
    classDef cal fill:#6cf,stroke:#333,stroke-width:2px;
    classDef game fill:#9f9,stroke:#333,stroke-width:2px;
    classDef main fill:#f9f,stroke:#333,stroke-width:2px;

    Main[Main.py]:::main --> GameApp[RedLightGreenLight/GameApp.py]:::main
    
    subgraph EEG_Backend [EEG Backend]
        EM[EEG/EEGManager.py]:::eeg
        SP[EEG/SignalProcessor.py]:::eeg
        RTP[EEG/RealTimeProcessor.py]:::eeg
    end

    subgraph Kalibrierung_Modul [Kalibrierungs-Modul]
        CA[Calibration/CalibrationApp.py]:::cal
        CM[Calibration/CalibrationModel.py]:::cal
        CC[Calibration/CalibrationController.py]:::cal
    end

    subgraph Spiel_Zustaende [Spiel-Zustände]
        GS[RedLightGreenLight/States/Game/GameState.py]:::game
        MS[RedLightGreenLight/States/Menu/MenuState.py]:::game
    end

    GameApp --> MS
    MS --> |Kalibrierung starten| CA
    MS --> |Spiel starten| GS
    
    RTP --> EM
    RTP --> SP
    CA --> CM
    CM --> SP"""

d2 = """sequenceDiagram
    participant Nutzer
    participant Controller as CalibrationController
    participant Model as CalibrationModel
    participant SP as SignalProcessor

    Nutzer->>Controller: Kalibrierung starten
    Controller->>Model: RELAXED-Phase starten
    Note over Nutzer, Model: 30s Datenerfassung (Relaxed)
    Nutzer->>Model: EEG Daten
    Controller->>Model: CONCENTRATED-Phase starten
    Note over Nutzer, Model: 30s Datenerfassung (Mathe-Aufgabe)
    Nutzer->>Model: EEG Daten
    
    Controller->>Model: calculate_calibration_results(SP)
    Model->>SP: calculate_ratios(relaxed_data)
    SP-->>Model: avg_rel_ratios
    Model->>SP: calculate_ratios(concentrated_data)
    SP-->>Model: avg_con_ratios
    
    Note over Model: Schwellenwert = (avg_rel + avg_con) / 2
    Note over Model: Richtung = 1 falls con > rel, sonst -1
    
    Model-->>Controller: Ergebnisse bereit
    Controller->>Nutzer: Ergebnisse anzeigen"""

d3 = """graph LR
    classDef hardware fill:#ccc,stroke:#333,stroke-dasharray: 5 5;
    classDef loop fill:#f96,stroke:#333,stroke-width:2px;
    classDef input fill:#9f9,stroke:#333,stroke-width:2px;

    subgraph EEG_Hardware [EEG Hardware / Mock]
        Data[(EEG Stream)]:::hardware
    end

    subgraph Verarbeitungs_Schleife [Echtzeit-Schleife]
        Manager[EEGManager]:::loop
        Buffer[Sliding Window Buffer]:::loop
        SP[SignalProcessor]:::loop
        Logic[Hystereselogik]:::loop
    end

    subgraph Spiel_Input [Spiel-Input]
        Queue[Command Queue]:::input
        SpaceKey[Simulierte LEERTASTE]:::input
    end

    Data --> Manager
    Manager --> Buffer
    Buffer --> |1s Fenster| SP
    SP --> |Beta/Alpha Verhältnis| Logic
    Logic --> |Dual-Channel Agreement| Queue
    Queue --> SpaceKey"""

content = f"""# Projektstruktur & EEG-Logik

Dieses Dokument bietet einen detaillierten Überblick über die Architektur des Projekts, insbesondere über das Zusammenspiel der Brain-Computer Interface (BCI) Komponenten mit dem Spiel.

## 1. High-Level Architektur

Das Projekt ist in drei Hauptkomponenten unterteilt: das **EEG-Backend**, das **Kalibrierungs-Modul** und die **Spiel-Zustände**.

![High-Level Architektur](https://mermaid.ink/svg/{encode(d1)})

---

## 2. Kalibrierungs-Logik

Der Kalibrierungsprozess ist entscheidend für die Bestimmung der individuellen Beta/Alpha-Verhältnis-Schwellenwerte. Er besteht aus zwei 30-sekündigen Phasen: **Relaxed** (Entspannt) und **Concentrated** (Konzentriert - Durchführung von Mathe-Aufgaben).

### Ablaufdiagramm der Kalibrierung

![Kalibrierungs-Ablauf](https://mermaid.ink/svg/{encode(d2)})

---

## 3. Echtzeit-Steuerungslogik (BCI)

Während das Spiel läuft, wird der `RealTimeProcessor` in einem separaten Prozess ausgeführt, um EEG-Daten zu erfassen und in Spielbefehle (Drücken/Loslassen der LEERTASTE) zu übersetzen.

### Diagramm der Steuerungs-Pipeline

![Steuerungs-Pipeline](https://mermaid.ink/svg/{encode(d3)})

### Detaillierte Verarbeitungsschritte:
1.  **Datenerfassung**: `EEGManager` ruft Samples mit 250Hz ab.
2.  **Sliding Window**: Ein 1-Sekunden-Puffer (250 Samples) wird kontinuierlich aktualisiert.
3.  **Signalverarbeitung**:
    - **Filterung**: Kausale `lfilter` (Butterworth 3. Ordnung) wird für die Alpha- (8-12Hz) und Beta-Bänder (13-30Hz) angewendet.
    - **FFT**: Die Spektralleistung wird über die FFT-Magnitudensummierung berechnet.
    - **Verhältnis**: Das Beta/Alpha-Verhältnis wird für Kanal 1 (Frontal) und Kanal 8 (Okzipital) berechnet.
4.  **Hystereselogik**:
    - Um **BEWEGUNG** auszulösen: Beide Kanäle müssen ihren jeweiligen `Schwellenwert + Margin` überschreiten.
    - Um **STILLSTAND** auszulösen: Mindestens ein Kanal muss unter `Schwellenwert - Margin` fallen.
5.  **Befehlsausführung**: Befehle werden über eine `multiprocessing.Queue` an die Haupt-`GameApp` gesendet, die den Tastaturbefehl simuliert.

---

## 4. Überblick der Ordnerstruktur

- **`EEG/`**: Kernlogik für die Signalverarbeitung und das Echtzeit-Multiprocessing.
- **`Calibration/`**: MVC-Implementierung für die EEG-Kalibrierungs-Sub-Anwendung.
- **`RedLightGreenLight/`**: Die Hauptanwendung des Spiels, die State Machine und Assets.
- **`UIUtils/`**: Wiederverwendbare Pygame GUI-Komponenten.
- **`TestData/`**: Testdaten für die Entwicklung ohne EEG-Hardware.
- **`Tests/`**: Automatisierte Skripte zur Verifizierung der Signalverarbeitung und Echtzeitlogik.
- **`Main.py`**: Der Einstiegspunkt, der das Spiel und den BCI-Hintergrundprozess steuert.
"""

with open('ProjectStructure.md', 'w', encoding='utf-8') as f:
    f.write(content)
print("ProjectStructure.md successfully updated in German with SVG links.")
