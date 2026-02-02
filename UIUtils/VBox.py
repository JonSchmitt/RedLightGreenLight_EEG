import pygame
import pygame_gui
from typing import List, Dict, Any, Optional, Tuple, Type, TypeVar

from pygame_gui.core import UIElement
from pygame_gui.elements import UIPanel

class VBox:
    _panel_offset = 6
    def __init__(self, relative_rect: pygame.Rect, manager: pygame_gui.UIManager, spacing: int = 10, anchors=None, object_id: str = "#VBoxPanel", **panel_kwargs):
        self._manager = manager
        self._spacing = spacing
        self._elements = []
        self._panel = UIPanel(relative_rect, manager=manager, anchors=anchors or {}, object_id=object_id, **panel_kwargs)

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

        # The user uses 20px extra buffer plus spacing to size the panel.
        # This creates enough room for the border and corner radius.
        padding = self._spacing + 20
        self._panel_height = max(needed_height + padding, 50)
        self._panel_width = max(needed_width + padding, 50)
        self._panel.set_dimensions((self._panel_width, self._panel_height))

    # --------------------------------------------------------------
    # Step 3: Center elements vertically + horizontally
    # --------------------------------------------------------------
    def _reposition_elements(self):
        if not self._elements:
            return

        total_height, _ = self._compute_needed_size()

        # We subtract the extra buffer to find the "content box" we just sized
        available_height = self._panel_height - self._spacing - 20
        available_width = self._panel_width - self._spacing - 20

        # Initial centering inside that content box
        start_y = (available_height - total_height) / 2 + (self._spacing / 2)
        current_y = start_y

        for elem in self._elements:
            width = elem.get_relative_rect().width
            height = elem.get_relative_rect().height

            x = (available_width - width) / 2 + (self._spacing / 2)

            elem.anchors = {'left': 'left', 'top': 'top'}
            
            # The -_panel_offset (6px) shift pushes the content towards the top-left corner.
            # This compensates for the bottom-right shadow and results in a very tight 
            # visual margin (approx 1px) against the border, which the user prefers.
            final_x = x - self._panel_offset
            final_y = current_y - self._panel_offset
            
            elem.set_relative_position((final_x, final_y))

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

