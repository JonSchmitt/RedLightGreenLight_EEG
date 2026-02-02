"""
Main Module for the Red Light Green Light Game Project.
Contains the entry point for the application.
"""
import pygame
from RedLightGreenLight.GameApp import GameApp
from Calibration.CalibrationApp import CalibrationApp


class Main:
    """
    Main class for application entry.
    Runs EEG Calibration first, then starts GameApp.
    """
    def __init__(self):
        self._alpha_threshold = 1.0
        self._beta_threshold = 1.0

    def main(self):
        """
        Entry point of the application.
        1. Runs Calibration.
        2. Initializes and starts the GameApp with calibration results.
        """
        # 1. Calibration
        print("Starting EEG Calibration...")
        calibration = CalibrationApp()
        self._alpha_threshold, self._beta_threshold = calibration.run()
        
        # 2. Game Start
        print(f"Starting Game with Thresholds: Alpha={self._alpha_threshold}, Beta={self._beta_threshold}")
        game = GameApp()
        # Optionally pass thresholds to game.run if it supports it, 
        # or store them in a shared configuration.
        game.run()


if __name__ == "__main__":
    main_app = Main()
    main_app.main()
