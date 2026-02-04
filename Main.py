"""
Main Module for the Red Light Green Light Game Project.
Contains the entry point for the application.
"""
import pygame
from multiprocessing import Queue
from RedLightGreenLight.GameApp import GameApp
from Calibration.CalibrationApp import CalibrationApp
from EEG.RealTimeProcessor import RealTimeProcessor


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
        th1, dir1, m1, th8, dir8, m8 = calibration.run()

        # 2. Setup Real-Time BCI
        command_queue = Queue()
        bci_process = RealTimeProcessor(th1, dir1, m1, th8, dir8, m8, command_queue)
        bci_process.start()

        # 3. Game Start
        try:
            print(f"Starting Game with thresholds: {th1:.4f} and {th8:.4f}")
            game = GameApp()
            game.run(command_queue)
        finally:
            bci_process.stop()
            bci_process.join(timeout=1.0)
            pygame.quit()


if __name__ == "__main__":
    main_app = Main()
    main_app.main()
