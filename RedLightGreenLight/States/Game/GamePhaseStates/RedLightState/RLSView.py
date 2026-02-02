import pygame
import pygame_gui

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSModel import RLSModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from UIUtils.VBox import VBox
from UIUtils.UIManager import UIManager


class RLSView:
    """
    View for Red Light Phase.
    Background is red, displays timer.
    """
    def __init__(self, screen: pygame.Surface, model: RLSModel, settings_model: SettingsModel,
                 music_manager: MusicManager):
        self._screen = screen
        self._model = model
        self._settings = settings_model
        self._music_manager = music_manager
        self._time_label = None
        self._manager = UIManager(self._screen)

        self._initialize_ui()

    def get_screen(self):
        return self._screen

    def show(self, delta_time: float) -> None:
        self._screen.fill((150, 0, 0))
        self._update_labels()
        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)

    def _initialize_ui(self):
        pass
        #self._initialize_timer_box()

    def _initialize_timer_box(self):
        vBox_height = int(60 * self._settings.get_ui_scaling())
        vBox_width = int(75 * self._settings.get_ui_scaling())
        label_height = int(50 * self._settings.get_ui_scaling())
        label_width = int(50 * self._settings.get_ui_scaling())
        self._vbox = VBox(pygame.Rect(-vBox_width, 0, vBox_width, vBox_height), self._manager, spacing=10,
                          anchors={'top': 'top', 'right': 'right'})
        self._time_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, label_width, label_height),
                                                       manager=self._manager, text="T: " + str(
                round(self._model.get_remaining_time_in_phase())), container=self._vbox.get_panel())
        self._vbox.add_element(self._time_label)

    def _update_labels(self):
        if self._time_label:
            self._time_label.set_text("T: " + str(round(self._model.get_remaining_time_in_phase())))

