import numpy as np
import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EEG.SignalProcessor import SignalProcessor

def verify_logic():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    relaxed_path = os.path.join(base_path, "TestData", "TestData_raw_relaxed.csv")
    concentrated_path = os.path.join(base_path, "TestData", "TestData_raw_concentrated.csv")
    
    if not os.path.exists(relaxed_path) or not os.path.exists(concentrated_path):
        print("Error: Test data files not found.")
        return

    print("Loading test data...")
    relaxed_data = np.loadtxt(relaxed_path, delimiter=',')
    concentrated_data = np.loadtxt(concentrated_path, delimiter=',')
    
    sp = SignalProcessor(sampling_rate=250)
    
    # 1. Simulate Calibration (matching MATLAB exactly)
    print("\n--- Simulating Spectral Calibration (Offline) ---")
    
    # Spectral ratios using causal filtering (now enforced in sp)
    def get_spectral_ba(data):
        a = np.array(sp.calculate_band_power(data, sp.alpha_band))
        b = np.array(sp.calculate_band_power(data, sp.beta_band))
        return b / a if np.all(a > 0) else np.ones(len(a))

    ratios_rel = get_spectral_ba(relaxed_data)
    ratios_con = get_spectral_ba(concentrated_data)
    
    # Thresholds and Directions for Ch 1 and Ch 8
    # Ch 1
    th1 = (ratios_rel[0] + ratios_con[0]) / 2.0
    dir1 = 1 if ratios_con[0] > ratios_rel[0] else -1
    m1 = abs(ratios_rel[0] - ratios_con[0]) * 0.1 # 10% Margin
    
    # Ch 8
    th8 = (ratios_rel[7] + ratios_con[7]) / 2.0
    dir8 = 1 if ratios_con[7] > ratios_rel[7] else -1
    m8 = abs(ratios_rel[7] - ratios_con[7]) * 0.1
    
    print(f"Ch 1 -> Rel: {ratios_rel[0]:.4f}, Con: {ratios_con[0]:.4f}, Th: {th1:.4f}, Dir: {dir1}")
    print(f"Ch 8 -> Rel: {ratios_rel[7]:.4f}, Con: {ratios_con[7]:.4f}, Th: {th8:.4f}, Dir: {dir8}")

    # 2. Simulate Real-Time Stream (matching RealTimeProcessor)
    print("\n--- Simulating Real-Time Detection (Causal) ---")
    fs = 250
    snippet_len = 5 * fs
    test_stream = np.vstack([
        relaxed_data[:snippet_len],
        concentrated_data[:snippet_len],
        relaxed_data[snippet_len:2*snippet_len]
    ])
    
    window_size = 250 # 1 second
    step_size = 50
    
    last_state = False
    print(f"{'Time (s)':<10} | {'Ch1 Score':<10} | {'Ch8 Score':<10} | {'State':<10}")
    print("-" * 55)
    
    for i in range(0, len(test_stream) - window_size, step_size):
        window = test_stream[i : i + window_size]
        # Real-time uses causal lfilter (now the only mode)
        scores = get_spectral_ba(window)
        s1, s8 = scores[0], scores[7]
        
        # Logic
        is_con1 = (s1 - th1) * dir1 > m1
        is_con8 = (s8 - th8) * dir8 > m8
        
        is_rel1 = (th1 - s1) * dir1 > m1
        is_rel8 = (th8 - s8) * dir8 > m8
        
        time_s = i / fs
        
        if not last_state:
            if is_con1 and is_con8:
                last_state = True
        else:
            if is_rel1 or is_rel8:
                last_state = False
        
        state_str = "MOVE" if last_state else "IDLE"
        
        if i % (fs * 1) == 0:
            print(f"{time_s:<10.2f} | {s1:<10.4f} | {s8:<10.4f} | {state_str:<10}")

    print("\nVerification complete.")

if __name__ == "__main__":
    verify_logic()
