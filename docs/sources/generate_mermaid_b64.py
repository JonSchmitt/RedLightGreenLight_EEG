import base64

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

    subgraph Calibration_Module [Calibration Module]
        CA[Calibration/CalibrationApp.py]:::cal
        CM[Calibration/CalibrationModel.py]:::cal
        CC[Calibration/CalibrationController.py]:::cal
    end

    subgraph Game_States [Game States]
        GS[RedLightGreenLight/States/Game/GameState.py]:::game
        MS[RedLightGreenLight/States/Menu/MenuState.py]:::game
    end

    GameApp --> MS
    MS --> |Start Calibration| CA
    MS --> |Start Game| GS
    
    RTP --> EM
    RTP --> SP
    CA --> CM
    CM --> SP"""

d2 = """sequenceDiagram
    participant User
    participant Controller as CalibrationController
    participant Model as CalibrationModel
    participant SP as SignalProcessor

    User->>Controller: Start Calibration
    Controller->>Model: Start RELAXED phase
    Note over User, Model: 30s Data Collection (Relaxed)
    User->>Model: EEG Data
    Controller->>Model: Start CONCENTRATED phase
    Note over User, Model: 30s Data Collection (Math Task)
    User->>Model: EEG Data
    
    Controller->>Model: calculate_calibration_results(SP)
    Model->>SP: calculate_ratios(relaxed_data)
    SP-->>Model: avg_rel_ratios
    Model->>SP: calculate_ratios(concentrated_data)
    SP-->>Model: avg_con_ratios
    
    Note over Model: Threshold = (avg_rel + avg_con) / 2
    Note over Model: Direction = 1 if con > rel else -1
    
    Model-->>Controller: Results Ready
    Controller->>User: Show Results"""

d3 = """graph LR
    classDef hardware fill:#ccc,stroke:#333,stroke-dasharray: 5 5;
    classDef loop fill:#f96,stroke:#333,stroke-width:2px;
    classDef input fill:#9f9,stroke:#333,stroke-width:2px;

    subgraph EEG_Hardware [EEG Hardware / Mock]
        Data[(EEG Stream)]:::hardware
    end

    subgraph Processing_Loop [Real-Time Loop]
        Manager[EEGManager]:::loop
        Buffer[Sliding Window Buffer]:::loop
        SP[SignalProcessor]:::loop
        Logic[Hysteresis Logic]:::loop
    end

    subgraph Game_Input [Game Input]
        Queue[Command Queue]:::input
        SpaceKey[Simulated SPACE Key]:::input
    end

    Data --> Manager
    Manager --> Buffer
    Buffer --> |1s Window| SP
    SP --> |Beta/Alpha Ratio| Logic
    Logic --> |Dual-Channel Agreement| Queue
    Queue --> SpaceKey"""

def encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')

print(f"D1: {encode(d1)}")
print(f"D2: {encode(d2)}")
print(f"D3: {encode(d3)}")
