import pygame
from pygame_gui.elements import UITextBox


class AutoLabel:
    def __init__(self, text, rect, manager, object_id=None, anchors=None):
        """
        rect: pygame.Rect - Position und MAXIMALE Größe
        """
        self._manager = manager
        self._rect = rect

        # Erstelle TextBox mit fester Rect (nicht -1)
        self._textbox = UITextBox(
            html_text=f'<font color=#FFFFFF size=5><p align="center">{text}</p></font>',
            relative_rect=rect,
            manager=manager,
            wrap_to_height=False,  # Wichtig: False für mehrzeiligen Text
            object_id=object_id,
            anchors=anchors or {}
        )

    def set_text(self, text):
        # Verwende center-aligned HTML
        self._textbox.html_text = f'<font color=#FFFFFF size=5><p align="center">{text}</p></font>'
        self._textbox.rebuild()

    def show(self):
        self._textbox.show()

    def hide(self):
        self._textbox.hide()