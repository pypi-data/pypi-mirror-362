import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import librosa
import librosa.display

#bandpass filter
def bandpass_filter(raw, sr, lowcut, highcut, order=5):
    #order: The order of the Butterworth filter (default: 5).
    # Calculate the Nyquist frequency
    nyquist = 0.5 * sr
    # Normalize the cutoff frequencies (0 < Wn < 1)
    low = lowcut / nyquist
    high = highcut / nyquist
    # Ensure cutoff frequencies are in the range (0, 1)
    if low <= 0 or high >= 1 or low >= high:
        raise ValueError(f"Cutoff frequencies must be 0 < low < high < 1. Received: low={low}, high={high}")
    # Design the Butterworth bandpass filter
    b, a = butter(order, [low, high], btype='band')    
    # Apply the filter to the data
    y = lfilter(b, a, raw)
    return y

# Define a noise gate function
def noise_gate(raw, sr, threshold_in_db=-40, attack_time=0.01, release_time=0.1):
    # Convert the threshold from dB to linear scale
    threshold_linear = 10 ** (threshold_in_db / 20)   
    # Create an envelope follower to detect signal levels over time
    raw_abs = np.abs(raw)  # Use `raw` instead of `audio`
    envelope = np.zeros_like(raw_abs)  
    # Attack and release coefficients
    attack_coeff = np.exp(-1.0 / (sr * attack_time))
    release_coeff = np.exp(-1.0 / (sr * release_time)) 
    # Initialize envelope
    envelope[0] = raw_abs[0]  # Initialize the first envelope value
    # Track the signal envelope
    for i in range(1, len(raw)):
        if raw_abs[i] > envelope[i - 1]:
            envelope[i] = attack_coeff * envelope[i - 1] + (1 - attack_coeff) * raw_abs[i]
        else:
            envelope[i] = release_coeff * envelope[i - 1] + (1 - release_coeff) * raw_abs[i]

    # Apply the noise gate based on the threshold
    y = np.where(envelope >= threshold_linear, raw, 0)  # Use `raw` instead of `audio`
    
    return y

def trim_adjust(raw, sr, top_db=30, frame_length=1024, hop_length=512, final_duration=None, indent_side='left', plot=True):

    #top_db: The threshold (in dB) below reference to consider as silence (default: 30 dB).
    #frame_length: The length of each analysis frame (default: 2048).
    #hop_length: The number of samples between successive frames (default: 512).
    #final_duration: In seconds. if None, no padding or truncation is applied.

    trimmed_audio, interval = librosa.effects.trim(raw, top_db=top_db, frame_length=frame_length, hop_length=hop_length)
    
    original_duration = librosa.get_duration(y=raw, sr=sr)
    trimmed_duration = librosa.get_duration(y=trimmed_audio, sr=sr)
    
    print(f'original duration was {original_duration}, trimmed duration is {trimmed_duration}')
    
    # Adjust the final duration
    if final_duration is not None:
        final_samples = int(final_duration * sr)  # Convert desired duration to samples
        trimmed_samples = len(trimmed_audio)
                
        # If the final duration is longer, pad with zeros (silence)
        if final_samples > trimmed_samples:
            padding_length = final_samples - trimmed_samples
            if indent_side == 'left':
                # Align to left, pad on the right
                adjusted_audio = np.pad(trimmed_audio, (0, padding_length), mode='constant')
            elif indent_side == 'right':
                # Align to right, pad on the left
                adjusted_audio = np.pad(trimmed_audio, (padding_length, 0), mode='constant')
            else:
                raise ValueError(f"Invalid indent_side: {indent_side}. Choose 'left' or 'right'.")
        
        # If the final duration is shorter, truncate the trimmed audio
        else:
            adjusted_audio = trimmed_audio[:final_samples]
    
    # If no final duration is specified, keep the trimmed audio as it is
    else:
        adjusted_audio = trimmed_audio
        
    adjusted_duration = librosa.get_duration(y=adjusted_audio, sr=sr)
    print(f'adjusted duration is {adjusted_duration}')

    if plot:
        plt.figure(figsize=(12, 6))
        # Original audio waveform
        plt.subplot(2, 1, 1)
        librosa.display.waveshow(raw, sr=sr, alpha=0.6, label='Original Audio')
        plt.title('Original Audio Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.xlim([0, original_duration])  # Set x-axis limit based on original duration
        # Trimmed audio waveform
        plt.subplot(2, 1, 2)
        librosa.display.waveshow(adjusted_audio, sr=sr, color='orange', alpha=0.6, label='Trimmed Audio')
        plt.title('Trimmed Audio Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.xlim([0, adjusted_duration])  # Set x-axis limit to match original duration

        plt.tight_layout()
        plt.show()

    return adjusted_audio, interval