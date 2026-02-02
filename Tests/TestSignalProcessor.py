import numpy as np
import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EEG.SignalProcessor import SignalProcessor

def generate_synthetic_eeg(duration_sec, fs, frequency, amplitude):
    """Generates a sine wave signal with white noise."""
    t = np.linspace(0, duration_sec, int(fs * duration_sec), endpoint=False)
    # 8 channels
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    noise = np.random.normal(0, 1.0, len(t))
    
    # Create 8 channels with slight variations
    multichannel_data = []
    for i in range(8):
        ch_signal = signal + np.random.normal(0, 0.5, len(t)) + noise
        multichannel_data.append(ch_signal)
        
    return np.array(multichannel_data).T

def test_signal_processor():
    fs = 250
    processor = SignalProcessor(sampling_rate=fs)
    print(f"Testing SignalProcessor with sampling rate: {processor.sampling_rate}")

    # Duration: 30 seconds
    duration = 30
    
    print("Generating 'Relaxed' data (Strong Alpha: 10Hz)...")
    relaxed_data = generate_synthetic_eeg(duration, fs, frequency=10, amplitude=15.0)
    
    print("Generating 'Concentrated' data (Strong Beta: 25Hz)...")
    concentrated_data = generate_synthetic_eeg(duration, fs, frequency=25, amplitude=15.0)

    print("\nPhase 1: Individual Band Power Checks")
    alpha_power_relaxed = processor.calculate_band_power(relaxed_data, (8, 13))
    alpha_power_concentrated = processor.calculate_band_power(concentrated_data, (8, 13))
    
    beta_power_relaxed = processor.calculate_band_power(relaxed_data, (14, 30))
    beta_power_concentrated = processor.calculate_band_power(concentrated_data, (14, 30))

    print(f"Alpha Power (Relaxed): {alpha_power_relaxed:.4f}")
    print(f"Alpha Power (Concentrated): {alpha_power_concentrated:.4f}")
    print(f"Beta Power (Relaxed): {beta_power_relaxed:.4f}")
    print(f"Beta Power (Concentrated): {beta_power_concentrated:.4f}")

    assert alpha_power_relaxed > alpha_power_concentrated, "Error: Alpha power should be higher in relaxed state (10Hz signal)"
    assert beta_power_concentrated > beta_power_relaxed, "Error: Beta power should be higher in concentrated state (25Hz signal)"
    print("Individual checks passed!")

    print("\nPhase 2: Ratio Calculation Check")
    alpha_ratio, beta_ratio = processor.process_calibration_data(relaxed_data, concentrated_data)
    
    print(f"Calculated Alpha Ratio: {alpha_ratio:.4f}")
    print(f"Calculated Beta Ratio: {beta_ratio:.4f}")

    expected_alpha_ratio = alpha_power_concentrated / alpha_power_relaxed
    expected_beta_ratio = beta_power_concentrated / beta_power_relaxed

    assert abs(alpha_ratio - expected_alpha_ratio) < 1e-5, f"Alpha ratio mismatch: {alpha_ratio} vs {expected_alpha_ratio}"
    assert abs(beta_ratio - expected_beta_ratio) < 1e-5, f"Beta ratio mismatch: {beta_ratio} vs {expected_beta_ratio}"
    
    print("Ratio checks passed!")
    print("\nSUCCESS: SignalProcessor is working correctly.")

if __name__ == "__main__":
    try:
        test_signal_processor()
    except Exception as e:
        print(f"\nFAILED: {e}")
        sys.exit(1)
