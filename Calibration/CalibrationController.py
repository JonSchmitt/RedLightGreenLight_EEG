import pygame
import pygame_gui
import sys
from .CalibrationPhase import CalibrationPhase
from EEG.EEGManager import EEGManager
from EEG.SignalProcessor import SignalProcessor

class CalibrationController:
    """
    Main controller for the EEG calibration. 
    Coordinates Model, View, EEG acquisition and Signal Processing.
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view
        
        # EEG components
        self._eeg_manager = EEGManager()
        self._signal_processor = SignalProcessor()
        
        self._running = True

    def run(self):
        # 1. Connect EEG
        if not self._eeg_manager.connect():
            print("Warning: Streaming may not work correctly without EEG hardware.")
        
        self._eeg_manager.start_stream()
        
        clock = pygame.time.Clock()
        
        try:
            while self._running:
                dt = clock.tick(60) / 1000.0
                
                self._handle_events()
                self._update()
                self._view.render(dt) # Pass dt for UI update
                
        finally:
            self._eeg_manager.stop_stream()

    def _handle_events(self):
        for event in pygame.event.get():
            # Pass to UI Manager
            self._view.get_manager().process_events(event)
            if event.type == pygame.QUIT:
                self._handle_quit_event()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_ui_events(event)
            if event.type == pygame.KEYDOWN:
                self._handle_key_events()

    def _handle_quit_event(self):
        self._running = False
        pygame.quit()
        sys.exit()

    def _handle_ui_events(self,event):
        if event.ui_element == self._view.get_start_button():
            self._eeg_manager.set_mock_mode("relaxed")
            self._model.start_phase(CalibrationPhase.RELAXED)

    def _handle_key_events(self):
        if self._model.phase == CalibrationPhase.FINISHED:
            self._running = False

    def _update(self):
        # Collect data if in active phase
        if self._model.phase in [CalibrationPhase.RELAXED, CalibrationPhase.CONCENTRATED]:
            new_data = self._eeg_manager.get_new_data()
            self._model.add_data(new_data)
            
            # Use model's check for math updates
            self._model.check_math_task_update()
            
            # Check for phase transitions
            self._update_calibration_phase()

    def _update_calibration_phase(self):
        if self._model.is_phase_over():
            if self._model.phase == CalibrationPhase.RELAXED:
                self._eeg_manager.set_mock_mode("concentrated")
                self._model.start_phase(CalibrationPhase.CONCENTRATED)
            elif self._model.phase == CalibrationPhase.CONCENTRATED:
                self._calculate_results()
                self._model.phase = CalibrationPhase.FINISHED

    def _calculate_results(self):
        """
        Calculates calibration results by delegating to the model.
        The results are used to set thresholds and margins for BCI control.
        """
        print("Calculating thresholds for frontal (Ch 1) and occipital (Ch 8) electrodes...")
        self._model.calculate_calibration_results(self._signal_processor)
