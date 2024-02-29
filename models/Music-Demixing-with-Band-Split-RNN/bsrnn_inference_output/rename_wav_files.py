import os

# Mapping of original names to new names
output_mapping = {
    "bass": "truth_bass",
    "vocals": "truth_tenor",
    "drums": "truth_alto",
    "other": "truth_soprano"
}

# Get a list of all subdirectories (folder names)
subdirectories = [d for d in os.listdir() if os.path.isdir(d)]

# Iterate through each subdirectory
for subdir in subdirectories:
    subdir_path = os.path.join(os.getcwd(), subdir)

    # List all .wav files in the subdirectory
    wav_files = [f for f in os.listdir(subdir_path) if f.endswith('.wav')]

    # Iterate through .wav files in the subdirectory
    for wav_file in wav_files:
        # Split the file name and extension
        file_name, file_extension = os.path.splitext(wav_file)

        # Get the new name from the mapping or use the original name if not found
        new_name = output_mapping.get(file_name, file_name)

        # Rename the file with folder name as suffix
        new_file_name = f"{subdir}_{new_name}{file_extension}"

        # Rename the file
        old_path = os.path.join(subdir_path, wav_file)
        new_path = os.path.join(subdir_path, new_file_name)
        os.rename(old_path, new_path)

        print(f'Renamed: {old_path} -> {new_path}')

print("All files renamed.")
