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
    # Use processor's internal bands to ensure consistency
    alpha_rel_vec = np.array(processor.calculate_band_power(relaxed_data, processor.alpha_band))
    alpha_con_vec = np.array(processor.calculate_band_power(concentrated_data, processor.alpha_band))
    
    beta_rel_vec = np.array(processor.calculate_band_power(relaxed_data, processor.beta_band))
    beta_con_vec = np.array(processor.calculate_band_power(concentrated_data, processor.beta_band))

    alpha_power_relaxed = np.mean(alpha_rel_vec)
    alpha_power_concentrated = np.mean(alpha_con_vec)
    beta_power_relaxed = np.mean(beta_rel_vec)
    beta_power_concentrated = np.mean(beta_con_vec)

    print(f"Alpha Power (Relaxed): {alpha_power_relaxed:.4f}")
    print(f"Alpha Power (Concentrated): {alpha_power_concentrated:.4f}")
    print(f"Beta Power (Relaxed): {beta_power_relaxed:.4f}")
    print(f"Beta Power (Concentrated): {beta_power_concentrated:.4f}")

    assert alpha_power_relaxed > alpha_power_concentrated, "Error: Alpha power should be higher in relaxed state (10Hz signal)"
    assert beta_power_concentrated > beta_power_relaxed, "Error: Beta power should be higher in concentrated state (25Hz signal)"
    print("Individual checks passed!")

    print("\nPhase 2: Ratio Calculation Check")
    # Test the new centralized ratio calculation
    ratios = processor.calculate_ratios(relaxed_data)
    
    # Mathematical consistency check: ratios should match per-channel power ratios
    expected_ratios = beta_rel_vec / alpha_rel_vec
    
    assert np.allclose(ratios, expected_ratios, atol=1e-7), "Ratio calculation doesn't match manual check"
    
    # Calibration ratios check (Concentrated / Relaxed)
    # Manual calculation to verify mathematical logic
    alpha_ratios = alpha_con_vec / alpha_rel_vec
    beta_ratios = beta_con_vec / beta_rel_vec
    
    print(f"Calculated Alpha Ratio (Mean): {np.mean(alpha_ratios):.4f}")
    print(f"Calculated Beta Ratio (Mean): {np.mean(beta_ratios):.4f}")

    assert np.all(alpha_ratios < 1.0), "In this test, Alpha should decrease during concentration"
    assert np.all(beta_ratios > 1.0), "In this test, Beta should increase during concentration"


    
    print("Ratio consistency checks passed!")
    
    print("Ratio checks passed!")
    print("\nSUCCESS: SignalProcessor is working correctly.")

if __name__ == "__main__":
    try:
        test_signal_processor()
    except Exception as e:
        print(f"\nFAILED: {e}")
        sys.exit(1)
