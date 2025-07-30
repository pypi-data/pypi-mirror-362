import os
import numpy as np
import soundfile as sf
import whisper


#Get the list of files of a folder
def get_files(directory, extensions=[".wav"], show=True):
    if extensions:
        file_list = [f for f in os.listdir(directory) if any(f.endswith(ext) for ext in extensions)]
    else:
        file_list = os.listdir(directory)

    if show:
        print(f"Found {len(file_list)} files: {file_list}")
    return file_list

#load audio
def load_audio(filepath):
    audio, samplerate = sf.read(filepath)
    return audio, samplerate

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

def play(audio):
    

