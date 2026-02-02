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
    """
    def __init__(self):
        # Pygame might be initialized already if called from Main.py
        if not pygame.get_init():
            pygame.init()
            
        # Create a fullscreen window
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("EEG Calibration")
        
        self._model = CalibrationModel()
        self._view = CalibrationView(self._screen, self._model)
        self._controller = CalibrationController(self._model, self._view)

    def run(self):
        self._controller.run()
        
        # Retrieve results before closing
        alpha = self._model.alpha_ratio
        beta = self._model.beta_ratio
        
        print(f"Calibration Results -> Alpha: {alpha}, Beta: {beta}")
        
        # Return results to caller
        return alpha, beta

if __name__ == "__main__":
    app = CalibrationApp()
    app.run()
    pygame.quit()
