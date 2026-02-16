import os
import csv
import time
import threading
from queue import Queue
from datetime import datetime

class DataLogger:
    """
    Handles thread-safe logging of EEG and BCI data to CSV files.
    Uses a background worker thread to minimize impact on real-time processing.
    """
    def __init__(self, session_type="unknown"):
        """
        Args:
            session_type (str): 'calibration' or 'session' (runtime).
        """
        self._queue = Queue()
        self._running = True
        
        # Create output directory
        self._output_dir = os.path.join(os.getcwd(), "measurement_data")
        os.makedirs(self._output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._filename = os.path.join(self._output_dir, f"{session_type}_{timestamp}.csv")
        self._meta_filename = os.path.join(self._output_dir, f"{session_type}_results_{timestamp}.txt")
        
        # Start background worker
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
        
        print(f"DataLogger started. Logging to: {self._filename}")

    def log(self, data_dict):
        """
        Queues a data row for logging.
        
        Args:
            data_dict (dict): Dictionary where keys are column headers and values are data.
        """
        self._queue.put(data_dict)

    def save_metadata(self, text_content):
        """
        Saves metadata (e.g., thresholds) to a separate text file.
        """
        try:
            with open(self._meta_filename, "w") as f:
                f.write(text_content)
            print(f"Metadata saved to: {self._meta_filename}")
        except Exception as e:
            print(f"Error saving metadata: {e}")

    def stop(self):
        """Stops the logging thread safely."""
        self._running = False
        self._worker_thread.join()
        print("DataLogger stopped.")

    def _worker(self):
        """Background loop to write data from queue to CSV."""
        # Wait for first item to determine headers
        first_item = self._queue.get()
        if first_item is None: 
            return # Exit if stopped immediately
            
        fieldnames = first_item.keys()
        
        try:
            with open(self._filename, "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(first_item)
                
                while self._running or not self._queue.empty():
                    try:
                        # Timeout allows checking self._running periodically
                        item = self._queue.get(timeout=0.1)
                        writer.writerow(item)
                        self._queue.task_done()
                    except:
                        continue
                        
        except Exception as e:
            print(f"DataLogger Error: {e}")
