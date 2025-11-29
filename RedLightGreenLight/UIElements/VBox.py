import pygame
import pygame_gui
from typing import List, Dict, Any, Optional, Tuple, Type, TypeVar

from pygame_gui.core import UIElement
from pygame_gui.elements import UIPanel

class VBox:
    _panel_offset = 6
    def __init__(self, relative_rect: pygame.Rect, manager: pygame_gui.UIManager, spacing: int = 10, anchors=None, **panel_kwargs):
        self._manager = manager
        self._spacing = spacing
        self._elements = []
        self._panel = UIPanel(relative_rect, manager=manager, anchors=anchors or {}, **panel_kwargs)

        # Panel size state
        self._panel_width = relative_rect.width
        self._panel_height = relative_rect.height

    def add_element(self, element: UIElement):
        self._elements.append(element)
        self._update_size()
        self._reposition_elements()

    # --------------------------------------------------------------
    # Step 1: Compute needed width + height
    # --------------------------------------------------------------
    def _compute_needed_size(self):
        if not self._elements:
            return 0, 0

        total_height = sum(e.get_relative_rect().height for e in self._elements)
        total_height += self._spacing * (len(self._elements) - 1)

        max_width = max(e.get_relative_rect().width for e in self._elements)

        return total_height, max_width

    # --------------------------------------------------------------
    # Step 2: Resize panel to fit elements (expand + shrink)
    # --------------------------------------------------------------
    def _update_size(self):
        needed_height, needed_width = self._compute_needed_size()

        # Add small padding
        needed_height += self._spacing
        needed_width += self._spacing

        # Expand/Shrink height
        if needed_height != self._panel_height:
            self._panel_height = max(needed_height, 50)  # minimum height optional
            self._panel.set_dimensions((self._panel_width, self._panel_height))

        # Expand/Shrink width
        if needed_width != self._panel_width:
            self._panel_width = max(needed_width, 50)
            self._panel.set_dimensions((self._panel_width, self._panel_height))

    # --------------------------------------------------------------
    # Step 3: Center elements vertically + horizontally
    # --------------------------------------------------------------
    def _reposition_elements(self):
        if not self._elements:
            return

        total_height, _ = self._compute_needed_size()

        # Ziehe das hinzugefügte Padding wieder ab für echte Zentrierung
        available_height = self._panel_height - self._spacing
        available_width = self._panel_width - self._spacing

        start_y = (available_height - total_height) / 2 + (self._spacing / 2)
        current_y = start_y

        for elem in self._elements:
            width = elem.get_relative_rect().width
            height = elem.get_relative_rect().height

            x = (available_width - width) / 2 + (self._spacing / 2)

            elem.anchors = {'left': 'left', 'top': 'top'}
            elem.set_relative_position((x-self._panel_offset, current_y-self._panel_offset))

            current_y += height + self._spacing

    # Public API
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

