import shutil
import os
import soundfile as sf

def convert_64_to_32_bit(input_file_path):
    # Load the 64-bit WAV file using soundfile
    
    audio_data, sample_rate = sf.read(input_file_path)

    shutil.os.remove(input_file_path)

    # Save as 32-bit WAV
    sf.write(input_file_path, audio_data, sample_rate, subtype='FLOAT')

def copy_non_wav_files(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through files in the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Check if the file is not a .wav file
            if file.endswith(".wav"):
                # Get the full path of the source and destination files
                source_file = os.path.join(root, file)
                destination_file = os.path.join(output_dir, file)

                # Copy the file to the output directory
                shutil.copy2(source_file, destination_file)

def group_audios(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".wav"):
            # Parse file name to get song_name and voice_type
            if "CSD_LI_soprano" in file_name:
                convert_64_to_32_bit(os.path.join(input_dir, file_name))
            
            parts = file_name.split('_')
            song_name = parts[1]
            voice_type = parts[2]

            # Create directory structure if it doesn't exist
            song_dir = os.path.join(output_dir, song_name)
            voice_dir = os.path.join(song_dir, voice_type)

            if not os.path.exists(song_dir):
                os.makedirs(song_dir)
            if not os.path.exists(voice_dir):
                os.makedirs(voice_dir)

            # Get the full path of the source and destination files
            source_file = os.path.join(input_dir, file_name)
            destination_file = os.path.join(voice_dir, file_name)

            # Copy the file to the output directory
            shutil.copy2(source_file, destination_file)
