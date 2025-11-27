import pygame
import pygame_gui
import os


class UIManager(pygame_gui.UIManager):

    def __init__(self, screen: pygame.Surface):
        # 1. Ohne Theme initialisieren
        super().__init__(screen.get_size(), theme_path=None)

        # 2. Font-Pfade registrieren
        font_path = os.path.abspath("RedLightGreenLight/Resources/Fonts/PressStart2P-Regular.ttf")
        self.add_font_paths('PS2P', font_path)

        # 3. Jetzt Theme laden
        self.get_theme().load_theme("RedLightGreenLight/Resources/CustomTheme.json")