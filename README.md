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

*   **[Project Structure & EEG Logic](ProjectStructure.md)**: Explains the internal architecture, signal processing pipeline, and how the BCI control works with Mermaid diagrams.
*   **[Game Details & Design Patterns](GameDetails.md)**: Details focusing on the game implementation, MVC structure, and used design patterns.

## Features

*   **Real-time EEG Processing**: Translates brain activity into game movement.
*   **Interactive Calibration**: Personalized thresholding based on relaxed and concentrated states.
*   **Dual-Channel Agreement**: High-reliability control using both Frontal and Occipital brain regions.
*   **Mack Mode**: Includes built-in support for testing without EEG hardware.

## Troubleshooting & Fine-Tuning

If the BCI control feels unresponsive or unstable during live testing, you can adjust the following parameters in the code:

### 1. Adjusting Sensitivity (Margins)
If the state switches too rapidly (flickering) or not at all (too hard).
- **File**: `Calibration/CalibrationModel.py`
- **Parameter**: `self._margin_1` and `self._margin_8`
- **Action**:
    - **Too nervous?** Increase factor (e.g., `* 0.2` or `* 0.3`).
    - **Too unresponsive?** Decrease factor (e.g., `* 0.05`).

### 2. Smoothing (Window Size)
Controls how much past data influences the current decision.
- **File**: `EEG/RealTimeProcessor.py`
- **Parameter**: `self._window_size`
- **Action**:
    - **Too slow?** Reduce to `int(sampling_rate * 0.5)` (0.5s).
    - **Too noisy?** Increase to `sampling_rate * 2` (2s).

### 3. Frequency Bands
Adjust if muscle artifacts or individual differences affect detection.
- **File**: `EEG/SignalProcessor.py`
- **Parameter**: `self._alpha_band`, `self._beta_band`
- **Action**: Shift ranges (e.g., Alpha `7-13`, Beta `15-30`) to avoid noise.

### 4. Threshold Difficulty
- **File**: `Calibration/CalibrationModel.py`
- **Parameter**: `self._threshold_1` calculation.
- **Action**: Use a weighted average instead of `(rel + con) / 2` to make it easier/harder to reach the concentrated state.
