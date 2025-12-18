# RedLightGreenLight EEG Project

Dieses Projekt ist eine Implementierung des Spiels "Red Light, Green Light" unter Verwendung von Pygame, entworfen für BCI (Brain-Computer Interface) Anwendungen im EEG-Kontext.

## Installation & Ausführung

1.  **Voraussetzungen installieren:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Spiel starten:**
    ```bash
    python Main.py
    ```

## Projektstruktur & Design Patterns

Das Projekt folgt einer klaren Struktur unter Verwendung bewährter Software-Design-Patterns, um Wartbarkeit und Erweiterbarkeit zu gewährleisten.

### Verwendete Patterns

*   **State Pattern**: Das Herzstück der Anwendung. `GameState`, `MenuState`, `SettingsState` und `QuitState` erben von einer abstrakten Basisklasse `State`. Jeder Zustand verwaltet sein eigenes Verhalten und Übergänge.
*   **Factory Pattern**: `StateFactory` wird verwendet, um Instanzen der verschiedenen States zu erzeugen und wiederzuverwenden (Lazy Initialization).
*   **Model-View-Controller (MVC)**: Die States (z.B. Menu, Game) sind intern in Model (Daten), View (Anzeige) und Controller (Logik) unterteilt.
*   **Observer Pattern**: Das `SettingsModel` fungiert als Subject. States registrieren sich als Observer, um bei Einstellungsänderungen (z.B. Auflösung, Sound) sofort reagieren zu können.
*   **Singleton (Konzept)**: `MusicManager` und Manager-Klassen werden einmalig initialisiert und durchgereicht.

### Architektur-Diagramm (Übersicht)

Das folgende Diagramm zeigt die Initialisierung und die Verwaltung der Zustände durch die zentrale `GameApp`.

