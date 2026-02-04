import pygame
import pygame_gui
from typing import Tuple, Optional

from pygame_gui.core import UIElement


class SliderWithLabel(UIElement):
    """
    A UI element that combines a horizontal slider with a label displaying its current value.
    """
    def __init__(
        self,
        manager: pygame_gui.UIManager,
        container: Optional[UIElement],
        width: int,
        height: int,
        label_text: str,
        start_value: float = 0.0,
        value_range: Tuple[float, float] = (0.0, 100.0),
        suffix: str = "",
        starting_height: int = 1,
        layer_thickness: int = 1,
    ):
        """
        Initializes the SliderWithLabel.

        Args:
            manager (pygame_gui.UIManager): The UI manager.
            container (UIElement, optional): The container for this element.
            width (int): Total width.
            height (int): Total height.
            label_text (str): The descriptive text for the label.
            start_value (float): The initial value.
            value_range (tuple): (min, max) values.
            suffix (str): Suffix for the value display (e.g., "%").
            starting_height (int): The starting height layer.
            layer_thickness (int): The thickness of the layer.
        """

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


    def on_slider_changed(self, event: pygame.event.Event):
        """Handles slider value changes and updates the label."""
        self._label.set_text(f"{self._label.text.split(':')[0]}: {int(event.value)}{self._suffix}")

    def get_value(self) -> float:
        """Returns the current value of the slider."""
        return self._slider.get_current_value()

    def set_value(self, value: float):
        """Sets the slider value and updates the label."""
        self._slider.set_current_value(value)
        self._label.set_text(f"{self._label.text.split(':')[0]}: {int(value)}{self._suffix}")

    def get_panel(self) -> pygame_gui.elements.UIPanel:
        """Returns the background panel."""
        return self._panel

    def get_slider(self) -> pygame_gui.elements.UIHorizontalSlider:
        """Returns the slider element."""
        return self._slider

