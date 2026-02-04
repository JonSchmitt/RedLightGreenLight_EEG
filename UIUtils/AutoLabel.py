import pygame
import pygame_gui
from typing import Optional, Dict

from pygame_gui.elements import UITextBox



class AutoLabel:
    """
    A helper class for centered labels with white text using UITextBox.
    """
    def __init__(self, text: str, rect: pygame.Rect, manager: pygame_gui.UIManager, object_id: Optional[str] = None, anchors: Optional[Dict[str, str]] = None):
        """
        Initializes the AutoLabel.

        Args:
            text (str): The initial text to display.
            rect (pygame.Rect): Position and MAX size for the label.
            manager (pygame_gui.UIManager): The UI manager.
            object_id (str, optional): The object ID for styling.
            anchors (dict, optional): Layout anchors.
        """
        self._manager = manager
        self._rect = rect

        self._textbox = UITextBox(
            html_text=f'<font color=#FFFFFF size=5><p align="center">{text}</p></font>',
            relative_rect=rect,
            manager=manager,
            wrap_to_height=False,
            object_id=object_id,
            anchors=anchors or {}
        )


    def set_text(self, text: str):
        """Updates the text of the label."""
        self._textbox.html_text = f'<font color=#FFFFFF size=5><p align="center">{text}</p></font>'
        self._textbox.rebuild()

    def show(self):
        """Shows the label."""
        self._textbox.show()

    def hide(self):
        """Hides the label."""
        self._textbox.hide()