![Architecture Overview](https://mermaid.ink/svg/Zmxvd2NoYXJ0IFRECiAgICBjbGFzc0RlZiBhcHAgZmlsbDojZjlmLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHg7CiAgICBjbGFzc0RlZiBmYWN0b3J5IGZpbGw6I2ZmZCxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4OwogICAgY2xhc3NEZWYgc3RhdGUgZmlsbDojYmRmLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHg7CgogICAgTWFpbltNYWluLnB5XSAtLS0tPnxjcmVhdGVzIGFuZCBydW5zfCBBcHBbR2FtZUFwcF06OjphcHAKICAgIEFwcCAtLS0tPnxtYW5hZ2VzfCBDdXJyZW50U3RhdGVbQ3VycmVudCBTdGF0ZV06OjpzdGF0ZQogICAgCiAgICBBcHAgLS4uLi0+fHVzZXN8IEZhY3RvcnlbU3RhdGVGYWN0b3J5XTo6OmZhY3RvcnkKICAgIAogICAgc3ViZ3JhcGggU3RhdGVzIFtBdmFpbGFibGUgU3RhdGVzXQogICAgICAgIGRpcmVjdGlvbiBMUgogICAgICAgIE1lbnVbTWVudVN0YXRlXTo6OnN0YXRlCiAgICAgICAgU2V0dGluZ3NbU2V0dGluZ3NTdGF0ZV06OjpzdGF0ZQogICAgICAgIEdhbWVbR2FtZVN0YXRlXTo6OnN0YXRlCiAgICAgICAgUXVpdFtRdWl0U3RhdGVdOjo6c3RhdGUKICAgIGVuZAogICAgCiAgICBGYWN0b3J5IC0uLi4tPnxpbnN0YW50aWF0ZXN8IE1lbnUKICAgIEZhY3RvcnkgLS4uLi0+fGluc3RhbnRpYXRlc3wgU2V0dGluZ3MKICAgIEZhY3RvcnkgLS4uLi0+fGluc3RhbnRpYXRlc3wgR2FtZQogICAgRmFjdG9yeSAtLi4uLT58aW5zdGFudGlhdGVzfCBRdWl0)




#### Zustandsübergangs-Lifecycle
Der Lebenszyklus der Anwendung wird durch die `GameApp` gesteuert. Ein wesentlicher Aspekt ist die delegierte Entscheidungsfindung:
1.  **Update**: Die `GameApp` ruft in jedem Frame die `update()` Methode des aktuellen `State` auf.
2.  **Delegation**: Der `State` delegiert die Logik an seinen internen `Controller`.
3.  **Transition**: Wenn ein Zustandswechsel nötig ist (z.B. Klick auf "Start"), entscheidet der `Controller` über den nächsten Zustand und lässt diesen über die `StateFactory` erzeugen.
4.  **Rückgabe**: Der Controller gibt den neuen Zustand an den `State` zurück, welcher diesen wiederum an die `GameApp` liefert. Die `GameApp` setzt diesen dann als aktuellen Zustand für den nächsten Frame.


### Architektur-Details (Hierarchisches MVC)

Das Projekt nutzt eine verschachtelte **Model-View-Controller (MVC)** Struktur. Nicht nur die Haupt-Zustände, sondern auch untergeordnete Systeme wie die Spielphasen und Entities folgen konsequent diesem Muster.

![MVC Details](https://mermaid.ink/svg/Zmxvd2NoYXJ0IFRECiAgICBjbGFzc0RlZiBhcHAgZmlsbDojZjlmLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHg7CiAgICBjbGFzc0RlZiBmYWN0b3J5IGZpbGw6I2ZmZCxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4OwogICAgY2xhc3NEZWYgc3RhdGUgZmlsbDojYmRmLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHg7CiAgICBjbGFzc0RlZiBjb250cm9sbGVyIGZpbGw6I2JiZixzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4OwogICAgY2xhc3NEZWYgbW9kZWwgZmlsbDojZGZkLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHg7CiAgICBjbGFzc0RlZiB2aWV3IGZpbGw6I2ZkZCxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4OwoKICAgIEFwcFtHYW1lQXBwXTo6OmFwcAogICAgRmFjdG9yeVtTdGF0ZUZhY3RvcnldOjo6ZmFjdG9yeQoKICAgIHN1YmdyYXBoIEdMT0JBTF9GTE9XIFtHbG9iYWwgU3RhdGUgTWFuYWdlbWVudCBMaWZlY3ljbGVdCiAgICAgICAgZGlyZWN0aW9uIFRCCiAgICAgICAgU1tDdXJyZW50IFN0YXRlXTo6OnN0YXRlCiAgICAgICAgQ1tDb250cm9sbGVyXTo6OmNvbnRyb2xsZXIKICAgICAgICBNW01vZGVsXTo6Om1vZGVsCiAgICAgICAgVltWaWV3XTo6OnZpZXcKICAgICAgICAKICAgICAgICBTIC0tLSBDCiAgICAgICAgQyAtLT58dXBkYXRlc3wgTQogICAgICAgIEMgLS0+fHVwZGF0ZXN8IFYKICAgIGVuZAoKICAgIEFwcCAtLS0tPnwxLiB1cGRhdGV8IFMKICAgIEMgLS4tPnwyLiBnZXQgbmV4dCBzdGF0ZXwgRmFjdG9yeQogICAgRmFjdG9yeSAtLi0+fDMuIGNyZWF0ZSBpbnN0YW5jZXwgTmV3U1tOZXh0IFN0YXRlXTo6OnN0YXRlCiAgICBDIC0uLT58NC4gcmV0dXJufCBOZXdTCiAgICBTIC0uLT58NS4gcmV0dXJufCBOZXdTCiAgICBBcHAgLS0tLT58Ni4gc2V0IGN1cnJlbnR8IE5ld1MKCiAgICBzdWJncmFwaCBHQU1FX1VOSVQgW0dhbWVTdGF0ZSBJbnRlcm5hbCBBcmNoaXRlY3R1cmVdCiAgICAgICAgZGlyZWN0aW9uIFRCCiAgICAgICAgR0NbR2FtZUNvbnRyb2xsZXJdOjo6Y29udHJvbGxlcgogICAgICAgIEdNW0dhbWVNb2RlbF06Ojptb2RlbAogICAgICAgIAogICAgICAgIHN1YmdyYXBoIFBIQVNFX01WQyBbR2FtZSBQaGFzZSBNVkMgQ2x1c3Rlcl0KICAgICAgICAgICAgZGlyZWN0aW9uIExSCiAgICAgICAgICAgIFBTW1BoYXNlIFN0YXRlXTo6OnN0YXRlCiAgICAgICAgICAgIFBDW1BoYXNlIENvbnRyb2xsZXJdOjo6Y29udHJvbGxlcgogICAgICAgICAgICBQTVtQaGFzZSBNb2RlbF06Ojptb2RlbAogICAgICAgICAgICBQVltQaGFzZSBWaWV3XTo6OnZpZXcKICAgICAgICAgICAgUFMgLS0tIFBDCiAgICAgICAgICAgIFBDIC0tPiBQTQogICAgICAgICAgICBQQyAtLT4gUFYKICAgICAgICBlbmQKCiAgICAgICAgc3ViZ3JhcGggRU5USVRZX01WQyBbRW50aXR5IE1WQyBDbHVzdGVyXQogICAgICAgICAgICBkaXJlY3Rpb24gTFIKICAgICAgICAgICAgRVNNW0VudGl0eVN0YXRlTWFjaGluZV06OjpzdGF0ZQogICAgICAgICAgICBFTVtFbnRpdHkgTW9kZWxdOjo6bW9kZWwKICAgICAgICAgICAgRVZbRW50aXR5IFZpZXddOjo6dmlldwogICAgICAgICAgICBFU00gLS0tIEVNCiAgICAgICAgICAgIEVTTSAtLS0gRVYKICAgICAgICBlbmQKICAgIGVuZAoKICAgIEMgPT09PT58aWYgR2FtZVN0YXRlfCBHQwogICAgR0MgLS0tLT58ZGVsZWdhdGVzIHVwZGF0ZXwgUFMKICAgIEdDIC0tLS0+fHVwZGF0ZXMgbGlzdHwgRVNNCiAgICBHTSAtLS0tPnxzdG9yZXMgZGF0YXwgUFMKICAgIEdNIC0tLS0+fHN0b3JlcyBlbnRpdGllc3wgRVNNCgogICAgUFMgLS0tLT58d3JpdGVzIHJ1bGVzIHRvfCBHTQoKICAgIGxpbmtTdHlsZSBkZWZhdWx0IHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoxcHg7)


#### Hierarchisches MVC
Innerhalb des `GameState` gibt es zwei Sub-Systeme, die ebenfalls dem MVC-Prinzip folgen:
*   **GamePhaseStates**: Repräsentieren die aktuelle Spielphase (z.B. Green Light, Red Light). Jede Phase hat ihre eigene Logik (Controller), Daten (Model) und Anzeige (View). Der `GameController` entscheidet anhand des Spielverlaufs, welche Phase aktuell aktiv ist und ruft deren `update()` auf.
*   **Entities**: Jeder Spieler oder NPC wird durch eine `EntityStateMachine` repräsentiert. Diese Maschinen sind in einer Liste im `GameModel` gespeichert. Der `GameController` iteriert über diese Liste und führt für jede Entity ein Update durch.

### Interaktion und Datenfluss (Blackboard Pattern)

Dieses Diagramm verdeutlicht die zentrale Rolle des `GameModel` als "Blackboard" bzw. gemeinsamer Datenspeicher.

![Blackboard Interaction](https://mermaid.ink/svg/Zmxvd2NoYXJ0IExSCiAgICBjbGFzc0RlZiBtb2RlbCBmaWxsOiNkZmQsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweDsKICAgIGNsYXNzRGVmIGNvbnRyb2xsZXIgZmlsbDojYmJmLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHg7CiAgICBjbGFzc0RlZiBhY3RvciBmaWxsOiNmZGQsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweDsKCiAgICBzdWJncmFwaCBXUklURVJTIFtXcml0ZXJzXQogICAgICAgIGRpcmVjdGlvbiBUQgogICAgICAgIEdQU1tHYW1lUGhhc2VTdGF0ZXNdOjo6Y29udHJvbGxlcgogICAgZW5kCgogICAgTW9kZWxbKEdhbWVNb2RlbCldOjo6bW9kZWwKCiAgICBzdWJncmFwaCBSRUFERVJTIFtSZWFkZXJzXQogICAgICAgIGRpcmVjdGlvbiBUQgogICAgICAgIEVTTVtFbnRpdHlTdGF0ZU1hY2hpbmVdOjo6YWN0b3IKICAgICAgICBQaGFzZVtDdXJyZW50IFBoYXNlIExvZ2ljXTo6OmFjdG9yCiAgICBlbmQKCiAgICBHUFMgLS0tLT58d3JpdGVzIHJ1bGVzIGFuZCBlbnVtc3wgTW9kZWwKICAgIAogICAgTW9kZWwgLS4tPnxyZWFkcyBzdGF0dXN8IEVTTQogICAgTW9kZWwgLS4tPnxyZWFkcyBydWxlc3wgUGhhc2UKCiAgICBsaW5rU3R5bGUgZGVmYXVsdCBzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MXB4Ow==)




#### Funktionsweise des Blackboard Patterns
Das Projekt verwendet das **Blackboard Pattern**, um die Kommunikation zwischen den verschiedenen Steuerungseinheiten (Controllern) und den Akteuren (Entities/Phasen) zu entkoppeln:
*   **Writers**: Die `GamePhaseStates` schreiben phasen-spezifische Informationen in das `GameModel` (z.B. aktuelle Zeit, Phasen-Enum, Regeln wie "Darf ich mich bewegen?").
*   Der **GameController** delegiert das Update an die Phasen und steuert die übergeordnete Entity-Liste.
*   Die **EntityStateMachines** lesen diesen Status autonom bei jedem Update aus dem Model.
*   Dies ermöglicht eine saubere Trennung zwischen Welt-Logik und individueller Actor-Logik (Akteure müssen den globalen Controller nicht kennen).

## State Machine (FSM)

Der folgende Graph zeigt die Zustandsübergänge der Anwendung (Finite State Machine).


### State Machine Diagram (High-Level)

Dieser Graph zeigt die Übergänge zwischen den Haupt-Zuständen der Anwendung. Die `GameApp` sorgt dafür, dass immer genau ein Zustand aktiv ist.

![High Level FSM](https://mermaid.ink/svg/Zmxvd2NoYXJ0IExSCiAgICBjbGFzc0RlZiBzdGF0ZSBmaWxsOiNiZGYsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweDsKICAgIGNsYXNzRGVmIHRlcm1pbmFsIGZpbGw6I2VlZSxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4LHN0cm9rZS1kYXNoYXJyYXk6IDUgNTsKCiAgICBTdGFydCgoU3RhcnQpKSAtLS0tPiBNZW51W01lbnVTdGF0ZV06OjpzdGF0ZQogICAgCiAgICBNZW51IC0tLS0+fFN0YXJ0fCBHYW1lW0dhbWVTdGF0ZV06OjpzdGF0ZQogICAgTWVudSAtLS0tPnxTZXR0aW5nc3wgU2V0dGluZ3NbU2V0dGluZ3NTdGF0ZV06OjpzdGF0ZQogICAgTWVudSAtLS0tPnxRdWl0fCBRdWl0W1F1aXRTdGF0ZV06Ojp0ZXJtaW5hbAogICAgCiAgICBTZXR0aW5ncyAtLS0tPnxCYWNrfCBNZW51CiAgICBTZXR0aW5ncyAtLS0tPnxRdWl0fCBRdWl0CiAgICAKICAgIEdhbWUgLS0tLT58UGF1c2V8IE1lbnUKICAgIEdhbWUgLS0tLT58RXhpdHwgUXVpdAogICAgCiAgICBRdWl0IC0tLS0+IEV4aXQoKEV4aXQpKQoKICAgIGxpbmtTdHlsZSBkZWZhdWx0IHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoxcHg7)




### Game Phases (Sub-FSM in GameState)

Innerhalb des `GameState` existiert ein eigenständiger Automat für den Spielablauf. Bemerkenswert ist, dass der Übergang von `GameOver` zu `Restart` ohne Nutzereingabe nach einem Timer erfolgt, um einen flüssigen Spielablauf für BCI-Experimente zu gewährleisten.

![Game Phases FSM](https://mermaid.ink/svg/Zmxvd2NoYXJ0IFRECiAgICBjbGFzc0RlZiBzdGF0ZSBmaWxsOiNiZGYsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweDsKICAgIGNsYXNzRGVmIGdyZWVuIGZpbGw6I2RmZCxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4OwogICAgY2xhc3NEZWYgcmVkIGZpbGw6I2ZkZCxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4OwogICAgY2xhc3NEZWYgYWxlcnQgZmlsbDojZjlmLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHg7CgogICAgU3RhcnQoKFN0YXJ0KSkgLS0tLT4gR3JlZW5bR3JlZW5MaWdodFN0YXRlXTo6OmdyZWVuCiAgICAKICAgIEdyZWVuIC0tLS0+fFRpbWVyfCBSZWRbUmVkTGlnaHRTdGF0ZV06OjpyZWQKICAgIFJlZCAtLS0tPnxUaW1lcnwgR3JlZW4KICAgIAogICAgUmVkIC0tLS0+fEFsbCBwbGF5ZXJzIGRlYWR8IEdhbWVPdmVyW0dhbWVPdmVyU3RhdGVdOjo6YWxlcnQKICAgIAogICAgR2FtZU92ZXIgLS0tLT58QXV0b21hdGljIHRpbWVyfCBSZXN0YXJ0W1Jlc3RhcnRTdGF0ZV06OjpzdGF0ZQogICAgUmVzdGFydCAtLS0tPnxSZXNldCBkb25lfCBHcmVlbgoKICAgIGxpbmtTdHlsZSBkZWZhdWx0IHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoxcHg7)


### Entity State Machine (Player Behavior)

Dieser Automat beschreibt das Verhalten einer einzelnen Spielfigur. Die "Todes-Logik" ist hierbei eng mit dem `GameModel` verknüpft: Wenn das Model signalisiert, dass der aktuelle Phasen-Regelsatz Bewegung verbietet, führt jede Input-Aktion zum sofortigen Wechsel in den `Dead`-Status.

![Entity FSM](https://mermaid.ink/svg/Zmxvd2NoYXJ0IExSCiAgICBjbGFzc0RlZiBzdGF0ZSBmaWxsOiNiZGYsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweDsKICAgIGNsYXNzRGVmIGRhbmdlciBmaWxsOiNmZGQsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweDsKCiAgICBJZGxlW0lkbGVTdGF0ZV06OjpzdGF0ZSAtLS0tPnxNb3ZlbWVudCBhbGxvd2VkfCBXYWxraW5nW1dhbGtpbmdTdGF0ZV06OjpzdGF0ZQogICAgV2Fsa2luZyAtLS0tPnxSZWxlYXNlIGlucHV0fCBJZGxlCiAgICAKICAgIFdhbGtpbmcgLS0tLT58TW92ZWQgZHVyaW5nIFJlZHwgRGVhZFtEZWFkRW50aXR5U3RhdGVdOjo6ZGFuZ2VyCiAgICBJZGxlIC0tLS0+fElucHV0IGR1cmluZyBSZWR8IERlYWQKICAgIAogICAgRGVhZCAtLS0tPnxHYW1lIHJlc3RhcnR8IElkbGUKCiAgICBsaW5rU3R5bGUgZGVmYXVsdCBzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MXB4Ow==)



## Analyse der Implementierung

### Hierarchischer Zustandsautomat (HSM)
Die Anwendung implementiert das Konzept eines **Hierarchischen Zustandsautomaten (Hierarchical State Machine)** durch Komposition und Delegation:

1.  **Level 1 (App)**: `GameApp` verwaltet die High-Level-Zustände (`Menu`, `Game`, `Settings`).
2.  **Level 2 (Game Phases)**: Innerhalb von `GameState` existiert ein Sub-Automat für die Spielphasen (`RedLight`, `GreenLight`, `GameOver`). Dieser wird explizit vom `GameController` gesteuert, der die zeitliche Abfolge und Sieg/Niederlage-Bedingungen prüft.
3.  **Level 2 (Entities)**: Jede Entity besitzt einen eigenen inneren Zustand (`Idle`, `Walking`, `Dead`), der durch die `EntityStateMachine` verwaltet wird.

### Kommunikation via Blackboard
Das `GameModel` fungiert als **Shared State Blackboard**:
*   Die aktiven **GamePhaseStates** schreiben globale Spielparameter (z.B. `is_movement_kills_player`) in das Model.
*   Der **GameController** delegiert das Update an die Phasen und steuert die übergeordnete Entity-Liste.
*   Die **EntityStateMachines** lesen diesen Status autonom bei jedem Update aus dem Model.
*   Dies ermöglicht eine saubere Trennung zwischen Welt-Logik und individueller Actor-Logik (Akteure müssen den globalen Controller nicht kennen).

## Dateistruktur (Auszug)

- `Main.py`: Einstiegspunkt.
- `RedLightGreenLight/`: Hauptpaket.
    - `GameApp.py`: Hauptschleife und Manager-Initialisierung.
    - `States/`: Enthält alle State-Implementierungen.
        - `State.py`: Basisklasse.
        - `StateFactory.py`: Erzeugung der States.
        - `Menu/`: MVC für das Menü.
        - `Game/`: MVC für das Spiel.
        - `SettingsSubMenu/`: MVC für Einstellungen.
