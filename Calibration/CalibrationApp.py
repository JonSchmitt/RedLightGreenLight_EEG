import pygame
import os
import sys

# Add root directory to path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Calibration.CalibrationModel import CalibrationModel
from Calibration.CalibrationView import CalibrationView
from Calibration.CalibrationController import CalibrationController

class CalibrationApp:
    """
    Main entry point for the standalone Calibration Application.
    Coordinates the calibration process and returns the calculated thresholds.
    """

    def __init__(self, screen=None):
        """
        Initializes the Calibration Application.
        
        Args:
            screen (pygame.Surface, optional): An existing pygame surface to use. 
                                              If None, a new fullscreen window is created.
        """
        self._model = CalibrationModel()
        self._view = CalibrationView(self._model, screen=screen)
        self._controller = CalibrationController(self._model, self._view)

    def run(self):
        """
        Starts the calibration loop and returns the results once finished.

        Returns:
            tuple: (threshold_1, dir_1, margin_1, threshold_8, dir_8, margin_8)
        """
        self._controller.run()


        m = self._model
        results = (m.threshold_ratio, m.margin_ratio)
        
        print(f"Calibration Results -> Ratio Threshold: {results[0]:.4f}, Margin: {results[1]:.4f}")

        return results

# FOR TESTING ONLY
if __name__ == "__main__":
    app = CalibrationApp()
    app.run()
    pygame.quit()
