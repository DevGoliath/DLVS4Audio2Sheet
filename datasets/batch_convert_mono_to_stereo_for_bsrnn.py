import os
from scipy.io import wavfile
import numpy as np

def mono_to_stereo(input_file, output_file):
    # Read the mono wav file
    sample_rate, mono_data = wavfile.read(input_file)

    # Create stereo data by duplicating the mono data to both channels
    stereo_data = np.column_stack((mono_data, mono_data))

    # Save the stereo wav file
    wavfile.write(output_file, sample_rate, stereo_data)

if __name__ == "__main__":
    # Directory paths
    input_dir = "combined_processed_dataset"
    output_dir = "combined_processed_dataset_converted_stereo"

    # Iterate through the directory structure
    for root, dirs, files in os.walk(input_dir):
        # Create the corresponding subdirectories in the output directory
        relative_path = os.path.relpath(root, input_dir)
        output_subdir = os.path.join(output_dir, relative_path)
        os.makedirs(output_subdir, exist_ok=True)

        # Process each .wav file in the current directory
        for file in files:
            if file.endswith(".wav"):
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_subdir, file)
                mono_to_stereo(input_file, output_file)
                print(f"Processed: {input_file} -> {output_file}")

    print("Conversion completed.")