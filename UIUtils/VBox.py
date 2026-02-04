import pygame
import pygame_gui
from typing import List, Dict, Any, Optional, Tuple, Type, TypeVar

from pygame_gui.core import UIElement
from pygame_gui.elements import UIPanel

class VBox:
    """
    A Vertical Box container that automatically positions and stacks UI elements vertically.
    It resizes its background panel to fit all added elements.
    """
    _panel_offset = 6
    
    def __init__(self, relative_rect: pygame.Rect, manager: pygame_gui.UIManager, spacing: int = 10, anchors: Optional[Dict[str, str]] = None, object_id: str = "#VBoxPanel", **panel_kwargs):
        """
        Initializes the VBox.

        Args:
            relative_rect (pygame.Rect): The initial position and size of the container.
            manager (pygame_gui.UIManager): The UI manager.
            spacing (int): Space between elements in pixels.
            anchors (dict, optional): Layout anchors.
            object_id (str): The object ID for styling.
            **panel_kwargs: Additional arguments for the UIPanel.
        """
        self._manager = manager
        self._spacing = spacing
        self._elements: List[UIElement] = []
        self._panel = UIPanel(relative_rect, manager=manager, anchors=anchors or {}, object_id=object_id, **panel_kwargs)

        # Panel size state
        self._panel_width = relative_rect.width
        self._panel_height = relative_rect.height

    def add_element(self, element: UIElement):
        """
        Adds a new UI element to the vertical stack.
        
        Args:
            element (UIElement): The element to add.
        """
        self._elements.append(element)
        self._update_size()
        self._reposition_elements()

    def _compute_needed_size(self) -> Tuple[int, int]:
        """Calculates the total height and maximum width needed for all elements."""
        if not self._elements:
            return 0, 0

        total_height = sum(e.get_relative_rect().height for e in self._elements)
        total_height += self._spacing * (len(self._elements) - 1)

        max_width = max(e.get_relative_rect().width for e in self._elements)

        return total_height, max_width

    def _update_size(self):
        """Resizes the background panel based on the contained elements."""
        needed_height, needed_width = self._compute_needed_size()

        # Padding for borders and shadows
        padding = self._spacing + 20
        self._panel_height = max(needed_height + padding, 50)
        self._panel_width = max(needed_width + padding, 50)
        self._panel.set_dimensions((self._panel_width, self._panel_height))

    def _reposition_elements(self):
        """Calculates and sets the relative positions of all stacked elements."""
        if not self._elements:
            return

        total_height, _ = self._compute_needed_size()

        available_height = self._panel_height - self._spacing - 20
        available_width = self._panel_width - self._spacing - 20

        # Center centering
        start_y = (available_height - total_height) / 2 + (self._spacing / 2)
        current_y = start_y

        for elem in self._elements:
            width = elem.get_relative_rect().width
            height = elem.get_relative_rect().height

            x = (available_width - width) / 2 + (self._spacing / 2)

            elem.anchors = {'left': 'left', 'top': 'top'}
            
            # Compensation for shadow/border
            final_x = x - self._panel_offset
            final_y = current_y - self._panel_offset
            
            elem.set_relative_position((final_x, final_y))

            current_y += height + self._spacing

    def get_panel(self) -> UIPanel:
        """Returns the underlying UIPanel."""
        return self._panel

    def show(self):
        """Shows the VBox and all its elements."""
        self._panel.show()
        for elem in self._elements:
            elem.show()

    def hide(self):
        """Hides the VBox and all its elements."""
        self._panel.hide()
        for elem in self._elements:
            elem.hide()


