from abc import ABC, abstractmethod


class SettingsObserver(ABC):
    @abstractmethod
    def update_settings(self):
        pass
