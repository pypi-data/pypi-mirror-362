import sounddevice as sd
import soundfile as sf
import threading
from queue import Queue
import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment
from scipy import signal
from scipy.signal import butter, lfilter
import soundfile as sf
import whisper
import subprocess
import imageio_ffmpeg as ffmpeg
import parselmouth


#AUDIO LIBRARY

#Getfiles
def get_files(directory, only_audio=True, show=True):
    if only_audio:
        file_list = [f for f in os.listdir(directory) if f.endswith('.wav')]  # Only wav files
    else:
        file_list = [f for f in os.listdir(directory)]  # All files
    if show:
        print(f"Found {len(file_list)} files: {file_list}")
    return file_list


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

#plot oscilograma
def oscilo(raw, sr):
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(raw, sr=sr)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(False) #show grid
    plt.show()

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
    
# Save function
def save_audio(audio, sr, filename, output_directory):

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created directory: {output_directory}")

    output_path = os.path.join(output_directory, filename)
    sf.write(output_path, audio, sr)
    print(f"Saved processed audio as: {output_path}")
    
    return output_path

def to_text(file_path, model="base", language=None, verbose=True):

    audio_data, sample_rate = sf.read(file_path)
    audio_data = audio_data.astype(np.float32)
    model = whisper.load_model(model)
    transcription_result = model.transcribe(audio_data, language=language)
    transcription_text = transcription_result["text"]
    if verbose==True:
        print(transcription_text)
    else:
        pass
    
    return(transcription_text)

##########################################################################################

class AudioRecorderNoMarks:
    def __init__(self, mic_id, sample_rate, channels):

        # Microphone ID
        self.mic_id = mic_id
        # Sample rate
        self.sample_rate = sample_rate
        # Number of channels
        self.channels = channels
        # Recording flag
        self.recording = False
        # Stop request flag
        self.stop_requested = False
        # Start the audio queue
        self.mic_queue = Queue()  
        
        # Connection to the Arduino board via serial communication
        #self._serial = serial.Serial(arduino_port, 115200)
        

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self.recording:
            self.mic_queue.put(indata.copy())

    def start_recording(self, filepath):
        # Output audio file
        self.filepath = filepath
        if not self.recording:
            self.recording = True
            self.stop_requested = False  # Reset the stop_requested flag
            #self._send_pulse_to_arduino()
            self.mic_queue = Queue()  # Reset the audio queue
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()

    def stop_recording(self):
        if self.recording:
            self.stop_requested = True
            #self._send_pulse_to_arduino()
            self.recording_thread.join()  # Wait for the recording thread to finish
            self.recording = False

    def _send_pulse_to_arduino(self):
        pass

    def _record_audio(self):
        with sf.SoundFile(self.filepath, mode='x', samplerate=self.sample_rate, channels=self.channels, subtype=None) as file:
            with sd.InputStream(samplerate=self.sample_rate, device=self.mic_id, channels=self.channels, callback=self.callback):
                try:
                    while not self.stop_requested:
                        file.write(self.mic_queue.get())
                except RuntimeError as re:
                    print(f"{re}. If recording was stopped by the user, then this can be ignored")
                finally:
                    self.recording = False
                    
                    
class AudioRecorder:
    def __init__(self, mic_id, sample_rate, channels, arduino_port):

        # Microphone ID
        self.mic_id = mic_id
        # Sample rate
        self.sample_rate = sample_rate
        # Number of channels
        self.channels = channels
        # Recording flag
        self.recording = False
        # Stop request flag
        self.stop_requested = False
        # Start the audio queue
        self.mic_queue = Queue()  
        
        # Connection to the Arduino board via serial communication
        self._serial = serial.Serial(arduino_port, 115200)
        

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self.recording:
            self.mic_queue.put(indata.copy())

    def start_recording(self, filepath):
        # Output audio file
        self.filepath = filepath
        if not self.recording:
            self.recording = True
            self.stop_requested = False  # Reset the stop_requested flag
            self._send_pulse_to_arduino()
            self.mic_queue = Queue()  # Reset the audio queue
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()

    def stop_recording(self):
        if self.recording:
            self.stop_requested = True
            self._send_pulse_to_arduino()
            self.recording_thread.join()  # Wait for the recording thread to finish
            self.recording = False

    def _send_pulse_to_arduino(self):
        # Message to send to Arduino
        message = "P"
        # Send the message to Arduino
        self._serial.write(message.encode())

    def _record_audio(self):
        with sf.SoundFile(self.filepath, mode='x', samplerate=self.sample_rate, channels=self.channels, subtype=None) as file:
            with sd.InputStream(samplerate=self.sample_rate, device=self.mic_id, channels=self.channels, callback=self.callback):
                try:
                    while not self.stop_requested:
                        file.write(self.mic_queue.get())
                except RuntimeError as re:
                    print(f"{re}. If recording was stopped by the user, then this can be ignored")
                finally:
                    self.recording = False
