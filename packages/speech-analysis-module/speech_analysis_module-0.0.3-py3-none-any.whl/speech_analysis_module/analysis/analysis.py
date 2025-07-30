import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

#envelope
def envelope(raw, sr, backtrack=True, plot=True, show_onsets=True, delta=0):
    # Compute the onset envelope
    onset_env = librosa.onset.onset_strength(y=raw, sr=sr)
    # Compute the time values for each frame in the onset envelope
    time_env = librosa.frames_to_time(range(len(onset_env)), sr=sr)
    
    onset_frames = librosa.onset.onset_detect(y=raw, sr=sr, onset_envelope=onset_env, units='frames', 
                                              delta=delta, #sensitivity (ex 0.4)
                                              backtrack=backtrack,
                                             )
    
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    onset_strengths = onset_env[onset_frames]
    
    if plot:
        plt.figure(figsize=(10, 4))
        plt.plot(time_env, onset_env)
        plt.title('Onset Strength Envelope')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Onset Strength')
        
        if show_onsets:
            # Plot the onsets into the envelope
            for onset_time in onset_times:
                plt.axvline(x=onset_time, color='r', linestyle='--')
            plt.show()
        #plt.close() #to avoid spam
    
    return(onset_env, time_env, onset_times, onset_strengths)

#get STFT and psd
def psd(raw, sr, n_fft=2048, plot=True):
    
    # Calculate the Short-Time Fourier Transform (STFT) with the specified n_fft
    stft = librosa.stft(raw, n_fft=n_fft) #n_fft= sample points for calculation
    psd = np.abs(stft) ** 2  # Power is the squared magnitude of the STFT
    psd_values = np.mean(psd, axis=1)  # Average over the time axis
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)  # Calculate frequencies for n_fft
    # Check the shapes of `freqs` and `psd_values` to ensure they match
    #print(f"Frequency bins: {freqs.shape}, PSD values: {psd_values.shape}")
    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(freqs, psd_values)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.title('Power Spectral Density (PSD)')
        plt.grid()
        plt.show()
    
    return stft, psd_values, freqs

def welch(raw, sr, n_fft=1024, db=False, plot=True):

    freqs, psd_values = signal.welch(raw, fs=sr, nperseg=n_fft)

    if db:
        # Clip to avoid taking log of zero or negative values
        psd_values_clipped = np.clip(psd_values, 1e-10, None)  # Minimum value of 1e-10
        psd_values = 10 * np.log10(psd_values_clipped)  # Convert power to dB scale

    if plot:
        plt.figure(figsize=(10, 6))
        if db:
            plt.plot(freqs, psd_values)  # Use linear plot since values are already in dB
            plt.ylabel('Power/Frequency (dB/Hz)')
        else:
            plt.semilogy(freqs, psd_values)  # Use semilog for linear power values
            plt.ylabel('Power/Frequency (linear scale)')
        
        plt.xlabel('Frequency (Hz)')
        plt.title('Power Spectral Density (PSD) using Welch\'s Method')
        plt.grid()
        plt.show()
    
    return freqs, psd_values