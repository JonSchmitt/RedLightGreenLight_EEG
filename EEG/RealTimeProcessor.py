import time
import numpy as np
from multiprocessing import Process, Queue
from collections import deque
from EEG.EEGManager import EEGManager
from EEG.SignalProcessor import SignalProcessor
from Tools.DataLogger import DataLogger
from RedLightGreenLight.Inputs.KeysEnum import KEY


class RealTimeProcessor(Process):
    """
    Handles real-time EEG processing in a separate process.
    Uses Single Metric: Frontal Beta (Ch1) / Occipital Alpha (Ch8).
    """
    def __init__(self, threshold_ratio, margin_ratio, command_queue, sampling_rate=250):
        super().__init__(daemon=True)
        self._threshold = threshold_ratio
        self._margin = margin_ratio
        self._command_queue = command_queue
        self._sampling_rate = sampling_rate
        
        # Buffer: sliding window using deque for performance
        self._window_size = sampling_rate*2
        self._buffer = deque(maxlen=self._window_size)

        self._running = True
        self._last_state = False # False = Idle, True = Move

    def stop(self):
        self._running = False

    def run(self):
        """Main process loop."""
        eeg_manager = EEGManager()
        signal_processor = SignalProcessor(sampling_rate=self._sampling_rate)
        data_logger = DataLogger(session_type="session")
        
        print(f"RealTimeProcessor (Single Metric) started.")
        print(f"  Ratio Threshold: {self._threshold:.4f}, Margin: {self._margin:.4f}")
        
        if not eeg_manager.connect():
            print("RealTimeProcessor: Failed to connect to EEG. Running in Mock mode.")
            
        eeg_manager.start_stream()
        
        try:
            while self._running:
                if self._acquire_data(eeg_manager, data_logger):
                    if len(self._buffer) >= self._window_size:
                        current_ratio = self._calculate_ratio(signal_processor)
                        self._process_logic(current_ratio, data_logger)
                
                if eeg_manager.mock_mode:
                    # Sleep briefly to avoid high CPU usage
                    time.sleep(0.004)
                
        finally:
            eeg_manager.disconnect()
            data_logger.stop()
            print("RealTimeProcessor: Stream stopped.")

    def _acquire_data(self, eeg_manager, data_logger):
        """
        Fetches new samples and maintains the sliding window in the buffer.
        """
        new_data = eeg_manager.get_new_data()
        if new_data:
            self._buffer.extend(new_data)
            
            # Log raw data
            import time
            current_time = time.time()
            for sample in new_data:
                row = {"Timestamp": current_time, "Type": "RAW"}
                for i, val in enumerate(sample):
                    row[f"Ch{i+1}"] = val
                data_logger.log(row)

            return True
        return False

    def _calculate_ratio(self, signal_processor):
        """
        Calculates Ratio = Beta(Ch1) / Alpha(Ch8).
        
        Args:
            signal_processor (SignalProcessor): The processor for spectral analysis.

        Returns:
            float: The calculated ratio.
        """
        # Convert deque to array for processing
        data_window = np.array(self._buffer)
        
        # Calculate Band Powers
        alpha_powers = np.array(signal_processor.calculate_band_power(data_window, signal_processor.alpha_band))
        beta_powers = np.array(signal_processor.calculate_band_power(data_window, signal_processor.beta_band))
        
        # Ch1 (Frontal) is index 0 -> Use Beta
        beta_front = beta_powers[0]
        
        # Ch8 (Occipital) is index 7 -> Use Alpha
        alpha_back = alpha_powers[7]
        
        # Avoid division by zero
        if alpha_back == 0: alpha_back = 0.0001
        
        return beta_front / alpha_back


    def _process_logic(self, ratio, data_logger):
        """Single Metric Hysteresis Logic."""
        
        # Concentration Check (Move): Ratio > Threshold + Margin
        is_concentrated = ratio > (self._threshold + self._margin)
        
        # Relaxation Check (Stop): Ratio < Threshold - Margin
        is_relaxed = ratio < (self._threshold)

        # Log Logic State
        import time
        data_logger.log({
            "Timestamp": time.time(),
            "Type": "LOGIC",
            "Ratio": ratio,
            "Threshold": self._threshold,
            "IsConcentrated": is_concentrated, 
            "IsRelaxed": is_relaxed,
            "State": "MOVING" if self._last_state else "IDLE"
        })

        if not self._last_state: # currently in IDLE
            if is_concentrated:
                self._last_state = True
                self._send_command("PRESS", KEY.SPACE)
                print(f"BCI: MOVE! (Ratio: {ratio:.3f})")
        else: # currently in MOVING
            if is_relaxed:
                self._last_state = False
                self._send_command("RELEASE", KEY.SPACE)
                print(f"BCI: IDLE. (Ratio: {ratio:.3f})")

    def _send_command(self, action, key):
        self._command_queue.put((action, key))
