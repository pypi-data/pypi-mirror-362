import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

#plot oscilograma
def oscilo(raw, sr):
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(raw, sr=sr)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(False) #show grid
    plt.show()

def spectro(stft, sr):
    plt.figure(figsize=(10, 6))
    # Convert the magnitude spectrogram to dB scale using the corrected approach
    magnitude_spectrogram = np.abs(stft)  # Get the magnitude of the STFT
    db_spectrogram = librosa.power_to_db(magnitude_spectrogram**2, ref=np.max)  # Convert to dB scale
    # Plot the spectrogram
    librosa.display.specshow(db_spectrogram, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram (dB scale)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.grid(False)  # Show grid
    plt.show()