import pygame
import pygame_gui
from typing import List, Dict, Any, Optional, Tuple, Type, TypeVar

from pygame_gui.core import UIElement
from pygame_gui.elements import UIPanel

from RedLightGreenLight.UIElements.SliderWithLabel import SliderWithLabel

T = TypeVar('T', bound=pygame_gui.core.UIElement)
class VBox:
    def __init__(self, relative_rect: pygame.Rect, manager: pygame_gui.UIManager, spacing: int = 10, anchors=None, **panel_kwargs):
        self._manager = manager
        self._spacing = spacing
        self._elements = []
        self._panel = UIPanel(relative_rect, manager=manager, anchors=anchors or {}, **panel_kwargs)
        self._panel_width = relative_rect.width
        self._panel_height = relative_rect.height

    def add_element(self, element: UIElement):
        self._elements.append(element)
        self._reposition_elements()

    def _reposition_elements(self):
        if not self._elements:
            return

        total_height = sum(e.get_relative_rect().height for e in self._elements)
        total_height += self._spacing * (len(self._elements) - 1)
        start_y = (self._panel_height - total_height) / 2
        current_y = start_y

        for elem in self._elements:
            width = elem.get_relative_rect().width
            height = elem.get_relative_rect().height
            x = (self._panel_width - width) / 2
            elem.anchors = {'left': 'left', 'top': 'top'}
            elem.set_relative_position((x, current_y))
            current_y += height + self._spacing

    def get_panel(self):
        return self._panel

    def show(self):
        self._panel.show()
        for elem in self._elements:
            elem.show()
    def hide(self):
        self._panel.hide()
        for elem in self._elements:
            elem.hide()

class VBox_old:
    """
    Ein vertikaler Container für pygame_gui Elemente.
    Ordnet Elemente vertikal zentriert in einem Panel an.
    """

    def __init__(
            self,
            relative_rect: pygame.Rect,
            manager: pygame_gui.UIManager,
            spacing: int = 10,
            anchors: Optional[Dict[str, str]] = None,
            **panel_kwargs
    ):
        """
        Args:
            relative_rect: Position und Größe des Panels
            manager: pygame_gui UIManager
            spacing: Abstand zwischen den Elementen in Pixeln
            anchors: Anchors für das Panel (z.B. {'centerx': 'centerx', 'centery': 'centery'})
            **panel_kwargs: Weitere Argumente für UIPanel
        """
        self._manager = manager
        self._spacing = spacing
        self._elements: List[pygame_gui.core.UIElement] = []

        # Panel erstellen
        self._panel = pygame_gui.elements.UIPanel(
            relative_rect=relative_rect,
            manager=manager,
            anchors=anchors or {},
            **panel_kwargs
        )

        self._panel_height = relative_rect.height
        self._panel_width = relative_rect.width





    def add_element(
        self,
        element_class: Type[T],
        width: int,
        height: int,
        **element_kwargs
    ) -> T:
        """
        Fügt ein Element zum VBox hinzu.

        Args:
            element_class: Die Klasse des Elements (z.B. UIButton, UILabel)
            width: Breite des Elements
            height: Höhe des Elements
            **element_kwargs: Weitere Argumente für das Element (z.B. text='OK')

        Returns:
            Das erstellte Element
        """
        # Position berechnen (wird nach dem Hinzufügen neu berechnet)
        element = element_class(
            relative_rect=pygame.Rect(0, 0, width, height),
            manager=self._manager,
            container=self._panel,
            **element_kwargs
        )

        self._elements.append(element)
        self._reposition_elements()

        return element

    def _reposition_elements(self):
        if not self._elements:
            return

        total_height = sum(elem.relative_rect.height for elem in self._elements)
        total_height += self._spacing * (len(self._elements) - 1)
        start_y = (self._panel_height - total_height) / 2

        current_y = start_y
        for elem in self._elements:
            height = elem.relative_rect.height
            width = elem.relative_rect.width
            x = (self._panel_width - width) / 2
            elem.anchors = {'left': 'left', 'top': 'top'}
            elem.set_relative_position((x, current_y))
            elem.set_dimensions((width, height))
            elem.rebuild()
            current_y += elem.relative_rect.height + self._spacing

    def remove_element(self, element: pygame_gui.core.UIElement):
        """Entfernt ein Element aus dem VBox."""
        if element in self._elements:
            self._elements.remove(element)
            element.kill()
            self._reposition_elements()

    def clear(self):
        """Entfernt alle Elemente aus dem VBox."""
        for elem in self._elements:
            elem.kill()
        self._elements.clear()

    def hide(self):
        for elem in self._elements:
            elem.hide()
        self._panel.hide()

    def show(self):
        for elem in self._elements:
            elem.show()
        self._panel.show()

    def set_spacing(self, spacing: int):
        """Ändert den Abstand zwischen Elementen."""
        self._spacing = spacing
        self._reposition_elements()


    def get_panel(self)->pygame_gui.elements.UIPanel:
        return self._panel

    def get_elements(self):
        return self._elements.copy()
