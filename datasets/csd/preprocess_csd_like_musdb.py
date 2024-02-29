import os
import itertools
import shutil
from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
from utils import copy_non_wav_files, group_audios

def get_modified_filename(source_filename):
    output_mapping = {
        "bass": "bass",
        "tenor": "vocals",
        "alto": "drums",
        "soprano": "other"
    }
    parts = source_filename.split('\\') # need to change to '\\' for windows
    voice_type = parts[-2]
    modified_name = output_mapping[voice_type] 
    return modified_name + ".wav"

def mono_to_stereo(input_file, output_file):
    # Read the mono wav file
    sample_rate, mono_data = wavfile.read(input_file)

    # Create stereo data by duplicating the mono data to both channels
    stereo_data = np.column_stack((mono_data, mono_data))

    # Save the stereo wav file
    wavfile.write(output_file, sample_rate, stereo_data)

def generate_test(input_dir, output_dir):
    source_folders = ['alto', 'tenor', 'bass', 'soprano']
    test_folder = os.path.join(output_dir, "test")
    mix_no = 1
    os.makedirs(test_folder, exist_ok=True)
    for song_folder in os.listdir(input_dir):
        song_path = os.path.join(input_dir, song_folder)

        if not os.path.isdir(song_path):
            continue

        combined_audio = AudioSegment.silent(duration=0)  # Create an empty audio segment
        
        # Generate all combinations of .wav files
        for source_folder in source_folders:
            source_folder_path = os.path.join(song_path, source_folder)
            voice_files = os.listdir(source_folder_path)
            for source_file in voice_files:
                if "1" not in source_file:
                    continue
                source_file_path = os.path.join(source_folder_path, source_file)

                mix_folder = os.path.join(test_folder, f"mix{mix_no}")
                os.makedirs(mix_folder, exist_ok=True)
                new_file_path = os.path.join(mix_folder, get_modified_filename(source_file_path))

                source_audio = AudioSegment.from_file(source_file_path)

                # Use the parameters of the first audio file for the combined file
                if source_folder == source_folders[0]:
                    combined_audio = source_audio

                else:
                    combined_audio = combined_audio.overlay(source_audio)

                # copy the source track to the mix folder and delete it
                shutil.copy2(source_file_path, new_file_path)
                shutil.os.remove(source_file_path)
        
        combined_audio.export(os.path.join(mix_folder, 'mixture.wav'), format="wav")
        mix_no += 1

def generate_train(input_dir, output_dir):
    source_folders = ['alto', 'tenor', 'bass', 'soprano']
    train_folder = os.path.join(output_dir, "train")
    mix_number = 1
    for song_folder in os.listdir(input_dir):
        song_path = os.path.join(input_dir, song_folder)

        if not os.path.isdir(song_path):
            continue

        # Generate all combinations of .wav files
        combinations = list(itertools.product(*[os.listdir(os.path.join(song_path, source_folder)) for source_folder in source_folders]))

        # Create a mix folder for each combination
        for idx, combination in enumerate(combinations, start=1):
            mix_folder = os.path.join(train_folder, f"mix{mix_number}")
            os.makedirs(mix_folder, exist_ok=True)

            # Combine the selected .wav files
            combined_audio = AudioSegment.silent(duration=0)  # Create an empty audio segment

            for source_folder, source_file in zip(source_folders, combination):
                source_file_path = os.path.join(song_path, source_folder, source_file)
                source_audio = AudioSegment.from_file(source_file_path)

                # Use the parameters of the first audio file for the combined file
                if source_folder == source_folders[0]:
                    combined_audio = source_audio

                else:
                    combined_audio = combined_audio.overlay(source_audio)

                # Copy individual .wav files
                modified_filename = get_modified_filename(source_file_path)
                shutil.copy2(source_file_path, os.path.join(mix_folder, modified_filename))

            # Save the combined audio as mixture.wav
            combined_audio.export(os.path.join(mix_folder, 'mixture.wav'), format="wav")
            mix_number += 1

def preprocess_csd_like_musdb(raw_csd_dir, output_dir):
    print("**************** start generating test/train for csd ****************")
    temp_dir = "./csd_temp"
    temp_dir_2 = "./csd_temp_2"
    print("-----------------copying non wav files to temporary folder-----------------")
    copy_non_wav_files(raw_csd_dir, temp_dir)
    print("-----------------grouping audio by song and voice type-----------------")
    group_audios(temp_dir, temp_dir_2)
    shutil.rmtree(temp_dir)
    print("-----------------generating test-----------------")
    generate_test(temp_dir_2, output_dir)
    print("-----------------generating train-----------------")
    generate_train(temp_dir_2, output_dir)
    shutil.rmtree(temp_dir_2)

if __name__ == "__main__":
    root_dir = "ChoralSingingDataset"
    output_dir = "processed_csd"
    preprocess_csd_like_musdb(root_dir, output_dir)
    
