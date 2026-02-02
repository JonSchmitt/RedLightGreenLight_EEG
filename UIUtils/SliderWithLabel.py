import pygame
import pygame_gui
from typing import Tuple

from pygame_gui.core import UIElement


class SliderWithLabel(UIElement):
    def __init__(
        self,
        manager: pygame_gui.UIManager,
        container,
        width: int,
        height: int,
        label_text: str,
        start_value: float = 0.0,
        value_range: Tuple[float, float] = (0.0, 100.0),
        suffix: str = "",
        starting_height:int = 1,
        layer_thickness:int = 1,
    ):
        super().__init__(relative_rect=pygame.Rect(0, 0, width, height), manager=manager, container=container,starting_height=starting_height,layer_thickness=layer_thickness)
        self._manager = manager
        self._container = container
        self._width = width
        self._height = height
        self._suffix = suffix

        self._panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, width, height),
            manager=manager,
            container=container,
            object_id="#PanelNoBorder"
        )


        padding = 10
        label_height = height // 2
        slider_height = height - label_height - padding

        self._label = pygame_gui.elements.UILabel(
            pygame.Rect(padding, padding, width - 2 * padding, label_height),
            text=f"{label_text}: {start_value}{suffix}",
            manager=manager,
            container=self._panel
        )

        self._slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect(padding, label_height, width - 2 * padding, slider_height),
            start_value=start_value,
            value_range=value_range,
            manager=manager,
            container=self._panel
        )


    def on_slider_changed(self, event):
        self._label.set_text(f"{self._label.text.split(':')[0]}: {int(event.value)}{self._suffix}")

    def get_value(self) -> float:
        return self._slider.get_current_value()

    def set_value(self, value: float):
        self._slider.set_current_value(value)
        self._label.set_text(f"{self._label.text.split(':')[0]}: {int(value)}{self._suffix}")

    def get_panel(self):
        return self._panel

    def get_slider(self):
        return self._slider
