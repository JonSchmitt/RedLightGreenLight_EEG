import pygame
import pygame_gui
from UIUtils.UIManager import UIManager
from RedLightGreenLight.States.Game.GamePhaseStates.WinState.WINSModel import WINSModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager

class WINSView:
    """
    View for Win state.
    Displays celebratory message.
    """
    def __init__(self, screen: pygame.Surface, model: WINSModel, settings_model: SettingsModel,
                 music_manager: MusicManager):
        self._screen = screen
        self._model = model
        self._settings = settings_model
        self._manager = UIManager(self._screen)
        self._music_manager = music_manager
        
        self._win_label = None
        self._initialize_ui()

    def _initialize_ui(self):
        screen_width = self._screen.get_width()
        screen_height = self._screen.get_height()
        label_width = 1000  # Significantly larger
        label_height = 300
        
        self._win_label = pygame_gui.elements.UILabel(
            pygame.Rect((screen_width // 2) - (label_width // 2), 
                        (screen_height // 2) - (label_height // 2), 
                        label_width, label_height),
            manager=self._manager,
            text="",
            object_id="#WinMessageLabel"
        )

    def show(self, delta_time: float) -> None:
        # Green background color (matches GreenLightState)
        self._screen.fill((0, 150, 0)) 
        
        self._win_label.set_text(f"{self._model.winner_name} won!")
        
        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)

    def get_screen(self):
        return self._screen
