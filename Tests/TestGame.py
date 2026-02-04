import os
import sys
import pygame

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RedLightGreenLight.GameApp import GameApp

if __name__ == "__main__":
    game = GameApp()
    game.run()
    pygame.quit()