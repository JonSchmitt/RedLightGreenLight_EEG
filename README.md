# RedLightGreenLight EEG Project

Welcome to the RedLightGreenLight EEG project. This application uses Brain-Computer Interface (BCI) technology to control a "Red Light, Green Light" game using EEG signals.

## Quick Start

1.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    ```bash
    python Main.py
    ```

## Documentation

For a detailed understanding of the project, please refer to the following documents:

*   **[ProjectStructure (Logik & Diagramme)](ProjectStructure.md)**: Erklärt die interne Architektur, die Signalverarbeitungspipeline und die BCI-Steuerung mit detaillierten **SVG-Diagrammen**.
*   **[Game Details & Design Patterns](GameDetails.md)**: Details focusing on the game implementation, MVC structure, and used design patterns.

## Features

*   **Real-time EEG Processing**: Translates brain activity into game movement using specialized spectral analysis.
*   **Interactive Calibration**: Personalized thresholding based on relaxed and concentrated states.
*   **Cross-Region Ratio Analysis**: Uses the ratio between Frontal Beta (Ch1) and Occipital Alpha (Ch8) for high-reliability focus detection.
*   **Time-based Debounce**: Prevents accidental movement triggers using continuous state verification.
*   **Mock Mode**: Includes built-in support for testing without EEG hardware.

## Troubleshooting & Fine-Tuning

If the BCI control feels unresponsive or unstable, you can adjust these core parameters:

### 1. Adjusting Sensitivity
If it's too hard or too easy to reach the "Concentrated" state.
- **File**: `Calibration/CalibrationModel.py`
- **Parameter**: `self._sensitivity` (Default: `0.7`)
- **Action**:
    - **Too hard?** Decrease (e.g., `0.5` or `0.6`).
    - **Too easy?** Increase (e.g., `0.8`).

### 2. Stability (Debounce Duration)
Controls how long a state must be held continuously to trigger a change.
- **File**: `EEG/RealTimeProcessor.py`
- **Parameter**: `self._duration_threshold` (Default: `0.5` seconds)
- **Action**:
    - **Flickering state?** Increase to `0.7` or `1.0`.
    - **Laggy response?** Decrease to `0.3` (Warning: may increase false positives).

### 3. Hysteresis Margin
The "buffer zone" around the threshold to prevent rapid switching.
- **File**: `Calibration/CalibrationModel.py`
- **Parameter**: `self._margin_ratio` calculation factor (Default: `0.2`)
- **Action**:
    - **Unstable switching?** Increase factor (e.g., `0.3`).

### 4. Frequency Bands
Adjust if individual differences affect detection.
- **File**: `EEG/SignalProcessor.py`
- **Parameter**: `self._alpha_band`, `self._beta_band`
- **Action**: Shift ranges (e.g., Alpha `7-13`, Beta `15-30`) to avoid noise.
