from pydub import AudioSegment
import os
import shutil

def filter_wav_files(raw_esmuc_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(raw_esmuc_dir):
        filename_type = filename.split(".")
        remove = False

        parts = filename_type[0].split("_")
        
        if len(parts) == 5:
            take_number = parts[2] + "_" + parts[3]
        elif len(parts) == 4:
            take_number = parts[2]
        else:
            remove = True

        # remove recordings of individual voices practice
        for voice in ["soprano", "alto", "tenor", "bass"]:
            if voice in take_number:
                remove = True

        # remove non-wav files or multiple voices recording
        if filename_type[-1] != "wav" or parts[-1] == "AB" or parts[-1] == "ORTF":
            remove = True

        if not remove:
            shutil.copy(os.path.join(raw_esmuc_dir, filename), os.path.join(output_dir, filename))
            # file_path = os.path.join(raw_esmuc_dir, filename)
            # if os.path.isfile(file_path):
            #     os.remove(file_path)
            #     print(f"Deleted: {file_path}")

def get_singing_voice(singer):
    voice_mapping = {
        'A': 'Alto',
        'B': 'Bass',
        'S': 'Soprano',
        'T': 'Tenor'
    }
    return voice_mapping.get(singer[0], 'Unknown')

# get tracks organized by song_name/recording_type/take_number/voice_type
def group_audios(input_dir, output_dir):
    file_list = os.listdir(input_dir)
    for file_name in file_list:
        parts = file_name.split(".")[0].split('_')
        song_name = parts[0]
        recording_type = parts[1]

        if len(parts) == 2:
            continue

        # some parts named short6_mixed etc. 
        if len(parts) == 5:
            take_number = parts[2] + "_" + parts[3]
        else:
            take_number = parts[2]

        singer = parts[-1]

        # Create directories if they don't exist

        song_dir = os.path.join(output_dir, song_name)
        recording_dir = os.path.join(song_dir, recording_type)
        take_dir = os.path.join(recording_dir, take_number)
        voice_dir = os.path.join(take_dir, get_singing_voice(singer))

        os.makedirs(voice_dir, exist_ok=True)

        # Copy the file
        shutil.copy(os.path.join(input_dir,file_name), os.path.join(voice_dir, file_name))

def get_modified_filename(source_filename):
    output_mapping = {
        "Bass": "bass",
        "Tenor": "vocals",
        "Alto": "drums",
        "Soprano": "other"
    }
    parts = source_filename.split(".")[0].split('\\') # need to change to '\\' for windows
    voice_type = parts[-2]
    modified_name = output_mapping[voice_type] 
    return modified_name

def generate_mixes(source_folders, combination, mix_folder):
    combined_audio = AudioSegment.silent(duration=0)

    source_files = []  # Keep track of the original audio files
    for source_folder, source_file in zip(source_folders, combination):
        # source_file_path = os.path.join(input_dir, source_folder, source_file)
        source_file_path = os.path.join(source_folder, source_file)
        source_audio = AudioSegment.from_file(source_file_path).set_frame_rate(44100)

        source_files.append((source_file_path,source_audio))  # Keep track of the original audio files

        # Use the parameters of the first audio file for the combined file
        if source_folder == source_folders[0]:
            combined_audio = source_audio
        else:
            combined_audio = combined_audio.overlay(source_audio)

    # Save the mixed audio
    mix_file_path = os.path.join(mix_folder, "mixture.wav")
    combined_audio.export(mix_file_path, format="wav")

    # Copy original audio files to the mix folder with their labels
    for i, (source_file_path, source_audio) in enumerate(source_files):
        modified_name = get_modified_filename(source_file_path)
        source_file_name = f"{modified_name}.wav"
        source_audio.export(os.path.join(mix_folder, source_file_name), format="wav")

def generate_train_tests(input_dir, mix_output_dir_base):
    # Iterate through the organized folder structure
    mix_folder_counter = 1
    for song_name in os.listdir(input_dir):
        song_path = os.path.join(input_dir, song_name)

        for recording_type in os.listdir(song_path):
            recording_type_path = os.path.join(song_path, recording_type)

            for take_number in os.listdir(recording_type_path):
                # arbitrarily pick some shorts for testing
                take_number_path = os.path.join(recording_type_path, take_number)

                # Define take-specific output directory
                if take_number == "short3":
                    mix_output_dir = os.path.join(mix_output_dir_base, "test")
                elif take_number == "take1":
                    mix_output_dir = os.path.join(mix_output_dir_base, "train")
                else:
                    continue
                take_number_path = os.path.join(recording_type_path, take_number)
                
                # some recordings have less than 4 voices
                if len(os.listdir(take_number_path)) < 4:
                    continue

                for voice_type in os.listdir(take_number_path):
                    voice_type_path = os.path.join(take_number_path, voice_type)

                    # Get a list of all wav files for this voice type
                    wav_files = [f for f in os.listdir(voice_type_path) if f.endswith('.wav')]

                    # Generate all possible combinations of voice_types
                    source_folders = [voice_type_path]
                    combinations = [[f] for f in wav_files]

                    for other_voice_type in os.listdir(take_number_path):
                        if other_voice_type != voice_type:
                            other_voice_type_path = os.path.join(take_number_path, other_voice_type)
                            other_wav_files = [f for f in os.listdir(other_voice_type_path) if f.endswith('.wav')]
                            source_folders.append(other_voice_type_path)
                            combinations = [combo + [f] for combo in combinations for f in other_wav_files]

                    # Create Mix folders and generate mixed audio
                    for combination in combinations:
                        print(combination)
                        mix_folder = os.path.join(mix_output_dir, f"Mix{mix_folder_counter}")
                        os.makedirs(mix_folder, exist_ok=True)

                        generate_mixes(source_folders, combination, mix_folder)

                        mix_folder_counter += 1
                    break


def preprocess_esmuc_like_musdb(raw_esmuc_dir, output_dir):
    print("********** start generating test/train for esmuc **********")
    temp_dir = "esmuc_wav"
    temp_2_dir = "esmuc_wav_grouped"
    print("----------------------------filtering wav files----------------------------")
    filter_wav_files(raw_esmuc_dir, temp_dir)
    print("----------------------------grouping audio in temporary folder----------------------------")
    group_audios(temp_dir, temp_2_dir)
    print("----------------------------separating into train and test folders----------------------------")
    generate_train_tests(temp_2_dir, output_dir)
    # shutil.rmtree(temp_2_dir)

if __name__ == "__main__":
    raw_esmuc_dataset = "./EsmucChoirDataset_v1.0.0"
    output_dir = "./processed_esmuc"
    preprocess_esmuc_like_musdb(raw_esmuc_dataset, output_dir)

    