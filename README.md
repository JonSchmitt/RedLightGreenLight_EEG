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
*   **Mock Mode**: Includes built-in support for testing without EEG hardware.
