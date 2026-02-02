import pygame
from .CalibrationPhase import CalibrationPhase

class CalibrationView:
    """
    View for the calibration process. Handles all Pygame rendering.
    Directly accesses the model to retrieve current state for drawing.
    """
    def __init__(self, screen, model):
        self._screen = screen
        self._model = model
        self._width = screen.get_width()
        self._height = screen.get_height()
        
        # Colors
        self._COLOR_BG = (30, 30, 40)
        self._COLOR_TEXT = (240, 240, 240)
        self._COLOR_HIGHLIGHT = (50, 150, 250)
        self._COLOR_BUTTON = (70, 70, 90)
        
        # Fonts
        pygame.font.init()
        self._font_title = pygame.font.SysFont('Arial', 48, bold=True)
        self._font_text = pygame.font.SysFont('Arial', 32)
        self._font_math = pygame.font.SysFont('Arial', 72, bold=True)
        
        # Button Rect
        self._start_btn_rect = pygame.Rect(self._width // 2 - 100, self._height // 2 + 100, 200, 60)

    def render(self):
        self._screen.fill(self._COLOR_BG)
        
        phase = self._model.phase
        
        if phase == CalibrationPhase.EXPLANATION:
            self._render_explanation()
        elif phase == CalibrationPhase.RELAXED:
            self._render_relaxed()
        elif phase == CalibrationPhase.CONCENTRATED:
            self._render_concentrated()
        elif phase == CalibrationPhase.FINISHED:
            self._render_finished()
            
        pygame.display.flip()

    def _render_explanation(self):
        self._draw_text("Kalibrierung", self._font_title, self._height // 4)
        
        lines = [
            "Willkommen zur EEG-Kalibrierung.",
            "1. Phase: 30s Entspannung (nichts Besonderes denken).",
            "2. Phase: 30s Konzentration (Kopfrechnen).",
            "Die Daten helfen uns, deine Gehirnaktivität zu verstehen."
        ]
        
        for i, line in enumerate(lines):
            self._draw_text(line, self._font_text, self._height // 2 - 50 + i * 40)
            
        # Button
        pygame.draw.rect(self._screen, self._COLOR_BUTTON, self._start_btn_rect, border_radius=10)
        self._draw_text("START", self._font_text, self._start_btn_rect.centery, color=self._COLOR_TEXT)

    def _render_relaxed(self):
        self._draw_text("Phase 1: Entspannung", self._font_title, self._height // 3)
        self._draw_text("Bitte entspannen. Denke an nichts Besonderes.", self._font_text, self._height // 2)
        
        # Timer
        time_text = f"Noch {int(self._model.get_remaining_time())} Sekunden"
        self._draw_text(time_text, self._font_text, self._height * 2 // 3, color=self._COLOR_HIGHLIGHT)

    def _render_concentrated(self):
        self._draw_text("Phase 2: Konzentration", self._font_title, self._height // 4)
        self._draw_text("Löse die Rechenaufgabe im Kopf:", self._font_text, self._height // 3)
        
        # Math Task
        self._draw_text(self._model.current_math_task, self._font_math, self._height // 2)
        
        # Timer
        time_text = f"Noch {int(self._model.get_remaining_time())} Sekunden"
        self._draw_text(time_text, self._font_text, self._height * 3 // 4, color=self._COLOR_HIGHLIGHT)

    def _render_finished(self):
        self._draw_text("Kalibrierung abgeschlossen", self._font_title, self._height // 3)
        
        results = [
            f"Alpha Ratio: {self._model.alpha_ratio:.2f}",
            f"Beta Ratio: {self._model.beta_ratio:.2f}",
            "Drücke eine beliebige Taste zum Fortfahren."
        ]
        
        for i, res in enumerate(results):
            self._draw_text(res, self._font_text, self._height // 2 + i * 40)

    def _draw_text(self, text, font, y_pos, color=None):
        if color is None: color = self._COLOR_TEXT
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(self._width // 2, y_pos))
        self._screen.blit(surf, rect)

    def is_start_clicked(self, pos):
        return self._start_btn_rect.collidepoint(pos)
