from queue import Queue

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.MenuState import MenuState
from RedLightGreenLight.States.GameState import GameState
import pygame

from RedLightGreenLight.States.SettingsState import SettingsState
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw
import sys

class GameApp:
    def __init__(self):
        pygame.init()
        settings_model = SettingsModel()
        music_manager = MusicManager()
        screen = pygame.display.set_mode((settings_model.get_window_width(), settings_model.get_window_height()))
        self._state = None
        self._state_events = Queue()

        self._menu_state = MenuState(screen,settings_model,music_manager,self._state_events)
        self._game_state = GameState(screen,settings_model,music_manager,self._state_events)
        self._settings_state = SettingsState(screen,settings_model,music_manager,self._state_events)

        settings_model.add_observer(self._menu_state)
        settings_model.add_observer(self._game_state)


        self.change_state(self._menu_state)
        self._clock = pygame.time.Clock()





    def change_state(self,new_state):
        if self._state:
            self._state.exit()
        self._state = new_state
        self._state.enter()

    def on_menu_ok(self):
        self.change_state(self._game_state)

    def on_menu_esc(self):
        self.change_state(self._game_state)

    def on_game_esc(self):
        self.change_state(self._menu_state)

    def on_game_quit(self):
        pygame.quit()
        sys.exit()

    def on_menu_settings(self):
        self.change_state(self._settings_state)

    def on_settings_ok(self):
        self.change_state(self._menu_state)

    def on_settings_esc(self):
        self.change_state(self._menu_state)

    def update(self):
        self._clock.tick(60)
        delta_time = self._clock.get_time()/1000.0
        if self._state:
            self._state.update(delta_time)

    def handle_state_events(self):
        while not self._state_events.empty():
            event = self._state_events.get()
            if event == skw.MENU_OK:
                self.on_menu_ok()
            elif event == skw.MENU_ESC:
                self.on_menu_esc()
            elif event == skw.GAME_ESC:
                self.on_game_esc()
            elif event == skw.GAME_QUIT:
                self.on_game_quit()
            elif event == skw.MENU_SETTINGS:
                self.on_menu_settings()
            elif event == skw.SETTINGS_OK:
                self.on_settings_ok()
            elif event == skw.SETTINGS_ESC:
                self.on_settings_esc()
            else:
                print(f"Unknown event: {event}")


    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    self.on_game_quit()
            self._state.handle_events(events)
            self.handle_state_events()
            self.update()
