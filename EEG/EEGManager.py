import numpy as np
import threading
import time

try:
    import UnicornPy
    _UNICORN_AVAILABLE = True
except ImportError:
    _UNICORN_AVAILABLE = False
    print("UnicornPy not found. EEGManager will run in MOCK mode.")

class EEGManager:
    """
    Manages connection and data acquisition from the Unicorn Hybrid Black headset.
    Supports a mock mode if the library or hardware is unavailable.
    """
    def __init__(self, use_mock=not _UNICORN_AVAILABLE):
        self._use_mock = use_mock
        self._device = None
        self._is_streaming = False
        self._data_thread = None
        self._sampling_rate = 250  # Unicorn default
        self._channels = 8  # EEG channels
        
        # Buffer for latest samples
        self._latest_data = []
        self._lock = threading.Lock()

        # Mock data state
        self._mock_data = {"concentrated": [], "relaxed": []}
        self._mock_mode = "concentrated"
        self._mock_index = 0

        if self._use_mock:
            self._load_mock_data()

    def _load_mock_data(self):
        """Loads experimental data from CSV files for mock mode."""
        import os
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths = {
            "concentrated": os.path.join(base_path, "TestData", "TestData_raw_concentrated.csv"),
            "relaxed": os.path.join(base_path, "TestData", "TestData_raw_relaxed.csv")
        }
        
        for mode, path in paths.items():
            if os.path.exists(path):
                try:
                    data = np.loadtxt(path, delimiter=',')
                    self._mock_data[mode] = data.tolist()
                    print(f"Loaded mock data for '{mode}': {len(data)} samples.")
                except Exception as e:
                    print(f"Error loading mock data from {path}: {e}")
            else:
                print(f"Warning: Mock data file not found at {path}")

    def set_mock_mode(self, mode: str):
        """Sets the active mock data set ('concentrated' or 'relaxed')."""
        if mode in self._mock_data:
            with self._lock:
                self._mock_mode = mode
                self._mock_index = 0
            print(f"Mock mode set to: {mode}")

    @property
    def mock_mode(self):
        return self._use_mock

    @property
    def is_streaming(self):
        return self._is_streaming



    @property
    def sampling_rate(self):
        return self._sampling_rate

    @property
    def channels(self):
        return self._channels

    def connect(self):
        if self._use_mock:
            print("Connected to MOCK EEG device.")
            return True
        
        try:
            device_count, serial_numbers = UnicornPy.GetAvailableDevices()
            if device_count == 0:
                print("No Unicorn devices found.")
                return False
            
            self._device = UnicornPy.Unicorn(serial_numbers[0])
            print(f"Connected to Unicorn: {serial_numbers[0]}")
            return True
        except Exception as e:
            print(f"Error connecting to Unicorn: {e}")
            return False

    def start_stream(self):
        if self._is_streaming:
            return
        
        self._is_streaming = True
        if not self._use_mock and self._device:
            self._device.StartAcquisition(False)
            
        self._data_thread = threading.Thread(target=self._acquire_data, daemon=True)
        self._data_thread.start()
        print("EEG Stream started.")

    def stop_stream(self):
        self._is_streaming = False
        if self._data_thread:
            self._data_thread.join(timeout=1.0)
        
        if not self._use_mock and self._device:
            self._device.StopAcquisition()
        print("EEG Stream stopped.")

    def _acquire_data(self):
        """Internal loop to fetch data from the device or iterate mock data samples."""
        num_samples = 1 
        
        if not self._use_mock:
            import array
            receive_buffer = array.array('f', [0.0] * UnicornPy.UnicornNumberOfConfiguredChannels)
        
        while self._is_streaming:
            if self._use_mock:
                # Use recorded data if available
                mode_data = self._mock_data[self._mock_mode]
                if mode_data:
                    sample = mode_data[self._mock_index]
                    self._mock_index = (self._mock_index + 1) % len(mode_data)
                else:
                    # Fallback to noise if files failed to load
                    sample = np.random.normal(0, 10, self._channels).tolist()
                
                time.sleep(1.0 / self._sampling_rate)
            else:
                self._device.GetData(num_samples, receive_buffer, len(receive_buffer) * 4) 
                sample = list(receive_buffer[:self._channels])
            
            with self._lock:
                self._latest_data.append(sample)
                if len(self._latest_data) > 1000:
                    self._latest_data.pop(0)

    def get_new_data(self):
        """Returns and clears the current data buffer."""
        with self._lock:
            data = list(self._latest_data)
            self._latest_data = []
            return data

    def __del__(self):
        self.stop_stream()
        if self._device:
            del self._device
