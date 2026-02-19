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
        self._window_size = sampling_rate//2
        self._buffer = deque(maxlen=self._window_size)
        
        # Time-Duration Check (Debounce)
        # The condition must be met CONTINUOUSLY for this duration to trigger a change.
        self._duration_threshold = 0.5 # seconds
        
        # Timers to track how long we are in a potential new state
        self._con_start_time = None
        self._rel_start_time = None

        self._running = True
        self._last_state = False # False = Idle, True = Move

    def stop(self):
        self._running = False

    def run(self):
        """Main process loop."""
        eeg_manager = EEGManager()
        signal_processor = SignalProcessor(sampling_rate=self._sampling_rate)
        data_logger = DataLogger(session_type="session")
        
        print(f"RealTimeProcessor (Single Metric + Time Debounce) started.")
        print(f"  Ratio Threshold: {self._threshold:.4f}, Margin: {self._margin:.4f}")
        print(f"  Duration Threshold: {self._duration_threshold}s")
        
        if not eeg_manager.connect():
            print("RealTimeProcessor: Failed to connect to EEG. Running in Mock mode.")
            
        eeg_manager.start_stream()
        
        try:
            while self._running:
                if self._acquire_data(eeg_manager, data_logger):
                    if len(self._buffer) >= self._window_size:
                        
                        # --- ARTIFACT REJECTION (Start) ---
                        # If the signal is too strong (> 100 uV), it is likely muscle noise (EMG).
                        # We ignore this window to prevent false positives.
                        
                        # max_amplitude = np.max(np.abs(np.array(self._buffer)))
                        # if max_amplitude > 100.0:
                        #     print(f"Artifact detected! (Amp: {max_amplitude:.1f} uV) - Ignoring.")
                        #     # Optional: Force "Relaxed" state or just skip processing
                        #     continue 
                        
                        # --- ARTIFACT REJECTION (End) ---

                        raw_ratio, beta_val, alpha_val = signal_processor.calculate_concentration_metric(self._buffer)
                        self._process_logic(raw_ratio, beta_val, alpha_val, data_logger)
                
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



    def _evaluate_conditions(self, ratio):
        """Checks if the ratio meets concentration/relaxation thresholds."""
        is_con = ratio > (self._threshold + self._margin)
        is_rel = ratio < (self._threshold - self._margin)
        return is_con, is_rel

    def _update_timers(self, is_con, is_rel, now):
        """Updates duration timers based on current conditions."""
        # Timer for Concentration
        if is_con:
            if self._con_start_time is None:
                self._con_start_time = now
        else:
            self._con_start_time = None

        # Timer for Relaxation
        if is_rel:
            if self._rel_start_time is None:
                self._rel_start_time = now
        else:
            self._rel_start_time = None

    def _handle_state_transitions(self, ratio, now):
        """Checks timers and executes state changes (PRESS/RELEASE)."""
        trigger_move = False
        trigger_stop = False
        
        if self._con_start_time is not None:
            if (now - self._con_start_time) >= self._duration_threshold:
                trigger_move = True
                
        if self._rel_start_time is not None:
            if (now - self._rel_start_time) >= self._duration_threshold:
                trigger_stop = True

        if not self._last_state: # currently IDLE
            if trigger_move:
                self._last_state = True
                self._send_command("PRESS", KEY.SPACE)
                print(f"BCI: MOVE! (Held > {self._duration_threshold}s | Ratio: {ratio:.3f})")
        else: # currently MOVING
            if trigger_stop:
                self._last_state = False
                self._send_command("RELEASE", KEY.SPACE)
                print(f"BCI: IDLE. (Held > {self._duration_threshold}s | Ratio: {ratio:.3f})")

    def _log_processing_state(self, ratio, beta, alpha, is_con, is_rel, now, data_logger):
        """Logs the logic state and metrics."""
        data_logger.log({
            "Timestamp": now,
            "Type": "LOGIC",
            "Ratio": ratio,
            "Beta": beta,
            "Alpha": alpha,
            "Threshold": self._threshold,
            "LoopCon": is_con,
            "LoopRel": is_rel,
            "TimerCon": (now - self._con_start_time) if self._con_start_time else 0,
            "TimerRel": (now - self._rel_start_time) if self._rel_start_time else 0,
            "State": "MOVING" if self._last_state else "IDLE"
        })

    def _process_logic(self, ratio, beta, alpha, data_logger):
        """
        Orchestrates the processing steps: Evaluation, Timer Update, State Transition, and Logging.
        """
        import time
        now = time.time()
        
        # 1. Evaluate conditions
        is_con, is_rel = self._evaluate_conditions(ratio)
        
        # 2. Update Timers
        self._update_timers(is_con, is_rel, now)
        
        # 3. Handle Transitions
        self._handle_state_transitions(ratio, now)
        
        # 4. Log state (Separated from core logic)
        self._log_processing_state(ratio, beta, alpha, is_con, is_rel, now, data_logger)

    def _send_command(self, action, key):
        self._command_queue.put((action, key))
