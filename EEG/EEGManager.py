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
        """Internal loop to fetch data from the device or generate mock data."""
        num_samples = 1 
        
        # UnicornPy numerical data handling:
        # The API provides float data directly if using the right methods.
        # GetData fills a buffer of floats.
        if not self._use_mock:
            # According to g.tec, UnicornGetDataSizeSamples is the size in bytes for one scan.
            # In Python, we often use a buffer that can hold the floats.
            # However, for simplicity and compatibility with the user's manual mention:
            # We assume GetData returns numerical values.
            import array
            # Each scan contains multiple float32 values (EEG, Accel, Gyro, etc.)
            # We need to know how many floats are in one scan.
            # UnicornPy.UnicornNumberOfConfiguredChannels gives this.
            receive_buffer = array.array('f', [0.0] * UnicornPy.UnicornNumberOfConfiguredChannels)
        
        while self._is_streaming:
            if self._use_mock:
                # Generate random EEG-like data (noise + some offset)
                sample = np.random.normal(0, 10, self._channels).tolist()
                time.sleep(1.0 / self._sampling_rate)
            else:
                # Fill receive_buffer with numerical values
                self._device.GetData(num_samples, receive_buffer, len(receive_buffer) * 4) # 4 bytes per float
                # We only want the first 8 channels (EEG)
                sample = list(receive_buffer[:self._channels])
            
            with self._lock:
                self._latest_data.append(sample)
                # Keep buffer manageable if not consumed
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
