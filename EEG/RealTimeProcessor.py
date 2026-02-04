import time
import numpy as np
from multiprocessing import Process, Queue
from collections import deque
from EEG.EEGManager import EEGManager
from EEG.SignalProcessor import SignalProcessor
from RedLightGreenLight.Inputs.KeysEnum import KEY


class RealTimeProcessor(Process):
    """
    Handles real-time EEG processing in a separate process.
    Uses Dual-Channel Agreement with independent thresholds and margins.
    """
    def __init__(self, th1, dir1, m1, th8, dir8, m8, command_queue, sampling_rate=250):
        super().__init__(daemon=True)
        self._th1 = th1     # Threshold Channel 1
        self._dir1 = dir1   # Direction Channel 1
        self._m1 = m1       # Margin Channel 1
        self._th8 = th8     # Threshold Channel 8
        self._dir8 = dir8   # Direction Channel 8
        self._m8 = m8       # Margin Channel 8
        self._command_queue = command_queue
        self._sampling_rate = sampling_rate
        
        # Buffer: sliding window using deque for performance
        self._window_size = sampling_rate 
        self._buffer = deque(maxlen=self._window_size)

        self._running = True
        self._last_state = False # False = Idle, True = Move

    def stop(self):
        self._running = False

    def run(self):
        """Main process loop."""
        eeg_manager = EEGManager()
        signal_processor = SignalProcessor(sampling_rate=self._sampling_rate)
        
        print(f"RealTimeProcessor (Dual-Channel) started.")
        print(f"  Ch1: Th={self._th1:.4f}, Dir={self._dir1}, Margin={self._m1:.4f}")
        print(f"  Ch8: Th={self._th8:.4f}, Dir={self._dir8}, Margin={self._m8:.4f}")
        
        if not eeg_manager.connect():
            print("RealTimeProcessor: Failed to connect to EEG. Running in Mock mode.")
            
        eeg_manager.start_stream()
        
        try:
            while self._running:
                if self._acquire_data(eeg_manager):
                    if len(self._buffer) >= self._window_size:
                        score1, score8 = self._calculate_scores(signal_processor)
                        self._process_logic(score1, score8)
                
                if eeg_manager.mock_mode:
                    # Sleep briefly to avoid high CPU usage
                    time.sleep(0.004)
                
        finally:
            eeg_manager.stop_stream()
            print("RealTimeProcessor: Stream stopped.")

    def _acquire_data(self, eeg_manager):
        """
        Fetches new samples and maintains the sliding window in the buffer.
     
        Args:
            eeg_manager (EEGManager): The EEG manager providing data.
            
        Returns:
            bool: True if new data was successfully acquired and added to the buffer, False otherwise.
        """
        new_data = eeg_manager.get_new_data()
        if new_data:
            self._buffer.extend(new_data)
            return True
        return False

    def _calculate_scores(self, signal_processor):
        """
        Calculates independent Beta/Alpha ratios for Ch 1 and Ch 8.
        
        Args:
            signal_processor (SignalProcessor): The processor for spectral analysis.

        Returns:
            tuple: (score1, score8) as floats.
        """
        # Convert deque to array for processing
        data_window = np.array(self._buffer)
        
        # Calculate ratios for all channels
        ratios = signal_processor.calculate_ratios(data_window)
        
        # Ch 1 (index 0), Ch 8 (index 7)
        return float(ratios[0]), float(ratios[7])


    def _process_logic(self, score1, score8):
        """Dual-Channel Agreement Hysteresis Logic."""
        # Concentration checks
        # If dir=1: current > th + m. If dir=-1: current < th - m.
        # Generalized: (current - th) * dir > m
        is_con1 = (score1 - self._th1) * self._dir1 > self._m1
        is_con8 = (score8 - self._th8) * self._dir8 > self._m8
        
        # Relaxation checks (for stopping move)
        # Generalized: (th - current) * dir > m
        is_rel1 = (self._th1 - score1) * self._dir1 > self._m1
        is_rel8 = (self._th8 - score8) * self._dir8 > self._m8

        # Dual Agreement
        is_dual_concentrated = is_con1 and is_con8
        is_any_relaxed = is_rel1 or is_rel8

        if not self._last_state: # currently in IDLE
            if is_dual_concentrated:
                self._last_state = True
                self._send_command("PRESS", KEY.SPACE)
                print(f"BCI: MOVE! (Scores: {score1:.3f}, {score8:.3f})")
        else: # currently in MOVING
            if is_any_relaxed:
                self._last_state = False
                self._send_command("RELEASE", KEY.SPACE)
                print(f"BCI: IDLE. (Rel triggered: Ch1={is_rel1}, Ch8={is_rel8})")

    def _send_command(self, action, key):
        self._command_queue.put((action, key))
